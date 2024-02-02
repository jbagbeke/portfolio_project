#!/usr/bin/python3
"""
    User class For the Portfilio Project
                                        """
from models.base_model import BaseModel, Base
from sqlalchemy import String, Integer, Column, ForeignKey
from sqlalchemy.orm import relationship


class User(BaseModel, Base):
    """
        User Class which represents a user in this project
                                                            """
    _userCount = 1000

    __tablename__ = 'users'

    user_id = Column(Integer, unique=True, nullable=False)
    name = Column(String(125), nullable=False)
    number = Column(String(20), unique=True, nullable=False)
    messages = relationship('Message', back_populates='user',
                                       cascade='all, delete')
    recipients = relationship('Recipient', back_populates='user',
                                           cascade='all, delete')

    def _UserID():
        """
            Generates unique User ID

            Return:
                Unique ID of User
                                        """

        import hashlib
        from models import storage

        user_string = str(storage.userCount())
        hashed = hashlib.sha256(user_string.encode()).hexdigest()

        user_id = int(hashed[:5], 16)

        return user_id
