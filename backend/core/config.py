from pydantic import BaseModel, PostgresDsn
from pydantic_settings import BaseSettings

class AppRunConfig(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8080
    debug: bool = False
    reload: bool = True

class ApiPrefixConfig(BaseModel):
    version: str = "v1"
    prefix: str = f"/api/{version}"


class DatabaseConfig(BaseModel):
    url: PostgresDsn #= f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"



class Settings(BaseSettings):
    app: AppRunConfig = AppRunConfig()
    api: ApiPrefixConfig = ApiPrefixConfig()
    db: DatabaseConfig

settings = Settings()