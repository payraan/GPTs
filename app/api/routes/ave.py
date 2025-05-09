from fastapi import APIRouter, Query, Path, HTTPException, Body
from typing import Optional, List, Dict, Any
from app.services import ave
from app.utils.rate_limiter import rate_limiter
from app.config.settings import RATE_LIMITS

router = APIRouter()

# تنظیم محدودیت نرخ برای API
rate_limiter.set_limit("/api/ave", RATE_LIMITS["AVE"])

# جستجوی توکن‌ها
@router.get("/tokens")
async def search_tokens(
    keyword: str = Query(..., description="کلیدواژه مورد نیاز برای جستجو"),
    chain: Optional[str] = Query(None, description="زنجیره (اختیاری)")
):
    """جستجوی توکن‌های مرتبط با کلیدواژه داده شده"""
    return ave.search_tokens(keyword, chain)

# دریافت قیمت توکن‌ها
@router.post("/tokens/price")
async def get_token_prices(
    token_ids: List[str] = Body(..., description="لیست شناسه‌های توکن، حداکثر 200 شناسه توکن"),
    tvl_min: int = Body(1000, description="حداقل TVL برای شمول در نتیجه جستجو (پیش‌فرض: 1000، 0 به معنی بدون آستانه)"),
    tx_24h_volume_min: int = Body(0, description="حداقل حجم 24 ساعته برای شمول در نتیجه جستجو (پیش‌فرض: 0، 0 به معنی بدون آستانه)")
):
    """دریافت قیمت آخرین توکن"""
    return ave.get_token_prices(token_ids, tvl_min, tx_24h_volume_min)

# دریافت جزئیات توکن
@router.get("/tokens/{token_id}")
async def get_token_details(
    token_id: str = Path(..., description="شناسه توکن = {توکن}-{زنجیره}, مثال: 0x05ea877924ec89ee62eefe483a8af97e77daeefd-bsc")
):
    """دریافت جزئیات توکن"""
    return ave.get_token_details(token_id)

# دریافت 100 نگهدارنده برتر توکن
@router.get("/tokens/top100/{token_id}")
async def get_token_top100_holders(
    token_id: str = Path(..., description="شناسه توکن = {توکن}-{زنجیره}, مثال: 0xd1fa42f9c7dcb525231e2cf6db0235290ada6381-bsc")
):
    """دریافت 100 نگهدارنده برتر توکن"""
    return ave.get_token_top100_holders(token_id)

# دریافت گزارش تشخیص ریسک قرارداد
@router.get("/contracts/{token_id}")
async def get_contract_risk_detection_report(
    token_id: str = Path(..., description="شناسه توکن = {توکن}-{زنجیره}, مثال: 0x05ea877924ec89ee62eefe483a8af97e77daeefd-bsc")
):
    """دریافت گزارش تشخیص ریسک قرارداد"""
    return ave.get_contract_risk_detection_report(token_id)
