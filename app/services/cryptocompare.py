from typing import Dict, Any, Optional, List
from app.config.settings import BASE_URLS, API_KEYS
from app.utils.helpers import make_request

CRYPTOCOMPARE_BASE_URL = BASE_URLS["CRYPTOCOMPARE"]
API_KEY = API_KEYS["CRYPTOCOMPARE"]

def get_headers():
    """هدرهای استاندارد برای CryptoCompare را برمی‌گرداند"""
    headers = {"Content-type": "application/json; charset=UTF-8"}
    if API_KEY:
        headers["authorization"] = f"Apikey {API_KEY}"
    return headers

# قیمت‌های فعلی
def get_price(fsym: str, tsyms: str) -> Dict[str, Any]:
    """دریافت قیمت فعلی رمزارز"""
    url = f"{CRYPTOCOMPARE_BASE_URL}/price"
    params = {
        "fsym": fsym,
        "tsyms": tsyms
    }
    return make_request(url=url, params=params, headers=get_headers())

# سیگنال‌های معاملاتی
def get_trading_signals_latest(fsym: str) -> Dict[str, Any]:
    """دریافت آخرین سیگنال‌های معاملاتی"""
    url = f"{CRYPTOCOMPARE_BASE_URL}/tradingsignals/intotheblock/latest"
    params = {"fsym": fsym}
    return make_request(url=url, params=params, headers=get_headers())

# اخبار
def get_news(lang: str = "EN") -> Dict[str, Any]:
    """دریافت اخبار"""
    url = f"{CRYPTOCOMPARE_BASE_URL}/v2/news/"
    params = {"lang": lang}
    return make_request(url=url, params=params, headers=get_headers())

def get_news_feeds() -> Dict[str, Any]:
    """دریافت فیدهای خبری"""
    url = f"{CRYPTOCOMPARE_BASE_URL}/news/feeds"
    return make_request(url=url, headers=get_headers())

def get_news_categories() -> Dict[str, Any]:
    """دریافت دسته‌بندی‌های خبری"""
    url = f"{CRYPTOCOMPARE_BASE_URL}/news/categories"
    return make_request(url=url, headers=get_headers())

def get_news_feeds_and_categories() -> Dict[str, Any]:
    """دریافت فیدها و دسته‌بندی‌های خبری"""
    url = f"{CRYPTOCOMPARE_BASE_URL}/news/feedsandcategories"
    return make_request(url=url, headers=get_headers())

