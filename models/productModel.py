from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from database.database import Base


class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=False, unique=True)
    description = Column(String)
    active = Column(Boolean, default=False)
    price = Column(Integer)
    quantity = Column(Integer)
