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
add_parser_args(__platform_parser__, "amount", float, default=0 )
add_parser_args(__platform_parser__, "quantity", float, default=0)
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
    parser = __platform_parser__.copy()
    parser.remove_argument("platform_id")
    parser.remove_argument("strategy")
    parser.remove_argument("pairs")
    parser.remove_argument("current_price")
    parser.replace_argument("status", required=False)
    parser.remove_argument("renew")
    parser.remove_argument("trades")

    status_parser = RequestParser()
    add_parser_args(status_parser, "status", str, True, "This field can't be blank")

    def get(self, id):
        bot =  BotModel.find_by_id(id)
        if not bot:
            return {"message": "No Bot exist with this id"},404
        return bot.json()
    
    @jwt_required()
    def patch(self, id):
        bot = BotModel.find_by_id(id)
        if not bot:
            return {"message": "Not found"},404
        data = self.status_parser.parse_args()
        bot.status = data["status"]
        bot.save_to_db()
        return {"message": "successfully updated bot"}

    @jwt_required()
    def put(self, id):
        data = self.parser.parse_args()
        bot = BotModel.find_by_id(id)
        if not bot:
            return {"message": "No Bot exist with this id"}, 404
        else:
            bot.first_grid = data["first_grid"]
            bot.grid_int = data["grid_int"]
            bot.average_margin = data["average_margin"]
            bot.current_margin = data["current_margin"]
            bot.amount = data["amount"]
            bot.quantity = data["quantity"]
            bot.sell_margin = data["sell_margin"]
            bot.save_to_db()
            return {"message": "successfully updated bot"}

    @jwt_required()
    def delete(self, id):
        bot = BotModel.find_by_id(id)
        bot.delete_from_db()
        return {"message": "Successfully deleted this bot"}

        

