# pyright: reportCallIssue=false

import os

def get_config():
    """
    Give you a comprehensive config (or .env file) loader to load enougn data needed for setting up Meta Trader connection
    Feel free to use your own
    """
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