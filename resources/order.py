from flask_jwt_extended import jwt_required
from flask_restful import Resource
from flask_restful.reqparse import RequestParser

from models.order import OrderModel
from helper import add_parser_args
from time import time

__order_parser__ = RequestParser()

add_parser_args(__order_parser__, "bot_id", int, True, "This field is required")
add_parser_args(__order_parser__, "pairs", str, True, "This field is required")
add_parser_args(__order_parser__, "order_id", str, True, "This field is required")
add_parser_args(__order_parser__, "side", str, True, "This field can't be blank")
add_parser_args(__order_parser__, "status", str, True, "This field can't be blank")

class NewOrder(Resource):
    def post(self):
        data = __order_parser__.parse_args()
        data["time"] = time()
        order = OrderModel(**data)
        order.save_to_db()
        return order.json(),201

class Order(Resource):
    parser = RequestParser()
    add_parser_args(parser, "status", str, True, "This field is required")

    def get(self, _id):
        order = OrderModel.find_by_id(_id)
        if not order:
            return {"message": "No order exist with this id"},404
        return order.json()

    @jwt_required()
    def put(self, _id):
        order = OrderModel.find_by_id(_id)
        if not order:
            return {"message": "No order found with this id"}, 404
        data = self.parser.parse_args()
        print(data)
        order.status = data["status"]
        order.save_to_db()
        return {"message": "successfully updated this order"}

    @jwt_required()
    def delete(self, _id):
        order = OrderModel.find_by_id(_id)
        if not order:
            return {"message": "order not found"},404
        order.delete_from_db()
        return {"message": "successfully deleted"}