from typing import Annotated

from fastapi import APIRouter, Depends

from server.deps import get_current_user
from server.models.user import User
from server.schemas import user as schema_user

router = APIRouter()


@router.get('/me', response_model=schema_user.InternalUser)
async def retrieve_current_user(
    current_user: Annotated[User, Depends(get_current_user)],
):
    """Retrieve current user internal data."""
    return current_user
