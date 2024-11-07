from source.components.user_auth import UserSignUp, UserLogin, UserLogout
from source.configuration.mongo_operations import MongoDBOperation
from source.components.products import Products
from source.components.customers import Customers
from source.constants import *

mngo = MongoDBOperation()
products = Products()
customers = Customers()

password_1 = 'abcdef'
email_1 = 'shindeaniket50@gmail.com'
name_1 = "Aniket shinde"

password_2 = '123456'
email_2 = 'shindeadi39@gmail.com'
name_2 = "Aditya shinde"

# signup = UserSignUp(user_name=name_1, user_emailid=email_1, user_password=password_1)

# msg = signup.start_user_sign_up()

# print(msg)

# signup = UserSignUp(user_name=name_2, user_emailid=email_2, user_password=password_2)

# msg = signup.start_user_sign_up()

# print(msg)

# login = UserLogin(user_name=name_1, user_emailid=email_1, user_password=password_1)

# token_1 = login.start_login()

# print("Logging done for Aniket....")

# login = UserLogin(user_name=name_2, user_emailid=email_2, user_password=password_2)

# token_2 = login.start_login()

# print("Logging done for Aditya....")

# logout = UserLogout(token=token_1)

# flag = logout.start_logout()

# print(f"{flag}....Aniket Logged out")

# logout = UserLogout(token=token_2)

# flag = logout.start_logout()

# print(f"{flag}....Aditya Logged out")

# mngo.insert_user_entry(db_name=DB_NAME, collection_name=COLLECTION_NAME, user_name="Aniket shinde", 
#                        user_emailid="shindeaniket50@gmail.com", user_password="abcdef")

# flag = mngo.delete_user(db_name=DB_NAME, collection_name=COLLECTION_NAME, user_emailid='shindeaniket50@gmail.com', user_name="Aniket shinde")
# print(flag)

# msg = mngo.validate_user_login(db_name=DB_NAME, collection_name=COLLECTION_NAME, user_emailid=email, user_name=name, user_password=passw)
# print(msg)





# login = UserLogin(user_name=name, user_password=passw)

# token = login.create_jwt(user_name=name, user_emailid=email)
# print(token)

# prod_collection = 'products'

# sdata = {
#             "product_name": '5/8 Unc',
#             "product_number": '103001899',
#             "company_for": 'omkar ind'
#         }

# data = [{
#             "product_name": '5/8 Unc',
#             "product_number": '103001899',
#             "company_for": 'omkar ind'
#         },
#         {
#             "product_name": 'stud 9/16 × 7/16',
#             "product_number": '101557699',
#             "company_for": 'omkar ind'
#         },
#         {
#             "product_name": 'stud 9/16',
#             "product_number": '5302645',
#             "company_for": 'omkar ind'
#         }]

# data = mngo.create_product(db_name=DB_NAME, product_collection_name=prod_collection, product_list=data)

# print(data)

# database = mngo.get_database(db_name=DB_NAME)

# collection = mngo.get_collection(database=database, collection_name=PRODUCTS_COLLECTION_NAME)


# result = collection.find_one({"product_name":"5/8 Unc",
#                                 "product_number":"103001899",
#                                 "company_for":"omkar ind"})

# print(type(result))

# data_needs_to_update = {
#     "product_name": "stud 9/16 × 7/16",
#     "product_number": "101557699",
#     "company_for": "omkar ind"
# }

# updated_data = {
#     "product_name": "stud 9/16 × 7/16",
#     "product_number": "101557699",
#     "company_for": "desai autocomp"
# }

# a = products.update_product(data_needs_to_update=data_needs_to_update, updated_data=updated_data)
# print(a)
# a = products.read_product(product_name="stud 9/16 × 7/16", product_number="101557699", company_for="desai autocomp")
# print(a)
# a = products.delete_product(product_name="stud 9/16 × 7/16", product_number="101557699", company_for="desai autocomp")
# print(a)

sdata = {
            "customer_name": 'aditya ind.',
            "customer_add": "sr. no. 53/8/1, near swami vivekananda industrial est, hadapsar, pune.",
            "pincode": "411028",
            "customer_gst": "27ARYPS5304E1ZD",
            "state": "maharashtra",
            "state_code": "27",
            "contact_person": "Ajay shinde",
            "contact_number": "9921282422",
            "emailid": "adityaindustries.pune94@gmail.com"
        }

data = [{
            "customer_name": 'desai autocomp',
            "customer_add": "gat no. 416, tupe wasti, wagholi pune.",
            "pincode": "411056",
            "customer_gst": "27DESAI0545D2EW",
            "state": "maharashtra",
            "state_code": "27",
            "contact_person": "Santosh shinde",
            "contact_number": "9922135684",
            "emailid": "desaiautocomp2@gmail.com"
        },
        {
            "customer_name": 'desai autocomp',
            "customer_add": "shop. 2, infront ratna gears, wadgaonsheri, pune.",
            "pincode": "411569",
            "customer_gst": "27DESAI0545D2EW",
            "state": "maharashtra",
            "state_code": "27",
            "contact_person": "mama desai",
            "contact_number": "9921897423",
            "emailid": "desaiautocomp2@gmail.com"
        },
        {
            "customer_name": 'omkar ind.',
            "customer_add": "block no.56, MIDC, chinchwad, pune.",
            "pincode": "411019",
            "customer_gst": "27AAAFO2000L1ZN",
            "state": "maharashtra",
            "state_code": "27",
            "contact_person": "Omkar joshi",
            "contact_number": "9955669922",
            "emailid": "omkar.industries@gmail.com"
        }]

# result = customers.create_customer(customer_list=data)
# print(result)
# result = customers.read_customer(customer_name="desai autocomp")
# print(result)

data_needs_to_update = {
            "customer_name": 'aditya ind.',
            "customer_add": "sr. no. 53/8/1, near swami vivekananda industrial est, hadapsar, pune.",
            "pincode": "411028",
            "customer_gst": "27ARYPS5304E1ZD",
            "state": "maharashtra",
            "state_code": "27",
            "contact_person": "Aditya shinde",
            "contact_number": "9921282422",
            "emailid": "adityaindustries.pune94@gmail.com"
        }

updated_data = {
            "customer_name": 'aditya ind.',
            "customer_add": "sr. no. 53/8/1, near swami vivekananda industrial est, hadapsar, pune.",
            "pincode": "411028",
            "customer_gst": "27ARYPS5304E1ZD",
            "state": "maharashtra",
            "state_code": "27",
            "contact_person": "Aditya shinde",
            "contact_number": "9921282422",
            "emailid": "adityaindustries.pune94@gmail.com"
        }

# result = customers.update_customer(data_needs_to_update=data_needs_to_update, updated_data=updated_data)
# print(result)

reult = customers.delete_customer(customer_name="aditya ind.", contact_person="Aditya shinde", pincode="411028")
print(reult)