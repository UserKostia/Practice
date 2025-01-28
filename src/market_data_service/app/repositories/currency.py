from typing import List

from fastapi import HTTPException

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.market_data_service.app.models.currency import Currency
from src.market_data_service.app.schemas.currency import (
    CurrencyCreate,
    CurrencyUpdate,
    CurrencyUpdatePartial, CurrencyResponse)


async def create_currency(db: AsyncSession, currency_in: CurrencyCreate) -> Currency:
    """
    Create a new currency in the database.

    Args:
        db (AsyncSession): Database session
        currency_in (CurrencyCreate): Currency to create

    Returns:
        Currency: Currency object

    Exceptions:
        HTTPException if a currency already exists
    """
    # Check for existing currency with same symbol or name
    existing_currency = await db.execute(
        select(Currency).
        where(Currency.currency_code == currency_in.currency_code)
    )

    # Choose the first match
    existing_currency = existing_currency.scalars().first()

    # Show exception if currency exists
    if existing_currency:
        raise HTTPException(status_code=400, detail="Currency already exists")

    # Create new currency object
    new_currency = Currency(
        currency_code=currency_in.currency_code,
        exchange_rate_usd=currency_in.exchange_rate_usd
    )

    # Add currency to db
    db.add(new_currency)
    await db.commit()
    await db.refresh(new_currency)

    return new_currency


async def get_currency(db: AsyncSession, currency_id: int) -> Currency:
    """
    Get currency by ID in the database.

    Args:
        db (AsyncSession): Database session
        currency_id (int): Currency id

    Returns:
        Currency: Currency object

    Exceptions:
        HTTPException if a currency does not exist
    """
    # Check for existing currency
    currency = await db.execute(
        select(Currency).
        where(Currency.id == currency_id)
    )

    # Choose the first match
    currency = currency.scalars().first()

    # Show exception if currency does not exist
    if not currency:
        raise HTTPException(status_code=404, detail=f"currency with ID {currency_id} does not exist")

    return currency


async def get_all_currencies(db: AsyncSession) -> List[Currency]:
    """
    Get all currencies in the database.

    Args:
        db (AsyncSession): Database session

    Returns:
        List[Currency]: List of Currency objects

    Exceptions:
        HTTPException if a currency does not exist
    """
    # Select all currencies
    currencies = await db.execute(
        select(Currency)
    )

    # Conver all to list
    currencies = list(currencies.scalars().all())

    if not currencies:
        raise HTTPException(status_code=404, detail="Currency does not exist")

    return currencies


async def update_currency(
        db: AsyncSession,
        currency_id: int,
        currency_update: CurrencyUpdate | CurrencyUpdatePartial,
        partial: bool = False
) -> Currency:
    """
    Update currency by ID in the database.

    Args:
        db (AsyncSession): Database session
        currency_id (int): Currency id
        currency_update (CurrencyUpdate): Currency to update
        partial (bool, optional): Partial update

    Returns:
        Currency: Currency object

    Exceptions:
        HTTPException if a currency does not exist
    """
    # Get currency by ID
    currency = await get_currency(db, currency_id)

    # Create dict with updated data
    update_data: dict = currency_update.model_dump(exclude_unset=partial)

    # Update data in currency
    for key, value in update_data.items():
        setattr(currency, key, value)

    # Update data in DB
    await db.commit()
    await db.refresh(currency)

    return currency


async def delete_currency(db: AsyncSession, currency_id: int) -> None:
    """
    Delete currency by ID in the database.

    Args:
        db (AsyncSession): Database session
        currency_id (int): Currency id

    Returns:
        None

    Exceptions:
        HTTPException if a currency does not exist
    """
    # Get currency by ID
    currency = await get_currency(db, currency_id)

    # Delete currency
    await db.delete(currency)
    await db.commit()
