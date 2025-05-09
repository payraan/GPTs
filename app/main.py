from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import time
import uvicorn
from app.config.settings import HOST, PORT, DEBUG
from app.utils.rate_limiter import rate_limiter

# وارد کردن روترها
from app.api.routes import (
    dexscreener, geckoterminal, coingecko, moralis, 
    ave, coinstats, cryptocompare, solsniffer, cryptopanic
)

app = FastAPI(
    title="Crypto Multi-API",
    description="API جامع برای دسترسی به چندین سرویس رمزارز معروف",
    version="1.0.0",
)

# تنظیم CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# میان‌افزار برای ثبت زمان‌ پاسخگویی
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    
    # دریافت مسیر درخواست برای محدودیت نرخ
    path = request.url.path
    try:
        # بررسی محدودیت نرخ
        rate_limiter.check_rate_limit(path)
        
        response = await call_next(request)
        
        # اضافه کردن سربرگ زمان پردازش
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(process_time)
        return response
    
    except HTTPException as exc:
        # اگر محدودیت نرخ تجاوز شده باشد
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail}
        )

# مسیر اصلی
@app.get("/")
async def root():
    return {
        "message": "به Crypto Multi-API خوش آمدید!",
        "version": "1.0.0",
        "apis_supported": [
            "DexScreener", "GeckoTerminal", "CoinGecko", 
            "Moralis", "Ave", "CoinStats", 
            "CryptoCompare", "SolSniffer", "CryptoPanic"
        ]
    }

# اضافه کردن روترها
app.include_router(dexscreener.router, prefix="/api/dexscreener", tags=["DexScreener"])
app.include_router(geckoterminal.router, prefix="/api/geckoterminal", tags=["GeckoTerminal"])
app.include_router(coingecko.router, prefix="/api/coingecko", tags=["CoinGecko"])
app.include_router(moralis.router, prefix="/api/moralis", tags=["Moralis"])
app.include_router(ave.router, prefix="/api/ave", tags=["Ave"])
app.include_router(coinstats.router, prefix="/api/coinstats", tags=["CoinStats"])
app.include_router(cryptocompare.router, prefix="/api/cryptocompare", tags=["CryptoCompare"])
app.include_router(solsniffer.router, prefix="/api/solsniffer", tags=["SolSniffer"])
app.include_router(cryptopanic.router, prefix="/api/cryptopanic", tags=["CryptoPanic"])

if __name__ == "__main__":
    uvicorn.run("app.main:app", host=HOST, port=PORT, reload=DEBUG)
