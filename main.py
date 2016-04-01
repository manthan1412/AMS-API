from settings import *


@api.resource("/")
class Test(Resource):

	def post(self):
		data = request.get_json()
		name = data["name"]
		return jsonify({"test" : name})

if __name__ == '__main__':
	app.run(debug=True)