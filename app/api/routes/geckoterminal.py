from fastapi import APIRouter, Query, Path, HTTPException
from typing import Optional
from app.services import geckoterminal
from app.utils.rate_limiter import rate_limiter
from app.config.settings import RATE_LIMITS

router = APIRouter()

# تنظیم محدودیت نرخ برای API
rate_limiter.set_limit("/api/geckoterminal", RATE_LIMITS["GECKOTERMINAL"])

# Pools endpoints
@router.get("/networks/trending_pools")
async def get_trending_pools_all_networks():
    """استخرهای ترند در تمام شبکه‌ها را دریافت می‌کند"""
    result = geckoterminal.get_trending_pools_all_networks()
    
    # محدود کردن تعداد نتایج به 20
    if "pools" in result and isinstance(result["pools"], list):
        result["pools"] = result["pools"][:20]
    
    return result

@router.get("/networks/{network}/trending_pools")
async def get_trending_pools_by_network(
    network: str = Path(..., description="نام شبکه")
):
    """استخرهای ترند در یک شبکه خاص را دریافت می‌کند"""
    result = geckoterminal.get_trending_pools_by_network(network)
    
    # محدود کردن تعداد نتایج به 20
    if "pools" in result and isinstance(result["pools"], list):
        result["pools"] = result["pools"][:20]
    
    return result

@router.get("/networks/{network}/tokens/{address}/info")
async def get_token_info(
    network: str = Path(..., description="نام شبکه"),
    address: str = Path(..., description="آدرس توکن")
):
    """اطلاعات خاص یک توکن در یک شبکه را دریافت می‌کند"""
    result = geckoterminal.get_token_info(network, address)
    
    # محدود کردن تعداد نتایج به 20 اگر داده‌ای وجود داشته باشد
    if "tokens" in result and isinstance(result["tokens"], list):
        result["tokens"] = result["tokens"][:20]
    
    return result

@router.get("/networks/{network}/pools/{pool_address}/info")
async def get_pool_tokens_info(
    network: str = Path(..., description="نام شبکه"),
    pool_address: str = Path(..., description="آدرس استخر")
):
    """اطلاعات توکن‌های یک استخر در یک شبکه را دریافت می‌کند"""
    return geckoterminal.get_pool_tokens_info(network, pool_address)

@router.get("/tokens/info_recently_updated")
async def get_recently_updated_tokens_info():
    """اطلاعات توکن‌های به‌روزرسانی شده اخیر در تمام شبکه‌ها را دریافت می‌کند"""
    result = geckoterminal.get_recently_updated_tokens_info()
    
    # محدود کردن تعداد نتایج به 20
    if "tokens" in result and isinstance(result["tokens"], list):
        result["tokens"] = result["tokens"][:20]
    
    return result

