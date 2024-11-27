from flask_restx import Api
from controller.ameristar_controller import mapper_controller as ameristar_mc


def register_routes(api: Api):
  api.add_namespace(ameristar_mc.api)
