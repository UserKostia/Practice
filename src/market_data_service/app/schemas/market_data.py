from typing import Optional
from datetime import datetime

from pydantic import BaseModel


class MarketDataBase(BaseModel):
    """
    Base schema for Market Data.

    Attributes:
        price_usd (float): The price of the cryptocurrency in USD.
        market_cap_usd (Optional[float]): The market capitalization in USD.
        volume_24h_usd (Optional[float]): The 24-hour trading volume in USD.
        percent_change_24h (Optional[float]): The percentage price change in the last 24 hours.
    """
    price_usd: float
    market_cap_usd: Optional[float] = None
    volume_24h_usd: Optional[float] = None
    percent_change_24h: Optional[float] = None


class MarketDataCreate(MarketDataBase):
    """
    Schema for creating market data.

    Attributes:
        crypto_id (int): The ID of the associated cryptocurrency.
    """
    crypto_id: int


class MarketDataUpdate(MarketDataBase):
    """
    Schema for full updating market data.
    """
    pass


class MarketDataUpdatePartial(MarketDataBase):
    """
    Schema for partial updating market data.
    """
    pass


class MarketDataResponse(MarketDataBase):
    """
    Schema for returning market data.

    Attributes:
        id (int): The unique identifier for the market data.
        last_updated (datetime): The timestamp when the market data was last updated.
    """
    id: int
    last_updated: datetime

    class Config:
        orm_mode = True
