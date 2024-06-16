
from pydantic import BaseModel


class StockIn(BaseModel):
    ticker: str


class StockOut(StockIn):
    forecast: dict