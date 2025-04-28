# from sqlalchemy import TIMESTAMP, Column, ForeignKey, Integer, String
# from sqlalchemy.orm import relationship
# from sqlalchemy.sql import func

# from database import Base

# class did(Base):
#     __tablename__ = "did"

#     id = Column(Integer, primary_key=True, index=True)
#     did = Column(String(15), unique=True, nullable=False)
#     id_country = Column(Integer, ForeignKey("country.id"))
#     state = Column(String(100))
#     city = Column(String(100))
#     phone_code = Column(Integer)
#     status = Column(Integer)


from sqlalchemy import text

from utils.connection import Database

database_name = 'cero208mx_api'
database = Database(database_name)
engine = database.engine

def get_dids():
    query = "SELECT d.id_hashed AS 'id', d.did, d.phone_code, c.name AS 'country', d.state, d.city, c.phone_code AS 'prefix', c.iso2 as 'country_iso2' \
        FROM did d \
        LEFT JOIN country c ON d.id_country = c.id \
        ORDER BY RAND() LIMIT 20"
    with engine.connect() as connection:
        result = connection.execute(text(query))
        # return result.fetchall()
        return [row._asdict() for row in result]
        # return [dict(row) for row in result.mappings()]


def get_did(did):
    query = "SELECT d.id_hashed AS 'id', d.did, d.phone_code, c.name AS 'country', d.state, d.city, c.phone_code AS 'prefix', c.iso2 as 'country_iso2' \
        FROM did d \
        LEFT JOIN country c ON d.id_country = c.id \
        WHERE did = :did"
    with engine.connect() as connection:
        result = connection.execute(text(query), {'did' : did})
        # return result.fetchall()
        if(result): 
            return [row._asdict() for row in result]
        return False
        # return [dict(row) for row in result.mappings()]