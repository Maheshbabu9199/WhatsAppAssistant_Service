from .logging_handler import CustomLogger
from .singleton_handler import SingletonClass
from pymongo import AsyncMongoClient

logging = CustomLogger.get_logger(__name__)

class DBHandler(metaclass=SingletonClass):

    def __init__(self, conn_string:str="", database_name:str=""):
        self.conn_string = conn_string
        self.database_name = database_name
        self.connection = AsyncMongoClient(host=self.conn_string)
        self.client = self.connection[self.database_name]

            
    async def insertDocs(self, collection_name:str=None, data:list[dict] = {}):
        try:
            logging.info(f"started inserting data into {collection_name}")
            collection = self.client[collection_name]
            result = await collection.insert_many(data)
            return result.inserted_ids
        
        except Exception as exe:
            logging.error(f"error while inserting data: {exe}", exc_info=True)
            raise exe
        

    async def updateDocs(self, collection_name:str=None, query:dict={}, new_values:dict={}):
        try:
            logging.info(f"started updating data into {collection_name}")
            collection = self.client[collection_name]
            logging.info(f"updating documents in {collection_name} with query: {query} to new values: {new_values}")
            result = await collection.update_many(query, {'$set': new_values})
            return result.modified_count

        except Exception as exec:
            logging.error(f"error while updating data: {exec}", exc_info=True)
            raise exec


    
    async def readDocs(self, collection_name:str=None, query:dict={}):
        try:
            collection = self.client[collection_name]
            logging.info(f"reading documents from {collection_name} with query: {query}")
            result = await collection.find(query).to_list(length=None)
            return result

        except Exception as exec:
            raise exec


    async def deleteDocs(self, collection_name:str=None, query:dict=None):
        try:
            collection = self.client[collection_name]
            logging.critical(f"deleting documents from {collection_name} with query: {query}")
            result = await collection.delete_many(query)
            return result.deleted_count

        except Exception as exec:
            raise exec


    def closeConnection(self):
        try:
            self.connection.close()
            logging.info("Database connection closed successfully.")

        except Exception as exec:
            raise exec
        
