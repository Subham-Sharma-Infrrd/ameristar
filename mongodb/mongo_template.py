"""
Mongo Template definition
"""

from dataclasses import dataclass

from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.errors import ConnectionFailure

from config import config
from error import AppError
from log import logger

NAMED_CONCERN_DICT = {"w1": 1, "w2": 2, "w3": 3, "majority": "majority"}


@dataclass
class MongoTemplate:
    # @staticmethod
    # def create_mongo_client() -> MongoClient:
    #     try:
    #         return MongoClient(
    #                         username=config.MONGODB_USERNAME, password=config.MONGODB_PASSWORD,
    #                         authSource=config.MONGODB_AUTH_SOURCE,
    #                         replicaSet=config.MONGODB_REPLICA_SET,
    #                         directConnection=True,
    #                         # maxPoolSize=config.MONGODB_CONNECTION_POOL_MAX_SIZE,
    #                         # minPoolSize=config.MONGODB_CONNECTION_POOL_MIN_SIZE,
    #                         # maxIdleTimeMS=config.MONGODB_MAX_CONNECTION_IDLE_TIME_MS,
    #                         # connectTimeoutMS=config.MONGODB_CONNECT_TIMEOUT_MS,
    #                         readPreference=config.MONGODB_READ_PREFERENCE, tls=config.MONGODB_SCHEME,
    #                         w=NAMED_CONCERN_DICT[config.MONGODB_WRITE_CONCERN_NAME]
    #                         if config.MONGODB_WRITE_CONCERN_NAME in NAMED_CONCERN_DICT.keys() else 1)

    #     except ConnectionFailure:
    #         logger().error(f"ERROR! Connecting to Mongo DB Failed !!")
    #         raise AppError(f"Connecting to Mongo DB Failed !!")

    @staticmethod
    def create_mongo_client() -> MongoClient:
        try:
            return MongoClient(
                host=config.MONGODB_CONNECT,
                username=config.MONGODB_USERNAME,
                password=config.MONGODB_PASSWORD,
                authSource=config.MONGODB_AUTH_SOURCE,
                replicaSet=config.MONGODB_REPLICA_SET,
                directConnection=True,
                # maxPoolSize=config.MONGODB_CONNECTION_POOL_MAX_SIZE,
                # minPoolSize=config.MONGODB_CONNECTION_POOL_MIN_SIZE,
                # maxIdleTimeMS=config.MONGODB_MAX_CONNECTION_IDLE_TIME_MS,
                # connectTimeoutMS=config.MONGODB_CONNECT_TIMEOUT_MS,
                readPreference=config.MONGODB_READ_PREFERENCE,
                tls=config.MONGODB_SCHEME,
                w=NAMED_CONCERN_DICT[config.MONGODB_WRITE_CONCERN_NAME]
                if config.MONGODB_WRITE_CONCERN_NAME in NAMED_CONCERN_DICT.keys()
                else 1,
            )

        except ConnectionFailure:
            logger().error(f"ERROR! Connecting to Mongo DB Failed !!")
            raise AppError(f"Connecting to Mongo DB Failed !!")

    @staticmethod
    def get_database(client: MongoClient):
        if MongoTemplate.check_db_existence(config.MONGODB_DB_NAME, client):
            return client.get_database(config.MONGODB_DB_NAME)
        raise AppError(message=f"No database found by name {config.MONGODB_DB_NAME}")

    @staticmethod
    def get_collection(database, collection_name) -> Collection:
        if MongoTemplate.check_collection_existence(collection_name, database):
            return database[collection_name]
        raise AppError(message=f"No collection found by name {collection_name}")

    @staticmethod
    def check_db_existence(db_name, client):
        list_of_dbs = client.list_database_names()
        if db_name in list_of_dbs:
            return True
        return False

    @staticmethod
    def check_collection_existence(collection, database):
        collection_list = database.list_collection_names()
        if collection in collection_list:
            return True
        return False


mongo_client = MongoTemplate.create_mongo_client()
titan_database = MongoTemplate.get_database(mongo_client)
