import datetime
import copy
import json
from typing import Union, Tuple, List, Dict, Any
import numpy as np
import xgboost
from segmenthee.config import Config
from segmenthee import parser_api
import math
import statsmodels.api as sm

ABANDONER = 1
BUYER = 0

FILE_NAME = 'xgbm.sav'
SCORE_THRESHOLD = Config.SCORE_THRESHOLD
FRUSTRATION_TOLERANCE = Config.FRUSTRATION_TOLERANCE

# event classes

classcount = 0
def nextclassindex():
    global classcount
    retval = classcount
    classcount += 1
    return retval

#collect name from classindex
classnames = dict()

PARAMS = {
    "clickrate": 0.5,
    "actionseparation": (0.0, 0.005),
    "actionaffinity": (0.0, 0.03),
    "categoryaffinity": (0.0, 0.03),
    "carttotaltrend": (0.0, 0.025),
    "cartcounttrend": (0.0, 0.04),
    "avgpricemanipulation": (0.0, 0.025),
    "lastpriceviewedtrend": (0.0, 0.025),
    "tabcounttrend": (0.0, 0.04),
    "redirectstrend": (0.0, 0.01),
    "tabtypetrend": (0.0, 0.01),
    "navigationtrend": (0.0, 0.01),
    "referrertrend": (0.0, 0.01),
    "pagetrend": (0.0, 0.04),
    "sorttrend": (0.0, 0.01)
}

def UpdateFactors(factor_dict, new_params, delta_time):
    # update factors with new params
    if new_params: # if not None
        for key in new_params:
            factor_dict[key] = new_params[key]
    # calculate time dependent factors: exp(-lambda * delta_time)
    for key in factor_dict:
        if key != "clickrate":
            factor_dict[key] = (factor_dict[key][0], math.exp(-factor_dict[key][-1] * delta_time))

MAX_CATEGORY = 10
tabtype_dict = {'New': 0, 'Existing': 1}
navigation_dict = {'NAVIGATE': 0, 'FORWARD': 1, 'BACK': 2, 'RELOAD': 3}
origin_dict = {"social":0,"google":1,"shop":2}
sort_dict = {'relevance': 0, 'popularity': 1, 'rating': 2, 'discountPercent': 3, 'price': 4, 'name': 5, 'publication_date': 6}


def get_navigation(navigation: str) -> int:
    return navigation_dict.get(navigation, len(navigation_dict))


def get_tabtype(tabtype: str) -> int:
    return tabtype_dict.get(tabtype, len(tabtype_dict))


def get_referrer(referrer: str) -> int:
    r = parser_api.parse_origin(referrer)
    return origin_dict.get(r, len(origin_dict))


def get_sort(sort: str) -> int:
    return sort_dict.get(parser_api.parse_sort(sort),len(sort_dict))


def get_page(page: str) -> int:
    try:
        return int(page)
    except:
        return 0

def get_utm_source(item: Dict) -> str:
    keys = item.keys()
    if 'utm_source' in keys:
        return item.get('utm_source')
    if 'gclid' in keys:
        return 'google'
    if 'fbclid' in keys:
        return 'facebook'
    return ''


def get_cart_total(state: Dict[str, Any]) -> Union[Any, None]:
    return state.get('carttotal')


def get_cart_count(state: Dict[str, Any]) -> Union[Any, None]:
    return state.get('cartcount')

def get_time_affinity(coeff, delta_time):
    return -math.log(coeff) / delta_time

def paramgroup2feature(params, avg_delta_time):
    coeffs = {}
    for p in params:
        coeffs[p] = (0.0, params[p], get_time_affinity(params[p], avg_delta_time))
    table_params = {
        "clickrate": coeffs["time"][0],
        "actionseparation": coeffs["time"],
        "actionaffinity": coeffs["aff"],
        "categoryaffinity": coeffs["aff"],
        "carttotaltrend": coeffs["price"],
        "cartcounttrend": coeffs["count"],
        "avgpricemanipulation": coeffs["price"],
        "lastpriceviewedtrend": coeffs["price"],
        "tabcounttrend": coeffs["count"],
        "redirectstrend": coeffs["trend"],
        "tabtypetrend": coeffs["trend"],
        "navigationtrend": coeffs["trend"],
        "referrertrend": coeffs["trend"],
        "pagetrend": coeffs["count"],
        "sorttrend": coeffs["trend"]
    }
    return table_params

def LogCategory(retval,factor_dict,category):
    if "categoryaffinity" not in retval:
        return None
    arr = retval["categoryaffinity"]
    factors = factor_dict["categoryaffinity"]
    for attix in range(len(factors)):
        factor = factors[attix]
        for cat in range(MAX_CATEGORY):
            arr[attix][cat] *= factor
    if category >= 0:
        for attix in range(len(factors)):
            arr[attix][category] += 1 - factors[attix]

def FeatureNotAvailableWarning(feature_str):
    print(f"Warning: {feature_str} not in state.")

def CalculateClickrates(retval, time, factor, initialize=False):
    if "z_score" not in retval:
        return None
    # for attix in range(len(factor_dict)):
    if retval["clickrate_var"] > 0.0:
        retval["z_score"] = (time - retval["lastactioneventtime"] - retval["clickrate_avg"]) / (retval["clickrate_var"]**(1/2))
    if initialize:
        first_delta_time = retval["lastactioneventtime"] - retval["sessionstart"]
        second_delta_time = time - retval["lastactioneventtime"]
        retval["clickrate_avg"] = (1-factor) * first_delta_time + factor * second_delta_time
        retval["clickrate_squares"] = (1-factor) * first_delta_time**2 + factor * second_delta_time**2
        retval["clickrate_var"] = retval["clickrate_squares"] - retval["clickrate_avg"]**2
    else:
        delta_time = time-retval["lastactioneventtime"]
        retval["clickrate_avg"] *= (1-factor)
        retval["clickrate_avg"] += factor * delta_time
        retval["clickrate_squares"] *= (1-factor)
        retval["clickrate_squares"] += factor * delta_time**2
        retval["clickrate_var"] = retval["clickrate_squares"] - retval["clickrate_avg"]**2

def CalculateUnalikeability(arr):
    n = len(arr)
    if n == 1:
        return 0 # may be better to return 1
    s = 0
    for i in range(n-1):
        for j in range(i+1,n):
            if arr[i] != arr[j]:
                s += 1
    u = 2*s/(n**2 - n)
    return u

def CalculateAutocorrelation(arr):
    if len(arr) == 1 or CalculateUnalikeability(arr) == 0:
        return 0
    s = set(arr)
    enc = {value:idx for idx,value in enumerate(s)}
    arr = [enc[val] for val in arr]
    autocorr = sm.tsa.acf(arr, nlags =len(arr) - 1)[1:]
    return max(autocorr, key=abs)

def UpdateTrendFeature(retval, factor_dict, feature, new_value):
    if feature not in retval:
        FeatureNotAvailableWarning(feature)
        return None
    values = retval[feature]
    factors = factor_dict[feature]
    for attix in range(len(values)):
        values[attix] *= factors[attix]
        values[attix] += (1 - factors[attix]) * new_value
        
def UpdateAffinityFeature(retval, factor_dict, feature, update_index):
    if feature not in retval:
        FeatureNotAvailableWarning(feature)
        return None
    values = retval[feature]
    factors = factor_dict[feature]
    for attix in range(len(factors)):
        factor = factors[attix]
        for act in range(len(values[0])):
            values[attix][act] *= factor
        values[attix][update_index] += 1 - factor

class SessionBodyEvent:
    def __init__(self, time: int):
        self.time = time #int(datetime.datetime.fromisoformat(time).timestamp())
        self.factor_dict = PARAMS.copy() # will change with UpdateFactors

    def Update(self, prevstate, newparams=None):
        retval = copy.deepcopy(prevstate)
        retval["lastbodyeventtime"] = self.time
        delta_time = 0.0
        if retval["lastactioneventtime"]: # if not None, ergo not
            delta_time = self.time - retval["lastactioneventtime"]
        UpdateFactors(self.factor_dict, newparams, delta_time)
        return retval

    @classmethod
    def classindex(cls):
        return cls.cindex

    def is_closing(self):
        return False

    def is_success(self) -> bool:
        return False

    def skip_update(self) -> bool:
        return False

    JSON_FIELDS: List[str] = [
        'time', 'delta_count', 'delta_total', 'event_label', 'referrer', 'tabcount', 'tabtype',
        'navigation', 'redirects', 'title', 'utm_source', 'utm_medium', 'category_id', 'price',
        'product_id', 'page', 'sort'
    ]

    def to_dict(self, **kwargs) -> Dict[str, Any]:
        data = {key: value for (key, value) in vars(self).items() if key in SessionBodyEvent.JSON_FIELDS}
        data = {'constructor': self.__class__.__name__, **data, **kwargs}
        return data

    def to_json(self, **kwargs) -> str:
        data = self.to_dict(kwargs)
        return json.dumps(data, ensure_ascii=False)


class UserActionEvent(SessionBodyEvent):
    def __init__(self, time: int):
        super().__init__(time)
        # self.eventclass = classnames[self.cindex]

    def Update(self, prevstate, newparams=None):
        retval = super().Update(prevstate,newparams)
        retval["actioncount"] += 1
        if retval["actioncount"] > 1: #lastactioneventtime is not None
            delta_time = self.time - retval["lastactioneventtime"]
            retval["clickrate"] = delta_time
            UpdateAffinityFeature(retval, self.factor_dict, "actionaffinity", self.classindex())
            UpdateTrendFeature(retval, self.factor_dict, "actionseparation", delta_time)
            #frustration: clickrates
            if retval["actioncount"] == 2: #initialize clickrates
                CalculateClickrates(retval, self.time, PARAMS["clickrate"], initialize=True)
            else: #actioncount >= 3
                CalculateClickrates(retval, self.time, PARAMS["clickrate"], initialize=False)
        else: #first action event
            UpdateAffinityFeature(retval, self.factor_dict, "actionaffinity", self.classindex())
        retval["lastactioneventtime"] = self.time
        retval["lastactioneventindex"] = self.classindex()
        # retval["lastactioneventclass"] = self.eventclass
        if retval["highwatermark"] < 1:
            retval["highwatermark"] = 1
        return retval

class CartModifyEvent(UserActionEvent):
    def __init__(self, time: int, delta_count: int, delta_total):
        super().__init__(time)
        self.delta_count = delta_count
        self.delta_total = delta_total

    cindex = nextclassindex()
    classnames[cindex] = "CartModifyEvent"

    def Update(self, prevstate, newparams=None):
        retval = super().Update(prevstate,newparams)
        retval["carttotal"] += self.delta_total
        retval["cartcount"] += self.delta_count
        retval["sessionstatus"] = "CartModified"
        UpdateTrendFeature(retval, self.factor_dict, "carttotaltrend", self.delta_total)
        UpdateTrendFeature(retval, self.factor_dict, "cartcounttrend", self.delta_count)
        if self.delta_count != 0:
            avgprice = self.delta_total/self.delta_count
            retval["cartmodification"] = self.delta_total/self.delta_count
            UpdateTrendFeature(retval, self.factor_dict, "avgpricemanipulation", avgprice)
        return retval

class WishListModifyEvent(UserActionEvent):

    cindex = nextclassindex()
    classnames[cindex] = "WishListModifyEvent"

class RegistrationEvent(UserActionEvent):

    cindex = nextclassindex()
    classnames[cindex] = "RegistrationEvent"

class CouponAcceptedEvent(UserActionEvent):
    def __init__(self, time: int, event_label: str = ""):
        super().__init__(time)
        self.event_label = event_label

    cindex = nextclassindex()
    classnames[cindex] = "CouponAcceptedEvent"

    def Update(self, prevstate, newparams=None):
        retval = super().Update(prevstate,newparams)
        retval["couponstatus"] = 2
        return retval

    def skip_update(self) -> bool:
        return True


class CouponRejectedEvent(UserActionEvent):
    def __init__(self, time: int, event_label: str):
        super().__init__(time)
        self.event_label = event_label

    def skip_update(self) -> bool:
        return True

    def is_pageview(self) -> bool:
        return False


class BrowsingEvent(UserActionEvent):
    def __init__(self, time: int, referrer: int, tabcount: int, tabtype: int, navigation: int, redirects: int, title: str, utm_source: str, utm_medium: str):
        super().__init__(time)
        self.referrer = referrer
        self.tabcount = tabcount
        self.tabtype = tabtype
        self.navigation = navigation
        self.redirects = redirects
        self.title = title
        self.utm_source = utm_source
        self.utm_medium = utm_medium

    cindex = nextclassindex()
    classnames[cindex] = "BrowsingEvent"

    def Update(self, prevstate, newparams=None):
        retval = super().Update(prevstate,newparams)
        UpdateTrendFeature(retval, self.factor_dict, "tabcounttrend", self.tabcount)
        UpdateTrendFeature(retval, self.factor_dict, "tabtypetrend", self.tabtype)
        UpdateTrendFeature(retval, self.factor_dict, "redirectstrend", self.redirects)
        UpdateTrendFeature(retval, self.factor_dict, "navigationtrend", self.navigation)
        UpdateTrendFeature(retval, self.factor_dict, "referrertrend", self.referrer)
        return retval

class MainPageBrowsingEvent(BrowsingEvent):

    cindex = nextclassindex()
    classnames[cindex] = "MainPageBrowsingEvent"

class ProductPageBrowsingEvent(BrowsingEvent):
    def __init__(self, time: int, category_id: int, price: int, referrer: int, tabcount: int, tabtype: int, navigation: int, redirects: int, title: str, utm_source: str, utm_medium: str, product_id: Any):
        super().__init__(time,referrer,tabcount,tabtype,navigation,redirects,title,utm_source,utm_medium)
        self.product_id = product_id
        self.category_id = category_id
        self.price = price if price else 0

    cindex = nextclassindex()
    classnames[cindex] = "ProductPageBrowsingEvent"

    def Update(self, prevstate, newparams=None):
        retval = super().Update(prevstate,newparams)
        retval["lastcategory"] = self.category_id
        category = self.category_id
        LogCategory(retval, self.factor_dict, category)
        retval["lastprice"] = self.price
        UpdateTrendFeature(retval, self.factor_dict, "lastpriceviewedtrend", self.price)
        retval["producteverviewed"] = 1
        retval["product_ids"].append(self.product_id)
        retval["autocorr"] = CalculateAutocorrelation(retval["product_ids"])
        retval["u_product"] = CalculateUnalikeability(retval["product_ids"])
        return retval


class ProductPageScrollEvent(BrowsingEvent):

    def skip_update(self) -> bool:
        return True


class CartBrowsingEvent(BrowsingEvent):

    cindex = nextclassindex()
    classnames[cindex] = "CartBrowsingEvent"

class WishListBrowsingEvent(BrowsingEvent):

    cindex = nextclassindex()
    classnames[cindex] = "WishListBrowsingEvent"

class RegistrationPageBrowsingEvent(BrowsingEvent):

    cindex = nextclassindex()
    classnames[cindex] = "RegistrationPageBrowsingEvent"

class SearchResultsBrowsingEvent(BrowsingEvent):
    def __init__(self, time: int, referrer: int, tabcount: int ,tabtype: int, navigation: int, redirects: int, title: str, utm_source: str, utm_medium: str, page: int, sort: int):
        super().__init__(time,referrer,tabcount,tabtype,navigation,redirects,title,utm_source,utm_medium)
        self.page = page
        self.sort = sort

    cindex = nextclassindex()
    classnames[cindex] = "SearchResultsBrowsingEvent"

    def Update(self, prevstate, newparams=None):
        retval = super().Update(prevstate,newparams)
        UpdateTrendFeature(retval, self.factor_dict, "sorttrend", self.sort)
        UpdateTrendFeature(retval, self.factor_dict, "pagetrend", self.page)
        return retval

class CategoryPageBrowsingEvent(BrowsingEvent):
    def __init__(self, time: int, category_id: int, referrer: int, tabcount: int, tabtype: int, navigation: int, redirects: int, title: str, utm_source: str, utm_medium: str, page: int, sort: int):
        super().__init__(time,referrer,tabcount,tabtype,navigation,redirects,title,utm_source,utm_medium)
        self.category_id = category_id
        self.page = page
        self.sort = sort

    cindex = nextclassindex()
    classnames[cindex] = "CategoryPageBrowsingEvent"

    def Update(self, prevstate, newparams=None):
        retval = super().Update(prevstate,newparams)
        retval["lastcategory"] = self.category_id
        category = self.category_id
        LogCategory(retval, self.factor_dict, category)
        UpdateTrendFeature(retval, self.factor_dict, "sorttrend", self.sort)
        UpdateTrendFeature(retval, self.factor_dict, "pagetrend", self.page)
        return retval

class PredefinedFilterBrowsingEvent(BrowsingEvent):
    def __init__(self, time: int, category_id: int, referrer: int, tabcount: int, tabtype: int, navigation: int, redirects: int, title: str, utm_source: str, utm_medium: str, page: int, sort: int):
        super().__init__(time,referrer,tabcount,tabtype,navigation,redirects,title,utm_source,utm_medium)
        self.category_id = category_id
        self.page = page
        self.sort = sort

    cindex = nextclassindex()
    classnames[cindex] = "PredefinedFilterBrowsingEvent"

    def Update(self, prevstate, newparams=None):
        retval = super().Update(prevstate,newparams)
        retval["lastcategory"] = self.category_id
        category = self.category_id
        LogCategory(retval, self.factor_dict, category)
        UpdateTrendFeature(retval, self.factor_dict, "sorttrend", self.sort)
        UpdateTrendFeature(retval, self.factor_dict, "pagetrend", self.page)
        return retval
    
class InformationPageBrowsingEvent(BrowsingEvent):

    cindex = nextclassindex()
    classnames[cindex] = "InformationPageBrowsingEvent"
    
class AccountPageBrowsingEvent(BrowsingEvent):

    cindex = nextclassindex()
    classnames[cindex] = "AccountPageBrowsingEvent"

class ShopListBrowsingEvent(BrowsingEvent):

    cindex = nextclassindex()
    classnames[cindex] = "ShopListBrowsingEvent"

class BoardGamesUpdateEvent(BrowsingEvent):

    cindex = nextclassindex()
    classnames[cindex] = "BoardGamesUpdateEvent"

class CheckoutPageBrowsingEvent(BrowsingEvent):

    def is_closing(self):
        return True

class CustomerDataEntryBrowsingEvent(CheckoutPageBrowsingEvent):

    def Update(self, prevstate, newparams=None):
        retval = super().Update(prevstate,newparams)
        if retval["highwatermark"] < 2:
            retval["highwatermark"] = 2
        return retval

class ShippingMethodBrowsingEvent(CheckoutPageBrowsingEvent):

    def Update(self, prevstate, newparams=None):
        retval = super().Update(prevstate,newparams)
        if retval["highwatermark"] < 3:
            retval["highwatermark"] = 3
        return retval

class PaymentMethodBrowsingEvent(CheckoutPageBrowsingEvent):

    def Update(self, prevstate, newparams=None):
        retval = super().Update(prevstate,newparams)
        if retval["highwatermark"] < 4:
            retval["highwatermark"] = 4
        return retval

class ConfirmationPageBrowsingEvent(CheckoutPageBrowsingEvent):

    def Update(self, prevstate, newparams=None):
        retval = super().Update(prevstate,newparams)
        if retval["highwatermark"] < 5:
            retval["highwatermark"] = 5
        return retval

class CheckoutSuccessPageBrowsingEvent(CheckoutPageBrowsingEvent):

    def Update(self, prevstate, newparams=None):
        retval = super().Update(prevstate,newparams)
        if retval["highwatermark"] < 6:
            retval["highwatermark"] = 6
        return retval

    def is_success(self) -> bool:
        return True

class SystemEvent(SessionBodyEvent):

    def skip_update(self) -> bool:
        return True

class CouponOfferedEvent(SystemEvent):
    def __init__(self, time: int, event_label: str):
        super().__init__(time)
        self.event_label = event_label

    cindex = nextclassindex()
    classnames[cindex] = "CouponOfferedEvent"

    def Update(self, prevstate, newparams=None):
        retval = super().Update(prevstate,newparams)
        retval["couponstatus"] = 1 if retval["couponstatus"] == 0 else retval["couponstatus"]
        return retval


# print(classnames)

# globals

device_dict = {"mobile":0,"tablet":1,"desktop":2}
os_dict = {"ms":0,"apple":1,"linux":2}
lang_dict = {"hu":0}
sessionstatus_dict = {"Browsing":0,"CartModified":1}

def Update(prevstate,bodyevent,newparams=None):
    if prevstate["sessionstatus"] == "Bot":
        return prevstate
    return bodyevent.Update(prevstate,newparams)

def NewState(origin_string, user_agent_string, lang_string, firstbodyevent, newparams=None, sessionstatus=None):
    
    origin_cls = parser_api.parse_origin(origin_string)
    if origin_cls in origin_dict:
        origin = origin_dict[origin_cls]
    elif origin_cls in ["fblink","ggbot"]:
        return {"sessionstatus":"Bot"}
    else:
        origin = len(origin_dict)

    device_cls,os_cls = parser_api.parse_user_agent(user_agent_string)
    device = device_dict.get(device_cls,len(device_dict))
    os = os_dict.get(os_cls,len(os_dict))

    lang_cls = parser_api.parse_lang(lang_string)
    lang = lang_dict.get(lang_cls,len(lang_dict))

    original_state = {
        "admin_origin": origin_string,
        "admin_user_agent": user_agent_string,
        "admin_lang": lang_string,
        "sessionstart": firstbodyevent.time,
        "origin": origin,
        "device": device,
        "os": os,
        "lang":lang,
        "actioncount": 0,
        "lastbodyeventtime": None,
        "lastactioneventtime": None,
        "lastactioneventindex": None,
        "clickrate_avg": 0.0,
        "clickrate_squares": 0.0,
        "clickrate_var": 0.0,
        "z_score": 0.0,
        "sessionstatus": "Browsing" if not sessionstatus else sessionstatus,
        "clickrate": 0.0,
        "actionseparation": [0.0] * len(PARAMS["actionseparation"]),
        "actionaffinity": [[1 / classcount] * classcount for _ in range(len(PARAMS["actionaffinity"]))],
        "lastcategory": None,
        "categoryaffinity": [[1/MAX_CATEGORY] * MAX_CATEGORY for _ in range(len(PARAMS["categoryaffinity"]))],
        "carttotal":0.0,
        "cartcount":0,
        "cartdeltatotal": 0.0,
        "cartdeltacount": 0,
        "carttotaltrend": [0.0] * len(PARAMS["carttotaltrend"]),
        "cartcounttrend": [0.0] * len(PARAMS["cartcounttrend"]),
        "cartmodification": 0.0,
        "avgpricemanipulation": [0.0] * len(PARAMS["avgpricemanipulation"]),
        "couponstatus": 0,
        "lastprice": 0.0,
        "lastpriceviewedtrend": [0.0] * len(PARAMS["lastpriceviewedtrend"]),
        "tabcounttrend" : [0.0] * len(PARAMS["tabcounttrend"]),
        "redirectstrend" : [0.0] * len(PARAMS["redirectstrend"]),
        "tabtypetrend" : [0.0] * len(PARAMS["tabtypetrend"]),
        "navigationtrend": [0.0] * len(PARAMS["navigationtrend"]),
        "referrertrend": [0.0] * len(PARAMS["referrertrend"]),
        "sorttrend": [0.0] * len(PARAMS["sorttrend"]),
        "pagetrend": [0.0] * len(PARAMS["pagetrend"]),
        "producteverviewed": 0,
        "highwatermark": 0,
        "product_ids": [],
        "u_product": -1,
        "autocorr": 0
    }

    return Update(original_state,firstbodyevent,newparams)

def RowOfState(state):
    row ={k:state[k] for k in ["actioncount","origin","device","os","lang",
                               "carttotal","cartcount","cartdeltatotal","cartdeltacount",
                               "producteverviewed","couponstatus",
                               #"clickrate_squares",
                               "clickrate_avg","clickrate_var","z_score", "u_product", "autocorr"]}                  
    row["sessionage"] = state["lastbodyeventtime"] - state["sessionstart"]
    lastbodyeventtime = datetime.datetime.fromtimestamp(state["lastbodyeventtime"])
    row["hourofday"] = lastbodyeventtime.hour
    row["dayofweek"] = lastbodyeventtime.weekday()
    row["dayofmonth"] = lastbodyeventtime.day
    row["cartaverageprice"] = state["carttotal"]/state["cartcount"] if state["cartcount"] != 0 else 0.0
    # row["highwatermark"] = state["highwatermark"]
    
    arr = state["actionseparation"]
    for i in range(len(arr)):
        row["actionseparation_" + str(i)] = arr[i]

    arr = state["actionaffinity"]
    for i in range(len(arr)):
        for j in range(len(arr[0])):
            row["actionaffinity_" + str(i) + "_" + classnames[j]] = arr[i][j]

    arr = state["categoryaffinity"]
    for i in range(len(arr)):
        for j in range(len(arr[0])):
            row["categoryaffinity_" + str(i) + "_" + str(j)] = arr[i][j]
            
    arr = state["carttotaltrend"]
    for i in range(len(arr)):
        row["carttotaltrend_" + str(i)] = arr[i]

    arr = state["cartcounttrend"]
    for i in range(len(arr)):
        row["cartcounttrend_" + str(i)] = arr[i]

    arr = state["avgpricemanipulation"]
    for i in range(len(arr)):
        row["avgpricemanipulation_" + str(i)] = arr[i]

    arr = state["lastpriceviewedtrend"]
    for i in range(len(arr)):
        row["lastpriceviewedtrend_" + str(i)] = arr[i]

    arr = state["tabcounttrend"]
    for i in range(len(arr)):
        row["tabcounttrend_" + str(i)] = arr[i]

    arr = state["redirectstrend"]
    for i in range(len(arr)):
        row["redirectstrend_" + str(i)] = arr[i]

    arr = state["tabtypetrend"]
    for i in range(len(arr)):
        row["tabtypetrend_" + str(i)] = arr[i]

    arr = state["navigationtrend"]
    for i in range(len(arr)):
        row["navigationtrend_" + str(i)] = arr[i]

    arr = state["referrertrend"]
    for i in range(len(arr)):
        row["referrertrend_" + str(i)] = arr[i]
        
    arr = state["pagetrend"]
    for i in range(len(arr)):
        row["pagetrend_" + str(i)] = arr[i]
    
    arr = state["sorttrend"]
    for i in range(len(arr)):
        row["sorttrend_" + str(i)] = arr[i]
        
    return row

def FeatureFields():
    origin_string = "www.segmenthee.com"
    user_agent_string = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"
    lang_string = "hu-hu"
    timestamp = int(datetime.datetime.now().timestamp())
    firstbodyevent = CartModifyEvent(timestamp,0,0)
    return RowOfState(NewState(origin_string, user_agent_string, lang_string, firstbodyevent))

def RestartSessionQ(eventname, laststate):
    return (eventname == "CartModifyEvent") and (laststate["sessionstatus"] == "Browsing")
# Cart abandon prediction

EPS = 0.09

def PredictionReadyQ(state) -> bool:
    return (state["sessionstatus"] == "CartModified" and state["actioncount"] >= 5)

def is_browsing(state) -> bool:
    return state.get('sessionstatus') == 'Browsing'

def Score2Vote(score,THRESHOLD,EPS):
    if score > THRESHOLD+EPS:
        return 1
    if score < THRESHOLD-EPS:
        return 0
    return -1

def WillAbandonQ(state, modelpath='') -> Union[None, Tuple[int, float]]:
    if not PredictionReadyQ(state):
        return None
    model = xgboost.XGBClassifier()
    model.load_model(modelpath + FILE_NAME)
    row = RowOfState(state)
    line = np.array( list(row.values()) ).reshape( (1,len(row)) )
    # you should cast np.float32 to float beacuse JSON can't serialize types of np
    score = float(model.predict_proba(line)[0][1])
    vote = ABANDONER if score>SCORE_THRESHOLD else BUYER
    return (vote,score)

# Frustration point

FREE_SHIPPING_LIMIT = 20_000
MAX_TABCOUNT = 20

event2cindex = {classnames[cindex]:cindex for cindex in classnames}

# def tanh(x):
#     if x == 0:
#         return 0
#     e_2x = math.exp(2*x)
#     return (e_2x + 1) / (e_2x - 1)

def FrustrationReadyQ(state):
    return (state["sessionstatus"] == "Browsing" and state["actioncount"] >= 5 and state["clickrate_var"] > 0.0)

def FrustrationScore(state):
    S = 0
    # INCREASERS
    # clickrate
    s = math.tanh((state["clickrate_avg"] - state["clickrate"]) / 60) # in minutes
    S += 0.5 * (s + 1)
    # category jump
    S += 1 - max(state["categoryaffinity"][1])
    # affinities
    for event in [
        "CategoryPageBrowsingEvent",
        "SearchResultsBrowsingEvent",
        "CartBrowsingEvent",
    ]:
        idx = event2cindex[event]
        S += state["actionaffinity"][1][idx]
    # tabcount
    S += math.log(max([MAX_TABCOUNT, state["tabcounttrend"][0]])) / math.log(MAX_TABCOUNT)
    # carttotal vs free shipping
    if state["carttotal"] < FREE_SHIPPING_LIMIT:
        c = (2 * math.log(10)) / FREE_SHIPPING_LIMIT
        S += math.exp(-c * (FREE_SHIPPING_LIMIT - state["carttotal"]))
    # DECREASERS
    # product page browsing
    idx = event2cindex["ProductPageBrowsingEvent"]
    S -= state["actionaffinity"][1][idx]
    # MIXED
    # cart modification
    deltacount = state["cartdeltacount"]
    if deltacount > 0:
        S += deltacount / state["cartcount"]
    elif deltacount < 0: # deltacount is negative!
        S -= abs(deltacount) / (state["cartcount"] - deltacount)
    return S

def WasFrustratedQ(state) -> Union[None, Tuple[bool, float]]:
    ''' If got frustrated in the previous state'''
    if not FrustrationReadyQ(state):
        return None
    return (abs(state["z_score"]) > FRUSTRATION_TOLERANCE, state["z_score"])

def FrustrationUpperLimit(state):
    ''' Upper limit of being frustrated: returns a timestamp after which visitor considered frustrated'''
    timestamp_limit = state["clickrate_avg"] #+ state["lastactioneventtime"]
    timestamp_limit += state["clickrate_var"]**(1/2) * FRUSTRATION_TOLERANCE
    return int(timestamp_limit) + 1

def GetFrustrationPoint(state):
    '''
    If not Ready: return None
    If was FrustratedQ (got frustrated before = clicked quicker then tolerated): return True
    If not: return upper limit in seconds (timestamp): after this time we consider it to be frustrated as well (clicked slower then expected)
    '''
    if not FrustrationReadyQ(state):
        return None
    if WasFrustratedQ(state): #got frustrated before this event
        return True
    else: #return upper limit of frustration
        return FrustrationUpperLimit(state)

def WillLeaveQ(state,timestamp):
    ''' Will leave at time 'timestamp'? '''
    if not FrustrationReadyQ(state):
        return None
    delta_time = timestamp - state["lastactioneventtime"]
    z_score = abs(delta_time - state["clickrate_avg"])
    z_score *= state["clickrate_var"]**(-1/2)
    return z_score > FRUSTRATION_TOLERANCE

def AorB(uuid: str, *groups: int) -> Union[int,None]:
    S = sum(groups)
    residue = int(uuid[28:],base=16) % S
    for i in range(len(groups)):
        if residue < sum(groups[:i+1]):
            return i
    else:
        return None
