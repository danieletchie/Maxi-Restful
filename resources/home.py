from flask_restful import Resource

class Home(Resource):
    def get(self):
        return {"message": "This is maxibot restful api version 1"}