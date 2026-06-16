from pathlib import Path

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent


class PentahoRepoSettings(BaseSettings):
    """Настройки pentaho репозитория."""

    user: str = "user"
    password: str = "password"
    host: str = "postgres"
    port: str = "5432"
    name: str = ""

    @property
    def conn_info(self) -> dict:
        return {
            "host": self.host,
            "port": self.port,
            "user": self.user,
            "password": self.password,
            "database": self.name,
        }

    class Config:
        env_prefix = "PENTAHO_REPO__"


class BlifeSettings(BaseSettings):
    """Настройки blife."""

    token: str = ""
    user_id: int = 0
    group_id: int = 0

    @property
    def url(self) -> dict:
        return f"https://test-blife.baiterek.gov.kz/rest/{self.user_id}/{self.token}/"

    class Config:
        env_prefix = "BLIFE__"


class Settings(BaseSettings):
    """Общие настройки приложения."""

    pentaho_repo: PentahoRepoSettings = PentahoRepoSettings()
    blife: BlifeSettings = BlifeSettings()


settings = Settings()
