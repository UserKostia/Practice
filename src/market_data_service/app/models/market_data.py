from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from src.common.db.base import Base


class MarketData(Base):
    """
    SQLAlchemy ORM model for table 'market_data'.

    Represents real-time market data for cryptocurrencies.

    Attributes:
        id (int): The unique identifier for the market data record.
        crypto_id (int): The foreign key referencing the associated cryptocurrency.
        price_usd (float): The price of the cryptocurrency in USD.
        market_cap_usd (Optional[float]): The market capitalization in USD.
        volume_24h_usd (Optional[float]): The 24-hour trading volume in USD.
        percent_change_24h (Optional[float]): The percentage price change in the last 24 hours.
        last_updated (datetime): The timestamp when the data was last updated.
    """
    __tablename__ = "market_data"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    crypto_id = Column(Integer, ForeignKey("cryptocurrencies.id"), nullable=False)
    price_usd = Column(Float, nullable=False)
    market_cap_usd = Column(Float, nullable=True)
    volume_24h_usd = Column(Float, nullable=True)
    percent_change_24h = Column(Float, nullable=True)

    # Metadata
    last_updated = Column(DateTime(timezone=True), default=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    cryptocurrency = relationship("Cryptocurrency", back_populates="market_data")
