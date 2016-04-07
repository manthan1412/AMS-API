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

@api.resource("/test")
class Check(Resource):

	def post(self):
		data = request.get_json()
		print data
		return data["name"]

@api.resource("/add/student")
class AddStudent(Resource):

	def post(self):
		data = request.get_json()
		stud = Student(name=data["name"], lastname = data["lastname"], username=data["username"], password=data["password"], image=data["image"])
		try:
			session.add(stud)
			session.commit()
			return status.HTTP_200_OK
		except:
			return status.HTTP_500_INTERNAL_SERVER_ERROR
		

@api.resource("/add/master")
class AddMaster(Resource):

	def post(self):
		data = request.get_json()
		master = Master(name=data["name"], username=data["username"], lastname=data["lastname"], password=data["password"], email=data["email"])
		try:
			session.add(master)
			session.commit()
			return status.HTTP_200_OK
		except:
			return status.HTTP_500_INTERNAL_SERVER_ERROR

@api.resource("/login")
class Login(Resource):

	def post(self):
		data = request.authorization
		users = session.query(Student).filter_by(username=data["username"])
		try:	
			if users.one().password == data["password"]:
				return status.HTTP_200_OK
			else:
				return jsonify({"error" : "Password Incorrect.",
								"status" : status.HTTP_401_UNAUTHORIZED}) 
		except:
			return  jsonify({"error" : "Invalid Username.",
							 "status" : status.HTTP_401_UNAUTHORIZED})


if __name__ == '__main__':
	# stud = Student(username="shadiest", password="xyz")
	# db.session.add(stud)
	# db.session.commit()
	port = int(os.environ.get('PORT', 8080))
	app.run(host='0.0.0.0', port=port, debug=True)