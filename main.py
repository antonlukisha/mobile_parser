import sys
import argparse
from datetime import datetime
from pathlib import Path

from logger import logger
from src import DataExporter
from src import Store, City, OutputFormat
from src import LemanaParser, LentaParser


def run_parser(store: Store, city: City, file_format: OutputFormat) -> None:
    logger.info("Parsing params:")
    logger.info(f"Store: {str(store)}")
    logger.info(f"City: {str(city)}")
    logger.info(f"Output format: {str(file_format).upper()}")

    parser = None

    match store:
        case Store.LEMANA:
            parser = LemanaParser()
        case Store.LENTA:
            parser = LentaParser()

    if not parser:
        return

    logger.info("Data parsing...")
    products = parser.parse(city)

    if not products:
        return

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = Path(f"./data/{str(store)}_{str(city)}_{timestamp}").absolute()

    logger.info(f"Saving in file {str(file_format)}...")

    exporter = DataExporter()
    match file_format:
        case OutputFormat.EXCEL:
            filename = filename.with_suffix(".xlsx")
            exporter.to_excel(products, filename)
        case OutputFormat.CSV:
            filename = filename.with_suffix(".csv")
            exporter.to_csv(products, filename)
        case OutputFormat.JSON:
            filename = filename.with_suffix(".json")
            exporter.to_json(products, filename)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--store", choices=["lemana", "lenta"], help="Магазин")
    parser.add_argument("--city", choices=["msk", "spb"], help="Город")
    parser.add_argument(
        "--format", choices=["excel", "csv", "json"], help="Формат экспорта"
    )

    args = parser.parse_args()

    store_name = Store(args.store or "lenta")
    city = City(args.city or "msk")
    file_format = OutputFormat(args.format or "json")

    run_parser(store_name, city, file_format)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Script interrupted by user.")
        sys.exit(0)
    except Exception as e:
        logger.exception(f"An error occurred {e}.")
        sys.exit(1)
