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
import os


def DBStorage():
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

        Session = sessionmaker(bind=engine)
        ScopedSession = scoped_session(Session)
        self.__session = ScopedSession()

    def get(self, cls=None, uuid=None, user_id=None):
        """
            Retrieves a particular user from database based on the [id]

            Args:
                cls - Class Table to Query
                uuid - UUID4 Generated ID of User
                user_id - Identification Number of User

            Return:
                Success - Returns the object
                Failure - Returns None
                                                                      """

        if cls:
            if uuid:
                obj = self.__session.query(cls).filter(cls.id=uuid).first()

            if user_id:
                obj = self.__session.query(cls).filter(cls.user_id=user_id).first()

    
        return obj

    def save(self, obj=None):
        """
            Saves object to database
            
            Args:
                obj - Object to save to database
            
            Return - Void
                                                """
        if obj:
            self.__session.commit(obj)

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
