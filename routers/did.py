from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query

import models.country as Country
import models.did as Did
import utils.utils as utils
from api.didww import DIDWW
from security import get_current_user_api

router = APIRouter(tags=["did"])
didww_api = DIDWW()


@router.get("/dids")
async def get_dids(
    state: Optional[str] = Query(
        None,
        alias="filter[state]",
        example="JAL,CDMX,NL,PUE,VER"
    ),
    phone_code: Optional[str] = Query(
        None,
        alias="filter[phone_code]",
        example="33,55,81,220,229"
    ),
    limit: Optional[int] = Query(
        20,
        example="30",
        le=100,
        ge=1

    )
):
    filters = {
        's.iso' : state,
        'd.phone_code' : phone_code
    }
    dids = Did.get_dids(filters, limit)
    if(not dids):
        raise HTTPException(status_code=404, detail="No hay DIDs que cumplan con los filtros brindados")

    return {
        'message' : f"Mostrando {limit} dids",
        'data' : dids,
    }


@router.get("/dids/{id}")
async def get_did(id:str):
    did = Did.get_did(id)
    if(not did):
       raise HTTPException(status_code=404, detail="DID no disponible o no encontrado")

    return {
        'message' : f"DID encontrado",
        'data' : did,
    }


@router.delete("/dids/{did}")
async def get_did(did:str):
    result = Did.get_did(did)
    if(not result):
       raise HTTPException(status_code=404, detail="DID")
    return result


@router.get('/dids_international')
async def get_dids_international(
    country: Optional[str] = Query(
        None,
        alias="filter[country]",
        example="US,AR,BR,FR"
    ),
    phone_code: Optional[str] = Query(
        None,
        alias="filter[phone_code]",
        example="1,54,55,33"
    ),
):
    filters = {
        'iso2' : country,
        'phone_code' : phone_code
    }

    countries_id_hashed = Country.get_countries_id(filters)
    params = {}
    if(len(countries_id_hashed) > 0):
        params['filter[country.id]'] = ",".join(countries_id_hashed)


    data = didww_api.get_dids(params)
    if data.get('status') == False:
        raise HTTPException(status_code=data['status_code'], detail=data['message'])

    return data
