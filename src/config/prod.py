from .base import BaseConfig

class ProdConfig(BaseConfig):
    debug: bool = False

__all__ = (
    "ProdConfig",
)