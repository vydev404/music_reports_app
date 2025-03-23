# -*- coding: utf-8 -*-
from core.config import settings
from core.models import TaskQueue, TaskStatus, TaskProcessingStage

import requests
from typing import Optional

from processing.data_filter import ParsedDataFilter
from processing.parsing.parser_manager import ParserManager
from processing.report_generator import ReportsGenerator
from processing.schemas.dto import TaskDTO, SourceFileDTO, ReportDTO


class APIClient:
    def __init__(self, api_url: str = settings.get_api_url()):
        self.api_url = api_url

    def fetch_tasks(self):
        response = requests.get(f"{self.api_url}/tasks/pending")
        response.raise_for_status()
        return [
            TaskDTO.from_response(data) for data in response.json()["data"]["tasks"]
        ]

    def update_task_status(
        self,
        task: TaskDTO,
    ):
        payload = dict(
            status=task.status,
            error_stage=task.error_stage,
            error_message=task.error_message,
        )
        response = requests.put(f"{self.api_url}/tasks/{task.id}", json=payload)
        response.raise_for_status()

    def get_source_file_info(self, file_id: int) -> SourceFileDTO:
        response = requests.get(f"{self.api_url}/files/{file_id}")
        return SourceFileDTO.from_response(response.json()["data"])

    def save_report(self, report_data: dict) -> bool:
        response = requests.post(f"{self.api_url}/reports", json=report_data)
        return response.status_code == 201


class Processor:
    def __init__(
        self,
        api_client: APIClient,
        data_filter: ParsedDataFilter,
        report_generator: ReportsGenerator,
        parser_manager: ParserManager,
    ):
        self.data_filter = data_filter
        self.report_generator = report_generator
        self.parser_manager = parser_manager

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
