# -*- coding: utf-8 -*-
import logging
from pathlib import Path

from pydantic import BaseModel, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class ApiClientConfig(BaseModel):
    url: str = r"http://192.168.73.85:8000/api/v1"


class ReportGeneratorConfig(BaseModel):
    template: str = "processing/report_template.xlsx"
    output_dir: str = "data/reports"


class ProcessingConfig(BaseModel):
    allowed_filetypes: list[str] | None = None


class LoggerConfig(BaseModel):
    log_dir: Path = Path("logs")
    log_level: int = logging.DEBUG
    log_time: str = "H"  # 'H' for hourly, 'midnight' for daily
    log_backup_count: int = 10
    log_max_size: int = 10
    log_type: str = "BY_TIME"  # "BY_TIME", "BY_SIZE", "SINGLE"


class Settings(BaseSettings):
    # model_config = SettingsConfigDict(
    #     env_file=".env",
    #     case_sensitive=False,
    #     env_prefix="PROCESSING__",
    #     env_nested_delimiter="__",
    # )
    api_client: ApiClientConfig = ApiClientConfig()
    logger: LoggerConfig = LoggerConfig()
    processing: ProcessingConfig = ProcessingConfig()
    report: ReportGeneratorConfig = ReportGeneratorConfig()


settings = Settings()

if __name__ == "__main__":
    pass
