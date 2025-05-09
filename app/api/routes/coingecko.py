from fastapi import APIRouter, Query, Path, HTTPException
from typing import Optional
from app.services import coingecko
from app.utils.rate_limiter import rate_limiter
from app.config.settings import RATE_LIMITS

router = APIRouter()

# تنظیم محدودیت نرخ برای API
rate_limiter.set_limit("/api/coingecko", RATE_LIMITS["COINGECKO"])

# Ping endpoint
@router.get("/ping")
async def ping():
    """وضعیت سرور API را بررسی می‌کند"""
    return coingecko.ping()

# Coins endpoints
@router.get("/coins/{id}/contract/{contract_address}")
async def get_coin_by_contract(
    id: str = Path(..., description="شناسه پلتفرم (مثل 'ethereum')"),
    contract_address: str = Path(..., description="آدرس قرارداد توکن")
):
    """همه متادیتا از صفحه رمزارز CoinGecko براساس پلتفرم دارایی و آدرس قرارداد توکن خاص دریافت می‌کند"""
    return coingecko.get_coin_by_contract(id, contract_address)

@router.get("/coins/{id}/contract/{contract_address}/market_chart")
async def get_coin_contract_market_chart(
    id: str = Path(..., description="شناسه پلتفرم (مثل 'ethereum')"),
    contract_address: str = Path(..., description="آدرس قرارداد توکن"),
    vs_currency: str = Query(..., description="ارز مقایسه (مثل 'usd')"),
    days: str = Query(..., description="تعداد روزها یا 'max'")
):
    """داده‌های نمودار تاریخی شامل زمان، قیمت، حجم بازار و حجم معاملات 24 ساعته براساس پلتفرم دارایی و آدرس قرارداد توکن خاص دریافت می‌کند"""
    return coingecko.get_coin_contract_market_chart(id, contract_address, vs_currency, days)

# Search endpoints
@router.get("/search")
async def search(query: str = Query(..., description="عبارت جستجو")):
    """جستجو برای رمزارزها، دسته‌بندی‌ها و بازارهای موجود در CoinGecko"""
    return coingecko.search(query)

@router.get("/search/trending")
async def search_trending():
    """رمزارزهای داغ، NFT‌ها و دسته‌بندی‌ها در CoinGecko در 24 ساعت اخیر را دریافت می‌کند"""
    return coingecko.search_trending()

# Global endpoints
@router.get("/global")
async def get_global():
    """داده‌های جهانی رمزارزها شامل رمزارزهای فعال، بازارها، حجم کل بازار رمزارزها و غیره را دریافت می‌کند"""
    return coingecko.get_global()

@router.get("/global/decentralized_finance_defi")
async def get_global_defi():
    """داده‌های جهانی امور مالی غیرمتمرکز (DeFi) رمزارزها شامل حجم بازار DeFi، حجم معاملات را دریافت می‌کند"""
    return coingecko.get_global_defi()

# Companies public treasury
@router.get("/companies/public_treasury/{coin_id}")
async def get_companies_public_treasury(coin_id: str = Path(..., description="شناسه کوین (مثل 'bitcoin')")):
    """اطلاعات ذخایر عمومی شرکت‌ها در بیتکوین یا اتریوم را دریافت می‌کند"""
    return coingecko.get_companies_public_treasury(coin_id)
