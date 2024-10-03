import logging
from source.exception import BillingException




class UserSignUp:
    def __init__(self, user_name: str, user_emailid, user_password) -> None:
        self.user_name = user_name
        self.user_emailid = user_emailid
        self.user_password = user_password
        
    
    # save the details in the database



class UserLogin:
    def __init__(self, user_name: str, user_password) -> None:
        self.user_name = user_name
        self.user_password = user_password


    # query the user_name and user_password to the database and retrun flag - True or False

class UserLogout:
    def __init__(self, user_name: str) -> None:
        self.user_name = user_name
    # returns a flag user logout successfully


class UserDelete:
    def __init__(self, user_name: str, user_email: str) -> None:
        self.user_email = user_email
        self.user_name = user_name

    # delete the user from database using id and name
