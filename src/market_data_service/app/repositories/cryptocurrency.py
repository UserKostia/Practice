from typing import List

from fastapi import HTTPException

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.market_data_service.app.models.cryptocurrency import Cryptocurrency
from src.market_data_service.app.schemas.cryptocarrency import (
    CryptocurrencyCreate,
    CryptocurrencyUpdate,
    CryptocurrencyUpdatePartial)


async def create_cryptocurrency(db: AsyncSession, cryptocurrency_in: CryptocurrencyCreate) -> Cryptocurrency:
    """
    Create a new Cryptocurrency in the database.

    Args:
        db (AsyncSession): Database session
        cryptocurrency_in (CryptocurrencyCreate): Cryptocurrency to create

    Returns:
        Cryptocurrency: Cryptocurrency object

    Exceptions:
        HTTPException if a cryptocurrency already exists
    """
    # Check for existing cryptocurrency with same symbol or name
    existing_cryptocarrency = await db.execute(
        select(Cryptocurrency).
        where(
            (Cryptocurrency.symbol == cryptocurrency_in.symbol) |
            (Cryptocurrency.name == cryptocurrency_in.name)
        )
    )

    # Choose the first match
    existing_cryptocarrency = existing_cryptocarrency.scalars().first()

    # Show exception if cryptocurrency exists
    if existing_cryptocarrency:
        raise HTTPException(status_code=400, detail="Cryptocurrency already exists")

    # Create new cryptocarrency object
    new_cryptocurrency = Cryptocurrency(
        name=cryptocurrency_in.name,
        symbol=cryptocurrency_in.symbol
    )

    # Add cryptocurrency to db
    db.add(new_cryptocurrency)
    await db.commit()
    await db.refresh(new_cryptocurrency)

    return new_cryptocurrency


async def get_cryptocurrency(db: AsyncSession, cryptocurrency_id: int) -> Cryptocurrency:
    """
    Get cryptocurrency by ID in the database.

    Args:
        db (AsyncSession): Database session
        cryptocurrency_id (int): Cryptocurrency id

    Returns:
        Cryptocurrency: Cryptocurrency object

    Exceptions:
        HTTPException if a cryptocurrency does not exist
    """
    # Check for existing cryptocurrency
    cryptocurrency = await db.execute(
        select(Cryptocurrency).
        where(Cryptocurrency.id == cryptocurrency_id)
    )

    # Choose the first match
    cryptocurrency = cryptocurrency.scalars().first()

    # Show exception if cryptocurrency does not exist
    if not cryptocurrency:
        raise HTTPException(status_code=404, detail=f"Cryptocurrency with ID {cryptocurrency_id} does not exist")

    return cryptocurrency


async def get_all_cryptocurrencies(db: AsyncSession) -> List[Cryptocurrency]:
    """
    Get all cryptocurrencies in the database.

    Args:
        db (AsyncSession): Database session

    Returns:
        List[Cryptocurrency]: List of Cryptocurrency objects

    Exceptions:
        HTTPException if a cryptocurrency does not exist
    """
    # Select all cryptocarrencies
    cryptocurrencies = await db.execute(
        select(Cryptocurrency)
    )

    # Conver all to list
    cryptocurrencies = list(cryptocurrencies.scalars().all())

    if not cryptocurrencies:
        raise HTTPException(status_code=404, detail="Cryptocurrency does not exist")

    return cryptocurrencies


async def update_cryptocurrency(
        db: AsyncSession,
        cryptocurrency_id: int,
        cryptocurrency_update: CryptocurrencyUpdate | CryptocurrencyUpdatePartial,
        partial: bool = False
) -> Cryptocurrency:
    """
    Update cryptocurrency by ID in the database.

    Args:
        db (AsyncSession): Database session
        cryptocurrency_id (int): Cryptocurrency id
        cryptocurrency_update (CryptocurrencyUpdate): Cryptocurrency to update
        partial (bool, optional): Partial update

    Returns:
        Cryptocurrency: Cryptocurrency object

    Exceptions:
        HTTPException if a cryptocurrency does not exist
    """
    # Get cryptocurrency by ID
    cryptocurrency = await get_cryptocurrency(db, cryptocurrency_id)

    # Create dict with updated data
    update_data: dict = cryptocurrency_update.model_dump(exclude_unset=partial)

    # Update data in cryptocarrency
    for key, value in update_data.items():
        setattr(cryptocurrency, key, value)

    # Update data in DB
    await db.commit()
    await db.refresh(cryptocurrency)

    return cryptocurrency


async def delete_cryptocurrency(db: AsyncSession, cryptocurrency_id: int) -> None:
    """
    Delete cryptocurrency by ID in the database.

    Args:
        db (AsyncSession): Database session
        cryptocurrency_id (int): Cryptocurrency id

    Returns:
        None

    Exceptions:
        HTTPException if a cryptocurrency does not exist
    """
    # Get cruptocurrency by ID
    cryptocurrency = await get_cryptocurrency(db, cryptocurrency_id)

    # Delete cryptocurrency
    await db.delete(cryptocurrency)
    await db.commit()
