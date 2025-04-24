from fastapi import Depends, HTTPException, Header, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from sqlalchemy import func, select
from models.user import User
from models.token import UserToken
from schemas.user import TokenData
import os

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
    db: AsyncSession = Depends(get_db)
) -> User:
    result = await db.execute(
        select(UserToken).where(
            UserToken.token == get_password_hash(api_token)
        )
    )
    db_token = result.scalar()
    
    if not db_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido"
        )
    
    return db_token.user

async def validate_api_token(
    token: str = Header(..., alias="X-API-Token"),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(UserToken).where(UserToken.token == get_password_hash(token))
    )
    db_token = result.scalar()
    
    if not db_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API Token"
        )
    
    return db_token.user