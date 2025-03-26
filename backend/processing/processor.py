# -*- coding: utf-8 -*-
import requests

# from core.config import settings
from processing.schemas.dto import TaskStatus, TaskProcessingStage
from processing.data_filter import ParsedDataFilter
from processing.parsing.parser_manager import ParserManager
from processing.parsing.parsers import BaseParser
from processing.report_generator import ReportsGenerator
from processing.schemas.dto import (
    TaskDTO,
    SourceFileDTO,
    FilteredDTO,
    ParsedDTO,
    MusicDTO,
    ReportDTO,
)


class APIClient:
    def __init__(self, api_url: str):
        self.api_url = api_url

    # def __init__(self, api_url: str = settings.get_api_url()):
    #     self.api_url = api_url

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

    def update_file_data(self, file: SourceFileDTO):
        payload = dict(file_data=file.data)
        response = requests.put(f"{self.api_url}/files/{file.id}", json=payload)
        response.raise_for_status()

    def get_source_file_info(self, file_id: int) -> SourceFileDTO:
        response = requests.get(f"{self.api_url}/files/{file_id}")
        return SourceFileDTO.from_response(response.json()["data"])

    def get_music_info(
        self, music_id: int = None, music_name: str = None
    ) -> MusicDTO | None:
        if music_name:
            response = requests.get(f"{self.api_url}/musics/search/{music_name}")
        elif music_id:
            response = requests.get(f"{self.api_url}/musics/{music_id}")
        else:
            return None
        return MusicDTO.from_response(response.json()["data"])

    def save_report(self, report_data: ReportDTO) -> bool:
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
        self.api_client = api_client
        self.data_filter = data_filter
        self.report_generator = report_generator
        self.parser_manager = parser_manager

    def get_task_list(self):
        return self.api_client.fetch_tasks()

    def process_task(self, task: TaskDTO):
        # update task status PENDING -> IN_PROGRESS
        task.status = TaskStatus.IN_PROGRESS.value
        self.api_client.update_task_status(task)

        file = self.api_client.get_source_file_info(task.source_file_id)
        if not file:
            task.status = TaskStatus.FAILED.value
            task.error_stage = TaskProcessingStage.VALIDATING.value
            task.error_message = (
                f"Failed to fetch info for source file id:{task.source_file_id}"
            )
            self.api_client.update_task_status(task)
            return
        # parser select and parse data from source file
        parser: BaseParser = self.parser_manager.get_parser(file.type)
        parsed_data: ParsedDTO = parser.parse(file.path)
        if not parsed_data:
            task.status = TaskStatus.FAILED.value
            task.error_stage = TaskProcessingStage.VALIDATING.value
            task.error_message = (
                f"Failed parse source file or file empty. Id:{task.source_file_id}"
            )
            self.api_client.update_task_status(task)

        # filter parsed_data: remove duplicates, count files, extract additional info from db
        filtered_data: FilteredDTO = self.data_filter.filter_parsed_data(parsed_data)
        if not filtered_data:
            task.status = TaskStatus.FAILED.value
            task.error_stage = TaskProcessingStage.FILTERING.value
            task.error_message = f"Failed filter parsed data. Id:{task.source_file_id}"
            self.api_client.update_task_status(task)
        file.data = filtered_data
        self.api_client.update_file_data(file)
        report: ReportDTO = self.report_generator.generate_report(file)
        self.api_client.save_report(report)
