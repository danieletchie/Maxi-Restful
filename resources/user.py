from flask_restful import Resource
from flask_restful.reqparse import RequestParser
from flask_jwt_extended import jwt_required, create_access_token, create_refresh_token, get_jwt_identity

from passlib.hash import sha256_crypt
from models.user import UserModel
from helper import add_parser_args

__userparser__ = RequestParser()

add_parser_args(__userparser__, "name", str, True, "This field cannot be blank")
add_parser_args(__userparser__, "email", str, True, "This field cannot be blank")
add_parser_args(__userparser__, "phone", int, True, "This field cannot be blank")
add_parser_args(__userparser__, "password", str, True, "This field cannot be blank")
add_parser_args(__userparser__, "status", str, True, "This field cannot be blank")


class UserRegister(Resource):

    def post(self):
        data = __userparser__.parse_args()
        if UserModel.find_by_email(data["email"]):
            return {"message": "email already exist proceed to login or use another email"}, 400

        user = UserModel(**data)
        user.password = sha256_crypt.hash(user.password)
        try:
            user.save_to_db()
        except Exception as e:
            print(e)
        return user.json(), 201

class User(Resource):
    @jwt_required()
    def get(self, _id):
        user = UserModel.find_by_id(_id)
        if not user:
            return {"message": "No user exist with this id {}".format(_id)},404
        return user.json()

class UserLogin(Resource):
    parser = __userparser__.copy()
    parser.remove_argument("name")
    parser.remove_argument("phone")
    parser.remove_argument("status")

    def post(self):
        data = self.parser.parse_args()
        user = UserModel.find_by_email(data["email"])
        if not user:
            return {"message": "No user found with this email kindly register"}, 404
        if sha256_crypt.verify(data["password"], user.password):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(identity=user.id)
            return {"id": user.id, "access_token": access_token, "refresh_token": refresh_token}
        return {"message": "Invalid credentials please check password"},401


class TokenRefresh(Resource):
    @jwt_required(refresh=True)
    def post(self):
        identity = get_jwt_identity()
        access_token = create_access_token(identity=identity, fresh=False)
        return {"access_token": access_token}