from source.components.user_auth import UserSignUp, UserLogin
from source.configuration.mongo_operations import MongoDBOperation
from source.constants import *

mngo = MongoDBOperation()

passw = 'abcdef'
email = 'shindeaniket50@gmail.com'
name = "Aniket shinde"

signup = UserSignUp(user_name=name, user_emailid=email, user_password=passw)

msg = signup.start_user_sign_up()

print(msg)

# mngo.insert_user_entry(db_name=DB_NAME, collection_name=COLLECTION_NAME, user_name="Aniket shinde", 
#                        user_emailid="shindeaniket50@gmail.com", user_password="abcdef")

# flag = mngo.delete_user(db_name=DB_NAME, collection_name=COLLECTION_NAME, user_emailid='shindeaniket50@gmail.com', user_name="Aniket shinde")
# print(flag)

# msg = mngo.validate_user_login(db_name=DB_NAME, collection_name=COLLECTION_NAME, user_emailid=email, user_name=name, user_password=passw)
# print(msg)





# login = UserLogin(user_name=name, user_password=passw)

# token = login.create_jwt(user_name=name, user_emailid=email)
# print(token)

