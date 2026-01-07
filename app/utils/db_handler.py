from pymongo import AsyncMongoClient

from .logging_handler import CustomLogger
from .singleton_handler import SingletonClass

logger = CustomLogger.get_logger(__name__)


class DBHandler(metaclass=SingletonClass):
    def __init__(self, conn_string: str = "", database_name: str = ""):
        self.conn_string = conn_string
        self.database_name = database_name
        self.connection = AsyncMongoClient(host=self.conn_string)
        self.client = self.connection[self.database_name]

    async def insertDocs(self, collection_name: str = None, data: list[dict] = []):
        """
        insert docs into the collection
        """
        try:
            logger.info(f"started inserting data into {collection_name}")

            async with await self.client.start_session() as session:
                async with session.start_transaction():
                    collection = self.client[collection_name]
                    result = await collection.insert_many(
                        documents=data, session=session, ordered=True
                    )

            return result.inserted_ids

        except Exception as exe:
            logger.error(f"error while inserting data: {exe}", exc_info=True)
            raise exe

    async def updateDocs(
        self,
        collection_name: str = None,
        query: dict = {},
        new_values: dict = {},
    ):
        try:
            logger.info(f"started updating data into {collection_name}")
            async with await self.client.start_session() as session:
                async with session.start_transaction():
                    collection = self.client[collection_name]
                    result = await collection.update_many(
                        query, {"$set": new_values}, session=session
                    )
            logger.info(
                f"updated documents in {collection_name} \
                with query: {query} to new values: {new_values}"
            )
            return result.modified_count

        except Exception as exec:
            logger.error(f"error while updating data: {exec}", exc_info=True)
            raise exec

    async def readDocs(self, collection_name: str = None, query: dict = {}):
        """
        read docs from the collection based on query
        """
        try:
            logger.info(f"reading documents from {collection_name} with query: {query}")
            async with await self.client.start_session() as session:
                async with session.start_transaction():
                    collection = self.client[collection_name]
                    result = await collection.find(query).to_list(length=None)
            return result

        except Exception as exec:
            logger.error(f"error while reading data: {exec}", exc_info=True)
            raise exec

    async def deleteDocs(self, collection_name: str = None, query: dict = None):
        """
        delete docs from the collection based on query
        """
        try:
            logger.critical(
                f"deleting documents from {collection_name} \
                with query: {query}"
            )

            async with await self.client.start_session() as session:
                async with session.start_transaction():
                    collection = self.client[collection_name]
                    result = await collection.delete_many(query, session=session)

            return result.deleted_count

        except Exception as exec:
            logger.error(f"error while deleting data: {exec}", exc_info=True)
            raise exec

    def closeConnection(self):
        try:
            self.connection.close()
            logger.info("Database connection closed successfully.")

        except Exception as exec:
            logger.error(f"error while closing connection: {exec}", exc_info=True)
            raise exec
