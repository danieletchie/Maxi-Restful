from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager

from db import db

import os
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

app.config["secret_key"] = os.getenv("secret_key")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True

api = Api(app)

jwt = JWTManager(app)

if __name__ == "__main__":
    db.init_app(app)
    app.run(debug=True)


