
from flask import request, json, jsonify
from flask_restx import Api, Resource, Namespace
from flask_accepts import accepts, responds
import usaddress
from model.mapping import MappingRequest, MappingResponse, WebScrappingDocType
from model import get_schema
from log import logger
from service.web_scrapping.web_scrapper import WebScraper
from utils.common_utils import generate_unique_id
from utils.web_scrapping_utils import (
    get_url_for_tax_docs, 
    update_account_number_format,
    update_tax_url_with_tax_number
)

api = Namespace("ameristarwrapper")


@api.route("/map")
class MapResource(Resource):
    @accepts(schema=get_schema(MappingRequest), api=api, use_swagger=False)
    @responds(schema=get_schema(MappingResponse), api=api, use_swagger=False)
    def post(self):
        try:
            unique_id = generate_unique_id()
            mapping_request: MappingRequest = request.parsed_obj
            scraper = WebScraper()
            logger.info(f"Mapping request: {json.dumps(request.json)}")
            data = request.get_json()
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
            
            cad_web_page_config = scraper.get_cad_configs(mapping_request.state, mapping_request.county)
            account_number_status = scraper.cad_perform_search(cad_web_page_config, mapping_request.street_number, mapping_request.street_address, mapping_request.owner_name)
            account_number_status = 1000021
            if account_number_status:
                # TODO: Add logic to download the Tax document and CAD document
                # downloading CAD document
                cad_pdf_path = scraper.download_or_screenshot(cad_web_page_config["xpaths"], doc_type=WebScrappingDocType.CAD.value)
                tax_web_page_config = scraper.get_tax_configs(mapping_request.state, mapping_request.county)

                base_url = get_url_for_tax_docs(mapping_request.state, mapping_request.county, tax_web_page_config)
                updated_account_number_format = update_account_number_format(mapping_request.state, mapping_request.county, account_number_status)
                complete_tax_url = update_tax_url_with_tax_number(base_url, updated_account_number_format)
                ### Calling TAX function to check for TAX related keywords and have a print for it.
                tax_pdf_path = scraper.process_tax_page(tax_web_page_config, complete_tax_url)
                # scraper.tax_page_expand_web_page(tax_web_page_config, link_to_page = complete_tax_url)
                
                logger.info("SUCCESSFULLY_SCRAPPED")
                response = MappingResponse(
                    cad="abc",
                    tax=tax_pdf_path,
                    job_id=mapping_request.job_id,
                    order_id=mapping_request.order_id,
                    account_number=account_number_status,
                    unique_id=unique_id
                )
            else:
                logger.info("SCRAPPING_FAILED")
                response = {
                    "status": "error",
                    "message": "Scraping failed"
                }
            
            
            return jsonify(response)
        
        except Exception as e:
            logger.error(f"An error occurred: {str(e)}")
            return jsonify({"status": "error", "message": str(e)})

        finally:
            scraper.close()

