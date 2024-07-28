from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from server.core import exceptions as exc
from server.core.security import oauth2_scheme
from server.db.session import get_session as get_base_session
from server.models import User
from server.service.user import get_user_by_token


async def get_session(
    session: Annotated[AsyncSession, Depends(get_base_session)],
):
    """Provide database async session."""
    return session


async def get_current_user(
    session: Annotated[AsyncSession, Depends(get_session)],
    token: Annotated[str, Depends(oauth2_scheme)],
):
    """Get current user by token.

    Raises:
        `UnauthorizedException`: if token is missing or user not found.
    """
    user = await get_user_by_token(session, token)
    if not user:
        raise exc.UnauthorizedException()
    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
):
    """Check if the current user is active.

    Raises:
        `InactiveUserException`: if the current user is inactive.
    """
    if not current_user.is_active:
        raise exc.InactiveUserException()
    return current_user


async def get_current_superuser(
    current_user: Annotated[User, Depends(get_current_user)],
):
    """Check if the current user is superuser.

    Raises:
        `NotSuperuserException`: if the current user is not superuser.
    """
    if not current_user.is_superuser:
        raise exc.NotSuperuserException()
    return current_user
