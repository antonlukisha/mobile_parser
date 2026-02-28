import json
import csv
from pathlib import Path
import pandas as pd
from logger import logger
from src.models import Product


class DataExporter:
    @staticmethod
    def to_excel(products: list[Product], filename: Path) -> str:
        try:
            data = [p.to_dict() for p in products]
            df = pd.DataFrame(data)

            df.to_excel(filename, index=False, engine="openpyxl")
            logger.info(f"Successful export data to excel: {filename}")
            return str(filename.absolute())
        except Exception as e:
            logger.error(f"Error exporting data to excel: {e}")
            return "no file"

    @staticmethod
    def to_csv(products: list[Product], filename: Path) -> str:
        try:
            data = [p.to_dict() for p in products]

            with open(filename, "w", newline="", encoding="utf-8-sig") as f:
                if data:
                    writer = csv.DictWriter(f, fieldnames=data[0].keys(), delimiter=";")
                    writer.writeheader()
                    writer.writerows(data)

            logger.info(f"Successful export data to CSV: {filename}")
            return str(filename.absolute())
        except Exception as e:
            logger.error(f"Error exporting data to CSV: {e}")
            return "no file"

    @staticmethod
    def to_json(products: list[Product], filename: Path) -> str:
        try:
            data = [p.to_dict() for p in products]
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

            logger.info(f"Successful export data to json: {filename}")
            return str(filename.absolute())
        except Exception as e:
            logger.error(f"Error exporting data to excel: {e}")
            return "no file"
