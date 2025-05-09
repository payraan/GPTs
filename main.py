from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import dexscreener, geckoterminal, coingecko, moralis
from app.api.routes import ave, coinstats, cryptocompare, solsniffer, cryptopanic
from app.config.settings import HOST, PORT

# ایجاد اپلیکیشن FastAPI
app = FastAPI(
    title="Crypto Multi-API",
    description="API یکپارچه برای دسترسی به چندین API ارزهای دیجیتال",
    version="1.0.0"
)

# تنظیم CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# افزودن مسیرهای API
app.include_router(dexscreener.router, prefix="/api/dexscreener", tags=["DexScreener"])
app.include_router(geckoterminal.router, prefix="/api/geckoterminal", tags=["GeckoTerminal"])
app.include_router(coingecko.router, prefix="/api/coingecko", tags=["CoinGecko"])
app.include_router(moralis.router, prefix="/api/moralis", tags=["Moralis"])
app.include_router(ave.router, prefix="/api/ave", tags=["Ave"])
app.include_router(coinstats.router, prefix="/api/coinstats", tags=["CoinStats"])
app.include_router(cryptocompare.router, prefix="/api/cryptocompare", tags=["CryptoCompare"])

# مسیر ریشه
@app.get("/", tags=["Root"])
async def root():
    return {
        "message": "به Crypto Multi-API خوش آمدید!",
        "version": "1.0.0",
        "apis_supported": [
            "DexScreener", "GeckoTerminal", "CoinGecko", "Moralis", 
            "Ave", "CoinStats", "CryptoCompare", "SolSniffer", "CryptoPanic"
        ]
    }

# اجرای برنامه با Uvicorn (تنها در صورت اجرای مستقیم فایل)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host=HOST, port=PORT, reload=True)
