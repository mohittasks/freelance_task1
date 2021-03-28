## Assignment instructions

You are given some CSV files of cars for sale and the connected car configurations data (make, models and submodels).
A car has a make,
a make has many models, and
a model has many submodels.


1) Unpack the files and have a look around.
2) Using a database of your choice, insert the data into a schema design, that you think makes sense - you are expected to make some reasonable assumptions about the underlying data model
3) Build an API using Python3 with endpoints that return JSON responses - the endpoints should include the following:
   - List all makes, models, and submodels
   - List all cars with their matching make, model and submodel names
   - Add new cars and enforce consistency of the inserted data directly in the database
   - Query cars within a certain price and mileage and return a list of matches sorted by `updated_at` (where the newest element is first)
     - Include the car names here as well
     - Make sure to validate user input and provide meaningful responses when input is wrong.
4) Unit test each of your endpoints to verify your implementation

## Setting up

1) Install psql, flask, psycopg2, sqlalchemy, flask_migrate
2) Use data_load.ipynb to load data into the dB (change paths and db connection)
After these steps we can simply run app.py (change db connection)


## API structures

1) To add new cars:
	Method: POST
	extension: "/cars"
	pass by: JSON request
	JSON request structure:{
					"id": "zzz", #Text
                    "active": "zzz", #Text
                    "year": "zzz", #Text
                    "mileage": 1234, #Numeric
                    "price": 1234, #Numeric	
                    "make_id": "zzz", #Text
                    "model_id": "zzz", #Text
                    "submodel_id": "zzz", #Text
                    "body_type": "zzz", #Text
                    "transmission": "zzz", #Text
                    "fuel_type": "zzz", #Text
                    "exterior_color": "zzz", #Text
				}
2) To list all makes, models, and submodels:
	Method: GET
	pass by: url arguments
	url arguments: table=cars (or) table=models (or) table=makes (or) table=submodels
3) Fetch cars using make, model, and submodel names:
	Method: GET
	extension: "/query-by-name"
	pass by: JSON request
	JSON request structure:{
					"table": "zzz", #"cars" or "models" or "makes" or "submodels"
                    "name": "zzz", #Text
				}
4) Fetch cars along with make, model, and submodel names of given price and mileage:
	Method: GET
	extension: "/query-by-price-mileage"
	pass by: JSON request
	JSON request structure:{
					"year": 1234, #Numeric
                    "mileage": 1234, #Numeric
				}

## Improvements

There are a few improvements which could be made (as the submission was asked to made on a quick notice I have made a few compromises), such as the following:

1) Instead of dumping the data in dB using pandas, tables with appropriate forgein key initializations and strict constraints (type/length) can be made and then the data can be inserted.
2) Models in the app can be made with those forgein key initializations.
3) The code can be split in to models.py, views.py, app.py etc.
4) Joins can be used instead of fetching the params and running the queries. But, as the given data is small it doesn't make much difference.
5) Case sensitive error handling can be done.
