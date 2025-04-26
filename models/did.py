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

from utils.connection import engine


def get_dids():
    query = "SELECT did, city, state FROM did ORDER BY RAND() LIMIT 20"
    with engine.connect() as connection:
        result = connection.execute(text(query))
        # return result.fetchall()
        return [row._asdict() for row in result]
        # return [dict(row) for row in result.mappings()]


def get_did(did):
    query = "SELECT did, city, state FROM did WHERE did = :did"
    with engine.connect() as connection:
        result = connection.execute(text(query), {'did' : did})
        # return result.fetchall()
        if(result):
            return [row._asdict() for row in result]
        return False
        # return [dict(row) for row in result.mappings()]