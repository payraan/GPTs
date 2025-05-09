from typing import Dict, Any, Optional, List
from app.config.settings import BASE_URLS, API_KEYS
from app.utils.helpers import make_request

DEXSCREENER_BASE_URL = BASE_URLS["DEXSCREENER"]
API_KEY = API_KEYS["DEXSCREENER"]

# تابع‌های دریافت پروفایل‌های توکن
def get_token_profiles() -> Dict[str, Any]:
    """دریافت آخرین پروفایل‌های توکن (محدودیت نرخ: 60 درخواست در دقیقه)"""
    url = f"{DEXSCREENER_BASE_URL}/token-profiles/latest/v1"
    headers = {"Accept": "*/*"}
    return make_request(url=url, headers=headers)

# تابع‌های دریافت توکن‌های تقویت شده
def get_boosted_tokens() -> Dict[str, Any]:
    """دریافت آخرین توکن‌های تقویت‌شده (محدودیت نرخ: 60 درخواست در دقیقه)"""
    url = f"{DEXSCREENER_BASE_URL}/token-boosts/latest/v1"
    headers = {"Accept": "*/*"}
    return make_request(url=url, headers=headers)

def get_most_active_boosts() -> Dict[str, Any]:
    """دریافت توکن‌هایی با بیشترین تقویت‌های فعال (محدودیت نرخ: 60 درخواست در دقیقه)"""
    url = f"{DEXSCREENER_BASE_URL}/token-boosts/top/v1"
    headers = {"Accept": "*/*"}
    return make_request(url=url, headers=headers)

# تابع بررسی سفارش‌های پرداخت شده برای توکن
def check_paid_orders(chain_id: str, token_address: str) -> Dict[str, Any]:
    """بررسی سفارش‌های پرداخت شده برای توکن (محدودیت نرخ: 60 درخواست در دقیقه)"""
    url = f"{DEXSCREENER_BASE_URL}/orders/v1/{chain_id}/{token_address}"
    headers = {"Accept": "*/*"}
    return make_request(url=url, headers=headers)

# تابع‌های دریافت جفت‌ها
def get_pairs_by_chain_and_address(chain_id: str, pair_id: str) -> Dict[str, Any]:
    """دریافت یک یا چند جفت بر اساس زنجیره و آدرس جفت (محدودیت نرخ: 300 درخواست در دقیقه)"""
    url = f"{DEXSCREENER_BASE_URL}/latest/dex/pairs/{chain_id}/{pair_id}"
    headers = {"Accept": "*/*"}
    return make_request(url=url, headers=headers)

def search_pairs(query: str) -> Dict[str, Any]:
    """جستجو برای جفت‌های مطابق با عبارت جستجو (محدودیت نرخ: 300 درخواست در دقیقه)"""
    url = f"{DEXSCREENER_BASE_URL}/latest/dex/search"
    params = {"q": query}
    headers = {"Accept": "*/*"}
    return make_request(url=url, params=params, headers=headers)

def get_pools_by_token(chain_id: str, token_address: str) -> Dict[str, Any]:
    """دریافت استخرهای یک توکن مشخص شده (محدودیت نرخ: 300 درخواست در دقیقه)"""
    url = f"{DEXSCREENER_BASE_URL}/token-pairs/v1/{chain_id}/{token_address}"
    headers = {"Accept": "*/*"}
    return make_request(url=url, headers=headers)

def get_pairs_by_token(chain_id: str, token_addresses: str) -> Dict[str, Any]:
    """دریافت یک یا چند جفت بر اساس آدرس‌های توکن (محدودیت نرخ: 300 درخواست در دقیقه)"""
    url = f"{DEXSCREENER_BASE_URL}/tokens/v1/{chain_id}/{token_addresses}"
    headers = {"Accept": "*/*"}
    return make_request(url=url, headers=headers)
