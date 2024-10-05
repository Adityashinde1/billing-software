from source.components.user_auth import UserSignUp, UserLogin, UserLogout
from source.configuration.mongo_operations import MongoDBOperation
from source.constants import *

mngo = MongoDBOperation()

password_1 = 'abcdef'
email_1 = 'shindeaniket50@gmail.com'
name_1 = "Aniket shinde"

password_2 = '123456'
email_2 = 'shindeadi39@gmail.com'
name_2 = "Aditya shinde"

signup = UserSignUp(user_name=name_1, user_emailid=email_1, user_password=password_1)

msg = signup.start_user_sign_up()

print(msg)

signup = UserSignUp(user_name=name_2, user_emailid=email_2, user_password=password_2)

msg = signup.start_user_sign_up()

print(msg)

login = UserLogin(user_name=name_1, user_emailid=email_1, user_password=password_1)

token_1 = login.start_login()

print("Logging done for Aniket....")

login = UserLogin(user_name=name_2, user_emailid=email_2, user_password=password_2)

token_2 = login.start_login()

print("Logging done for Aditya....")

logout = UserLogout(token=token_1)

flag = logout.start_logout()

print(f"{flag}....Aniket Logged out")

logout = UserLogout(token=token_2)

flag = logout.start_logout()

print(f"{flag}....Aditya Logged out")

# mngo.insert_user_entry(db_name=DB_NAME, collection_name=COLLECTION_NAME, user_name="Aniket shinde", 
#                        user_emailid="shindeaniket50@gmail.com", user_password="abcdef")

# flag = mngo.delete_user(db_name=DB_NAME, collection_name=COLLECTION_NAME, user_emailid='shindeaniket50@gmail.com', user_name="Aniket shinde")
# print(flag)

# msg = mngo.validate_user_login(db_name=DB_NAME, collection_name=COLLECTION_NAME, user_emailid=email, user_name=name, user_password=passw)
# print(msg)





# login = UserLogin(user_name=name, user_password=passw)

# token = login.create_jwt(user_name=name, user_emailid=email)
# print(token)

