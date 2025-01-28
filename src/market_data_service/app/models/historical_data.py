from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from src.common.db.base import Base


class HistoricalData(Base):
    """
    SQLAlchemy ORM model for table 'historical_data'.

    Represents historical market data for cryptocurrencies.

    Attributes:
        id (int): The unique identifier for the historical data record.
        crypto_id (int): The foreign key referencing the associated cryptocurrency.
        price_usd (float): The historical price of the cryptocurrency in USD.
        market_cap_usd (Optional[float]): The historical market capitalization in USD.
        volume_24h_usd (Optional[float]): The historical 24-hour trading volume in USD.
        percent_change (Optional[float]): The percentage price change for the historical record.
        recorded_at (datetime): The timestamp when the data was recorded.
    """
    __tablename__ = "historical_data"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    crypto_id = Column(Integer, ForeignKey("cryptocurrencies.id"), nullable=False)
    price_usd = Column(Float, nullable=False)
    market_cap_usd = Column(Float, nullable=True)
    volume_24h_usd = Column(Float, nullable=True)
    percent_change = Column(Float, nullable=True)

    # Metadata
    recorded_at = Column(DateTime(timezone=True), default=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    cryptocurrency = relationship("Cryptocurrency", back_populates="historical_data")
