from sqlalchemy.ext.asyncio import AsyncSession

from server.models import Token
from server.service.token import create_token, get_token


async def get_or_create_token(
    session: AsyncSession,
    user_id: int,
) -> tuple[Token, bool]:
    """Get or create user token.

    Returns:
        `tuple[Token, bool]`: user token and token creating status. Returns
            `True` if token has been created, `False` otherwise.
    """
    token = await get_token(session, user_id)

    if token:
        return token, False

    return await create_token(session, user_id), True
