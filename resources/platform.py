from os import name
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt
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

    @jwt_required()
    def delete(self, id):
        platform = PlatformModel.find_by_id(id)
        if not platform:
            return {"message": "No platform exist with this id"},404
        platform.delete_from_db()
        return {"message": "Successfully deleted"},200

class PlatformBots(Resource):

    parser = RequestParser()
    add_parser_args(parser, "platform", str, True, "This field is required")

    @jwt_required()
    def get(self):
        my_jwt = get_jwt()
        if my_jwt["is_admin"]:
            data = self.parser.parse_args()
            all_platforms = PlatformModel.find_all_by_name(**data)
            if not all_platforms:
                return {"message": "No platform exist with this name"},404
            platforms = [bot.json() for bot in all_platforms]
            bots = [bot for bots in platforms for bot in bots["bots"] if bot["status"] == 'RUNNING']
            return bots
        return {"message": "Admin Privilage is required"},401
