from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager

from db import db
from resources.user import User, UserLogin, UserRegister
from resources.platform import NewPlatform, Platform
from resources.bot import NewBot, Bot
from resources.order import NewOrder, Order
from resources.home import Home

import os
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///data.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True

api = Api(app)

jwt = JWTManager(app)

@app.before_first_request
def create_tables():
    db.create_all()


api.add_resource(Home, "/")
api.add_resource(UserRegister, "/register")
api.add_resource(UserLogin, "/login")
api.add_resource(User, "/user/<int:_id>")
api.add_resource(NewPlatform, "/new_platform")
api.add_resource(Platform, "/platform/<int:id>")
api.add_resource(NewBot, "/new_bot")
api.add_resource(Bot, "/bot/<int:id>")
api.add_resource(NewOrder, "/new_order")
api.add_resource(Order, "/order/<int:_id>")

db.init_app(app)
if __name__ == "__main__":
    app.run()


