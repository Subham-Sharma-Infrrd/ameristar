"""
User Model Collection DB Queries
"""

from typing import Optional

from pymongo.errors import PyMongoError

from mongodb.dbo.user_model import UserModel
from mongodb.mongo_operations import find_document
from mongodb.mongo_template import MongoTemplate, titan_database

from config import config
from error import AppError
from log import logger

document_collection = MongoTemplate.get_collection(
    titan_database, config.DOCUMENT_COLLECTION
)


def get_document_by_id(document_id: str) -> Optional[UserModel]:
    """
    Retrieves document using id from document collection
    :param document_id: document  id
    :return: UserModel if entry found in DB None otherwise
    """
    try:
        logger.info("Getting the document entry for user model id: %s", document_id)
        search_query = {"_id": document_id}

        projection = {"_id": 1, "docTypeHierarchy": 1, "taggedDocTypeHierarchy": 1}
        document_entry = find_document(
            collection=document_collection, query=search_query, projection=projection
        )
        return document_entry

    except PyMongoError as e:
        logger.exception(
            "Mongo exception occurred in get_user_model_by_id. Error is %s", e
        )
        raise AppError("MONGODB_EXCEPTION_OCCURRED")
