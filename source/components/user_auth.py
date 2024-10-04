import sys
import jwt
import datetime
import logging
from source.exception import BillingException
from source.constants import DB_NAME, COLLECTION_NAME
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

            logger.info("exited the start_user_sign_up method of User Sign up class")

            return message

        except Exception as e:
            raise BillingException(e, sys) from e
    
    # save the details in the database

class UserLogin:

    secret_key = JWT_SECRET_KEY

    def __init__(self, user_name: str, user_password: str) -> None:
        self.user_name = user_name
        self.user_password = user_password

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
        
    def verify_jwt(self, token: str) -> bool:
        logger.info("Entered the verify_jwt method of User Login class")

        try:
            payload = jwt.decode(token, self.secret_key, algorithms=["HS256"])

            logger.info("Existed the verify_jwt method of User Login class")
            return payload

        except jwt.ExpiredSignatureError:
            logger.info("Token has expired")
            return None
        
        except jwt.InvalidTokenError:
            logger.info("Invalid token")
            return None

    # query the user_name and user_password to the database and retrun flag - True or False

class UserLogout:
    def __init__(self, user_name: str) -> None:
        self.user_name = user_name
    # returns a flag user logout successfully


class UserDelete:
    def __init__(self, user_name: str, user_email: str) -> None:
        self.user_email = user_email
        self.user_name = user_name

    # delete the user from database using emailid and name
