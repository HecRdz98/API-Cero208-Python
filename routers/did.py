from fastapi import APIRouter, Depends, HTTPException

import models.did as Did
from api.didww import DIDWW
from security import get_current_user_api

router = APIRouter(tags=["did"])
didww_api = DIDWW()


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


@router.get('/dids_international')
async def get_dids_international():
    data = didww_api.get_dids()
    if data.get('status') == False:
        raise HTTPException(status_code=data['status_code'], detail=data['message'])

    return data['dids']
