"""#!/usr/bin/python3"""
"""
    Represents the recipients class with each instance representing
    the recipient of the message a user sends
                                                                """
from models.base_model import BaseModel
from models.base_model import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship


class Recipient(BaseModel, Base):
    """
        Represents the recipient class of a message
                                                    """
    __tablename__ = 'recipients'

    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    message_id = Column(String(60), ForeignKey('messages.id'), nullable=False)
    receiver_number = Column(String(20), nullable=False)
    message = relationship('Message', back_populates='recipients')
    user = relationship('User', back_populates='recipients')
