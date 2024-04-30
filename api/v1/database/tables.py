from sqlalchemy import Column, String, Integer, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base
from datetime import datetime

BaseDBModel = declarative_base()


class TableUsers(BaseDBModel):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, nullable=False)
    nickname = Column(String, nullable=False)
    password = Column(String)
    active = Column(Boolean, nullable=True, default=True)


class TableOrders(BaseDBModel):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, autoincrement=True)
    buyer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    seller_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    amount = Column(Integer, nullable=False)
    active = Column(Boolean, nullable=False, default=True)
    date = Column(DateTime, nullable=True, default=datetime.today())
