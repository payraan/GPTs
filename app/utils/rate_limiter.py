import time
from typing import Dict, DefaultDict
from collections import defaultdict, deque
from fastapi import HTTPException

class RateLimiter:
    """
    محدودکننده نرخ درخواست برای API‌ها
    """
    
    def __init__(self):
        # مسیر -> زمان درخواست‌ها
        self.request_times: DefaultDict[str, deque] = defaultdict(lambda: deque(maxlen=1000))
        # مسیر -> حد مجاز در دقیقه
        self.limits: Dict[str, int] = {}
    
    def set_limit(self, path: str, limit_per_minute: int) -> None:
        """
        تنظیم محدودیت نرخ برای مسیر مشخص شده
        """
        self.limits[path] = limit_per_minute
    
    def check_rate_limit(self, path: str) -> None:
        """
        بررسی محدودیت نرخ برای مسیر معین
        اگر محدودیت نرخ تجاوز شود، استثنا ایجاد می‌شود
        """
        if path not in self.limits:
            return  # اگر محدودیتی تنظیم نشده باشد، محدودیتی اعمال نمی‌شود
        
        current_time = time.time()
        one_minute_ago = current_time - 60
        
        # حذف درخواست‌های قدیمی‌تر از یک دقیقه
        while self.request_times[path] and self.request_times[path][0] < one_minute_ago:
            self.request_times[path].popleft()
        
        # بررسی تعداد درخواست‌ها در دقیقه اخیر
        if len(self.request_times[path]) >= self.limits[path]:
            raise HTTPException(
                status_code=429,
                detail=f"حد مجاز درخواست تجاوز شده. محدودیت: {self.limits[path]} درخواست در دقیقه."
            )
        
        # اضافه کردن زمان درخواست جدید
        self.request_times[path].append(current_time)

# نمونه سینگلتون از محدودکننده نرخ
rate_limiter = RateLimiter()
