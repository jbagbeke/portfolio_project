#!usr/bin/python3
"""
    Base Model For Portfolio Project

    Purpose:
        All other classes will inherit from this class

    What it will do:
        Handle inherit instantiation and time updates

    Storage Type:
        Database specifically Mysql with SQLAlchemy
                                                    """
from sqlalchemy import String, Column, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
from uuid import uuid4
from datetime import datetime


Base = declarative_base()


class BaseModel:
    """
        Base Model Class For this Project

        Purpose:
            Perform inherit tasks and other classes will inherit from this
                                                                        """
    id = Column(String(60), primary_key=True, nullable=False)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)


    def __init__(self, **kwargs):
        """
            Handles Initialization of base attributes of all classes
                                                                    """
        if kwargs:
            for key, value in kwargs.items():
                if key == 'updated_at' or key == 'created_at':
                    continue
                setattr(self, key, value)

            if 'updated_at' not in kwargs.keys() and 'created_at' not in kwargs.keys():
                self.created_at = datetime.utcnow()
                self.updated_at = datetime.utcnow()
                self.id = uuid4()

    def save(self):
        """
            Saves An Object into the Database

            Return - Void
                                                    """
        from models import storage

        self.updated_at = datetime.utcnow()
        storage.save()

    def delete(self, obj=None):
        """
            Deletes instance object from the database
            
            Args:
                obj - Object to delete from database

            Return - Void
                                                    """
        from models import storage

        if obj:
            storage.delete(obj)

    def to_dict(self):
        """
            Returns Dictionary representation of an object

            Args:
                obj - Object to return dictionay representation of
                time - Option to determine whether to retrieve with updated_at
                       and created_at key and value

            Return:
                Dictionary representation of object
                                                                """
        time = "%Y-%m-%dT%H:%M:%S.%f"
        object_dict = {}

        object_dict.update(self.__dict__)
        object_dict['__class__'] = self.__class__.__name__

        if 'updated_at' in object_dict.keys():
            object_dict["updated_at"] = self.updated_at.strftime(time)

        if 'created_at' in object_dict.keys():
            object_dict["created_at"] = self.created_at.strftime(time)

        if object_dict.get('messages'):
            object_dict['messages'] = self.get_ids('messages')

        if object_dict.get('recipients'):
            object_dict['recipients'] = self.get_ids('recipients')

        if object_dict.get('message'):
            object_dict['message'] = self.get_ids('message')

        if object_dict.get('user'):
            object_dict['user'] = self.get_ids('user')

        if '_sa_instance_state' in object_dict.keys():
            del object_dict['_sa_instance_state']

        return object_dict

    def __str__(self):
        """
            Controls how an object is printed when print() is called on it

            Args:
                None

            Return - Void
                                                                        """
        object_name = self.__class__.__name__
        object_id = self.id

        return str("[{}] ({}): {}".format(object_name,
                                          object_id,
                                          self.to_dict()))

    def get_ids(self, relation):
        """
            Returns a list of IDs of all related objects to the object
                                                                    """
        obj_id_list = []

        if relation == 'user':
            user_obj = self.user
            obj_id_list.append(user_obj.id)

        if relation == 'recipients':
            recipients_list = self.recipients

            for obj in recipients_list:
                obj_id_list.append(obj.id)

        if relation == 'messages':
            message_list = self.messages

            for obj in message_list:
                obj_id_list.append(obj.id)
        if relation == 'message':
            message_obj = self.message
            obj_id_list.append(message_obj.id)

        return obj_id_list
