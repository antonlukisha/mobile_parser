# Mobile API Parser

Парсер данных из мобильных API магазинов Лента и Лемана (Леруа Мерлен). Данное решение позволяет собирать информацию о товарах (название, бренд, цены).

---
## Реализация

Для разработки парсеров использовались инструменты сниффинга трафика мобильных приложений. Я использовал Proxyman.

---
## Возможности

- Парсинг товаров из мобильных API:
  - **Лента** — работает с использованием токенов авторизации
  - **Лемана (Леруа Мерлен)** — требуется валидный API ключ
- Поддержка двух городов: Москва и Санкт-Петербург
- Экспорт данных в форматах: Excel, CSV, JSON
- Прогресс-бар для отслеживания процесса парсинга
- Логирование всех операций
---
## Установка

### Требования
- Python 3.13 или выше
- uv или pip

### Развёртывание и запуск

Файл *.env.example* переименовываем в *.env* и заполняем необходимые переменные окружения.

```bash
git clone <url-репозитория>
cd mobile_parser

# с uv
uv venv
uv sync
uv run parser
uv run parser --store lenta --city msk --format json
# Парсинг Лемана (если есть рабочий API ключ)
uv run parser --store lemana --city spb --format excel
# Доступные форматы: excel, csv, json
uv run parser --store lenta --city spb --format csv

# без uv
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate
pip install -r requirements.txt
python main.py
python main.py --store lenta --city msk --format json
# Парсинг Лемана (если есть рабочий API ключ)
python main.py --store lemana --city spb --format excel
# Доступные форматы: excel, csv, json
python main.py --store lenta --city spb --format csv
```
---
## Структура
Каждый товар содержит следующие поля:

```json
{
  "id": "уникальный идентификатор",
  "name": "название товара",
  "brand": "бренд",
  "regular_price": 999.99,
  "promo_price": 799.99,
  "store": "lenta",
  "city": "msk"
}
```
Пример содержимого .env:
```env
LEMANA_URL=https://mobile.api-lmn.ru
LEMANA_APIKEY=ApiKey
LEMANA_USER_ID=UserID
LEMANA_APP_VERSION=0.0.0
LEMANA_MOBILE_VERSION=0.0.0
LEMANA_MOBILE_VERSION_OS=0.0.0
LEMANA_MOBILE_BUILD=0
LEMANA_REGION_MSK=0
LEMANA_REGION_SPB=0
LEMANA_CATEGORY_PATH=/.../.../

LENTA_URL=https://api.lenta.com
LENTA_DEVICE_ID=DeviceID
LENTA_TOKEN=Token
LENTA_APP_VERSION=6.73.0
LENTA_CLIENT=device_0.0.0
LENTA_DEVICE_OS_VERSION=0.0.0
LENTA_DEVICE_NAME=Device
LENTA_DEVICE_BRAND=Device
LENTA_DEVICE_OS=iOS
LENTA_CATEGORY_ID=0
```

## Проблемы
Лемана (Леруа Мерлен) — не удаётся получить валидный API ключ. Текущая реализация требует корректный apikey для работы и повторного дебага после получения ключа.