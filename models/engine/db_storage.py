#!/usr/bin/python3
"""
    Database storage File for Handling Database transactions

    Purpose: Connects to The DataBase Specified Via Env Variables
             to perform database activities as required
                                                                """
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.user import User
from models.message import Message
from models.recipient import Recipient
from models.usercount import UserCount
from models.base_model import Base
import os


class DBStorage:
    """
        Handles DataBase related activities
                                            """
    def __init__(self):
        """
            Connects to a database and creates a session
                                                        """
        username = os.getenv('PORTFOLIO_DB_USERNAME')
        password = os.getenv('PORTFOLIO_DB_PASSWORD')
        host = os.getenv('PORTFOLIO_DB_HOST')
        database = os.getenv('PORTFOLIO_DB_DATABASE')
        
        engine_url = "mysql+mysqldb://{}:{}@{}/{}".format(username,
                                                          password,
                                                          host,
                                                          database)
        engine = create_engine(engine_url)
        self.__engine = engine

    def get(self, cls=None, obj_id=None):
        """
            Retrieves a particular user from database based on the [id]

            Args:
                cls - Class Table to Query
                user_id - Identification Number of User

            Return:
                Success - Returns the object
                Failure - Returns None
                                                                      """
        obj = None

        if cls:
            if cls == User:
                obj = self.__session.query(cls).filter(cls.user_id==obj_id).first()
            else:
                obj = self.__session.query(cls).filter(cls.id==obj_id).first()

        return obj

    def reload(self):
        """
            Reloads data from the database
                                            """
        Base.metadata.create_all(self.__engine)
        factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(factory)
        self.__session = Session

    def all(self, cls=None):
        """
            Retrives all instances of a particular class or of all classes
                                                                        """
        
        all_list = []

        cls_dict = {"User": User,
                    "Message": Message,
                    "Recipient": Recipient}

        if cls:
            all_objects = self.__session.query(cls_dict[cls]).all()
        else:
            user_objects = self.__session.query(User).all()
            recipient_objects = self.__session.query(Recipient).all()
            message_objects = self.__session.query(Message).all()
            all_objects = user_objects + recipient_objects + message_objects

        if len(all_objects) > 0:
            all_list = [obj.to_dict() for obj in all_objects]

        return all_list

    def count(self, cls=None):
        """
            Counts the number of instances of a class if specified
            
            Args:
                cls - class specified to be counted
                                                                """
        if cls:
            cls_count = len(self.all(cls))
        else:
            cls_count = len(self.all())

        return cls_count


    def save(self):
        """
            Saves object to database
            
            Return - Void
                                                """
        self.__session.commit()

    def new(self, obj=None):
        """
            Adds newly created object to the database

            Args:
                obj - New instance object to add to the database

            Return - Void
                                                                """
        if obj:
            self.__session.add(obj)
    
    def delete(self, obj=None):
        """
            Deletes an object from the database

            Args:
                obj - object to delete

            Return - Void
                                                """
        if obj:
            self.__session.delete(obj)

    def close(self):
        """
            CLoses current session to the DataBase
                                                    """

        self.__session.close()

    def user_login(self, user_id):
        """
            Returns User object if user_id exists else None
                                                            """
        user_obj = self.__session.query(User).filter(User.user_id==user_id).all()

        if (user_obj):
            return user_obj

        return None

    def userCount(self):
        """
            Returns current Count of Users from the database
                                                            """
        count_object = self.__session.query(UserCount).first()

        if not count_object:
            count_obj = UserCount(usercount=1000)
            count_obj.usercount = 1001
            self.__session.add(count_obj)
            self.__session.commit()

            return 1000

        count = count_object.usercount
        count_object.usercount = count + 1

        self.__session.commit()

        return count
