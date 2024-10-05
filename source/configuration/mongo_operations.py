import sys
import bcrypt
import logging
from json import loads
from os import environ
from typing import Collection
from pandas import DataFrame
from pymongo.database import Database
import pandas as pd
from pymongo import MongoClient
from secretts_key import DB_URL


class MongoDBOperation:
    def __init__(self):
        self.DB_URL = DB_URL
        
        self.client = MongoClient(self.DB_URL)

    def get_database(self, db_name) -> Database:

        logging.info("Entered get_database method of MongoDB_Operation class")

        try:
            db = self.client[db_name]

            logging.info(f"Created {db_name} database in MongoDB")

            logging.info("Exited get_database method MongoDB_Operation class")

            return db

        except Exception as e:
            raise e
        
    @staticmethod
    def get_collection(database, collection_name) -> Collection:

        logging.info("Entered get_collection method of MongoDB_Operation class")

        try:
            collection = database[collection_name]

            logging.info(f"Created {collection_name} collection in mongodb")

            logging.info("Exited get_collection method of MongoDB_Operation class ")

            return collection

        except Exception as e:
            raise e
        
    def get_collection_as_dataframe(self, db_name, collection_name) -> DataFrame:

        logging.info(
            "Entered get_collection_as_dataframe method of MongoDB_Operation class"
        )

        try:
            database = self.get_database(db_name)

            collection = database.get_collection(name=collection_name)

            df = pd.DataFrame(list(collection.find()))

            if "_id" in df.columns.to_list():
                df = df.drop(columns=["_id"], axis=1)

            logging.info("Converted collection to dataframe")

            logging.info(
                "Exited get_collection_as_dataframe method of MongoDB_Operation class"
            )

            return df

        except Exception as e:
            raise e
        
    def insert_user_entry(self, db_name: str, collection_name: str, user_name: str, user_emailid: str, user_password: str) -> None:
        """
        This method is used to insert user into the database.

        """
        logging.info("Entered insert_user_entry method of MongoDB_Operation")

        try:
            hashed_password = bcrypt.hashpw(user_password.encode('utf-8'), bcrypt.gensalt())

            record = {
                "user_name": user_name,
                "user_emailid": user_emailid,
                "password": hashed_password
            }

            logging.info("gathered user's information")

            database = self.get_database(db_name)

            collection = database.get_collection(collection_name)

            if collection.find_one({
                "user_name": user_name,
                "user_emailid": user_emailid
            }):
                message = "User already exists..!"

            else:

                logging.info("Inserting record to MongoDB",)

                collection.insert_one(record)

                logging.info("Inserted record to MongoDB")

                message = "User's signed up successfully...!"

                logging.info(f"User signed up successfully. User name - {user_name}")

            logging.info(
                "Exited the insert_user_entry method of MongoDB_Operation"
            )

            return message

        except Exception as e:
            raise e

    def delete_user(self, db_name: str, collection_name: str, user_emailid: str = None, user_name: str = None, users_list: list = None) -> str:
        """
        If you want to delete single user at a time Delete the user by proving its user_name and 
        user_email.
        users_list: If you want to delete multiple users at a time, you have to use users_list parameter

        e.g. 
        users = [
                    {"user_name": "JohnDoe", "user_email": "john@example.com"},
                    {"user_name": "JaneDoe", "user_email": "jane@example.com"}
                ]
        result = delete_user(db_name=<db_name>, collection_name=<collection_name>, users_list=users)    
        print(result) # True or False
        """
        
        logging.info("Entered delete_user method of MongoDB_Operation")
        
        try:
            deletion_flag = False

            database = self.get_database(db_name)

            collection = database.get_collection(collection_name)

            if user_name and user_emailid:
                query = {}
                if user_name:
                    query["user_name"] = user_name
                if user_emailid:
                    query["user_emailid"] = user_emailid

                result = collection.delete_many(query)

                if result.deleted_count > 0:
                    deletion_flag = True
                    logging.info(f"Deleted user from the database. User name - {user_name}, User Email - {user_emailid}")

                else:
                    deletion_flag = False

            elif users_list:
                query = {"$or": users_list}

                result = collection.delete_many(query)
            
                if result.deleted_count > 0:
                    deletion_flag = True
                    logging.info(f"Deleted users from the database. User's list - {users_list}")
                else:
                    deletion_flag = False

            logging.info("Exited delete_user method of MongoDB_Operation")
            
            return deletion_flag

        except Exception as e:
            raise e

    def validate_user_login(self, db_name: str, collection_name: str, user_emailid: str, user_name: str, user_password: str) -> str:
        
        logging.info("Entered validate_user_login method of MongoDB_Operation")

        try:
            message = ""
            database = self.get_database(db_name)

            collection = database.get_collection(collection_name)

            user = collection.find_one({
                "user_name": user_name,
                "user_emailid": user_emailid
            })

            if user:
                hashed_password = user["password"]

                if bcrypt.checkpw(user_password.encode('utf-8'), hashed_password=hashed_password):
                    logging.info(f"Login successful..! for user - {user_name}")
                    message = "Login successful..!"
                else:
                    logging.info(f"Invalid password. for user - {user_name}")
                    message = "Invalid password."

            else:
                logging.info(f"User not found. User name - {user_name}. User Email - {user_emailid}")
                message = "User not found."

            logging.info("Entered validate_user_login method of MongoDB_Operation")

            return message

        except Exception as e:
            raise e

    def insert_blacklist_token(self, db_name: str, blacklist_collection_name: str, token: str) -> None:
        
        logging.info("Entered the insert_blacklist_token method of MongoDb operation class")

        try:
            database = self.get_database(db_name)

            blacklist_collection = database.get_collection(blacklist_collection_name)

            blacklist_collection.insert_one({"token": token})

            logging.info("Token has been inserted to the blacklisted collection")

        except Exception as e:
            raise e
