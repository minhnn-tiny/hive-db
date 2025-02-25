import falcon
from falcon_cors import CORS
from logbook import Logger
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from falcon_apispec import FalconPlugin
from marshmallow import Schema, fields

from .middleware.permissions import APIPermission
from .conf import settings
from .hive_db.views.accounts import TestResourceView, AccountView


logger = Logger(__name__)


class TestSchema(Schema):
    q = fields.Str()

class Accountchema(Schema):
    author = fields.Str()
    body = fields.Str()
    url = fields.Str()
    permlink = fields.Str()
    post_id = fields.Str()


def create_app():
    cors = CORS(allow_origins_list=settings.ALLOWED_HOSTS)
    middlewares = [cors.middleware, APIPermission()]
    app = falcon.App(middleware=middlewares)
    test_resource = TestResourceView()
    account_resource = AccountView()
    app.add_route(f"/{settings.PREFIX}/test", test_resource)
    app.add_route(f"/{settings.PREFIX}/accounts", account_resource)
    # Create an APISpec
    # spec = APISpec(
    #     title='Swagger Petstore',
    #     version='1.0.0',
    #     openapi_version='2.0',
    #     plugins=[
    #         FalconPlugin(app),
    #         MarshmallowPlugin(),
    #     ],
    # )
    # # Register entities and paths
    # spec.components.schema('Test', schema=TestSchema)
    # # spec.components.schema('Account', schema=Accountchema)
    # # pass created resource into `path` for APISpec
    # spec.path(resource=test_resource)
    # print(spec.to_dict())
    return app


app = application = create_app()
