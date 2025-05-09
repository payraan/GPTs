from fastapi import APIRouter, Query, Path, HTTPException
from typing import Optional
from app.services import dexscreener
from app.utils.rate_limiter import rate_limiter
from app.config.settings import RATE_LIMITS

router = APIRouter()

# تنظیم محدودیت‌های نرخ برای انواع مختلف درخواست‌ها
rate_limiter.set_limit("/api/dexscreener/token-profiles/latest", RATE_LIMITS["DEXSCREENER_TOKEN_PROFILES"])
rate_limiter.set_limit("/api/dexscreener/token-boosts/latest", RATE_LIMITS["DEXSCREENER_TOKEN_BOOSTS"])
rate_limiter.set_limit("/api/dexscreener/token-boosts/top", RATE_LIMITS["DEXSCREENER_TOKEN_BOOSTS"])
rate_limiter.set_limit("/api/dexscreener/orders", RATE_LIMITS["DEXSCREENER_ORDERS"])
# درخواست‌های پیش‌فرض با نرخ 300 در دقیقه
rate_limiter.set_limit("/api/dexscreener/pairs", RATE_LIMITS["DEXSCREENER_DEFAULT"])
rate_limiter.set_limit("/api/dexscreener/search", RATE_LIMITS["DEXSCREENER_DEFAULT"])
rate_limiter.set_limit("/api/dexscreener/token-pairs", RATE_LIMITS["DEXSCREENER_DEFAULT"])
rate_limiter.set_limit("/api/dexscreener/tokens", RATE_LIMITS["DEXSCREENER_DEFAULT"])

@router.get("/token-profiles/latest")
async def get_token_profiles():
    """دریافت آخرین پروفایل‌های توکن"""
    return dexscreener.get_token_profiles()

@router.get("/token-boosts/latest")
async def get_boosted_tokens():
    """دریافت آخرین توکن‌های تقویت‌شده"""
    return dexscreener.get_boosted_tokens()

@router.get("/token-boosts/top")
async def get_most_active_boosts():
    """دریافت توکن‌هایی با بیشترین تقویت‌های فعال"""
    return dexscreener.get_most_active_boosts()

@router.get("/orders/{chain_id}/{token_address}")
async def check_paid_orders(
    chain_id: str = Path(..., description="شناسه زنجیره بلاکی"),
    token_address: str = Path(..., description="آدرس قرارداد توکن")
):
    """بررسی سفارش‌های پرداخت شده برای توکن"""
    return dexscreener.check_paid_orders(chain_id, token_address)

@router.get("/pairs/{chain_id}/{pair_id}")
async def get_pairs_by_chain_and_address(
    chain_id: str = Path(..., description="شناسه زنجیره بلاکی"),
    pair_id: str = Path(..., description="آدرس جفت")
):
    """دریافت یک یا چند جفت بر اساس زنجیره و آدرس جفت"""
    return dexscreener.get_pairs_by_chain_and_address(chain_id, pair_id)

@router.get("/search")
async def search_pairs(
    query: str = Query(..., description="عبارت جستجو")
):
    """جستجو برای جفت‌های مطابق با عبارت جستجو"""
    return dexscreener.search_pairs(query)

@router.get("/token-pairs/{chain_id}/{token_address}")
async def get_pools_by_token(
    chain_id: str = Path(..., description="شناسه زنجیره بلاکی"),
    token_address: str = Path(..., description="آدرس قرارداد توکن")
):
    """دریافت استخرهای یک توکن مشخص شده"""
    return dexscreener.get_pools_by_token(chain_id, token_address)

@router.get("/tokens/{chain_id}/{token_addresses}")
async def get_pairs_by_token(
    chain_id: str = Path(..., description="شناسه زنجیره بلاکی"),
    token_addresses: str = Path(..., description="آدرس‌های قرارداد توکن (می‌تواند چندین آدرس جدا شده با کاما باشد)")
):
    """دریافت یک یا چند جفت بر اساس آدرس‌های توکن"""
    return dexscreener.get_pairs_by_token(chain_id, token_addresses)
