# pyright: reportCallIssue=false

import os

def get_config():
    env = os.getenv("APP_ENV", "dev").lower()
    
    if env == "prod":
        from .prod import ProdConfig
        return ProdConfig()
    else:
        from .dev import DevConfig
        return DevConfig()

__all__ = (
    "get_config",
)