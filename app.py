import os
from flask import Flask
from log import logger, setup_logger
from flask_cors import CORS
from healthcheck import HealthCheck
from flask_restx import Api
from controller import register_routes


application = Flask(__name__)


def create_app():    
    setup_logger()
    CORS(application, supports_credentials=True)
    health = HealthCheck()
    application.add_url_rule("/ameristarwrapper/healthcheck", view_func=health.run_check)
    return application


def configure_api(application):
    api = Api(
        application,
        version="0.1",
        title="Ameristar PDF Wrapper",
        description="""This wrapper is used to download the pdf documentation for ameristar websites.""",
    )
    register_routes(api)


application = create_app()
configure_api(application)

if __name__ == "__main__":
    # load_dotenv(dotenv_path=".env.development", verbose=True)
    logger.info("starting the app in dev env")
    application.run(
        host="0.0.0.0",
        port=8080,
        # host=os.getenv("FLASK_HOST"),
        # port=int(os.getenv("FLASK_PORT", 8080)),
        load_dotenv=True,
    )
