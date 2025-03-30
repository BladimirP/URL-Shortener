from sqlalchemy import Column, Integer, String, Date, BigInteger
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class URL(Base):
    __tablename__ = 'URLs'

    id = Column(Integer, primary_key=True, index=True)
    original_url = Column(String)
    short_url = Column(String)
    click_count = Column(BigInteger)
    activation_date = Column(Date)
    expiration_date = Column(Date)