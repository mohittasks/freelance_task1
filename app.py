# -*- coding: utf-8 -*-
"""
Created on Sat Mar 27 21:31:53 2021

@author: Admin
"""
from flask import Flask, request, jsonify, make_response
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import datetime
from json import JSONEncoder
import decimal 
import sys
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:supermohit@localhost:5432/postgres"
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class CustomJSONEncoder(JSONEncoder):
  def default(self, obj):
        if isinstance(obj, (datetime.datetime, datetime.date, datetime.time)):
            return obj.isoformat()
        elif isinstance(obj, datetime.timedelta):
            return (datetime.datetime.min + obj).time().isoformat()
        elif isinstance(obj, decimal.Decimal):
            return str(obj)
        return super(CustomJSONEncoder, self).default(obj)
    
app.json_encoder = CustomJSONEncoder

class Cars(db.Model):
    __tablename__ = 'cars'

    id = db.Column(db.Text(), primary_key=True)
    active = db.Column(db.Text())
    year = db.Column(db.Text())
    mileage = db.Column(db.Numeric())		
    price = db.Column(db.Numeric())	
    make_id = db.Column(db.Text())
    model_id = db.Column(db.Text())
    submodel_id = db.Column(db.Text())
    body_type = db.Column(db.Text())
    transmission = db.Column(db.Text())	
    fuel_type = db.Column(db.Text())
    exterior_color = db.Column(db.Text())
    created_at = db.Column(db.DateTime())
    updated_at = db.Column(db.DateTime())

    def __init__(self, id, active, year, mileage, price, make_id, model_id, submodel_id, body_type, transmission,	fuel_type, exterior_color, created_at, updated_at):
        self.id = id
        self.active	= active
        self.year = year
        self.mileage = mileage
        self.price = price
        self.make_id = make_id
        self.model_id = model_id
        self.submodel_id = submodel_id
        self.body_type = body_type
        self.transmission = transmission
        self.fuel_type = fuel_type	
        self.exterior_color	= exterior_color
        self.created_at	= created_at
        self.updated_at = updated_at

    def __repr__(self):
        return f"<Car {self.id}>"
    
class Models(db.Model):
    __tablename__ = 'models'
    
    index = db.Column(db.BigInteger(), primary_key=True)
    id = db.Column(db.Text())
    name = db.Column(db.Text())
    active = db.Column(db.Text())	
    make_id = db.Column(db.Text())
    created_at = db.Column(db.DateTime())
    updated_at = db.Column(db.DateTime())

    def __init__(self, index, id, name, active, make_id, created_at, updated_at):
        self.index = index
        self.id = id
        self.active	= active
        self.name = name       
        self.make_id = make_id
        self.created_at	= created_at
        self.updated_at = updated_at

    def __repr__(self):
        return f"<Model {self.id}>"
    
class Makes(db.Model):
    __tablename__ = 'makes'

    index = db.Column(db.BigInteger(), primary_key=True)
    id = db.Column(db.Text())
    name = db.Column(db.Text())
    active = db.Column(db.Text())
    created_at = db.Column(db.DateTime())
    updated_at = db.Column(db.DateTime())

    def __init__(self, index, id, name, active, created_at, updated_at):
        self.index = index
        self.id = id
        self.active	= active
        self.name = name  
        self.created_at	= created_at
        self.updated_at = updated_at

    def __repr__(self):
        return f"<Make {self.id}>"
    
class Submodels(db.Model):
    __tablename__ = 'submodels'
    
    index = db.Column(db.BigInteger(), primary_key=True)
    id = db.Column(db.Text())
    name = db.Column(db.Text())
    active = db.Column(db.Text())
    model_id = db.Column(db.Text())
    created_at = db.Column(db.DateTime())
    updated_at = db.Column(db.DateTime())

    def __init__(self, index, id, name, active, model_id, created_at, updated_at):
        self.index = index
        self.id = id
        self.name = name  
        self.active	= active
        self.model_id = model_id
        self.created_at	= created_at
        self.updated_at = updated_at

    def __repr__(self):
        return f"<Submodel {self.id}>"
    
table_models_map = {
        'cars': Cars,
        'models': Models,
        'makes': Makes,
        'submodels': Submodels
    }

table_ids_map = {
        'models': 'model_id',
        'makes': 'make_id',
        'submodels': 'submodel_id'
    }

@app.route('/cars', methods=['POST'])
def add_cars():
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            try: 
                new_car = Cars(
                    id=data.get('id'),
                    active=data.get('active'),
                    year=data.get('year'),
                    mileage = data.get('mileage'),	
                    price = data.get('price'),	
                    make_id = data.get('make_id'),
                    model_id = data.get('model_id'),
                    submodel_id = data.get('submodel_id'),
                    body_type = data.get('body_type'),
                    transmission = data.get('transmission'),
                    fuel_type = data.get('fuel_type'),
                    exterior_color = data.get('exterior_color'),
                    created_at = datetime.datetime.now(),
                    updated_at = datetime.datetime.now()
                    )
                db.session.add(new_car)
                db.session.commit()
                return make_response(jsonify({"message": f"car {new_car.id} has been created successfully."}), 200)
            except Exception as e:
            exc_type, _, exc_tb = sys.exc_info()
            error = {
                "exc_type": str(exc_type),
                "error": str(e),
                "line number": exc_tb.tb_lineno
                }
            return make_response(jsonify({"error": error}), 401)
        else:
            return make_response(jsonify({"error": "The request payload is not in JSON format."}), 401)

    
@app.route('/full-list', methods=['GET'])
def display_full_list():
    if request.method == 'GET':
        table = request.args.get('table')
        try:
            resultproxy = table_models_map[table].query.all()
            results = []
            for row in resultproxy:
                row = row.__dict__
                row.pop('_sa_instance_state', None)
                results.append(row)
            return make_response(jsonify({"count": len(results), "results": results}), 200)
        except Exception as e:
            exc_type, _, exc_tb = sys.exc_info()
            error = {
                "exc_type": str(exc_type),
                "error": str(e),
                "line number": exc_tb.tb_lineno
                }
            return make_response(jsonify({"error": error}), 401)
    
@app.route('/query-by-name', methods=['GET'])
def query_by_name():
    if request.method == 'GET':
        data = request.get_json()
        table = data.get("table")           
        name = data.get("name")
        try:
            table_matches = table_models_map[table].query.filter_by(name=name).all()
            ids = [x.__dict__['id'] for x in table_matches]
            list_of_cars_queried = []
            for id in ids:
                filter = {table_ids_map[table]: id}
                subset_of_cars_queried = Cars.query.filter_by(**filter).all()
                for row in subset_of_cars_queried:
                    row = row.__dict__
                    row.pop('_sa_instance_state', None)
                    list_of_cars_queried.append(row)
            return make_response(jsonify({"car_name_queried": name, "results": list_of_cars_queried}), 200)
        except Exception as e:
            exc_type, _, exc_tb = sys.exc_info()
            error = {
                "exc_type": str(exc_type),
                "error": str(e),
                "line number": exc_tb.tb_lineno
                }
            return make_response(jsonify({"error": error}), 401)

@app.route('/query-by-price-mileage', methods=['GET'])
def query_by_price_mileage():
    if request.method == 'GET':
        data = request.get_json()
        price = data.get("price")          
        mileage = data.get("mileage")
        try:
            if price and mileage:
                car_table_matches = Cars.query.filter_by(price=price, mileage=mileage).all()
            elif price:
                car_table_matches = Cars.query.filter_by(price=price).all()
            elif mileage:
                car_table_matches = Cars.query.filter_by(mileage=mileage).all()
            result_dict = {}
            for row in car_table_matches:
                car_table_match = row.__dict__
                car_table_match.pop('_sa_instance_state', None)
                car_table_match['make_name'] = db.session.query(Makes.name).filter_by(id=car_table_match['make_id']).first()[0]
                car_table_match['model_name'] = db.session.query(Models.name).filter_by(id=car_table_match['model_id']).first()[0]
                car_table_match['submodel_name'] = db.session.query(Submodels.name).filter_by(id=car_table_match['submodel_id']).first()[0]
                result_dict[car_table_match["updated_at"]] = car_table_match
            results = [result_dict[key] for key in sorted(result_dict.keys(), reverse=True)]
            return make_response(jsonify({"count": len(results), "results": results}), 200)
        except Exception as e:
            exc_type, _, exc_tb = sys.exc_info()
            error = {
                "exc_type": str(exc_type),
                "error": str(e),
                "line number": exc_tb.tb_lineno
                }
            return make_response(jsonify({"error": error}), 401)

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)