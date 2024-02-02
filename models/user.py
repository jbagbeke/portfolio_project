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

    def get_ids(self, relation):
        """
            Returns a list of IDs of all related objects to the object
                                                                    """
        obj_id_list = []

        if str(relation) == 'messages':
            message_list = self.messages

            for obj in message_list:
                obj_id_list.append(obj.id)

        if str(relation) == 'recipients':
            recipients_list = self.recipients

            for obj in recipients_list:
                obj_id_list.append(obj.id)

        return obj_id_list
