from typing import Dict, Any, Optional, List
import logging
from app.config.settings import BASE_URLS, API_KEYS
from app.utils.helpers import make_request

# تنظیم لاگر
logger = logging.getLogger(__name__)

MORALIS_SOLANA_BASE_URL = BASE_URLS["MORALIS_SOLANA"]
MORALIS_INDEX_BASE_URL = BASE_URLS["MORALIS_INDEX"]
API_KEY = API_KEYS["MORALIS"]

def get_headers():
    """هدرهای استاندارد برای Moralis را برمی‌گرداند"""
    headers = {
        "accept": "application/json",
        "X-API-Key": API_KEY
    }
    logger.debug(f"استفاده از هدرهای موریالیس: {headers}")
    return headers

# Token API
def search_tokens(query: str, limit: int = 10) -> Dict[str, Any]:
    """جستجوی توکن‌ها"""
    try:
        url = f"{MORALIS_INDEX_BASE_URL}/tokens/search"
        params = {
            "query": query,
            "limit": limit
        }
        return make_request(url=url, params=params, headers=get_headers())
    except Exception as e:
        if "not available on your plan" in str(e):
            return {
                "error": "این قابلیت در پلن رایگان موریالیس در دسترس نیست",
                "message": "برای استفاده از جستجوی توکن، لطفاً به پلن پولی موریالیس ارتقا دهید.",
                "suggestion": "می‌توانید از اندپوینت‌های /tokens/trending یا /discovery/tokens استفاده کنید."
            }
        return {"error": str(e)}

# Token Discovery & Trending
def get_trending_tokens(limit: int = 10) -> Dict[str, Any]:
    """دریافت توکن‌های محبوب"""
    url = f"{MORALIS_INDEX_BASE_URL}/tokens/trending"
    params = {"limit": limit}
    return make_request(url=url, params=params, headers=get_headers())

# Strategy Builder
def get_filtered_tokens(chain: str = "solana", limit: int = 10, 
                      min_price: Optional[float] = None, max_price: Optional[float] = None,
                      min_volume_24h: Optional[float] = None, min_market_cap: Optional[float] = None) -> Dict[str, Any]:
    """دریافت توکن‌های فیلتر شده"""
    url = f"{MORALIS_INDEX_BASE_URL}/discovery/tokens"
    params = {
        "chain": chain,
        "limit": limit
    }
    
    if min_price is not None:
        params["min_price"] = min_price
    if max_price is not None:
        params["max_price"] = max_price
    if min_volume_24h is not None:
        params["min_volume_24h"] = min_volume_24h
    if min_market_cap is not None:
        params["min_market_cap"] = min_market_cap
        
    return make_request(url=url, params=params, headers=get_headers())

# Strategy Builder
def get_filtered_tokens(chain: str = "solana", limit: int = 10, 
                      min_price: Optional[float] = None, max_price: Optional[float] = None,
                      min_volume_24h: Optional[float] = None, min_market_cap: Optional[float] = None) -> Dict[str, Any]:
    """دریافت توکن‌های فیلتر شده"""
    url = f"{MORALIS_INDEX_BASE_URL}/discovery/tokens"
    params = {
        "chain": chain,
        "limit": limit
    }
    
    if min_price is not None:
        params["min_price"] = min_price
    if max_price is not None:
        params["max_price"] = max_price
    if min_volume_24h is not None:
        params["min_volume_24h"] = min_volume_24h
    if min_market_cap is not None:
        params["min_market_cap"] = min_market_cap
        
    return make_request(url=url, params=params, headers=get_headers())

# Pump Fun Tokens
def get_new_tokens_by_exchange(exchange: str = "pumpfun", limit: int = 100) -> Dict[str, Any]:
    """دریافت توکن‌های جدید بر اساس صرافی"""
    url = f"{MORALIS_SOLANA_BASE_URL}/token/mainnet/exchange/{exchange}/new"
    params = {"limit": limit}
    return make_request(url=url, params=params, headers=get_headers())

def get_bonding_tokens_by_exchange(exchange: str = "pumpfun", limit: int = 100) -> Dict[str, Any]:
    """دریافت توکن‌های در فاز پیوند بر اساس صرافی"""
    url = f"{MORALIS_SOLANA_BASE_URL}/token/mainnet/exchange/{exchange}/bonding"
    params = {"limit": limit}
    return make_request(url=url, params=params, headers=get_headers())

def get_graduated_tokens_by_exchange(exchange: str = "pumpfun", limit: int = 100) -> Dict[str, Any]:
    """دریافت توکن‌های فارغ‌التحصیل شده بر اساس صرافی"""
    url = f"{MORALIS_SOLANA_BASE_URL}/token/mainnet/exchange/{exchange}/graduated"
    params = {"limit": limit}
    return make_request(url=url, params=params, headers=get_headers())

def get_token_bonding_status(token_address: str) -> Dict[str, Any]:
    """دریافت وضعیت پیوند بر اساس آدرس توکن"""
    url = f"{MORALIS_SOLANA_BASE_URL}/token/mainnet/{token_address}/bonding-status"
    return make_request(url=url, headers=get_headers())

# Token Prices & Charts
def get_token_price(network: str, address: str) -> Dict[str, Any]:
    """دریافت قیمت توکن"""
    # اطمینان از استفاده از mainnet
    if network.lower() != "mainnet":
        logger.warning(f"شبکه نامعتبر: {network} - استفاده از 'mainnet' به جای آن")
        network = "mainnet"
    
    url = f"{MORALIS_SOLANA_BASE_URL}/token/{network}/{address}/price"
    return make_request(url=url, headers=get_headers())

# Token Metadata
def get_token_metadata(network: str, address: str) -> Dict[str, Any]:
    """دریافت متادیتای توکن"""
    # اطمینان از استفاده از mainnet
    if network.lower() != "mainnet":
        logger.warning(f"شبکه نامعتبر: {network} - استفاده از 'mainnet' به جای آن")
        network = "mainnet"
    
    url = f"{MORALIS_SOLANA_BASE_URL}/token/{network}/{address}/metadata"
    return make_request(url=url, headers=get_headers())

# Token Holders
def get_token_holder_stats(address: str) -> Dict[str, Any]:
    """دریافت آمار دارندگان توکن"""
    url = f"{MORALIS_SOLANA_BASE_URL}/token/mainnet/holders/{address}"
    return make_request(url=url, headers=get_headers())

def get_historical_token_holders(address: str, time_frame: str = "1d") -> Dict[str, Any]:
    """دریافت آمار تاریخی دارندگان توکن"""
    url = f"{MORALIS_SOLANA_BASE_URL}/token/mainnet/holders/{address}/historical"
    
    # بر اساس داکیومنت موریالیس، ترکیبی از پارامترها را امتحان می‌کنیم
    params = {}
    
    # گزینه 1: در برخی داکیومنت‌ها timeFrame با F بزرگ
    params["timeFrame"] = time_frame
    
    # گزینه 2: در برخی داکیومنت‌ها timeframe با f کوچک
    params["timeframe"] = time_frame
    
    # گزینه 3: ممکن است به پارامترهای اضافی نیاز باشد
    from datetime import datetime, timedelta
    today = datetime.now()
    from_date = (today - timedelta(days=30)).strftime("%Y-%m-%d")
    to_date = today.strftime("%Y-%m-%d")
    
    params["fromDate"] = from_date
    params["toDate"] = to_date
    
    logger.debug(f"درخواست تاریخی دارندگان توکن با پارامترهای: {params}")
    return make_request(url=url, params=params, headers=get_headers())

# Token Pairs & Liquidity
def get_token_pairs_by_address(network: str, address: str) -> Dict[str, Any]:
    """دریافت جفت‌های توکن بر اساس آدرس"""
    # اطمینان از استفاده از mainnet
    if network.lower() != "mainnet":
        logger.warning(f"شبکه نامعتبر: {network} - استفاده از 'mainnet' به جای آن")
        network = "mainnet"
    
    url = f"{MORALIS_SOLANA_BASE_URL}/token/{network}/{address}/pairs"
    return make_request(url=url, headers=get_headers())

def get_token_pair_stats(network: str, pair_address: str) -> Dict[str, Any]:
    """دریافت آمار جفت توکن"""
    # اطمینان از استفاده از mainnet
    if network.lower() != "mainnet":
        logger.warning(f"شبکه نامعتبر: {network} - استفاده از 'mainnet' به جای آن")
        network = "mainnet"
    
    url = f"{MORALIS_SOLANA_BASE_URL}/token/{network}/pairs/{pair_address}/stats"
    return make_request(url=url, headers=get_headers())

def get_aggregated_token_pair_stats(network: str, address: str) -> Dict[str, Any]:
    """دریافت آمار تجمیعی جفت توکن"""
    # اطمینان از استفاده از mainnet
    if network.lower() != "mainnet":
        logger.warning(f"شبکه نامعتبر: {network} - استفاده از 'mainnet' به جای آن")
        network = "mainnet"
    
    url = f"{MORALIS_SOLANA_BASE_URL}/token/{network}/{address}/pairs/stats"
    return make_request(url=url, headers=get_headers())

# Token Swaps
def get_swaps_by_pair_address(network: str, pair_address: str, limit: int = 100) -> Dict[str, Any]:
    """دریافت سوآپ‌ها بر اساس آدرس جفت"""
    # اطمینان از استفاده از mainnet
    if network.lower() != "mainnet":
        logger.warning(f"شبکه نامعتبر: {network} - استفاده از 'mainnet' به جای آن")
        network = "mainnet"
    
    url = f"{MORALIS_SOLANA_BASE_URL}/token/{network}/pairs/{pair_address}/swaps"
    params = {"limit": limit}
    return make_request(url=url, params=params, headers=get_headers())

def get_swaps_by_token_address(network: str, token_address: str, limit: int = 100) -> Dict[str, Any]:
    """دریافت سوآپ‌ها بر اساس آدرس توکن"""
    # اطمینان از استفاده از mainnet
    if network.lower() != "mainnet":
        logger.warning(f"شبکه نامعتبر: {network} - استفاده از 'mainnet' به جای آن")
        network = "mainnet"
    
    url = f"{MORALIS_SOLANA_BASE_URL}/token/{network}/{token_address}/swaps"
    params = {"limit": limit}
    return make_request(url=url, params=params, headers=get_headers())

def get_swaps_by_wallet_address(network: str, wallet_address: str, limit: int = 100) -> Dict[str, Any]:
    """دریافت سوآپ‌ها بر اساس آدرس کیف پول"""
    # اطمینان از استفاده از mainnet
    if network.lower() != "mainnet":
        logger.warning(f"شبکه نامعتبر: {network} - استفاده از 'mainnet' به جای آن")
        network = "mainnet"
    
    url = f"{MORALIS_SOLANA_BASE_URL}/account/{network}/{wallet_address}/swaps"
    params = {"limit": limit}
    return make_request(url=url, params=params, headers=get_headers())

# Token Snipers
def get_snipers_by_pair_address(network: str, pair_address: str) -> Dict[str, Any]:
    """دریافت sniper ها بر اساس آدرس جفت"""
    # اطمینان از استفاده از mainnet
    if network.lower() != "mainnet":
        logger.warning(f"شبکه نامعتبر: {network} - استفاده از 'mainnet' به جای آن")
        network = "mainnet"
    
    url = f"{MORALIS_SOLANA_BASE_URL}/token/{network}/pairs/{pair_address}/snipers"
    return make_request(url=url, headers=get_headers())

# Wallet API
def get_native_balance(network: str, address: str) -> Dict[str, Any]:
    """دریافت موجودی بومی بر اساس آدرس کیف پول"""
    # اطمینان از استفاده از mainnet
    if network.lower() != "mainnet":
        logger.warning(f"شبکه نامعتبر: {network} - استفاده از 'mainnet' به جای آن")
        network = "mainnet"
    
    url = f"{MORALIS_SOLANA_BASE_URL}/account/{network}/{address}/balance"
    return make_request(url=url, headers=get_headers())

def get_spl(network: str, address: str) -> Dict[str, Any]:
    """دریافت موجودی توکن بر اساس آدرس کیف پول"""
    # اطمینان از استفاده از mainnet
    if network.lower() != "mainnet":
        logger.warning(f"شبکه نامعتبر: {network} - استفاده از 'mainnet' به جای آن")
        network = "mainnet"
    
    url = f"{MORALIS_SOLANA_BASE_URL}/account/{network}/{address}/tokens"
    return make_request(url=url, headers=get_headers())

def get_portfolio(network: str, address: str) -> Dict[str, Any]:
    """دریافت داده‌های پرتفولیو بر اساس آدرس کیف پول"""
    # اطمینان از استفاده از mainnet
    if network.lower() != "mainnet":
        logger.warning(f"شبکه نامعتبر: {network} - استفاده از 'mainnet' به جای آن")
        network = "mainnet"
    
    url = f"{MORALIS_SOLANA_BASE_URL}/account/{network}/{address}/portfolio"
    return make_request(url=url, headers=get_headers())

