from sqlalchemy import Boolean, Column, Integer, String
from config.database import Base
from typing import Optional

class User(Base):
    __table_args__ = {'extend_existing': True}
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)  
    phone = Column(String)
    address = Column(String)
    state = Column(String)
    city = Column(String)
    calle = Column(String)
    postal_code = Column(String)
    interior_number = Column(String)
    tree = Column(Integer)

