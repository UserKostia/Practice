from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class HistoricalDataBase(BaseModel):
    """
    Base schema for Historical Data.

    Attributes:
        price_usd (float): The historical price of the cryptocurrency in USD.
        market_cap_usd (Optional[float]): The historical market capitalization in USD.
        volume_24h_usd (Optional[float]): The historical 24-hour trading volume in USD.
        percent_change (Optional[float]): The percentage price change for the historical record.
    """
    price_usd: float
    market_cap_usd: Optional[float] = None
    volume_24h_usd: Optional[float] = None
    percent_change: Optional[float] = None


class HistoricalDataCreate(HistoricalDataBase):
    """
    Schema for creating historical data.

    Attributes:
        crypto_id (int): The ID of the associated cryptocurrency.
    """
    crypto_id: int


class HistoricalDataResponse(HistoricalDataBase):
    """
    Schema for returning historical data.

    Attributes:
        id (int): The unique identifier for the historical data.
        recorded_at (datetime): The timestamp when the data was recorded.
    """
    id: int
    recorded_at: datetime

    class Config:
        orm_mode = True
