from typing import Dict, Any, Optional, List
from app.config.settings import BASE_URLS, API_KEYS
from app.utils.helpers import make_request

COINSTATS_BASE_URL = BASE_URLS["COINSTATS"]
API_KEY = API_KEYS["COINSTATS"]

def get_headers():
    """هدرهای استاندارد برای CoinStats را برمی‌گرداند"""
    return {
        "accept": "application/json"
    }

# Coin endpoints
def get_coins() -> Dict[str, Any]:
    """دریافت لیست رمزارزها"""
    url = f"{COINSTATS_BASE_URL}/coins"
    return make_request(url=url, headers=get_headers())

def get_coin(coin_id: str) -> Dict[str, Any]:
    """دریافت اطلاعات یک رمزارز با شناسه خاص"""
    url = f"{COINSTATS_BASE_URL}/coins/{coin_id}"
    return make_request(url=url, headers=get_headers())

