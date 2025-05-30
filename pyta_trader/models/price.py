from pydantic import BaseModel

class Price(BaseModel):
    time: int
    open: float
    high: float
    low: float
    close: float
    tick_volume: float
    spread: float
    real_volume: float = 0.0

__all__ = ("Price",)