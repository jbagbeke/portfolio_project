#!/usr/bin/python3
"""
    Keeps Track Of Number of Users in the DataBase
                                                    """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, Integer


class UserCount(BaseModel, Base):
    """
        Updates User Count
                            """

    __tablename__ = 'usercount'

    usercount = Column(Integer, nullable=False)
