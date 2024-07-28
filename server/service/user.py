from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from server.models import Token, User


async def get_users(session: AsyncSession, *criteria):
    """Select User instance by criteria."""
    users = await session.execute(select(User).filter(*criteria))
    return users.scalars().all()


async def get_user_by_token(session: AsyncSession, token: str):
    """Select User instance by token."""
    users = await session.execute(
        select(User)
        .join(User.tokens)
        .filter(Token.token == token),
    )
    return users.scalars().first()


async def create_user(session: AsyncSession, **fields):
    """Create User instance."""
    user = User(**fields)

    session.add(user)
    await session.commit()
    await session.refresh(user)

    return user
