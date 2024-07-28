from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from server.deps import get_current_user, get_session
from server.models.user import User
from server.repositories import user as repository_user
from server.schemas import auth as schema_auth
from server.schemas import user as schema_user

router = APIRouter()


@router.post(
    '/signup',
    response_model=schema_user.InternalUser,
    status_code=status.HTTP_201_CREATED,
)
async def signup(
    signup_user: schema_auth.SignupUser,
    session: Annotated[AsyncSession, Depends(get_session)],
):
    """Create new user instance by email and password."""
    user = await repository_user.create_user(session, signup_user)
    return user


@router.post('/login', response_model=schema_auth.Token)
async def login(
    credentials: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: Annotated[AsyncSession, Depends(get_session)],
):
    """Login user by provided credentials."""
    login_user = schema_auth.LoginUser(
        email=credentials.username,
        password=credentials.password,
    )

    token = await repository_user.login_user(session, login_user)
    return schema_auth.Token(access_token=token.token)


@router.post('/logout', status_code=status.HTTP_204_NO_CONTENT)
async def logout(
    user: Annotated[User, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(get_session)],
):
    """Logout user."""
    return await repository_user.logout_user(session, user)
