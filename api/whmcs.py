import os
import requests
from fastapi import HTTPException
from schemas.user import UserCreate

from dotenv import load_dotenv
load_dotenv()

def create_whmcs_client(user: UserCreate):
    whmcs_url = os.getenv("WHMCS_API_URL")
    whmcs_identifier = os.getenv("WHMCS_API_IDENTIFIER")
    whmcs_secret = os.getenv("WHMCS_API_SECRET")

    payload = {
        "identifier": whmcs_identifier,
        "secret": whmcs_secret,
        "action": "AddClient",
        "firstname": user.username,
        "lastname": "User",  # Personalízalo si tienes el campo
        "email": user.email,
        "address1": "Default Address",
        "city": "Default City",
        "state": "NA",
        "postcode": "00000",
        "country": "US",
        "phonenumber": "000-000-0000",
        "password2": user.password,
        "responsetype": "json"
    }

    try:
        response = requests.post(whmcs_url, data=payload)
        data = response.json()

        if response.status_code != 200 or data.get("result") != "success":
            raise HTTPException(
                status_code=500,
                detail=f"WHMCS error: {data.get('message', response.text)}"
            )
    except requests.RequestException as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error conectando a WHMCS: {str(e)}"
        )
def get_whmcs_client_by_email(email: str):
    whmcs_url = os.getenv("WHMCS_API_URL")
    whmcs_identifier = os.getenv("WHMCS_API_IDENTIFIER")
    whmcs_secret = os.getenv("WHMCS_API_SECRET")

    payload = {
        "identifier": whmcs_identifier,
        "secret": whmcs_secret,
        "action": "GetClientsDetails",
        "email": email,
        "responsetype": "json"
    }

    try:
        response = requests.post(whmcs_url, data=payload)
        data = response.json()
        if data.get("result") != "success":
            raise HTTPException(
                status_code=400,
                detail=f"WHMCS client lookup failed: {data.get('message')}"
            )
        return data
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"WHMCS error: {str(e)}")