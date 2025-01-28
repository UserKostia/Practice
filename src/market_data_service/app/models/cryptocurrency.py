from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean, func
from sqlalchemy.orm import relationship
from src.common.db.base import Base


class Cryptocurrency(Base):
    """
    SQLAlchemy ORM model for table 'cryptocurrencies'.

    Represents cryptocurrency coins and their basic information.

    Attributes:
        id (int): The unique identifier for the cryptocurrency.
        name (str): The full name of the cryptocurrency.
        symbol (str): The unique symbol of the cryptocurrency (e.g., BTC, ETH).
        is_active (bool): Indicates if the cryptocurrency is active.
        created_at (datetime): The timestamp when the cryptocurrency was added to the database.
    """
    __tablename__ = "cryptocurrencies"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    symbol = Column(String(10), unique=True, nullable=False, index=True)
    is_active = Column(Boolean, default=True)

    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    market_data = relationship("MarketData", back_populates="cryptocurrency", cascade="all, delete-orphan")
    historical_data = relationship("HistoricalData", back_populates="cryptocurrency", cascade="all, delete-orphan")
