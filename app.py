from flask import Flask, request, send_from_directory
from flask_restx import Resource, Api, reqparse
from models import City, Space
from pydantic import ValidationError
from werkzeug.exceptions import NotFound as WerkzeugFileNotFound

# Schema
from schemas.file_resource_schema import getImageSchema

app = Flask(__name__)
app.config['SITE_URL'] = 'http://127.0.0.1:5000/'
api = Api(app, add_specs=False, doc=False)

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
    
class ResourceSpace(Resource):
    def get(self):
        getSpaces = Space.select().limit(5)
        spaces = []
        for item in getSpaces:
            spaceData:Space = item
            photos = []
            for photo in spaceData.photos:
                photoUrl = f"{app.config['SITE_URL']}api/v1/resource?space_id={spaceData.id}&filename={photo.photo}"
                photos.append(photoUrl)

            space = {
                "id": spaceData.id,
                "name": spaceData.name,
                "city": spaceData.city.name,
                "country": spaceData.country.name,
                "price": spaceData.price,
                "thumbnail": f"{app.config['SITE_URL']}api/v1/resource?space_id={spaceData.id}&filename={spaceData.thumbnail}",
                "rating": spaceData.rating,
                "address": spaceData.address,
                "phone": spaceData.phone,
                "map_url": spaceData.mapUrl,
                "number_of_kitchens": spaceData.kitchens,
                "number_of_bedrooms": spaceData.bedrooms,
                "number_of_closets": spaceData.closets,
                "photos":photos
            }
            spaces.append(space)
        dataReturn = setReturn(True, 'Get recommended spaces successfully', spaces)
        return dataReturn, 200

class ResourceImage(Resource):
    def get(self):
        try:
            imageProperty = getImageSchema(**request.args)
        except ValidationError as e:
            return setReturn(False, 'Invalid input', error=e.errors()), 400

        # get file from statics folder
        try:
            return send_from_directory(f'statics/images/{imageProperty.space_id}', imageProperty.filename)
        except WerkzeugFileNotFound:
            return setReturn(False, 'File not found'), 404
        except Exception as e:
            return setReturn(False, 'Internal server error'), 500
    
api.add_resource(ResourceCity, '/api/v1/cities')
api.add_resource(ResourceSpace, '/api/v1/spaces')
api.add_resource(ResourceImage, '/api/v1/resource')

if __name__ == "__main__":
    app.run(debug=True)