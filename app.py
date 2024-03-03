from flask import Flask
from flask_restful import Resource, Api, reqparse
from models import City

app = Flask(__name__)
api = Api(app)

def setReturn(success: bool, message: str, data: dict|list|None = None, error: dict|list|None = None):
    return {
        'success': success,
        'message': message,
        'data': data,
        'error': error
    }

class ResourceCity(Resource):
    def get(self):
        cities = list(City.select().dicts())
        dataReturn = setReturn(True, 'Get cities successfully', cities)
        return dataReturn, 200


api.add_resource(ResourceCity, '/api/v1/cities')

if __name__ == "__main__":
    app.run(debug=True)