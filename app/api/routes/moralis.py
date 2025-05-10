from fastapi import APIRouter, Query, Path, HTTPException, Body
from typing import Optional, List, Dict, Any
import logging
from app.services import moralis
from app.utils.rate_limiter import rate_limiter
from app.config.settings import RATE_LIMITS

# تنظیم لاگر
logger = logging.getLogger(__name__)

router = APIRouter()

# تنظیم محدودیت نرخ برای API
rate_limiter.set_limit("/api/moralis", RATE_LIMITS["MORALIS"])

# Token Discovery & Trending
@router.get("/tokens/trending")
async def get_trending_tokens(
    limit: int = Query(10, description="محدودیت تعداد نتایج", le=100)
):
    """دریافت توکن‌های محبوب"""
    return moralis.get_trending_tokens(limit)

# Strategy Builder
@router.get("/discovery/tokens")
async def get_filtered_tokens(
    chain: str = Query("solana", description="زنجیره بلاکچین"),
    limit: int = Query(10, description="محدودیت تعداد نتایج", le=100),
    min_price: Optional[float] = Query(None, description="حداقل قیمت"),
    max_price: Optional[float] = Query(None, description="حداکثر قیمت"),
    min_volume_24h: Optional[float] = Query(None, description="حداقل حجم 24 ساعته"),
    min_market_cap: Optional[float] = Query(None, description="حداقل حجم بازار")
):
    """دریافت توکن‌های فیلتر شده"""
    return moralis.get_filtered_tokens(chain, limit, min_price, max_price, min_volume_24h, min_market_cap)

# Token Prices & Charts
@router.get("/token/{network}/{address}/price")
async def get_token_price(
    network: str = Path(..., description="شبکه (فقط mainnet مجاز است)"),
    address: str = Path(..., description="آدرس توکن")
):
    """دریافت قیمت توکن"""
    # اعتبارسنجی شبکه - فقط mainnet مجاز است
    if network.lower() != "mainnet":
        logger.warning(f"درخواست با شبکه نامعتبر: {network}. فقط 'mainnet' مجاز است.")
        raise HTTPException(
            status_code=400, 
            detail="برای API موریالیس سولانا فقط شبکه 'mainnet' مجاز است"
        )
    return moralis.get_token_price("mainnet", address)  # ارسال صریح mainnet

# Token Metadata
@router.get("/token/{network}/{address}/metadata")
async def get_token_metadata(
    network: str = Path(..., description="شبکه (فقط mainnet مجاز است)"),
    address: str = Path(..., description="آدرس توکن")
):
    """دریافت متادیتای توکن"""
    # اعتبارسنجی شبکه
    if network.lower() != "mainnet":
        logger.warning(f"درخواست با شبکه نامعتبر: {network}. فقط 'mainnet' مجاز است.")
        raise HTTPException(
            status_code=400, 
            detail="برای API موریالیس سولانا فقط شبکه 'mainnet' مجاز است"
        )
    return moralis.get_token_metadata("mainnet", address)

# Token Holders
@router.get("/token/mainnet/holders/{address}")
async def get_token_holder_stats(
    address: str = Path(..., description="آدرس توکن")
):
    """دریافت آمار دارندگان توکن"""
    return moralis.get_token_holder_stats(address)

@router.get("/token/mainnet/holders/{address}/historical")
async def get_historical_token_holders(
    address: str = Path(..., description="آدرس توکن"),
    time_frame: str = Query("1d", description="بازه زمانی")
):
    """دریافت آمار تاریخی دارندگان توکن"""
    logger.debug(f"درخواست تاریخی دارندگان توکن با آدرس: {address} و time_frame: {time_frame}")
    # اصلاح پارامترها مطابق با داکیومنت موریالیس
    return moralis.get_historical_token_holders(address, time_frame)

# Token Pairs & Liquidity
@router.get("/token/{network}/{address}/pairs")
async def get_token_pairs_by_address(
    network: str = Path(..., description="شبکه (فقط mainnet مجاز است)"),
    address: str = Path(..., description="آدرس توکن")
):
    """دریافت جفت‌های توکن بر اساس آدرس"""
    # اعتبارسنجی شبکه
    if network.lower() != "mainnet":
        logger.warning(f"درخواست با شبکه نامعتبر: {network}. فقط 'mainnet' مجاز است.")
        raise HTTPException(
            status_code=400, 
            detail="برای API موریالیس سولانا فقط شبکه 'mainnet' مجاز است"
        )
    return moralis.get_token_pairs_by_address("mainnet", address)

@router.get("/token/{network}/pairs/{pair_address}/stats")
async def get_token_pair_stats(
    network: str = Path(..., description="شبکه (فقط mainnet مجاز است)"),
    pair_address: str = Path(..., description="آدرس جفت")
):
    """دریافت آمار جفت توکن"""
    # اعتبارسنجی شبکه
    if network.lower() != "mainnet":
        logger.warning(f"درخواست با شبکه نامعتبر: {network}. فقط 'mainnet' مجاز است.")
        raise HTTPException(
            status_code=400, 
            detail="برای API موریالیس سولانا فقط شبکه 'mainnet' مجاز است"
        )
    return moralis.get_token_pair_stats("mainnet", pair_address)

@router.get("/token/{network}/{address}/pairs/stats")
async def get_aggregated_token_pair_stats(
    network: str = Path(..., description="شبکه (فقط mainnet مجاز است)"),
    address: str = Path(..., description="آدرس توکن")
):
    """دریافت آمار تجمیعی جفت توکن"""
    # اعتبارسنجی شبکه
    if network.lower() != "mainnet":
        logger.warning(f"درخواست با شبکه نامعتبر: {network}. فقط 'mainnet' مجاز است.")
        raise HTTPException(
            status_code=400, 
            detail="برای API موریالیس سولانا فقط شبکه 'mainnet' مجاز است"
        )
    return moralis.get_aggregated_token_pair_stats("mainnet", address)

# Token Swaps
@router.get("/token/{network}/pairs/{pair_address}/swaps")
async def get_swaps_by_pair_address(
    network: str = Path(..., description="شبکه (فقط mainnet مجاز است)"),
    pair_address: str = Path(..., description="آدرس جفت"),
    limit: int = Query(100, description="محدودیت تعداد نتایج", le=100),
    min_value_usd: Optional[float] = Query(None, description="حداقل ارزش سوآپ به دلار")
):
    """دریافت سوآپ‌ها بر اساس آدرس جفت"""
    # اعتبارسنجی شبکه
    if network.lower() != "mainnet":
        logger.warning(f"درخواست با شبکه نامعتبر: {network}. فقط 'mainnet' مجاز است.")
        raise HTTPException(
            status_code=400, 
            detail="برای API موریالیس سولانا فقط شبکه 'mainnet' مجاز است"
        )
    return moralis.get_swaps_by_pair_address("mainnet", pair_address, limit, min_value_usd)

@router.get("/token/{network}/{token_address}/swaps")
async def get_swaps_by_token_address(
    network: str = Path(..., description="شبکه (فقط mainnet مجاز است)"),
    token_address: str = Path(..., description="آدرس توکن"),
    limit: int = Query(100, description="محدودیت تعداد نتایج", le=100),
    min_value_usd: Optional[float] = Query(None, description="حداقل ارزش سوآپ به دلار")
):
    """دریافت سوآپ‌ها بر اساس آدرس توکن"""
    # اعتبارسنجی شبکه
    if network.lower() != "mainnet":
        logger.warning(f"درخواست با شبکه نامعتبر: {network}. فقط 'mainnet' مجاز است.")
        raise HTTPException(
            status_code=400, 
            detail="برای API موریالیس سولانا فقط شبکه 'mainnet' مجاز است"
        )
    return moralis.get_swaps_by_token_address("mainnet", token_address, limit, min_value_usd)

@router.get("/account/{network}/{wallet_address}/swaps")
async def get_swaps_by_wallet_address(
    network: str = Path(..., description="شبکه (فقط mainnet مجاز است)"),
    wallet_address: str = Path(..., description="آدرس کیف پول"),
    limit: int = Query(100, description="محدودیت تعداد نتایج", le=100),
    min_value_usd: Optional[float] = Query(None, description="حداقل ارزش سوآپ به دلار")
):
    """دریافت سوآپ‌ها بر اساس آدرس کیف پول"""
    # اعتبارسنجی شبکه
    if network.lower() != "mainnet":
        logger.warning(f"درخواست با شبکه نامعتبر: {network}. فقط 'mainnet' مجاز است.")
        raise HTTPException(
            status_code=400, 
            detail="برای API موریالیس سولانا فقط شبکه 'mainnet' مجاز است"
        )
    return moralis.get_swaps_by_wallet_address("mainnet", wallet_address, limit, min_value_usd)

# Token Snipers
@router.get("/token/{network}/pairs/{pair_address}/snipers")
async def get_snipers_by_pair_address(
    network: str = Path(..., description="شبکه (فقط mainnet مجاز است)"),
    pair_address: str = Path(..., description="آدرس جفت")
):
    """دریافت sniper ها بر اساس آدرس جفت"""
    # اعتبارسنجی شبکه
    if network.lower() != "mainnet":
        logger.warning(f"درخواست با شبکه نامعتبر: {network}. فقط 'mainnet' مجاز است.")
        raise HTTPException(
            status_code=400, 
            detail="برای API موریالیس سولانا فقط شبکه 'mainnet' مجاز است"
        )
    return moralis.get_snipers_by_pair_address("mainnet", pair_address)

# Wallet API
@router.get("/account/{network}/{address}/balance")
async def get_native_balance(
    network: str = Path(..., description="شبکه (فقط mainnet مجاز است)"),
    address: str = Path(..., description="آدرس کیف پول")
):
    """دریافت موجودی بومی بر اساس آدرس کیف پول"""
    # اعتبارسنجی شبکه
    if network.lower() != "mainnet":
        logger.warning(f"درخواست با شبکه نامعتبر: {network}. فقط 'mainnet' مجاز است.")
        raise HTTPException(
            status_code=400, 
            detail="برای API موریالیس سولانا فقط شبکه 'mainnet' مجاز است"
        )
    return moralis.get_native_balance("mainnet", address)

@router.get("/account/{network}/{address}/tokens")
async def get_spl(
    network: str = Path(..., description="شبکه (فقط mainnet مجاز است)"),
    address: str = Path(..., description="آدرس کیف پول")
):
    """دریافت موجودی توکن بر اساس آدرس کیف پول"""
    # اعتبارسنجی شبکه
    if network.lower() != "mainnet":
        logger.warning(f"درخواست با شبکه نامعتبر: {network}. فقط 'mainnet' مجاز است.")
        raise HTTPException(
            status_code=400, 
            detail="برای API موریالیس سولانا فقط شبکه 'mainnet' مجاز است"
        )
    return moralis.get_spl("mainnet", address)

@router.get("/account/{network}/{address}/portfolio")
async def get_portfolio(
    network: str = Path(..., description="شبکه (فقط mainnet مجاز است)"),
    address: str = Path(..., description="آدرس کیف پول")
):
    """دریافت داده‌های پرتفولیو بر اساس آدرس کیف پول"""
    # اعتبارسنجی شبکه
    if network.lower() != "mainnet":
        logger.warning(f"درخواست با شبکه نامعتبر: {network}. فقط 'mainnet' مجاز است.")
        raise HTTPException(
            status_code=400, 
            detail="برای API موریالیس سولانا فقط شبکه 'mainnet' مجاز است"
        )
    return moralis.get_portfolio("mainnet", address)
