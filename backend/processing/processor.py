# -*- coding: utf-8 -*-
from core.config import settings
from core.models import TaskQueue, TaskStatus

import requests
from typing import Optional


class Processor:
    def __init__(self, api_url: str = settings.API_URL):
        self.api_url = api_url

    def fetch_tasks(self) -> list[TaskQueue]:
        response = requests.get(f"{self.api_url}/tasks/pending")
        response.raise_for_status()
        return response.json()

    def update_task_status(
        self,
        task_id: int,
        status: str,
        error_stage: Optional[str] = None,
        error_message: Optional[str] = None,
    ):

        payload = {
            "status": status,
            "error_stage": error_stage,
            "error_message": error_message,
        }
        response = requests.put(f"{self.api_url}/tasks/{task_id}", json=payload)
        response.raise_for_status()

    def get_file(self, file_id: int) -> Optional[dict]:

        response = requests.get(f"{self.api_url}/files/{file_id}")
        if response.status_code == 200:
            return response.json()
        return None

    def parse_file(self, file_path: str) -> Optional[dict]:

        return {"parsed_data": f"Processed data from {file_path}"}

    def generate_report(self, file: dict, parsed_data: dict) -> Optional[dict]:

        return {"report": f"Report based on {parsed_data}"}

    def process_task(self, task: dict):

        task_id = task["id"]
        self.update_task_status(task_id, "IN_PROGRESS")

        file = self.get_file(task["source_file_id"])
        if not file:
            self.update_task_status(task_id, "FAILED", "file_fetch", "File not found")
            return

        parsed_data = self.parse_file(file["path"])
        if not parsed_data:
            self.update_task_status(task_id, "FAILED", "parsing", "Parsing error")
            return

        report = self.generate_report(file, parsed_data)
        if not report:
            self.update_task_status(
                task_id, "FAILED", "report_generation", "Report error"
            )
            return

        response = requests.post(f"{self.api_url}/reports", json=report)
        if response.status_code != 201:
            self.update_task_status(
                task_id, "FAILED", "report_saving", "Failed to save report"
            )
            return

        self.update_task_status(task_id, "DONE")
