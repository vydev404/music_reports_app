# -*- coding: utf-8 -*-
import time
from processing.processor import Processor


class Worker:
    def __init__(self, processor: Processor, interval: int = 5):
        self.processor = processor
        self.interval = interval

    def run(self):
        while True:
            try:
                tasks = self.processor.fetch_tasks()
                if not tasks:
                    time.sleep(self.interval)
                    continue

                for task in tasks:
                    self.processor.process_task(task)

            except Exception as e:
                print(f"Worker error: {e}")

            time.sleep(self.interval)


if __name__ == "__main__":
    API_URL = "http://localhost:8000/api"
    processor = Processor(API_URL)
    worker = Worker(processor, interval=10)
    worker.run()
