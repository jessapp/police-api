from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps

# Create an engine connecting to SQLite3
# DB should be in app root folder

e = create_engine('sqlite:///salaries.db')

app = Flask(__name__)
api = Api(app)

class Departments_Meta(Resource):

    def get(self):
        #connect to the DB
        conn = e.connect()
        # Perform query and return JSON
        query = conn.execute("SELECT DISTINCT department FROM salaries")
        return jsonify({'departments': [i[0] for i in query.cursor.fetchall()]})

class Departmental_Salary(Resource):

    def get(self, department_name):
        conn = e.connect()
        query = conn.execute("SELECT * FROM salaries WHERE department='%s'" % department_name.upper())

        result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        return jsonify(result)

api.add_resource(Departmental_Salary, '/dept/<string:department_name>')
api.add_resource(Departments_Meta, '/departments')

if __name__ == '__main__':
     app.run()