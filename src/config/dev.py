from .base import BaseConfig

class DevConfig(BaseConfig):
    debug: bool = True

__all__ = (
    "DevConfig",
)