import hashlib
import json
import time
import random
from abc import ABC, abstractmethod
from datetime import datetime
import urllib3
import requests
from tqdm import tqdm
import config
from logger import logger
from src.models import City, Product, Store

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class StoreParser(ABC):
    def __init__(self) -> None:
        self.session = requests.Session()
        self.session.verify = False
        self.session.trust_env = False

    @abstractmethod
    def parse(self, city: City, page: int = 0, limit: int = 28) -> list[Product]:
        pass

    @abstractmethod
    def _parse_item(self, item: dict, city: City) -> Product | None:
        pass


class LemanaParser(StoreParser):

    def __init__(self) -> None:
        super().__init__()
        self.url = config.LEMANA_URL

        self.session.headers.update(
            {
                "Host": config.LEMANA_HOST,
                "apikey": config.LEMANA_APIKEY,
                "User-Agent": "ktor-client",
                "mobile-platform": "ios",
                "user_id": config.LEMANA_USER_ID,
                "plp-srp-view": "mixed",
                "app_version": config.LEMANA_APP_VERSION,
                "mobile-version": config.LEMANA_MOBILE_VERSION,
                "cat4-monetization": "true",
                "mobile-version-os": config.LEMANA_MOBILE_VERSION_OS,
                "Accept-Language": "ru",
                "X-Firebase-InstanceID": config.LEMANA_USER_ID,
                "Accept-Charset": "UTF-8",
                "Accept": "application/json",
                "Content-Type": "application/json; charset=UTF-8",
                "Accept-Encoding": "gzip, deflate, br",
                "mobile-build": config.LEMANA_MOBILE_BUILD,
                "ab-test-option": "opt1",
            }
        )

    @staticmethod
    def _generate_hash(payload: dict, timestamp: str) -> str:
        payload_str = json.dumps(payload, sort_keys=True, separators=(",", ":"))
        data = f"{timestamp}{payload_str}"
        return hashlib.md5(data.encode()).hexdigest()

    def parse(self, city: City, page: int = 0, limit: int = 28) -> list[Product]:
        all_products: list[Product | None] = []

        region_id = int(
            config.LEMANA_REGION_MSK
            if city == City.MOSCOW
            else config.LEMANA_REGION_SPB
        )
        total_items = 500

        pbar = tqdm(
            total=total_items,
            desc=f"Parsing Lemana PRO",
            unit="batch",
            ncols=80,
            bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]",
        )

        while True:
            offset = page * limit

            payload = {
                "familyId": "",
                "limitCount": limit,
                "limitFrom": offset,
                "regionsId": region_id,
                "facets": [],
                "firebasePseudoId": config.LEMANA_USER_ID,
                "availability": True,
                "showProducts": True,
                "showFacets": True,
                "showServices": True,
                "sitePath": config.LEMANA_CATEGORY_PATH,
            }

            timestamp = str(int(time.time()))
            self.session.headers.update(
                {
                    "timestamp": timestamp,
                    "hash": self._generate_hash(payload, timestamp),
                }
            )

            try:
                response = self.session.post(
                    f"{self.url}/mobile/v2/search", json=payload, timeout=10
                )

                if response.status_code != 200:
                    logger.error(
                        f"Response status [{response.status_code}] {response.text}"
                    )
                    break

                data = response.json()
                items = data.get("items", [])
                total = data.get("items_cnt", 0)

                if not items:
                    break

                old_products_size = len(all_products)
                all_products.extend(
                    [
                        product
                        for item in items
                        if (product := self._parse_item(item, city))
                    ]
                )

                pbar.update(len(all_products) - old_products_size)

                if total != total_items:
                    total_items = total
                    pbar.total = total_items
                    pbar.refresh()

                if len(all_products) >= total:
                    break

                page += 1
                time.sleep(random.uniform(0.5, 1.5))

            except Exception as e:
                logger.error(f"Parsing error: {e}")
                break
        pbar.close()
        return all_products

    def _parse_item(self, item: dict, city: City) -> Product | None:
        try:
            product_id = item.get("articul")
            if not product_id:
                return None

            name = item.get("displayedName", "")
            brand = item.get("brand", "Не указан")

            # Цены
            regular_price = None
            promo_price = None

            for price in item.get("prices", []):
                price_type = price.get("type")
                price_value = price.get("price")

                if price_type == "displayOld":
                    regular_price = price_value
                elif price_type == "displayMain":
                    promo_price = price_value

            if regular_price is None and promo_price is not None:
                regular_price = promo_price
                promo_price = None

            return Product(
                id=str(product_id),
                name=name,
                brand=brand,
                regular_price=float(regular_price) if regular_price else 0,
                promo_price=float(promo_price) if promo_price else None,
                store=Store.LEMANA,
                city=city,
            )

        except Exception as e:
            logger.error(f"Parsing item error: {e}")
            return None


class LentaParser(StoreParser):

    def __init__(self) -> None:
        super().__init__()
        self.url = config.LENTA_URL
        self.city_coords = {
            City.MOSCOW: {"lat": "55.7558", "lon": "37.6176"},
            City.SPB: {"lat": "59.9343", "lon": "30.3351"},
        }

        self.session.headers.update(
            {
                "Host": config.LENTA_HOST,
                "X-Device-Brand": config.LENTA_DEVICE_BRAND,
                "X-Organization-ID": "",
                "X-Device-OS-Version": config.LENTA_DEVICE_OS_VERSION,
                "Accept": "application/json",
                "DeviceId": config.LENTA_DEVICE_ID,
                "Accept-Encoding": "br;q=1.0, gzip;q=0.9, deflate;q=0.8",
                "User-Agent": f"lo, {config.LENTA_APP_VERSION}",
                "Att": "0",
                "X-Device-Name": config.LENTA_DEVICE_NAME,
                "Team": "SE",
                "X-Retail-Brand": "lo",
                "Client": config.LENTA_CLIENT,
                "Accept-Language": "ru-RU;q=1.0",
                "Method": "catalogItemsListing",
                "X-Platform": "omniapp",
                "AppStore": "AppStore",
                "X-Device-OS": config.LENTA_DEVICE_OS,
                "X-Delivery-Mode": "delivery",
                "Connection": "keep-alive",
                "AdvertisingId": "00000000-0000-0000-0000-000000000000",
                "SessionToken": config.LENTA_SESSION_TOKEN,
                "AuthToken": config.LENTA_AUTH_TOKEN,
                "Content-Type": "application/json",
                "App-Version": config.LENTA_APP_VERSION,
                "X-Device-id": config.LENTA_DEVICE_ID,
            }
        )

    def parse(self, city: City, page: int = 0, limit: int = 28) -> list[Product]:

        page = 0
        all_products: list[Product | None] = []
        total_items = 500

        pbar = tqdm(
            total=total_items,
            desc=f"Parsing Lenta",
            unit="batch",
            ncols=80,
            bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]",
        )

        while True:
            offset = page * limit

            payload = {
                "offset": offset,
                "limit": limit,
                "sort": {"order": "desc", "type": "popular"},
                "categoryId": config.LENTA_CATEGORY_ID,
            }

            timestamp = str(int(time.time()))
            self.session.headers.update(
                {
                    "Timestamp": timestamp,
                    "Created": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "LocalTime": datetime.now().strftime("%Y-%m-%dT%H:%M:%S+07:00"),
                }
            )

            try:
                response = self.session.post(
                    f"{self.url}/v1/catalog/items", json=payload, timeout=10
                )

                if response.status_code != 200:
                    logger.error(
                        f"Response status [{response.status_code}] {response.text}"
                    )
                    break

                data = response.json()
                items = data.get("items", [])
                total = data.get("total", 0)

                if not items:
                    break

                old_products_size = len(all_products)
                all_products.extend(
                    [
                        product
                        for item in items
                        if (product := self._parse_item(item, city))
                    ]
                )

                pbar.update(len(all_products) - old_products_size)

                if total != total_items:
                    total_items = total
                    pbar.total = total_items
                    pbar.refresh()

                if len(items) < limit or len(all_products) >= total:
                    break

                page += 1
                time.sleep(random.uniform(0.5, 1.0))

            except Exception as e:
                logger.error(f"Parsing error: {e}")
                break
        pbar.close()
        return all_products

    @staticmethod
    def _extract_brand_from_attributes(item_details: dict) -> str | None:
        if not item_details:
            return None

        attributes: list[dict[str, str | None]] = item_details.get("attributes", [])
        for attr in attributes:
            if (
                attr.get("name") == "Бренд"
                or attr.get("alias") == "brand"
                or attr.get("slug") == "brand"
            ):
                return attr.get("value")
        return None

    def _fetch_item_details(self, product_id: int) -> dict | None:
        max_retries = 3
        for attempt in range(max_retries):
            try:
                url = f"{self.url}/v1/catalog/items/{product_id}"

                timestamp = str(int(time.time()))
                self.session.headers.update(
                    {
                        "Timestamp": timestamp,
                        "Method": "catalogItemGet",
                        "Created": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    }
                )

                response = self.session.get(url, timeout=5)

                if response.status_code == 200:
                    data: dict = response.json()
                    time.sleep(0.1)
                    return data
                elif response.status_code == 429:
                    retry_after = int(response.headers.get("Retry-After", 3))
                    time.sleep(retry_after)
                    continue
                else:
                    logger.error(
                        f"Error fetching details for product {product_id} with status [{response.status_code}]"
                    )
                    return None

            except Exception as e:
                logger.error(f"Error fetching details for product {product_id}: {e}")
                if attempt >= max_retries - 1:
                    return None
        return None

    def _parse_item(self, item: dict, city: City) -> Product | None:
        try:
            product_id = item.get("id")
            if not product_id:
                return None

            brand = None
            item_details = self._fetch_item_details(product_id)
            if item_details:
                brand = self._extract_brand_from_attributes(item_details)

            name = item.get("name", "")

            prices = item.get("prices", {})

            regular_price = (
                prices.get("priceRegular")
                or prices.get("costRegular")
                or prices.get("price")
                or prices.get("cost")
            )
            promo_price = None

            if prices.get("isPromoactionPrice"):
                current_price = prices.get("price") or prices.get("cost")
                if current_price and current_price != regular_price:
                    promo_price = current_price

            return Product(
                id=str(product_id),
                name=name,
                brand=brand or "Не указан",
                regular_price=float(regular_price) if regular_price else 0,
                promo_price=float(promo_price) if promo_price else None,
                store=Store.LENTA,
                city=city,
            )

        except Exception as e:
            logger.error(f"Parsing item error: {e}")
            return None
