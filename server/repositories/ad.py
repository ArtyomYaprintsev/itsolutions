import logging

from server.db.session import async_session
from server.models import Ad as model_Ad
from server.schemas import ad as schema_ad
from server.service import ad as service_ad

logger = logging.getLogger(__name__)


async def save_actual_ads(actual_ads: list[schema_ad.Ad]):
    """Save actual Ad list."""
    async with async_session() as session:  # type: ignore
        actual_ad_ids = [ad.id for ad in actual_ads]

        try:
            # Archive all ads whose ID is not in the actual ids list
            await service_ad.bulk_update_ad(
                session,
                schema_ad.UpdateAd(
                    position=0,
                    is_archived=True,
                ),
                ~model_Ad.id.in_(actual_ad_ids),
            )

            # Delete existing records of current ads
            # This will help to avoid multiple Update requests in cases when
            # ad data changes
            await service_ad.delete_ads(
                session,
                model_Ad.id.in_(actual_ad_ids),
            )
            await service_ad.bulk_create(session, actual_ads)

            await session.commit()
        except Exception as exc:  # noqa: W0703
            logger.error(
                f'Caught error while saving actual ads: {exc})',
                exc_info=exc,
            )
            await session.rollback()
