import os
import logging
from dotenv import load_dotenv
from typing import Dict, Any, Optional

# بارگذاری متغیرهای محیطی از فایل .env
load_dotenv()

# تنظیمات سرور
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "8086"))
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

# تنظیم لاگینگ برای عیب‌یابی بهتر
logging.basicConfig(
    level=logging.DEBUG if DEBUG else logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# کلیدهای API با مقادیر پیش‌فرض برای همه
API_KEYS: Dict[str, Optional[str]] = {
    "DEXSCREENER": os.getenv("DEXSCREENER_API_KEY", "FREE"),
    "GECKOTERMINAL": os.getenv("GECKOTERMINAL_API_KEY", "FREE"),
    "COINGECKO": os.getenv("COINGECKO_API_KEY", "FREE"),
    "MORALIS": os.getenv("MORALIS_API_KEY", "FREE"),  # اضافه کردن مقدار پیش‌فرض
    "AVE": os.getenv("AVE_API_KEY", "FREE"),  # اضافه کردن مقدار پیش‌فرض
    "COINSTATS": os.getenv("COINSTATS_API_KEY", "FREE"),  # اضافه کردن مقدار پیش‌فرض
    "CRYPTOCOMPARE": os.getenv("CRYPTOCOMPARE_API_KEY", "FREE"),  # اضافه کردن مقدار پیش‌فرض
    "SOLSNIFFER": os.getenv("SOLSNIFFER_API_KEY", "FREE"),  # اضافه کردن مقدار پیش‌فرض
    "CRYPTOPANIC": os.getenv("CRYPTOPANIC_API_KEY", "FREE"),  # اضافه کردن مقدار پیش‌فرض
}

# لاگ کردن کلیدهای API برای اشکال‌زدایی
for key, value in API_KEYS.items():
    # امنیتی: نمایش بخشی از کلید API و مخفی کردن باقی آن
    masked_value = value[:4] + '****' if value and len(value) > 8 else "Not set"
    logger.debug(f"API Key {key}: {masked_value}")

# پایه URL‌های API
BASE_URLS = {
    "DEXSCREENER": "https://api.dexscreener.com",
    "GECKOTERMINAL": "https://api.geckoterminal.com/api/v2",
    "COINGECKO": "https://api.coingecko.com/api/v3",
    "MORALIS_SOLANA": "https://solana-gateway.moralis.io",
    "MORALIS_INDEX": "https://deep-index.moralis.io/api/v2.2",
    "AVE": "https://prod.ave-api.com/v2",
    "COINSTATS": "https://openapiv1.coinstats.app",
    "CRYPTOCOMPARE": "https://min-api.cryptocompare.com/data",
    "SOLSNIFFER": "https://api.solsniffer.com",
    "CRYPTOPANIC": "https://cryptopanic.com/api/v1",
}

# محدودیت‌های نرخ درخواست (درخواست در دقیقه)
RATE_LIMITS = {
    "DEXSCREENER_DEFAULT": 300,
    "DEXSCREENER_TOKEN_PROFILES": 60,
    "DEXSCREENER_TOKEN_BOOSTS": 60,
    "DEXSCREENER_ORDERS": 60,
    "GECKOTERMINAL": 30,
    "COINGECKO": 30,
    "MORALIS": 60,
    "AVE": 50,
    "COINSTATS": 100,
    "CRYPTOCOMPARE": 100,
    "SOLSNIFFER": 50,
    "CRYPTOPANIC": 50,
}

# تنظیمات مربوط به محدودسازی اندازه پاسخ‌ها
MAX_RESPONSE_SIZE = 1024 * 1024  # 1 مگابایت
MAX_ITEMS_PER_PAGE = 100

# بررسی اعتبار تنظیمات
if DEBUG:
    logger.info(f"سرور در حالت دیباگ اجرا می‌شود با میزبان {HOST} و پورت {PORT}")
    for name, url in BASE_URLS.items():
        logger.debug(f"URL پایه برای {name}: {url}")
