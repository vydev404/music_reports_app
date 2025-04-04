# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-


class ErrorMessages:
    APICLIENT_ERRORS = {
        "FETCH_TASKS_ERROR": "Failed to fetch tasks from API. Error: {error}",
        "UPDATE_TASK_ERROR": "Failed to update task {task_id}. Error: {error}",
        "UPDATE_FILE_ERROR": "Failed to update file {file_id}. Error: {error}",
        "FETCH_FILE_ERROR": "Failed to fetch file info for ID {file_id}. Error: {error}",
        "FETCH_MUSIC_ERROR": "Failed to fetch music info. Error: {error}",
        "SAVE_REPORT_ERROR": "Failed to save report. Error: {error}",
    }
    PARSING_ERRORS = {
        "invalid_timecode_format": "Invalid timecode format: '{timecode}' must be 'HH:MM:SS:FF'",
        "input_empty": "Missing 1 required positional argument: 'frames'",
        "input_type_error": "Invalid type: '{type}' must be 'int'",
        "file_reading_error": "File reading error: '{error}'",
        "file_empty_error": "No data for parsing. File empty: '{file}'",
    }
    FILTERING_ERRORS = {
        "no_data": "Received empty data list",
    }
    PROCESSING_ERRORS = {
        "parsed_data_empty": "Received empty Parsed Data object from: {file}",
        "is_processed_failed": "File was already processed: {file} with status {status} on {stage}",
        "is_processed_successful": "File was already processed: {file}. Skipping",
    }
    REPORTING_ERRORS = {}


class BaseError(Exception):
    def __init__(self, message):
        # Call the base class constructor with the parameters it needs
        super().__init__(message)


class ProcessingError(BaseError):
    def __init__(self, error_type: str, **kwargs):
        """
        :param error_type: Key from  `ErrorMessages.PROCESSING_ERRORS`
        :param kwargs: Additional params for message formating
        """
        message_template = ErrorMessages.PROCESSING_ERRORS.get(
            error_type, "Unknown processing error."
        )
        message = message_template.format(**kwargs)
        super().__init__(message)


class APIClientError(BaseError):
    """ApiClient custom errors"""

    def __init__(self, error_type: str, **kwargs):
        """
        :param error_type: Key from  `ErrorMessages.APICLIENT_ERRORS`
        :param kwargs:Additional params for message formating
        """
        message_template = ErrorMessages.APICLIENT_ERRORS.get(
            error_type, "Unknown api_client error."
        )
        message = message_template.format(**kwargs)
        super().__init__(message)


class ParsingError(BaseError):
    """File parsing errors"""

    def __init__(self, error_type: str, **kwargs):
        """
        :param error_type: Key from  `ErrorMessages.PARSING_ERRORS`
        :param kwargs:Additional params for message formating
        """
        message_template = ErrorMessages.PARSING_ERRORS.get(
            error_type, "Unknown parsing error."
        )
        message = message_template.format(**kwargs)
        super().__init__(message)


class ParserManagerError(BaseError):
    """Помилка парсингу файлу."""

    def __init__(self, error_type: str, **kwargs):
        """
        :param error_type: Key from  `ErrorMessages.PARSING_ERRORS`
        :param kwargs:Additional params for message formating
        """
        message_template = ErrorMessages.PARSING_ERRORS.get(
            error_type, "Unknown parser manager error."
        )
        message = message_template.format(**kwargs)
        super().__init__(message)


class FilteringError(BaseError):
    def __init__(self, error_type: str, **kwargs):
        """
        :param error_type: Key from  `ErrorMessages.FILTERING_ERRORS`
        :param kwargs:Additional params for message formating
        """
        message_template = ErrorMessages.FILTERING_ERRORS.get(
            error_type, "Unknown filtering error."
        )
        message = message_template.format(**kwargs)
        super().__init__(message)


class ReportingError(BaseError):
    def __init__(self, error_type: str, **kwargs):
        """
        :param error_type: Key from  `ErrorMessages.REPORTING_ERRORS`
        :param kwargs:Additional params for message formating
        """
        message_template = ErrorMessages.REPORTING_ERRORS.get(
            error_type, "Unknown reporting error."
        )
        message = message_template.format(**kwargs)
        super().__init__(message)
