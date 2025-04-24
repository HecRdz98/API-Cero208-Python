from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from models.user import User
from models.token import UserToken
from schemas.token import TokenResponse
from security import get_current_user_api

router = APIRouter(tags=["tokens"])

@router.get("/tokens", response_model=list[TokenResponse])
async def list_tokens(
    current_user: User = Depends(get_current_user_api),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(UserToken)
        .where(UserToken.user_id == current_user.id)
        .order_by(UserToken.created_at.desc())
    )
    tokens = result.scalars().all()
    
    return tokens


@router.delete("/tokens/{token_name}")
async def revoke_token(
    token_name: str,
    current_user: User = Depends(get_current_user_api),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(UserToken)
        .where(UserToken.token_name == token_name)
        .where(UserToken.user_id == current_user.id)
    )
    token = result.scalar()
    
    if not token:
        raise HTTPException(status_code=404, detail="Token not found")
    
    await db.delete(token)
    await db.commit()
    
    return {"message": "Token revoked successfully"}