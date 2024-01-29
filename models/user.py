#!/usr/bin/python3
"""
    User class For the Portfilio Project
                                        """
from models.base_model import Base
from models.base_model import BaseModel
from sqlalchemy import String, Integer


def User(BaseModel, Base):
    """
        User Class which represents a user in this project
                                                            """
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True)
    user_name = Column(String(125), unique=True, nullable=False)
    user_number = Column(Integer, nullable=False)
    messages = relationship('Message', back_populates='message',
                                       cascade='all, delete')
