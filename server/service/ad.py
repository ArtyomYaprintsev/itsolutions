from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from server.models import Ad
from server.schemas import ad as schema_ad


async def create_ad(session: AsyncSession, **fields):
    """Create new Ad instance."""
    ad_instance = Ad(**fields)

    session.add(ad_instance)
    await session.commit()
    await session.refresh(ad_instance)

    return ad_instance


async def get_ads(session: AsyncSession, *criteria, with_order: bool = False):
    """Select Ad instances by provided criteria.

    Args:
        with_order(`bool`): order ads by position if True. Default: False.
    """
    stmt = select(Ad).filter(*criteria)

    if with_order:
        stmt = stmt.order_by(Ad.position.asc())

    ads = await session.execute(stmt)
    return ads.scalars().all()


async def get_ad_by_id(session: AsyncSession, ad_id: str):
    """Select Ad instance by id."""
    ad_instance = await session.execute(select(Ad).filter(Ad.id == ad_id))
    return ad_instance.scalars().first()


async def update_ad(
    session: AsyncSession,
    ad_instance: Ad,
    ad_update: schema_ad.UpdateAd,
):
    """Update Ad instance with provided fields."""
    for key, value in ad_update.model_dump(exclude_none=True).items():
        setattr(ad_instance, key, value)

    session.add(ad_instance)
    await session.commit()
    await session.refresh(ad_instance)

    return ad_instance


async def bulk_create(session: AsyncSession, ads_create: list[schema_ad.Ad]):
    """Bulk create Ad instances."""
    await session.execute(
        insert(Ad),
        [ad_create.model_dump(exclude_none=True) for ad_create in ads_create],
    )


async def bulk_update_ad(
    session: AsyncSession,
    ad_update: schema_ad.UpdateAd,
    *update_criteria,
) -> None:
    """Bulk update Ad instances."""
    await session.execute(
        update(Ad)
        .filter(*update_criteria)
        .values(**ad_update.model_dump(exclude_none=True)),
    )


async def delete_ads(session: AsyncSession, *criteria):
    """Delete Ad instances by provided criteria."""
    await session.execute(delete(Ad).filter(*criteria))
