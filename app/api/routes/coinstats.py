from fastapi import APIRouter, Query, Path, HTTPException
from typing import Optional
from app.services import coinstats
from app.utils.rate_limiter import rate_limiter
from app.config.settings import RATE_LIMITS

router = APIRouter()

# تنظیم محدودیت نرخ برای API
rate_limiter.set_limit("/api/coinstats", RATE_LIMITS["COINSTATS"])

# Coin endpoints
@router.get("/coins")
async def get_coins():
    """دریافت لیست رمزارزها"""
    return coinstats.get_coins()

@router.get("/coins/{coin_id}")
async def get_coin(
    coin_id: str = Path(..., description="شناسه رمزارز")
):
    """دریافت اطلاعات یک رمزارز با شناسه خاص"""
    return coinstats.get_coin(coin_id)

