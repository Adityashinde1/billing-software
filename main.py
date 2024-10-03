from source.components.user_auth import UserSignUp
from source.configuration.mongo_operations import MongoDBOperation
from source.constants import *

mngo = MongoDBOperation()

# mngo.insert_user_entry(db_name=DB_NAME, collection_name=COLLECTION_NAME, user_name="Aditya shinde", 
#                        user_emailid="shindeadi39@gmail.com", user_password="123456")


flag = mngo.delete_user(db_name=DB_NAME, collection_name=COLLECTION_NAME, user_emailid='shindeadi39@gmail.com', user_name="Aditya shinde")
print(flag)