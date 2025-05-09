from typing import Dict, Any, Optional, List
from app.config.settings import BASE_URLS, API_KEYS
from app.utils.helpers import make_request

AVE_BASE_URL = BASE_URLS["AVE"]
API_KEY = API_KEYS["AVE"]

def get_headers():
    """هدرهای استاندارد برای Ave را برمی‌گرداند"""
    return {
        "X-API-KEY": API_KEY
    }

# جستجوی توکن‌ها
def search_tokens(keyword: str, chain: Optional[str] = None) -> Dict[str, Any]:
    """جستجوی توکن‌های مرتبط با کلیدواژه داده شده"""
    url = f"{AVE_BASE_URL}/tokens"
    params = {"keyword": keyword}
    if chain:
        params["chain"] = chain
    
    return make_request(url=url, params=params, headers=get_headers())

# دریافت قیمت توکن‌ها
def get_token_prices(token_ids: List[str], tvl_min: int = 1000, tx_24h_volume_min: int = 0) -> Dict[str, Any]:
    """دریافت قیمت آخرین توکن"""
    url = f"{AVE_BASE_URL}/tokens/price"
    data = {
        "token_ids": token_ids,
        "tvl_min": tvl_min,
        "tx_24h_volume_min": tx_24h_volume_min
    }
    
    return make_request(url=url, method="POST", data=data, headers=get_headers())

# دریافت جزئیات توکن
def get_token_details(token_id: str) -> Dict[str, Any]:
    """دریافت جزئیات توکن"""
    url = f"{AVE_BASE_URL}/tokens/{token_id}"
    return make_request(url=url, headers=get_headers())

# دریافت 100 نگهدارنده برتر توکن
def get_token_top100_holders(token_id: str) -> Dict[str, Any]:
    """دریافت 100 نگهدارنده برتر توکن"""
    url = f"{AVE_BASE_URL}/tokens/top100/{token_id}"
    return make_request(url=url, headers=get_headers())

# دریافت گزارش تشخیص ریسک قرارداد
def get_contract_risk_detection_report(token_id: str) -> Dict[str, Any]:
    """دریافت گزارش تشخیص ریسک قرارداد"""
    url = f"{AVE_BASE_URL}/contracts/{token_id}"
    return make_request(url=url, headers=get_headers())
