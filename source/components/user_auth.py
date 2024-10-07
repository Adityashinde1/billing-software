import sys
import jwt
import datetime
import logging
from source.exception import BillingException
from source.constants import DB_NAME, COLLECTION_NAME, BLACKLIST_COLLECTION_NAME
from source.configuration.mongo_operations import MongoDBOperation
from secretts_key import JWT_SECRET_KEY

logger = logging.getLogger(__name__)


class UserSignUp:
    def __init__(self, user_name: str, user_emailid, user_password) -> None:
        self.user_name = user_name
        self.user_emailid = user_emailid
        self.user_password = user_password
        self.mongo_operations = MongoDBOperation()

    def start_user_sign_up(self) -> str:
        logger.info("Entered the start_user_sign_up method of User Sign up class")

        try:
            message = self.mongo_operations.insert_user_entry(db_name=DB_NAME, collection_name=COLLECTION_NAME, user_name=self.user_name,
                                                          user_emailid=self.user_emailid, user_password=self.user_password)

            logger.info("Exited the start_user_sign_up method of User Sign up class")

            return message

        except Exception as e:
            raise BillingException(e, sys) from e
    
    # save the details in the database

class UserLogin:

    secret_key = JWT_SECRET_KEY

    def __init__(self, user_name: str, user_emailid: str, user_password: str) -> None:
        self.user_name = user_name
        self.user_emailid = user_emailid
        self.user_password = user_password
        self.mongo_operations = MongoDBOperation()

    def create_jwt(self, user_name: str, user_emailid: str) -> str:
        logger.info("Entered the create_jwt method of User Login class")

        try:
            payload = {
                "user_name": user_name,
                "user_emailid": user_emailid,
                "exp": datetime.datetime.now() + datetime.timedelta(hours=1)  # 1 hour token expiry
            }
            token = jwt.encode(payload, self.secret_key, algorithm="HS256")

            logger.info(f"Generated token for {user_name}, Token - {token}")

            logger.info("Exited the create_jwt method of User Login class")

            return token

        except Exception as e:
            raise BillingException(e, sys) from e

    def start_login(self) -> str:

        logger.info("Entered the start_login method of User Login class")

        try:
            message = self.mongo_operations.validate_user_login(db_name=DB_NAME, collection_name=COLLECTION_NAME, user_emailid=self.user_emailid, user_name=self.user_name, user_password=self.user_password)

            if message == "Login successful..!":
                token = self.create_jwt(user_name=self.user_name, user_emailid=self.user_emailid)

                logger.info(f"Login successful and generated token for User - {self.user_name}, and Token - {token}")
                logger.info("Exited the start_login method of User Login class")

                return token
            
            else:
                
                logger.info(f"Login failed and did not generated the token for User - {self.user_name}")
                return None

        except Exception as e:
            raise BillingException(e, sys) from e

    # query the user_name and user_password to the database and retrun flag - True or False

class UserLogout:
    def __init__(self) -> None:
        self.mongo_operations = MongoDBOperation()

    def start_logout(self, token: str) -> bool:
        
        logger.info("Entered the start_logout method of User Logout class")

        try:
            self.mongo_operations.insert_blacklist_token(db_name=DB_NAME, blacklist_collection_name=BLACKLIST_COLLECTION_NAME, token=token)

            logger.info("User has been log out successfully.")

            logger.info("Exited the start_logout method of User Logout class")

            return True

        except Exception as e:
            logger.info(f"An error occured during logout, Error: {e}")

        # returns a flag user logout successfully


class UserDelete:
    def __init__(self, user_name: str, user_email: str) -> None:
        self.user_email = user_email
        self.user_name = user_name

    # delete the user from database using emailid and name
