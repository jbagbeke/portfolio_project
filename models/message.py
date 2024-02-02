#!/usr/bin/python3
"""
    Message Class Defining class attributes and functions

    Purpose: Represents a message sent by the User
                                                        """
from models.base_model import BaseModel
from models.base_model import Base
from sqlalchemy import String, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship


class Message(BaseModel, Base):
    """
        Class representing a message of a user with each instance created
                                                                        """
    __tablename__ = 'messages'
   
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    body = Column(String(1024), nullable=False)
    user = relationship('User', back_populates='messages')
    recipients = relationship('Recipient', back_populates='message',
                                          cascade='all, delete')

    def get_ids(self, relation):
        """
            Returns a list of IDs of all related objects to the object
                                                                    """
        obj_id_list = []

        if str(relation) == 'user':
            user_obj = self.user
            obj_id_list.append(user_obj.id)

        if str(relation) == 'recipients':
            recipients_list = self.recipients
            
            for obj in recipients_list:
                obj_id_list.append(obj.id)

        return obj_id_list
            
