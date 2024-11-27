
from flask import request, json, jsonify
from flask_restx import Api, Resource, Namespace
from flask_accepts import accepts, responds
from model.mapping import MappingRequest, MappingResponse
from model import get_schema
from log import logger


api = Namespace("ameristarwrapper")


@api.route("/map")
class MapResource(Resource):
    @accepts(schema=get_schema(MappingRequest), api=api, use_swagger=False)
    @responds(schema=get_schema(MappingResponse), api=api, use_swagger=False)
    def post(self):
        try:
            logger.info(f"Mapping request: {json.dumps(request.json)}")
            data = request.get_json()

            address = data.get('address')
            city = data.get('city')
            state = data.get('state')
            county = data.get('county')
            owner_name = data.get('ownerName')
            job_id = data.get('jobId')
            order_id = data.get('orderId')

            logger.info(f"Received Data: {data}")

            missing_fields = []
            if not owner_name:
                missing_fields.append("ownerName")
            if not job_id:
                missing_fields.append("jobId")
            if not order_id:
                missing_fields.append("orderId")

            if missing_fields:
                return jsonify({
                    "status": "error",
                    "message": f"Missing required fields: {', '.join(missing_fields)}"
                })

            response = MappingResponse(
                cad="Some CAD Data",
                tax="Some Tax Data",
                jobId=job_id,
                orderId=order_id
            )
            
            return jsonify(response.to_json())
        
        except Exception as e:
            logger.error(f"An error occurred: {str(e)}")
            return jsonify({"status": "error", "message": str(e)})

