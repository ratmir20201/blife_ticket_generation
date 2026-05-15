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


class Settings(BaseSettings):
    """Общие настройки приложения."""

    repo: PentahoRepoSettings = PentahoRepoSettings()


settings = Settings()
