import sys
import logging
from datetime import datetime
from source.exception import BillingException
from source.configuration.mongo_operations import MongoDBOperation
from source.constants import DB_NAME, PRODUCTS_COLLECTION_NAME


logger = logging.getLogger(__name__)


class Products:

    def __init__(self) -> None:
        self.mongo_operations = MongoDBOperation()

    def create_product(self, data: dict = None, product_list: list[dict] = None) -> dict:
        """
        If you want to create single product at a time create the product by providing its product_name, product_number and 
        company_for.
        products_list: If you want to create multiple products at a time, you have to use product_list parameter

        e.g. 
        products = [
                    {"product_name": "stud 5/8 × 3/8", "product_number": "835201199", "company_for": "omkar ind"},
                    {"product_name": "stud 5/16 × 7/16", "product_number": "835201799", "company_for": "omkar ind"}
                ]
        result = create_product(db_name=<db_name>, product_collection_name=<product_collection_name>, product_list=products)    
        print(result) # dict of id and message.

        output type - dict
        {'inserted_ids': "", 'message': ""} or
        incase of duplicates - 
        {'message': ""}
        """

        logger.info("Entered the create_product method of products class")

        try:
            database = self.mongo_operations.get_database(DB_NAME)

            collection = database.get_collection(PRODUCTS_COLLECTION_NAME)

            if data:
                query = {
                    "product_name": data["product_name"],
                    "product_number": data["product_number"],
                    "company_for": data["company_for"]
                }

                if collection.count_documents(query, limit=1) == 0:
                    current_date = datetime.now().strftime("%d_%m_%Y")
                    current_time = datetime.now().strftime("%I:%M:%S_%p")
                    data["created_date"] = current_date
                    data["created_time"] = current_time
                    result = collection.insert_one(data)

                    message = "Created product successfully...!"
                    logger.info(f"Successfully created new single product. product - {data}")

                    metadata = {"inserted_id": result.inserted_id, "message": message}
                    return metadata

                else:
                    message = f"Duplicate product! Product with this product_name, product_number and company_for already exists. Duplicate product data - {data}"
                    metadata = {"message": message}
                    logger.info(f"Duplicate single product! hence not created the product - {data}")
                    return metadata

            elif product_list:
                unique_products = set()
                products_to_insert = []

                for data in product_list:
                    query = {
                        "product_name": data["product_name"],
                        "product_number": data["product_number"],
                        "company_for": data["company_for"]
                    }

                    identifier = (data["product_name"], data["product_number"], data["company_for"])

                    if identifier not in unique_products:
                        unique_products.add(identifier)

                        if collection.count_documents(query, limit=1) == 0:
                            current_date = datetime.now().strftime("%d_%m_%Y")
                            current_time = datetime.now().strftime("%I:%M:%S_%p")
                            data["created_date"] = current_date
                            data["created_time"] = current_time

                            products_to_insert.append(data)
                        
                        else:
                            logger.info(f"Duplicate product! Product with this product_name, product_number and company_for already exists. Duplicate product data - {data}")

                if products_to_insert:
                    result = collection.insert_many(products_to_insert)
                    message = "Created product successfully...!"
                    logger.info(f"Successfully created list of products. products - {products_to_insert}")
                    metadata = {"inserted_ids": result.inserted_ids, "message": message}
                    return metadata
                else:
                    message = "No new products to insert."
                    logger.info(message)
                    metadata = {"message": message}
                    return metadata

            logger.info("Exited the create_product method of products class")

        except Exception as e:
            raise BillingException(e, sys) from e
        
    def read_product(self, product_name: str, product_number: str, company_for: str) -> dict:
        """
        Fetches a product document from MongoDB based on provided fields.
        Parameters:
        - product_name (str): Name of the product.
        - product_number (str): Product's unique number.
        - company_for (str): Company associated with the product.

        Returns:
        - dict: The product document if found, else an empty dict.
        """

        logger.info("Entered the read_product method of products class")

        try:
            database = self.mongo_operations.get_database(DB_NAME)

            collection = database.get_collection(PRODUCTS_COLLECTION_NAME)

            data = {
                "product_name": product_name,
                "product_number": product_number,
                "company_for": company_for
            }

            result = collection.find_one(data)

            if result:
                logger.info(f"Found one result with the provided data. result - {result}")

            else:
                logger.info("No product found with the provided details.")
                result = {}

            logger.info("Exited the read_product method of products class")
            return result

        except Exception as e:
            raise BillingException(e, sys) from e
        
    def update_product(self, data_needs_to_update: dict, updated_data: dict) -> dict:
        """
        Updates a product document in MongoDB based on provided filter criteria.
        
        Parameters:
        - data_needs_to_update (dict): Filter criteria to find the specific document to update.
        - updated_data (dict): Data to update in the matched document.

        Returns:
        - dict: A dictionary with an update status message and modified count.
        """

        logger.info("Entered the update_product method of products class")

        try:
            database = self.mongo_operations.get_database(DB_NAME)

            collection = database.get_collection(PRODUCTS_COLLECTION_NAME)

            current_date = datetime.now().strftime("%d_%m_%Y")
            current_time = datetime.now().strftime("%I:%M:%S_%p")

            updated_data["modified_date"] = current_date
            updated_data["modified_time"] = current_time

            newvalues = { "$set": updated_data } 

            result = collection.update_one(data_needs_to_update, newvalues)

            if result.matched_count > 0:
                message = "Product updated successfully" if result.modified_count > 0 else "Product already up to date"
            else:
                message = "No matching product found"

            logger.info(f"New product data updated with the previous data. Previous product data - {data_needs_to_update}. New updated data - {updated_data}")
            logger.info("Exited the update_product method of products class")
            
            return {
                "message": message,
                "matched_count": result.matched_count,
                "modified_count": result.modified_count
            }

        except Exception as e:
            raise BillingException(e, sys) from e
        
    def delete_product(self, product_name: str, product_number: str, company_for: str) -> dict:
        """
        Deletes a product document from MongoDB based on provided filter criteria.

        Parameters:
        - product_name (str): The name of the product to delete.
        - product_number (str): The number of the product to delete.
        - company_for (str): The company associated with the product.

        Returns:
        - dict: A dictionary with deletion status message and deleted count.
        """
 
        logger.info("Entered the delete_product method of products class")

        try:
            database = self.mongo_operations.get_database(DB_NAME)

            collection = database.get_collection(PRODUCTS_COLLECTION_NAME)

            data = {
                "product_name": product_name,
                "product_number": product_number,
                "company_for": company_for
            }

            result = collection.delete_one(data)

            if result.deleted_count > 0:
                message = "Product deleted successfully"
            else:
                message = "No matching product found"

            logger.info(f"Single entry for product deleted from the database. deleted product data - {result}")
            logger.info("Exited the delete_product method of products class")
            
            return {
                "message": message,
                "deleted_count": result.deleted_count
            }

        except Exception as e:
            raise BillingException(e, sys) from e
