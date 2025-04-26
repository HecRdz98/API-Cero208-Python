from fastapi import APIRouter, Depends, HTTPException

import models.did as Did
from security import get_current_user_api

router = APIRouter(tags=["did"])

@router.get("/dids")
async def get_dids():
    return Did.get_dids()


@router.get("/dids/{did}")
async def get_did(did:str):
    result = Did.get_did(did)
    if(not result):
       raise HTTPException(status_code=404, detail="DID no disponible")
    return result


@router.delete("/dids/{did}")
async def get_did(did:str):
    result = Did.get_did(did)
    if(not result):
       raise HTTPException(status_code=404, detail="DID")
    return result