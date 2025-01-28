from datetime import datetime

from pydantic import BaseModel, Field


class CurrencyBase(BaseModel):
    """
    Base schema for Currency.

    Attributes:
        currency_code (str): The ISO code or symbol of the currency (e.g., USD, EUR).
        exchange_rate_usd (float): The exchange rate of the currency relative to USD.
    """
    currency_code: str = Field(..., max_length=10)
    exchange_rate_usd: float


class CurrencyCreate(CurrencyBase):
    """
    Schema for creating a currency.
    """
    pass


class CurrencyUpdate(CurrencyBase):
    """
    Schema for full updating a currency.
    """
    pass


class CurrencyUpdatePartial(CurrencyUpdate):
    """
    Schema for partial updating a currency.
    """
    pass


class CurrencyResponse(CurrencyBase):
    """
    Schema for returning currency data.

    Attributes:
        id (int): The unique identifier for the currency.
        last_updated (datetime): The timestamp when the exchange rate was last updated.
    """
    id: int
    last_updated: datetime

    class Config:
        orm_mode = True
