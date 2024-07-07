#!/usr/bin/env python3

from flask import Flask, make_response, request
from flask_migrate import Migrate
from flask_restful import Api, Resource
from models import db, Plant

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = True

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

class Plants(Resource):
    def get(self):
        response_dict_list = [plant.to_dict() for plant in Plant.query.all()]
        return make_response(response_dict_list, 200)

    def post(self):
        try:
            data = request.get_json()
            name = data.get('name')
            image = data.get('image')
            price = data.get('price')

            if not name or not image or not price:
                return make_response({"error": "Missing data"}, 400)

            new_record = Plant(name=name, image=image, price=float(price))
            db.session.add(new_record)
            db.session.commit()

            response_dict = new_record.to_dict()
            return make_response(response_dict, 201)
        except Exception as e:
            db.session.rollback()
            return make_response({"error": str(e)}, 500)

api.add_resource(Plants, '/plants')

class PlantByID(Resource):
    def get(self, id):
        plant = Plant.query.get(id)
        if plant is None:
            return make_response({"error": "Plant not found"}, 404)

        response_dict = plant.to_dict()
        return make_response(response_dict, 200)

api.add_resource(PlantByID, '/plants/<int:id>')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
