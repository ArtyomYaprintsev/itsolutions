from sqlalchemy.ext.asyncio import AsyncSession

from server.core import exceptions as exc
from server.models import User
from server.schemas import auth as schema_auth
from server.service import user as crud_user
from server.service.token import delete_tokens
from server.tools import hash_password, verify_password

from .token import get_or_create_token


async def create_user(session: AsyncSession, user: schema_auth.SignupUser):
    """Create new user.

    Raises:
        UniqueException: if user with provided email already exists.
    """
    existed_user = await crud_user.get_users(session, User.email == user.email)

    if existed_user:
        raise exc.UniqueException('User with provided email already exist')

    user.password = hash_password(user.password)
    return await crud_user.create_user(
        session,
        **user.model_dump(include={'email', 'password'}),
    )


async def login_user(session: AsyncSession, login_user: schema_auth.LoginUser):
    """Login user.

    Raises:
        `InvalidCredentialsException`: if user with provided email not found
            or password does not match.
        `InactiveUserException`: if user is inactive.
    """
    searched_users = await crud_user.get_users(
        session,
        User.email == login_user.email,
    )

    if not searched_users:
        raise exc.InvalidCredentialsException()

    user = searched_users[0]

    if not user.is_active:
        raise exc.InactiveUserException()

    if not verify_password(login_user.password, user.password):
        raise exc.InvalidCredentialsException()

    token, _ = await get_or_create_token(session, user.id)

    return token


async def logout_user(session: AsyncSession, user: User) -> None:
    """Logout user."""
    await delete_tokens(session, user.id)
