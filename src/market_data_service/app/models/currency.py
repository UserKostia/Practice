from sqlalchemy import Column, Integer, String, Float, DateTime, func
from src.common.db.base import Base


class Currency(Base):
    """
    SQLAlchemy ORM model for table 'currencies'.

    Represents fiat or alternative currencies and their exchange rates relative to USD.

    Attributes:
        id (int): The unique identifier for the currency record.
        currency_code (str): The ISO code or symbol of the currency (e.g., USD, EUR).
        exchange_rate_usd (float): The exchange rate of the currency relative to USD.
        last_updated (datetime): The timestamp when the exchange rate was last updated.
    """
    __tablename__ = "currencies"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    currency_code = Column(String(10), unique=True, nullable=False)
    exchange_rate_usd = Column(Float, nullable=False)

    # Metadata
    last_updated = Column(DateTime(timezone=True), default=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
