import json
from typing import List

from pymongo.errors import PyMongoError

from model import get_schema
from mongodb.dbo.ntp_rules import ConfidenceRule, Rule
from mongodb.mongo_template import MongoTemplate, titan_database

from config import Config
from error import AppError
from log import logger

ntp_rules_collection = MongoTemplate.get_collection(
    titan_database, Config.NTP_RULES_COLLECTION
)


def retrieve_field_rules(
    field_id_list, user_model_id: str = None
) -> List[ConfidenceRule]:
    field_rules = []
    try:
        logger.info("Getting the field_rules entry for all fields")

        conditions_with_document = {
            "fieldId": {"$in": field_id_list},
            "userModelId": user_model_id,
            "isActive": True,
        }
        conditions_without_document = {
            "fieldId": {"$in": field_id_list},
            "userModelId": "",
            "isActive": True,
        }

        pipeline = [
            {"$match": conditions_with_document},
            {"$sort": {"version": -1}},
            {"$group": {"_id": "$fieldId", "record": {"$first": "$$ROOT"}}},
            {
                "$project": {
                    "_id": "$record._id",
                    "fieldId": "$record.fieldId",
                    "userModelId": "$record.userModelId",
                    "fieldName": "$record.fieldName",
                    "isActive": "$record.isActive",
                    "isCustom": "$record.isCustom",
                    "version": "$record.version",
                    "rules": "$record.rules",
                }
            },
        ]

        rules_with_user_model_id = list(ntp_rules_collection.aggregate(pipeline))

        # To remove field Ids having rules with usermodelid
        for result in rules_with_user_model_id:
            field_id_list.remove(result["fieldId"])

        pipeline[0]["$match"] = conditions_without_document

        rules_without_user_model_id = list(ntp_rules_collection.aggregate(pipeline))

        field_rules_list = rules_with_user_model_id + rules_without_user_model_id

        for field in field_rules_list:
            rule_schema = get_schema(Rule)()
            for rule in field["rules"]:
                rule: Rule = rule_schema.loads(json.dumps(rule))
            schema = get_schema(ConfidenceRule)()
            field_rule: ConfidenceRule = schema.loads(json.dumps(field))
            field_rules.append(field_rule)

    except PyMongoError as e:
        logger.exception(
            "Mongo exception occurred in retrieve_field_rules. Error is %s", e
        )
        raise AppError("MONGODB_EXCEPTION_OCCURRED")

    return field_rules
