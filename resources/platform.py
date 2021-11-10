from flask_restful import Resource
from flask_jwt_extended import jwt_required
from flask_restful.reqparse import RequestParser

from models.platform import PlatformModel
from helper import add_parser_args

__platform_parser__ = RequestParser()

add_parser_args(__platform_parser__, "name", str, True, "This field is required")
add_parser_args(__platform_parser__, "user_id", int, True, "This field is required")
add_parser_args(__platform_parser__, "api_key", str, True, "This field can't be blank")
add_parser_args(__platform_parser__, "secret_key", str, True, "This field can't be blank")
add_parser_args(__platform_parser__, "passphrase", str)


class NewPlatform(Resource):
    @jwt_required()
    def post(self):
        data = __platform_parser__.parse_args()
        if PlatformModel.find_by_name_user_id(data["name"], data["user_id"]):
            return {"message": "The user is already on this platform"},400
        elif PlatformModel.find_by_api_key(data["api_key"]):
            return {"message": "This api key is already associated with an account"},401
        platform = PlatformModel(**data)
        platform.save_to_db()
        return platform.json(), 201

class Platform(Resource):
    @jwt_required()
    def get(self, id):
        platform = PlatformModel.find_by_id(id)
        if not platform:
            return {"message": "No platform exist with this id"},404
        return platform.json()

