from sqlalchemy import Column, String, Integer
from db import *


class Website(Base):
    __tablename__ = 'websites'
    web_id = Column(Integer, primary_key=True)
    url = Column(String)
    server = Column(String)
