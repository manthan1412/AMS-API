from settings import *
from models import *

@api.resource("/")
class Test(Resource):

	def get(self):
		# data = request.get_json()
		# name = data["name"]
		output = ""
		output += "<h1> It's working ! </h1>"
		return output

@api.resource("/add/student")
class AddStudent(Resource):

	def post(self):
		data = request.get_json()
		stud = Student(name=data["name"], lastname = data["lname"], username=data["uname"], password=data["password"], image=data["image"])
		session.add(stud)
		try:
			session.commit()
			return status.HTTP_200_OK
		except:
			return status.HTTP_500_INTERNAL_SERVER_ERROR
		

@api.resource("/add/master")
class AddMaster(Resource):

	def post(self):
		pass

@api.resource("/login")
class Login(Resource):

	def get(self):
		data = request.authorization
		users = session.query(Student).filter_by(username=data["username"])
		try:	
			if users.one().password == data["password"]:
				return status.HTTP_200_OK
			else:
				return jsonify({"error" : "Password Incorrect."}), status.HTTP_401_UNAUTHORIZED
		except:
			return  jsonify({"error" : "Invalid Username."}), status.HTTP_401_UNAUTHORIZED


if __name__ == '__main__':
	# stud = Student(username="shadiest", password="xyz")
	# db.session.add(stud)
	# db.session.commit()
	app.run(debug=True)