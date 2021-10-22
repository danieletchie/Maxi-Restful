from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager

import os
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

app.config["secret_key"] = os.getenv("secret_key")

api = Api(app)

jwt = JWTManager(app)


