from fastapi import APIRouter, Depends, HTTPException

import models.did as Did
from security import get_current_user_api

router = APIRouter(tags=["did"])

@router.get("/dids")
async def get_dids():
    return Did.get_dids()
