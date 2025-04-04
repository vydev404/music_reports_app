# -*- coding: utf-8 -*-
import requests

from processing.config import settings
from processing.exceptions import APIClientError
from processing.logger import Logger
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

log_file = settings.logger.log_dir / "api.log"
logger = Logger(log_file)


class APIClient:
    def __init__(self, api_url: str = settings.api_client.url):
        self.api_url = api_url
        logger.info(f"API Client initialized with URL: {self.api_url}")

    def fetch_tasks(self):
        try:
            logger.debug("Fetching pending tasks from API...")
            response = requests.get(f"{self.api_url}/tasks/pending")
            response.raise_for_status()
            task_count = len(response.json()["data"]["tasks"])
            logger.info(f"Successfully fetched {task_count} tasks")
            return [
                TaskDTO.from_response(data) for data in response.json()["data"]["tasks"]
            ]
        except requests.RequestException as e:
            logger.error(f"Error fetching tasks: {e}")
            raise APIClientError("FETCH_TASKS_ERROR", error=str(e))

    def update_task_status(self, task: TaskDTO):
        try:
            logger.debug(f"Updating status for task {task.id}...")
            payload = dict(
                status=task.status,
                error_stage=task.error_stage,
                error_message=task.error_message,
            )
            response = requests.put(f"{self.api_url}/tasks/{task.id}", json=payload)
            response.raise_for_status()
            logger.info(f"Successfully updated task {task.id}")
        except requests.RequestException as e:
            logger.error(f"Error updating task {task.id}: {e}")
            raise APIClientError("UPDATE_TASK_ERROR", task_id=task.id, error=str(e))

    def update_file_data(self, file: SourceFileDTO):
        try:
            logger.debug(f"Updating data for file {file.id}...")
            payload = dict(file_data=file.data)
            response = requests.put(f"{self.api_url}/files/{file.id}", json=payload)
            response.raise_for_status()
            logger.info(f"Successfully updated file {file.id}")
        except requests.RequestException as e:
            logger.error(f"Error updating file {file.id}: {e}")
            raise APIClientError("UPDATE_FILE_ERROR", file_id=file.id, error=str(e))

    def get_source_file_info(self, file_id: int) -> SourceFileDTO:
        try:
            logger.debug(f"Fetching source file info for ID {file_id}...")
            response = requests.get(f"{self.api_url}/files/{file_id}")
            response.raise_for_status()
            logger.info(f"Successfully fetched file info for ID {file_id}")
            return SourceFileDTO.from_response(response.json()["data"])
        except requests.RequestException as e:
            logger.error(f"Error fetching file info for ID {file_id}: {e}")
            raise APIClientError("FETCH_FILE_ERROR", file_id=file_id, error=str(e))

    def get_music_info(
        self, music_id: int = None, music_name: str = None
    ) -> MusicDTO | None:
        try:
            if music_name:
                logger.debug(f"Searching for music by name: {music_name}")
                response = requests.get(f"{self.api_url}/musics/search/{music_name}")
            elif music_id:
                logger.debug(f"Fetching music info for ID: {music_id}")
                response = requests.get(f"{self.api_url}/musics/{music_id}")
            else:
                return None
            response.raise_for_status()
            logger.info(f"Successfully fetched music info")
            return MusicDTO.from_response(response.json()["data"])
        except requests.RequestException as e:
            logger.error(f"Error fetching music info: {e}")
            raise APIClientError("FETCH_MUSIC_ERROR", error=str(e))

    def save_report(self, report_data: ReportDTO) -> bool:
        try:
            logger.debug("Saving report to API...")
            response = requests.post(f"{self.api_url}/reports", json=report_data)
            response.raise_for_status()
            logger.info("Report saved successfully")
            return response.status_code == 201
        except requests.RequestException as e:
            logger.error(f"Error saving report: {e}")
            raise APIClientError("SAVE_REPORT_ERROR", error=str(e))


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
        logger.info()
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
