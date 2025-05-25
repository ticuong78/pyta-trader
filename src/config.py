import os
import logging

from pathlib import Path

from exceptions import MissingKeys

logger = logging.getLogger(__name__)

SUPPORTED_KEYS = [
    "MT5_LOGIN",
    "MT5_PASSW",
    "MT5_SERVER"
]

def get_my_env_var(var_name: str):
    if var_name not in SUPPORTED_KEYS:
        msg = "Unspported keys found, please choose supported ones."
        raise MissingKeys(msg)
    
    return os.getenv(var_name)

try:
    mt5_login = get_my_env_var('MT5_LOGIN')
    mt5_passw = get_my_env_var('MT5_PASSW')
    mt5_server = get_my_env_var('MT5_SERVER')
except Exception as e:
    logger.exception(e)

__all__ = (
    "mt5_login",
    "mt5_passw",
    "mt5_server"
)