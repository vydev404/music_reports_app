from pydantic import BaseModel, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppRunConfig(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8080
    debug: bool = False
    reload: bool = True


class ApiPrefixConfig(BaseModel):
    version: str = "v1"
    prefix: str = f"/api/{version}"


class DatabaseConfig(BaseModel):
    url: PostgresDsn  # = f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    url_sync: PostgresDsn
    echo: bool = True
    echo_pool: bool = False
    pool_size: int = 10
    max_overflow: int = 10

    def get_url(self):
        return str(self.url)

    def get_url_sync(self):
        return str(self.url_sync)


class ReportGeneratorConfig(BaseModel):
    template: str = "processing/report_template.xlsx"
    output_dir: str = "data/reports"


class ProcessingConfig(BaseModel):
    allowed_filetypes: list[str]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        env_prefix="APP__",
        env_nested_delimiter="__",
    )
    app: AppRunConfig = AppRunConfig()
    api: ApiPrefixConfig = ApiPrefixConfig()
    db: DatabaseConfig
    report: ReportGeneratorConfig = ReportGeneratorConfig()

    def get_api_url(self):
        return f"http://{self.app.host}:{self.app.port}{self.api.prefix}"


settings = Settings()
