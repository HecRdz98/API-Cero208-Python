import os
from datetime import datetime, timedelta

from dotenv import load_dotenv
from fastapi import Depends, Header, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from models.token import UserToken
from models.user import User
from schemas.user import TokenData

load_dotenv()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def validate_password(password: str):
    if len(password) < 8:
        raise ValueError("Password must be at least 8 characters")
    if not any(c.isupper() for c in password):
        raise ValueError("Password must contain at least one uppercase letter")
    if not any(c.isdigit() for c in password):
        raise ValueError("Password must contain at least one number")


def get_password_hash(password):
    return pwd_context.hash(password)


async def get_current_user_api(
    api_token: str = Header(..., alias="X-API-Token"),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        # select(UserToken).where(UserToken.token == get_password_hash(api_token))
        select(UserToken).where(UserToken.token == api_token)
    )
    user_token = result.scalar()

    if not user_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token adjunto invalido"
        )

    return user_token


async def validate_api_token(
    token: str = Header(..., alias="X-API-Token"), db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(UserToken).where(UserToken.token == get_password_hash(token))
    )
    db_token = result.scalar()

    if not db_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API Token"
        )

    return db_token.user
