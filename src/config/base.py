from pydantic import Field
from pydantic_settings import BaseSettings

class BaseConfig(BaseSettings):
    mt5_login: int = Field(alias="MT5_LOGIN")
    mt5_passw: str = Field(alias="MT5_PASSW")
    mt5_server: str = Field(alias="MT5_SERVER")
    mt5_path: str = Field(alias="MT5_PATH")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"

__all__ = (
    "BaseConfig",
)