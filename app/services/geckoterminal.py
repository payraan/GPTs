from typing import Dict, Any, Optional, List
from app.config.settings import BASE_URLS, API_KEYS
from app.utils.helpers import make_request

GECKOTERMINAL_BASE_URL = BASE_URLS["GECKOTERMINAL"]
API_KEY = API_KEYS["GECKOTERMINAL"]  # این FREE است

def get_headers():
    """هدرهای استاندارد برای GeckoTerminal را برمی‌گرداند"""
    return {
        "Accept": "application/json;version=20230302"  # ورژن توصیه شده در مستندات
    }

# Pools endpoints
def get_trending_pools_all_networks() -> Dict[str, Any]:
    """استخرهای روند در تمام شبکه‌ها را دریافت می‌کند"""
    url = f"{GECKOTERMINAL_BASE_URL}/networks/trending_pools"
    return make_request(url=url, headers=get_headers())

def get_trending_pools_by_network(network: str) -> Dict[str, Any]:
    """استخرهای روند در یک شبکه خاص را دریافت می‌کند"""
    url = f"{GECKOTERMINAL_BASE_URL}/networks/{network}/trending_pools"
    return make_request(url=url, headers=get_headers())

def get_token_info(network: str, token_address: str) -> Dict[str, Any]:
    """اطلاعات خاص یک توکن در یک شبکه را دریافت می‌کند"""
    url = f"{GECKOTERMINAL_BASE_URL}/networks/{network}/tokens/{token_address}/info"
    return make_request(url=url, headers=get_headers())

def get_pool_tokens_info(network: str, pool_address: str) -> Dict[str, Any]:
    """اطلاعات توکن‌های یک استخر در یک شبکه را دریافت می‌کند"""
    url = f"{GECKOTERMINAL_BASE_URL}/networks/{network}/pools/{pool_address}/info"
    return make_request(url=url, headers=get_headers())

def get_recently_updated_tokens_info() -> Dict[str, Any]:
    """اطلاعات 100 توکن به‌روزرسانی شده اخیر در تمام شبکه‌ها را دریافت می‌کند"""
    url = f"{GECKOTERMINAL_BASE_URL}/tokens/info_recently_updated"
    return make_request(url=url, headers=get_headers())

