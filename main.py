from settings import *
from models import *

@api.resource("/")
class Test(Resource):

	def post(self):
		data = request.get_json()
		name = data["name"]
		return jsonify({"test" : name})

if __name__ == '__main__':
	stud = Student(username="shadiest", password="xyz")
	db.session.add(stud)
	db.session.commit()
	app.run(debug=True)