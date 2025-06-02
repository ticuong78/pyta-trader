import numpy as np

from typing import Optional
from pydantic import BaseModel, ConfigDict

class Price(BaseModel):
    model_config = ConfigDict(extra="forbid")

    time: int
    open: float
    high: float
    low: float
    close: float
    tick_volume: Optional[float] = 0.0
    spread: Optional[float] = 0.0
    real_volume: Optional[float] = 0.0

def convert_rate_to_price(rate: np.void) -> Price:
    try:
        new_price = Price(
            time=int(rate["time"]),
            open=float(rate["open"]),
            high=float(rate["high"]),
            low=float(rate["low"]),
            close=float(rate["close"]),
            tick_volume=float(rate["tick_volume"]),
            spread=float(rate["spread"]),
            real_volume=float(rate["real_volume"]),
        )
    except Exception as e: 
        raise e

    return new_price

__all__ = ("Price", "convert_rate_to_price")