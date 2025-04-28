import json
import os

import requests
from dotenv import load_dotenv
from sqlalchemy import text

from utils import encryption
from utils.connection import Database

load_dotenv()


class DIDWW:
    def __init__(self):
        database_name = "cero208mx_api"
        database = Database(database_name)
        self.engine = database.engine
        data = self.__get_api_data_by_database()
        self.token = encryption.decrypt(data["token"])
        self.url = data["url"]

    '''
    |<><><><><><><><>| DIDWW Fetchs |<><><><><><><><>|
    '''

    def get_dids(self):
        params = {
            # "include" : "did_group,did_group.stock_keeping_units"
            "include": "did_group.stock_keeping_units"
        }
        url_request = f"{self.url}/available_dids"
        data = self.__fetch_didww(url_request, params)
        if data.get("status") == False:
            return data

        dids = self.__process_did_data(data)
        return {"status": True, "status_code": 200, "dids": dids}

    '''
    |<><><><><><><><>| Functions |<><><><><><><><>|
    '''

    def __process_did_data(self, data: dict):
        did_groups = {}
        stocks = {}

        # Procesar los includes
        for include in data["included"]:
            if include["type"] == "did_groups":
                country_url = include["relationships"]["country"]["links"]["related"]
                country_response = self.__fetch_didww(country_url)
                country, prefix, country_iso2 = None, None, None
                if country_response:
                    country = country_response["data"]["attributes"]["name"]
                    prefix = country_response["data"]["attributes"]["prefix"]
                    country_iso2 = country_response["data"]["attributes"]["iso"]

                did_groups[include["id"]] = {
                    "phone_code": include["attributes"]["prefix"],
                    "area_name": include["attributes"]["area_name"],
                    "stocks": include["relationships"]["stock_keeping_units"]["data"],
                    "country": country,
                    "prefix": prefix,
                    "country_iso2": country_iso2,
                }

            elif include["type"] == "stock_keeping_units":
                stocks[include["id"]] = {
                    "setup_price": include["attributes"]["setup_price"],
                    "monthly_price": include["attributes"]["monthly_price"],
                    "channels": include["attributes"]["channels_included_count"],
                }

        dids = []
        for item in data["data"]:
            did_group_id = item["relationships"]["did_group"]["data"]["id"]

            did = {
                'id': item['id'],
                "did": item["attributes"]["number"],
                "phone_code": did_groups[did_group_id]["phone_code"],
                "city": did_groups[did_group_id]["area_name"],
                "country": did_groups[did_group_id]["country"],
                "prefix": did_groups[did_group_id]["prefix"],
                "country_iso2": did_groups[did_group_id]["country_iso2"],
            }
            stock = []
            for did_groups_stock in did_groups[did_group_id]["stocks"]:
                stock.append(stocks[did_groups_stock["id"]])

            did["stocks"] = stock
            # dids.append({item["id"]: did})
            dids.append(did)

        return dids

    '''
    |<><><><><><><><>| Utilities |<><><><><><><><>|
    '''

    def __get_api_data_by_database(self) -> dict:
        query = "SELECT * FROM api WHERE name = 'didww'"
        with self.engine.connect() as connection:
            result = connection.execute(text(query))
            row = result.first()
            return row._asdict() if row else None

    def __fetch_didww(self, url: str, params=[]):
        response = requests.get(url, params=params, headers=self.__get_headers())
        if not response.ok:
            return self.__failed_response(response)

        return response.json()

    def __get_headers(self):
        return {
            # "Accept": "application/vnd.api+json",
            "Content-Type": "application/vnd.api+json",
            # "X-Didww-Api-Version": "2022-05-10",
            "Api-Key": self.token,
        }

    def __failed_response(self, response):
        try:
            error = response.json()
        except ValueError:
            error = response.text
        return {
            "status": False,
            "status_code": response.status_code,
            "message": "No es posible procesar su solicitud",
            "error": error,
        }
