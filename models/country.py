from sqlalchemy import text

import utils.utils as utils
from utils.connection import Database

database_name = 'cero208mx_api'
database = Database(database_name)
engine = database.engine

def get_countries_id(filters=""):
    query = "SELECT id_hashed \
        FROM country \
        WHERE id_hashed IS NOT NULL \
            AND phone_code IS NOT NULL"

    filter_stmt, params = utils.get_filter_query(filters=filters, need_where=False)
    if(not filter_stmt):
        return []

    query = f"{query} AND ({filter_stmt})"
    
    with engine.connect() as connection:
        result = connection.execute(text(query), params)
        return [row._asdict()['id_hashed'] for row in result]
