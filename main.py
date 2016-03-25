from flask import Flask, jsonify, request
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)

@api.resource("/")
class Test(Resource):

	def post(self):
		data = request.get_json()
		name = data["name"]
		return jsonify({"test" : name})

if __name__ == '__main__':
	app.run(debug=True)