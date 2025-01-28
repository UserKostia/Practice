from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException, status

from src.market_data_service.app.models.market_data import MarketData
from src.market_data_service.app.schemas.market_data import (
    MarketDataCreate,
    MarketDataUpdate,
    MarketDataUpdatePartial,
    MarketDataResponse)


async def create_market_data(db: AsyncSession, market_data_in: MarketDataCreate) -> MarketData:
    """
    Create a new MarketData entry in the database.

    Args:
        db (AsyncSession): database session
        market_data_in (MarketDataCreate): Data for creation

    Returns:
        MarketData: Created MarketData object
    """
    market_data = MarketData(**market_data_in.model_dump())

    db.add(market_data)
    await db.commit()
    await db.refresh(market_data)

    return market_data


async def get_market_data(db: AsyncSession, market_data_id: int) -> MarketData:
    """
    Retrieve a single MarketData entry by its ID.

    Args:
        db (AsyncSession): database session
        market_data_id (int): MarketData ID

    Returns:
        MarketDataResponse: MarketData object

    Raises:
        HTTPException: If the MarketData entry does not exist
    """
    result = await db.execute(
        select(MarketData).
        where(MarketData.id == market_data_id)
    )
    market_data = result.scalars().first()

    if not market_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"MarketData with ID {market_data_id} not found."
        )

    return market_data


async def get_all_market_data(db: AsyncSession) -> list[MarketData]:
    """
    Retrieve all MarketData entries.

    Args:
        db (AsyncSession): database session

    Returns:
        list[MarketDataResponse]: List of MarketData objects
    """
    result = await db.execute(select(MarketData))
    market_data = result.scalars().all()

    return list(market_data)


async def update_market_data(
    db: AsyncSession,
    market_data_id: int,
    market_data_in: MarketDataUpdate | MarketDataUpdatePartial,
    partial: bool = False
) -> MarketData:
    """
    Update an existing MarketData entry.

    Args:
        db (AsyncSession): database session
        market_data_id (int): MarketData ID
        market_data_in (MarketDataUpdate): Updated data
        partial (bool, optional): Partial update. Defaults to False.

    Returns:
        MarketDataResponse: Updated MarketData object

    Raises:
        HTTPException: If the MarketData entry does not exist
    """
    result = await db.execute(
        select(MarketData).
        where(MarketData.id == market_data_id)
    )

    market_data = result.scalars().first()
    if not market_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"MarketData with ID {market_data_id} not found."
        )

    updated_data = market_data_in.model_dump(exclude_unset=partial)

    for key, value in updated_data.items():
        setattr(market_data, key, value)

    await db.commit()
    await db.refresh(market_data)

    return market_data


async def delete_market_data(db: AsyncSession, market_data_id: int):
    """
    Delete an existing MarketData entry.

    Args:
        db (AsyncSession): database session
        market_data_id (int): MarketData ID

    Raises:
        HTTPException: If the MarketData entry does not exist
    """
    result = await db.execute(
        select(MarketData).
        where(MarketData.id == market_data_id)

    )

    market_data = result.scalars().first()

    if not market_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"MarketData with ID {market_data_id} not found."
        )

    await db.delete(market_data)
    await db.commit()
