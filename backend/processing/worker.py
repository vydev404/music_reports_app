# -*- coding: utf-8 -*-
import time
from processing.logger import Logger
from processing.config import settings
from processing.data_filter import ParsedDataFilter
from processing.parsing import PARSERS, ParserManager
from processing.processor import Processor, APIClient
from processing.report_generator import ReportsGenerator

log_file = settings.logger.log_dir / "worker.log"
logger = Logger(log_file)


class Worker:
    def __init__(self, api_url: str = settings.api_client.url, interval: int = 5):
        logger.debug("Initializing worker")
        self.interval = interval
        self.api_client = APIClient(api_url)
        self.data_filter = ParsedDataFilter(self.api_client)
        self.parser_manager = ParserManager()
        self.report_generator = ReportsGenerator()
        logger.debug("Register parsers")
        self.register_parsers()

        logger.debug("Initializing file processor")
        self.processor = Processor(
            self.api_client,
            self.data_filter,
            self.report_generator,
            self.parser_manager,
        )
        logger.debug(f"Worker initialized successfully. ID: {id(self)}")

    def register_parsers(self):
        for parser_name, parser_class in PARSERS.items():
            self.parser_manager.register_parser(parser_name, parser_class())

    def run(self):
        while True:
            try:
                tasks = self.processor.get_task_list()
                if not tasks:
                    time.sleep(self.interval)
                    continue

                for task in tasks:
                    self.processor.process_task(task)

            except Exception as e:
                print(f"Worker error: {e}")

            time.sleep(self.interval)


if __name__ == "__main__":
    worker = Worker()
    worker.run()
