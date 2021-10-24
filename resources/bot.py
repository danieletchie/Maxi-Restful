from flask_restful import Resource
from flask_jwt_extended import jwt_required
from flask_restful.reqparse import RequestParser

from models.bot import BotModel
from helper import add_parser_args
from time import time

__platform_parser__ = RequestParser()

add_parser_args(__platform_parser__, "platform_id", int, True, "This field is required")
add_parser_args(__platform_parser__, "strategy", str, True, "This field is required")
add_parser_args(__platform_parser__, "pairs", str, True, "This field can't be blank")
add_parser_args(__platform_parser__, "current_price", str, True, "This field can't be blank")
add_parser_args(__platform_parser__, "first_grid", float, default=0)
add_parser_args(__platform_parser__, "grid_int", float,default=0)
add_parser_args(__platform_parser__, "average_margin", float, default=0)
add_parser_args(__platform_parser__, "current_margin", float, default=0)
add_parser_args(__platform_parser__, "amount", float, True, "This field can't be blank")
add_parser_args(__platform_parser__, "quantity", float, True, "This field can't be blank")
add_parser_args(__platform_parser__, "sell_margin", float, True, "This field can't be blank")
add_parser_args(__platform_parser__, "trades", int, default=0)
add_parser_args(__platform_parser__, "renew", int, default=0)
add_parser_args(__platform_parser__, "status", str, True, "This field can't be blank")
# add_parser_args(__platform_parser__, "passphrase", str)


class NewBot(Resource):
    def post(self):
        data = __platform_parser__.parse_args()
        data["time"] = time()
        bot = BotModel(**data)
        bot.save_to_db()
        return bot.json(), 201

class Bot(Resource):
    def get(self, id):
        bot =  BotModel.find_by_id(id)
        if not bot:
            return {"message": "No Bot exist with this id"},404
        return bot.json()

