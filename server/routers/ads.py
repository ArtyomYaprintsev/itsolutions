from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from server.core import exceptions as exc
from server.deps import get_session, get_current_active_user
from server.models import ad as model_ad
from server.schemas import ad as schema_ad
from server.service import ad as service_ad
from server.tasks import sync_ads_list

router = APIRouter(dependencies=[Depends(get_current_active_user)])


@router.get('/', response_model=list[schema_ad.Ad])
async def get_ads_list(
    session: Annotated[AsyncSession, Depends(get_session)],
):
    """Get actual ads list."""
    ads = await service_ad.get_ads(
        session,
        model_ad.Ad.is_archived == False,
        with_order=True,
    )
    return ads


@router.post('/', status_code=204)
async def sync_ads():
    """Run celery task with actual ads synchronization."""
    sync_ads_list.delay()


@router.get('/{ad_id}', response_model=schema_ad.Ad)
async def get_ad(
    ad_id: str,
    session: Annotated[AsyncSession, Depends(get_session)],
):
    """Retrieve non-archived task by id.

    Raises:
        AdNotFoundException: if ad with provided id not found.
        ArchivedAdException: if ad is archived.
    """
    ad = await service_ad.get_ad_by_id(session, ad_id)

    if ad is None:
        raise exc.AdNotFoundException()

    if ad.is_archived:
        raise exc.ArchivedAdException()

    return ad
