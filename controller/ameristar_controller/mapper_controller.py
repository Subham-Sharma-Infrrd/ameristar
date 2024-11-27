
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
            owner_name = data.get('owner_name')
            job_id = data.get('job_id')
            order_id = data.get('order_id')

            print(f"Received Data: {data}")

            response = MappingResponse(
                cad="Some CAD Data",
                tax="Some Tax Data",
                job_id=job_id,
                order_id=order_id
            )

            return jsonify(response.to_json()), 200

        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 400

