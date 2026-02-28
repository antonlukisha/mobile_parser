import os
from typing import Final
from urllib.parse import urlparse
from dotenv import load_dotenv

load_dotenv()

# ================== ЛЕМАНА ПРО ==================
LEMANA_URL: Final = os.getenv("LEMANA_URL") or ""
LEMANA_HOST: Final = urlparse(LEMANA_URL).hostname or ""

LEMANA_APIKEY: Final = os.getenv("LEMANA_APIKEY") or ""
LEMANA_USER_ID: Final = os.getenv("LEMANA_USER_ID") or ""

LEMANA_ACCESS_TOKEN: Final = os.getenv("LEMANA_ACCESS_TOKEN") or ""

LEMANA_FIREBASE_ID: Final = os.getenv("LEMANA_FIREBASE_ID") or ""

LEMANA_APP_VERSION: Final = os.getenv("LEMANA_APP_VERSION") or ""
LEMANA_MOBILE_VERSION: Final = os.getenv("LEMANA_MOBILE_VERSION") or ""
LEMANA_MOBILE_VERSION_OS: Final = os.getenv("LEMANA_MOBILE_VERSION_OS") or ""
LEMANA_MOBILE_BUILD: Final = os.getenv("LEMANA_MOBILE_BUILD") or ""

LEMANA_REGION_MSK: Final = int(os.getenv("LEMANA_REGION_MSK") or "")
LEMANA_REGION_SPB: Final = int(os.getenv("LEMANA_REGION_SPB") or "")

LEMANA_CATEGORY_PATH: Final = os.getenv("LEMANA_CATEGORY_PATH") or ""

# ================== ЛЕНТА ==================
LENTA_URL: Final = os.getenv("LENTA_URL") or ""
LENTA_HOST: Final = urlparse(LENTA_URL).hostname or ""

LENTA_DEVICE_ID: Final = os.getenv("LENTA_DEVICE_ID") or ""
LENTA_SESSION_TOKEN: Final = os.getenv("LENTA_TOKEN") or ""
LENTA_AUTH_TOKEN: Final = os.getenv("LENTA_TOKEN") or ""

LENTA_APP_VERSION: Final = os.getenv("LENTA_APP_VERSION") or ""
LENTA_CLIENT: Final = os.getenv("LENTA_CLIENT") or ""
LENTA_DEVICE_OS_VERSION: Final = os.getenv("LENTA_DEVICE_OS_VERSION") or ""
LENTA_DEVICE_NAME: Final = os.getenv("LENTA_DEVICE_NAME") or ""
LENTA_DEVICE_BRAND: Final = os.getenv("LENTA_DEVICE_BRAND") or ""
LENTA_DEVICE_OS: Final = os.getenv("LENTA_DEVICE_OS") or ""

LENTA_CATEGORY_ID: Final = int(os.getenv("LENTA_CATEGORY_ID") or "")
