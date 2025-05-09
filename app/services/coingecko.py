from typing import Dict, Any, Optional, List
from app.config.settings import BASE_URLS, API_KEYS
from app.utils.helpers import make_request

COINGECKO_BASE_URL = BASE_URLS["COINGECKO"]
API_KEY = API_KEYS["COINGECKO"]  # این FREE است

def get_headers():
    """هدرهای استاندارد برای CoinGecko را برمی‌گرداند"""
    headers = {"accept": "application/json"}
    if API_KEY != "FREE":
        headers["x-cg-demo-api-key"] = API_KEY
    return headers

# بررسی وضعیت سرور API
def ping() -> Dict[str, Any]:
    """وضعیت سرور API را بررسی می‌کند"""
    url = f"{COINGECKO_BASE_URL}/ping"
    return make_request(url=url, headers=get_headers())

# Coins endpoints
def get_coin_by_contract(id: str, contract_address: str) -> Dict[str, Any]:
    """همه متادیتا از صفحه رمزارز CoinGecko براساس پلتفرم دارایی و آدرس قرارداد توکن خاص دریافت می‌کند"""
    url = f"{COINGECKO_BASE_URL}/coins/{id}/contract/{contract_address}"
    return make_request(url=url, headers=get_headers())

def get_coin_contract_market_chart(id: str, contract_address: str, vs_currency: str, days: str) -> Dict[str, Any]:
    """داده‌های نمودار تاریخی شامل زمان، قیمت، حجم بازار و حجم معاملات 24 ساعته 
    براساس پلتفرم دارایی و آدرس قرارداد توکن خاص دریافت می‌کند"""
    url = f"{COINGECKO_BASE_URL}/coins/{id}/contract/{contract_address}/market_chart"
    params = {
        "vs_currency": vs_currency,
        "days": days
    }
    return make_request(url=url, params=params, headers=get_headers())

# Search endpoints
def search(query: str) -> Dict[str, Any]:
    """جستجو برای رمزارزها، دسته‌بندی‌ها و بازارهای موجود در CoinGecko"""
    url = f"{COINGECKO_BASE_URL}/search"
    params = {"query": query}
    return make_request(url=url, params=params, headers=get_headers())

def search_trending() -> Dict[str, Any]:
    """رمزارزهای داغ، NFT‌ها و دسته‌بندی‌ها در CoinGecko در 24 ساعت اخیر را دریافت می‌کند"""
    url = f"{COINGECKO_BASE_URL}/search/trending"
    return make_request(url=url, headers=get_headers())

# Global endpoints
def get_global() -> Dict[str, Any]:
    """داده‌های جهانی رمزارزها شامل رمزارزهای فعال، بازارها، حجم کل بازار رمزارزها و غیره را دریافت می‌کند"""
    url = f"{COINGECKO_BASE_URL}/global"
    return make_request(url=url, headers=get_headers())

def get_global_defi() -> Dict[str, Any]:
    """داده‌های جهانی امور مالی غیرمتمرکز (DeFi) رمزارزها شامل حجم بازار DeFi، حجم معاملات را دریافت می‌کند"""
    url = f"{COINGECKO_BASE_URL}/global/decentralized_finance_defi"
    return make_request(url=url, headers=get_headers())

# Companies public treasury
def get_companies_public_treasury(coin_id: str) -> Dict[str, Any]:
    """اطلاعات ذخایر عمومی شرکت‌ها در بیتکوین یا اتریوم را دریافت می‌کند"""
    url = f"{COINGECKO_BASE_URL}/companies/public_treasury/{coin_id}"
    return make_request(url=url, headers=get_headers())

