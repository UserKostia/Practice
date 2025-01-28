from pydantic import BaseModel, Field
from datetime import datetime


class CryptocurrencyBase(BaseModel):
    """
    Base schema for Cryptocurrency.

    Attributes:
        name (str): The name of the cryptocurrency.
        symbol (str): The symbol of the cryptocurrency (e.g., BTC, ETH).
        is_active (bool): Indicates whether the cryptocurrency is active.
    """
    name: str = Field(..., max_length=100)
    symbol: str = Field(..., max_length=10)
    is_active: bool = Field(default=True)


class CryptocurrencyCreate(CryptocurrencyBase):
    """
    Schema for creating a cryptocurrency.
    """
    pass


class CryptocurrencyUpdate(CryptocurrencyBase):
    """
    Schema for full updating a cryptocurrency.
    """
    pass


class CryptocurrencyUpdatePartial(CryptocurrencyBase):
    """
    Schema for partial updating a cryptocurrency.
    """
    pass


class CryptocurrencyResponse(CryptocurrencyBase):
    """
    Schema for returning cryptocurrency data.

    Attributes:
        id (int): The unique identifier for the cryptocurrency.
        created_at (datetime): The timestamp when the cryptocurrency was created.
    """
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
