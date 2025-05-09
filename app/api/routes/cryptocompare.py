from fastapi import APIRouter, Query, Path, HTTPException
from typing import Optional
from app.services import cryptocompare
from app.utils.rate_limiter import rate_limiter
from app.config.settings import RATE_LIMITS

router = APIRouter()

# تنظیم محدودیت نرخ برای API
rate_limiter.set_limit("/api/cryptocompare", RATE_LIMITS["CRYPTOCOMPARE"])

# قیمت‌های فعلی
@router.get("/price")
async def get_price(
    fsym: str = Query(..., description="نماد ارز (مثلاً BTC)"),
    tsyms: str = Query(..., description="نمادهای ارز مقصد (با کاما جدا شده، مثلاً USD,JPY,EUR)")
):
    """دریافت قیمت فعلی رمزارز"""
    return cryptocompare.get_price(fsym, tsyms)

# سیگنال‌های معاملاتی
@router.get("/tradingsignals/intotheblock/latest")
async def get_trading_signals_latest(
    fsym: str = Query(..., description="نماد ارز (مثلاً BTC)")
):
    """دریافت آخرین سیگنال‌های معاملاتی"""
    return cryptocompare.get_trading_signals_latest(fsym)

# اخبار
@router.get("/v2/news")
async def get_news(
    lang: str = Query("EN", description="زبان (مثلاً EN)")
):
    """دریافت اخبار"""
    return cryptocompare.get_news(lang)

@router.get("/news/feeds")
async def get_news_feeds():
    """دریافت فیدهای خبری"""
    return cryptocompare.get_news_feeds()

@router.get("/news/categories")
async def get_news_categories():
    """دریافت دسته‌بندی‌های خبری"""
    return cryptocompare.get_news_categories()

@router.get("/news/feedsandcategories")
async def get_news_feeds_and_categories():
    """دریافت فیدها و دسته‌بندی‌های خبری"""
    return cryptocompare.get_news_feeds_and_categories()
