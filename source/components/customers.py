import sys
import logging
from datetime import datetime
from source.exception import BillingException
from source.configuration.mongo_operations import MongoDBOperation
from source.constants import DB_NAME, CUSTOMERS_COLLECTION_NAME


logger = logging.getLogger(__name__)


class Customers:

    def __init__(self) -> None:
        self.mongo_operations = MongoDBOperation()

    def create_customer(self, data: dict = None, customer_list: list[dict] = None) -> dict:
        '''
        Create a single customer or a list of customers in the `customers` collection.

        Parameters:
        - data (dict, optional): Dictionary containing customer details for a single customer.
        - customer_list (list of dict, optional): List of dictionaries, each containing details for a customer.

        Returns:
        - dict: A dictionary containing either the `inserted_id(s)` for the successfully created customers or an error message indicating duplication or failure.
        - Single customer returns a message with `inserted_id`, while a list returns `inserted_ids` if created successfully.

        Note:
        - Checks for duplicate customers based on `customer_name` and `contact_person`, `pincode`.
        '''

        logger.info("Entered the create_customer method of customer class")

        try:
            database = self.mongo_operations.get_database(DB_NAME)

            collection = database.get_collection(CUSTOMERS_COLLECTION_NAME)

            if data:
                query = {"customer_name": data["customer_name"], 
                         "contact_person": data["contact_person"],
                         "pincode": data["pincode"]}

                if collection.count_documents(query, limit=1) == 0:

                    data["created_date"] = datetime.now().strftime("%d_%m_%Y")
                    data["created_time"] = datetime.now().strftime("%I:%M:%S_%p")

                    result = collection.insert_one(data)
                    logger.info(f"Successfully created new single customer. customer details - {data}")

                    return {"inserted_id": result.inserted_id, "message": "Customer created successfully."}
                else:
                    logger.info(f"Duplicate single customer! hence not created the customer - {data}")
                    return {"message": "Duplicate customer! Customer with this name, contact person and pincode already exists."}

            elif customer_list:
                unique_customers = set()
                customers_to_insert = []

                for data in customer_list:
                    query = {"customer_name": data["customer_name"], 
                            "contact_person": data["contact_person"],
                            "pincode": data["pincode"]}

                    identifier = (data["customer_name"], data["contact_person"], data["pincode"])

                    if identifier not in unique_customers:
                        unique_customers.add(identifier)

                        if collection.count_documents(query, limit=1) == 0:

                            data["created_date"] = datetime.now().strftime("%d_%m_%Y")
                            data["created_time"] = datetime.now().strftime("%I:%M:%S_%p")

                            customers_to_insert.append(data)
                        else:
                            logger.info(f"Duplicate customer found: {data}")

                if customers_to_insert:
                    result = collection.insert_many(customers_to_insert)
                    logger.info(f"Successfully created list of customers. customers - {customers_to_insert}")
                    return {"inserted_ids": result.inserted_ids, "message": "Customers created successfully."}
                else:
                    return {"message": "No new customers to insert."}

        except Exception as e:
            raise BillingException(e, sys) from e
        
    def read_customer(self, customer_name: str) -> list:
        '''
        Retrieve a customer's details from the `customers` collection.

        Parameters:
        - customer_name (str): Name for the customer.

        Returns:
        - list: A list containing the customer's information if found.
        - If no customer matches the criteria, returns a message indicating that the customer was not found.
        '''

        logger.info("Entered the read_customer method of customers class")

        try:
            database = self.mongo_operations.get_database(DB_NAME)

            collection = database.get_collection(CUSTOMERS_COLLECTION_NAME)

            data = {
                "customer_name": customer_name
            }

            result = collection.find(data)
            result = [res for res in result]

            if result:
                logger.info(f"Found customer/s with the provided data. result - {result}")

            else:
                logger.info("No customer/s found with the provided details.")
                result = {}
            
            logger.info("Exited the read_customer method of customers class")
            return result

        except Exception as e:
            raise BillingException(e, sys) from e
        
    def update_customer(self, data_needs_to_update: dict, updated_data: dict) -> dict:
        """
        Update the details of an existing customer in the `customers` collection.

        Parameters:
        - data_needs_to_update (dict): Dictionary of key-value pairs used to locate the customer record to update (e.g., `{ "customer_name": "aditya ind.", "contact_person": "Aditya shinde", "pincode": "411028" }`).
        - updated_data (dict): Dictionary containing the fields and new values to update for the specified customer.

        Returns:
        - dict: A dictionary containing `message`, `matched_count` and `modified_count`, indicating the number of records matched and modified, respectively.
        """

        logger.info("Entered the update_customer method of customers class")

        try:
            database = self.mongo_operations.get_database(DB_NAME)

            collection = database.get_collection(CUSTOMERS_COLLECTION_NAME)

            current_date = datetime.now().strftime("%d_%m_%Y")
            current_time = datetime.now().strftime("%I:%M:%S_%p")

            updated_data["modified_date"] = current_date
            updated_data["modified_time"] = current_time

            newvalues = { "$set": updated_data } 

            result = collection.update_one(data_needs_to_update, newvalues)

            if result.matched_count > 0:
                message = "Customer updated successfully" if result.modified_count > 0 else "Customer already up to date"
            else:
                message = "No matching customer found"

            logger.info(f"New customer data updated with the previous data. Previous customer data - {data_needs_to_update}. New updated data - {updated_data}")
            logger.info("Exited the update_customer method of customers class")
            
            return {
                "message": message,
                "matched_count": result.matched_count,
                "modified_count": result.modified_count
            }

        except Exception as e:
            raise BillingException(e, sys) from e
        
    def delete_customer(self, customer_name: str, contact_person: str, pincode: str) -> dict:
        """
        Delete a customer's record from the `customers` collection.

        Parameters:
        - customer_name (str): Name of the customer to delete.
        - contact_person (str): Contact person of the customer to delete.
        - pincode (str): Pincode of the customer to delete.

        Returns:
        - dict: A dictionary containing `message` and `deleted_count`, which is `1` if the customer was successfully deleted, or `0` if no matching record was found.
        """
 
        logger.info("Entered the delete_customer method of customers class")

        try:
            database = self.mongo_operations.get_database(DB_NAME)

            collection = database.get_collection(CUSTOMERS_COLLECTION_NAME)

            data = {
                "customer_name": customer_name,
                "contact_person": contact_person,
                "pincode": pincode
            }

            result = collection.delete_one(data)

            if result.deleted_count > 0:
                message = "Customer deleted successfully"
            else:
                message = "No matching customer found"

            logger.info(f"Single entry for customer deleted from the database. deleted customer data - {result}")
            logger.info("Exited the delete_customer method of customers class")
            
            return {
                "message": message,
                "deleted_count": result.deleted_count
            }

        except Exception as e:
            raise BillingException(e, sys) from e
