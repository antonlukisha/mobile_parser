from dataclasses import dataclass
from enum import Enum


class OutputFormat(Enum):
    EXCEL = "excel"
    CSV = "csv"
    JSON = "json"

    def __str__(self) -> str:
        return self.value


class City(Enum):
    MOSCOW = "msk"
    SPB = "spb"

    def __str__(self) -> str:
        return self.value

    @property
    def name_ru(self) -> str:
        return {"msk": "Москва", "spb": "Санкт-Петербург"}[self.value]


class Store(Enum):
    LEMANA = "lemana"
    LENTA = "lenta"

    def __str__(self) -> str:
        return self.value

    @property
    def name_ru(self) -> str:
        return {"lemana": "Лемана ПРО", "lenta": "Лента"}[self.value]


@dataclass
class Product:
    id: str
    name: str
    regular_price: float
    promo_price: float | None
    brand: str
    store: Store
    city: City

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "brand": self.brand,
            "regular_price": self.regular_price,
            "promo_price": self.promo_price,
            "store": self.store.name_ru,
            "city": self.city.name_ru,
        }
