from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from models.token import UserToken
from models.user import User
from security import get_current_user_api

router = APIRouter(tags=["tokens"])

@router.get("/tokens")
async def get_user_tokens(
    user_token: User = Depends(get_current_user_api),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(UserToken)
        .where(UserToken.user_id == user_token.user_id)
        .order_by(UserToken.created_at.desc())
    )

    tokens = result.scalars().all()
    return [{"token": token.token, "token_name": token.token_name, "created_at": token.created_at} for token in tokens]


@router.delete("/tokens/{token_name}")
async def revoke_token(
    token_name: str,
    user_token: User = Depends(get_current_user_api),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(UserToken)
        .where(UserToken.token_name == token_name)
        .where(UserToken.user_id == user_token.user_id)
    )
    token = result.scalar()
    
    if not token:
        raise HTTPException(status_code=404, detail="Token not found")
    
    await db.delete(token)
    await db.commit()
    
    return {"message": "Token revoked successfully"}