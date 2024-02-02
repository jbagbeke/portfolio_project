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
                self.created_at = datetime.now()
                self.updated_at = datetime.now()
                self.id = uuid4()

                self.new(self)

    def save(self, obj=None):
        """
            Saves An Object into the Database

            Args:
                obj - Object to save to the database

            Return - Void
                                                    """
        from models import storage

        if obj:
            storage.save(obj)

    def new(self, obj=None):
        """
            Saves new instance of an object
            
            Args:
                Obj - New instance object to save

            Return Void
                                                """
        from models import storage

        if obj:
            storage.new(obj)

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

    def to_dict(self, time=False):
        """
            Returns Dictionary representation of an object

            Args:
                obj - Object to return dictionay representation of
                time - Option to determine whether to retrieve with updated_at
                       and created_at key and value

            Return:
                Dictionary representation of object
                                                                """
        object_dict = {}

        object_dict.update(self.__dict__)
        object_dict['__class__'] = self.__class__.__name__

        if time:
            return object_dict

        if 'updated_at' in object_dict.keys() and 'created_at' in object_dict.keys():
            del object_dict['created_at']
            del object_dict['updated_at']

        if object_dict.get('messages'):
            tmp = [obj.id for obj in object_dict['messages'] if obj]
            object_dict['messages'] = tmp

        if object_dict.get('recipients'):
            tmp = [obj.id for obj in object_dict['recipients'] if obj]
            object_dict['recipients'] = tmp

        if object_dict.get('recipient'):
            obj = object_dict['recipient']
            object_dict['recipient'] = obj.id

        if object_dict.get('message'):
            obj = object_dict['message']
            object_dict['message'] = obj.id

        if object_dict.get('user'):
            obj = object_dict['user']
            object_dict['user'] = obj.id

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
