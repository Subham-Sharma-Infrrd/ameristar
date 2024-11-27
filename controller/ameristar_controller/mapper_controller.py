
from flask import request, json, jsonify
from flask_restx import Api, Resource, Namespace
from flask_accepts import accepts, responds
import usaddress
from model.mapping import MappingRequest, MappingResponse
from model import get_schema
from log import logger
from service.web_scrapping.web_scrapper import WebScraper


api = Namespace("ameristarwrapper")


@api.route("/map")
class MapResource(Resource):
    @accepts(schema=get_schema(MappingRequest), api=api, use_swagger=False)
    @responds(schema=get_schema(MappingResponse), api=api, use_swagger=False)
    def post(self):
        try:
            mapping_request: MappingRequest = request.parsed_obj
            scraper = WebScraper()
            logger.info(f"Mapping request: {json.dumps(request.json)}")
            data = request.get_json()

            adrress_dict = usaddress.parse(mapping_request.address)
            if not adrress_dict.get("street"):

            logger.info(f"Received Data: {data}")

            missing_fields = []
            if not mapping_request.owner_name:
                missing_fields.append("ownerName")
            if not mapping_request.job_id:
                missing_fields.append("jobId")
            if not mapping_request.order_id:
                missing_fields.append("orderId")

            if missing_fields:
                return jsonify({
                    "status": "error",
                    "message": f"Missing required fields: {', '.join(missing_fields)}"
                })
            # TODO : Add logics to seprate street values
            street_number = adrress_dict["AddressNumber"]
            # TODO : Add logics to seprate street values
            street_name = "" #" ".join([])

            web_page_config = scraper.navigate_to_website(mapping_request.state, mapping_request.county)
            status = scraper.perform_search(web_page_config, street_number, street_name, mapping_request.owner_name)
            if status:
                scraper.download_or_screenshot(web_page_config["xpaths"])
                print("SUCCESSFULLY_SCRAPPED")
                response = MappingResponse(
                    cad="Some CAD Data",
                    tax="Some Tax Data",
                    jobId=mapping_request.job_id,
                    orderId=mapping_request.order_id
                )
            else:
                print("SCRAPPING_FAILED")
                response = {
                    "status": "error",
                    "message": "Scraping failed"
                }
            
            
            return jsonify(response.to_json())
        
        except Exception as e:
            logger.error(f"An error occurred: {str(e)}")
            return jsonify({"status": "error", "message": str(e)})

        finally:
            scraper.close()

