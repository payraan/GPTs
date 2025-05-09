import json
import logging
from typing import Dict, Any, Optional, Union, List
import requests
from fastapi import HTTPException

# تنظیم لاگر
logger = logging.getLogger(__name__)

def make_request(
    url: str, 
    method: str = "GET", 
    params: Optional[Dict[str, Any]] = None,
    headers: Optional[Dict[str, str]] = None,
    data: Optional[Dict[str, Any]] = None,
    timeout: int = 30,
    max_retries: int = 3,
) -> Dict[str, Any]:
    """
    تابع عمومی برای ارسال درخواست‌های HTTP با قابلیت تلاش مجدد در صورت خطا
    همراه با لاگ‌گذاری گسترده برای عیب‌یابی بهتر
    """
    headers = headers or {}
    params = params or {}
    data_json = json.dumps(data) if data else None
    
    # لاگ اطلاعات درخواست برای عیب‌یابی
    logger.debug(f"API Request: {method} {url}")
    logger.debug(f"Headers: {mask_sensitive_headers(headers)}")
    logger.debug(f"Params: {params}")
    if data:
        logger.debug(f"Data: {data}")
    
    retry_count = 0
    while retry_count < max_retries:
        try:
            if method == "GET":
                response = requests.get(url, params=params, headers=headers, timeout=timeout)
            elif method == "POST":
                response = requests.post(url, params=params, headers=headers, json=data, timeout=timeout)
            elif method == "PUT":
                response = requests.put(url, params=params, headers=headers, json=data, timeout=timeout)
            elif method == "DELETE":
                response = requests.delete(url, params=params, headers=headers, timeout=timeout)
            else:
                raise ValueError(f"متد HTTP غیرمجاز: {method}")
            
            # لاگ اطلاعات پاسخ
            logger.debug(f"Response Status: {response.status_code}")
            
            # نمایش بخشی از پاسخ (برای جلوگیری از لاگ‌های خیلی بزرگ)
            response_preview = response.text[:200] + "..." if len(response.text) > 200 else response.text
            logger.debug(f"Response Body: {response_preview}")
            
            if response.status_code < 400:
                try:
                    return response.json()
                except json.JSONDecodeError:
                    logger.warning(f"پاسخ JSON نامعتبر: {response.text[:100]}...")
                    return {"status": "success", "content": response.text}
            
            # اطلاعات بیشتر برای خطاهای رایج
            if response.status_code == 401:
                logger.error(f"خطای احراز هویت (401): احتمالاً کلید API نامعتبر است - {url}")
                # بررسی برای خطاهای خاص API موریالیس
                if "moralis" in url.lower():
                    logger.error("برای API موریالیس: لطفاً کلید API را در فایل .env بررسی کنید.")
            elif response.status_code == 400:
                logger.error(f"خطای درخواست نامعتبر (400): پارامترهای نادرست - {url}")
                # لاگ پارامترها برای کمک به عیب‌یابی
                logger.error(f"پارامترهای ارسال شده: {params}")
                # بررسی برای خطاهای خاص API موریالیس
                if "moralis" in url.lower() and "solana" in url.lower():
                    logger.error("برای API سولانا موریالیس: از 'mainnet' به جای 'solana' استفاده کنید.")
            elif response.status_code == 429:  # حد مجاز درخواست (Rate Limit)
                logger.warning(f"محدودیت نرخ درخواست (429): تلاش مجدد {retry_count + 1}/{max_retries}")
                retry_count += 1
                continue
            else:
                logger.error(f"خطای API: {response.status_code} - {response_preview}")
            
            error_message = f"خطای API: {response.status_code} - {response.text}"
            raise HTTPException(status_code=response.status_code, detail=error_message)
        
        except (requests.RequestException, requests.Timeout) as e:
            logger.warning(f"خطای شبکه در درخواست: {str(e)} - تلاش مجدد {retry_count + 1}/{max_retries}")
            retry_count += 1
            if retry_count == max_retries:
                logger.error(f"تمام تلاش‌های مجدد ناموفق بود: {str(e)}")
                raise HTTPException(status_code=503, detail=f"خطای اتصال به سرویس: {str(e)}")
    
    logger.error("تعداد درخواست‌ها بیش از حد مجاز است.")
    raise HTTPException(status_code=429, detail="تعداد درخواست‌ها بیش از حد مجاز است. لطفاً بعداً تلاش کنید.")

def mask_sensitive_headers(headers: Dict[str, str]) -> Dict[str, str]:
    """
    مخفی کردن اطلاعات حساس در هدرها مانند کلیدهای API
    """
    masked_headers = headers.copy()
    sensitive_keys = ['x-api-key', 'api-key', 'apikey', 'authorization', 'x-cg-demo-api-key', 'auth-token']
    
    for key in masked_headers:
        if key.lower() in sensitive_keys and masked_headers[key]:
            # نمایش 4 کاراکتر اول و مخفی کردن بقیه
            value = masked_headers[key]
            if len(value) > 8:
                masked_headers[key] = value[:4] + '*' * (len(value) - 4)
            else:
                masked_headers[key] = '****'
    
    return masked_headers

def filter_response(response: Dict[str, Any], max_items: int = 100) -> Dict[str, Any]:
    """
    محدود کردن تعداد آیتم‌ها در پاسخ برای جلوگیری از پاسخ‌های بسیار بزرگ
    """
    # کپی پاسخ اصلی
    filtered = response.copy()
    
    # بررسی و محدود کردن آرایه‌ها
    for key, value in filtered.items():
        if isinstance(value, list) and len(value) > max_items:
            filtered[key] = value[:max_items]
            filtered[f"{key}_total"] = len(value)
            filtered[f"{key}_truncated"] = True
    
    return filtered

def construct_error_response(status_code: int, message: str) -> Dict[str, Any]:
    """
    ایجاد پاسخ خطای استاندارد
    """
    return {
        "status": "error",
        "code": status_code,
        "message": message
    }

def suggest_fix_for_error(url: str, status_code: int, response_text: str) -> str:
    """
    پیشنهاد راه‌حل براساس خطای دریافتی
    """
    if "moralis" in url.lower():
        if status_code == 401:
            return "کلید API موریالیس احتمالاً نامعتبر است. فایل .env را بررسی کنید."
        elif status_code == 400:
            if "solana" in url.lower():
                return "برای API سولانا موریالیس، از 'mainnet' به جای 'solana' در پارامتر شبکه استفاده کنید."
            elif "timeFrame" in url.lower() or "timeFrame" in response_text:
                return "پارامتر 'timeFrame' باید به 'timeframe' تغییر یابد."
    
    elif "coinstats" in url.lower() and status_code == 401:
        return "کلید API کوین استتس احتمالاً نامعتبر است. فایل .env را بررسی کنید."
    
    return "لطفاً پارامترهای درخواست و اعتبار API را بررسی کنید."
