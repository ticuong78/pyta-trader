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

__all__ = ("Price",)