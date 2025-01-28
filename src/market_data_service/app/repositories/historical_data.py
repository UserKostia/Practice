from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException, status

from src.market_data_service.app.models.historical_data import HistoricalData
from src.market_data_service.app.schemas.historical_data import HistoricalDataCreate, HistoricalDataResponse


async def create_historical_data(db: AsyncSession, data_in: HistoricalDataCreate) -> HistoricalData:
    """
    Create a new HistoricalData in the database.

    Args:
        db (AsyncSession): database session
        data_in (HistoricalDataCreate): data for creation

    Returns:
        HistoricalData: HistoricalData object
    """
    historical_data = HistoricalData(**data_in.model_dump())

    db.add(historical_data)
    await db.commit()

    return historical_data


async def get_historical_data(db: AsyncSession, data_id: int) -> HistoricalData:
    """
    Retrieve a single HistoricalData entry by its ID.

    Args:
        db (AsyncSession): database session
        data_id (int): HistoricalData ID

    Returns:
        HistoricalDataResponse: HistoricalData object

    Raises:
        HTTPException: If the HistoricalData entry does not exist
    """
    historical_data = await db.execute(
        select(HistoricalData).
        where(HistoricalData.id == data_id)
    )

    historical_data = historical_data.scalars().first()

    if not historical_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"HistoricalData with ID {data_id} not found."
        )

    return historical_data


async def get_all_historical_data(db: AsyncSession) -> list[HistoricalData]:
    """
    Retrieve all HistoricalData entries.

    Args:
        db (AsyncSession): database session

    Returns:
        list[HistoricalDataResponse]: List of HistoricalData objects
    """
    result = await db.execute(select(HistoricalData))
    result = result.scalars().all()

    return list(result)


async def update_historical_data(db: AsyncSession, data_id: int, data_in: HistoricalDataCreate) -> HistoricalData:
    """
    Update an existing HistoricalData entry.

    Args:
        db (AsyncSession): database session
        data_id (int): HistoricalData ID
        data_in (HistoricalDataCreate): Updated data

    Returns:
        HistoricalDataResponse: Updated HistoricalData object

    Raises:
        HTTPException: If the HistoricalData entry does not exist
    """
    result = await db.execute(
        select(HistoricalData).
        where(HistoricalData.id == data_id)
    )

    historical_data = result.scalars().first()

    if not historical_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"HistoricalData with ID {data_id} not found."
        )

    for key, value in data_in.model_dump().items():
        setattr(historical_data, key, value)

    return historical_data


async def delete_historical_data(db: AsyncSession, data_id: int):
    """
    Delete an existing HistoricalData entry.

    Args:
        db (AsyncSession): database session
        data_id (int): HistoricalData ID

    Raises:
        HTTPException: If the HistoricalData entry does not exist
    """
    result = await db.execute(
        select(HistoricalData).
        where(HistoricalData.id == data_id)
    )

    historical_data = result.scalars().first()

    if not historical_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"HistoricalData with ID {data_id} not found."
        )

    await db.delete(historical_data)
