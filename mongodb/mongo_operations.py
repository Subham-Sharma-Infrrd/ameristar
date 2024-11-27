"""
Holds all the methods required for the mongo operations
"""

from typing import Dict, List

# from core_db_encryption import encrypt, encrypt_wrapper, decrypt_wrapper
from pymongo.collection import Collection


# @decrypt_wrapper
def find_document(
    collection: Collection,
    query: Dict,
    projection=None,
    multiple=False,
    sort_by=None,
    order_by=None,
    size=0,
    *args,
    **kwargs
):
    """
    Retrieves single or multiple documents from a provided collection using a dictionary
    containing of the document elements
    """

    # checking if multiple documents are to be fetched from DB
    if multiple:
        # checking if the documents fetched are to be sorted or ordered
        if sort_by and order_by:
            # sorting the documents fetched from DB
            results = (
                collection.find(filter=query, projection=projection)
                .sort(sort_by, order_by)
                .limit(size)
            )
        else:
            results = collection.find(query, projection).limit(size)

        # returning the list of results
        return [r for r in results]

    else:
        return collection.find_one(filter=query, projection=projection)


# @encrypt_wrapper
def insert_many_document(collection: Collection, data: List[Dict], *args, **kwargs):
    """ Function to insert many document into a collection
    """
    # return collection.insert_many(data)
    pass


# @encrypt_wrapper
def insert_document(collection: Collection, data: Dict, *args, **kwargs):
    """Function to insert a document into a collection and return the document's id."""
    # return collection.insert_one(data)
    pass


def update_document(collection: Collection, new_values: Dict, query_elements: Dict, **kwargs):
    """ Function to update a single document in a collection.
    """
    # if kwargs.get("account_id") or kwargs.get("user_model_id"):
    #     account_id = kwargs.get("account_id")
    #     user_model_id = kwargs.get("user_model_id")
    #     secure_fields_cls = kwargs.get("secure_fields_cls")
    #     new_values = encrypt(
    #         new_values,
    #         collection.name,
    #         account_id,
    #         secure_fields_cls=secure_fields_cls,
    #         user_model_id=user_model_id
    #     )

    # return collection.update_one(query_elements, {'$set': new_values})
    pass


def update_many_document(collection: Collection, new_values: Dict, query_elements: Dict, **kwargs):
    """ Function to update a multiple document in a collection.
    """
    # if kwargs.get("account_id") or kwargs.get("user_model_id"):
    #     account_id = kwargs.get("account_id")
    #     user_model_id = kwargs.get("user_model_id")
    #     secure_fields_cls = kwargs.get("secure_fields_cls")
    #     new_values = encrypt(
    #         new_values,
    #         collection.name,
    #         account_id,
    #         secure_fields_cls=secure_fields_cls,
    #         user_model_id=user_model_id
    #     )

    # return collection.update_many(query_elements, {'$set': new_values})
    pass
