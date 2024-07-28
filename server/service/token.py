from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from server.models import Token


async def get_token(session: AsyncSession, user_id: int):
    """Get Token instance by `user_id`."""
    tokens = await session.execute(
        select(Token)
        .filter(Token.user_id == user_id),
    )
    return tokens.scalars().first()


async def create_token(session: AsyncSession, user_id: int) -> Token:
    """Create Token instance."""
    token = Token(user_id=user_id)

    session.add(token)
    await session.commit()
    await session.refresh(token)
    return token


async def delete_tokens(session: AsyncSession, user_id: int):
    """Delete Token instances by `user_id`."""
    await session.execute(delete(Token).filter(Token.user_id == user_id))
