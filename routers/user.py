import os
import secrets
from datetime import datetime

from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from models.token import UserToken
from models.user import User
from schemas.user import LoginRequest, UserCreate, UserResponse
from security import get_password_hash, verify_password

from starlette.concurrency import run_in_threadpool
from api.whmcs import create_whmcs_client, get_whmcs_client_by_email


load_dotenv()

router = APIRouter(tags=["authentication"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Configuración JWT
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

@router.post("/register", response_model=UserResponse)
async def register(user: UserCreate, db: AsyncSession = Depends(get_db)):
    # Verificar si el usuario ya existe
    db_user = await db.execute(
        select(User).where(
            (User.email == user.email) |
            (User.username == user.username)
        )
    )
    db_user = db_user.scalar()
    
    if db_user:
        if db_user.email == user.email:
            raise HTTPException(status_code=400, detail="Email already registered")
        else:
            raise HTTPException(status_code=400, detail="Username already taken")

    hashed_password = get_password_hash(user.password)
    new_user = User(
        username=user.username,
        email=user.email,
        password=hashed_password
    )
        
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    # Crear cliente en WHMCS
    await run_in_threadpool(create_whmcs_client, user)
    
    return new_user



# @router.post("/login", response_model=TokenResponse)
@router.post("/login")
async def login(
    login_data: LoginRequest,
    db: AsyncSession = Depends(get_db)
):
    # Buscar usuario
    user = await db.execute(
        select(User).where(
            (User.username == login_data.username) |
            (User.email == login_data.username)
        )
    )
    user = user.scalar()
    
    if not user or not verify_password(login_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,  # <-- Forma correcta
            detail="Credenciales inválidas"
        )
    # Generar API Token
    raw_api_token = f"inb-{secrets.token_urlsafe(64)}"
    
    
    new_token = UserToken(
        user_id=user.id,
        token_name=login_data.token_name,
        token=raw_api_token,
        created_at=datetime.utcnow()
    )
    
    db.add(new_token)
    await db.commit()
    await db.refresh(new_token)
    
    whmcs_client = await run_in_threadpool(get_whmcs_client_by_email, user.email)


    return {
        "token_type": "bearer",
        "token_name": new_token.token_name,
        "api_token": raw_api_token,
        "whmcs_client_id": whmcs_client.get("userid")
    }