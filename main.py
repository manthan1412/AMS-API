from settings import *
from models import *
# use .get()
@app.after_request
def after_request(response):
	response.headers.add('Access-Control-Allow-Origin', '*')
	response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
	response.headers.add('Access-Control-Allow-Methods', 'GET, PUT, POST, DELETE')
	return response

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

	def get(self):
		return jsonify({"name" : "ams"})

	def post(self):
		# resp = make_response("Hello world", 200)
		# resp.headers.extend({'Access-Control-Allow-Origin' : 'http://127.0.0.1'})
		data = request.get_json()
		# print data
		# return data["name"]

		return jsonify({"name" : data["name"]})

@api.resource("/teachers")
class Teachers(Resource):

	def post(self):
		data = request.get_json()
		try:
			teachers = session.query(Teacher).filter_by(master_id=data["id"]).all()
			return jsonify(teacher=[teacher.serialize for teacher in teachers])
		except:
			return status.HTTP_500_INTERNAL_SERVER_ERROR

@api.resource("/students")
class Students(Resource):

	def post(self):
		data = request.get_json()
		try:
			students = session.query(Student).filter_by(master_id=data["id"]).all()
			return jsonify(student=[student.serialize for student in students])
		except:
			return status.HTTP_500_INTERNAL_SERVER_ERROR

@api.resource("/masters")
class Masters(Resource):

	def post(self):
		try:
			masters = session.query(Master).all()
			return jsonify(master=[master.serialize for master in masters])
		except:
			return status.HTTP_500_INTERNAL_SERVER_ERROR

@api.resource("/classes")
class Classes(Resource):

	pass

@api.resource("/subjects")
class Subjects(Resource):

	pass

@api.resource("/timetable")
class Timetable(Resource):

	pass

@api.resource("/add/master")
class AddMaster(Resource):

	def post(self):
		data = request.get_json()
		if session.query(Master).filter_by(username=data["username"]).first() is not None:
			return jsonify({"message" : "Username already exists"})
		try:
			master = Master(name=data["name"], username=data["username"], lastname=data["lastname"], password=data["password"], email=data["email"])
			session.add(master)
			session.commit()
			return status.HTTP_200_OK
		except:
			session.rollback()
			return status.HTTP_500_INTERNAL_SERVER_ERROR

@api.resource("/add/student")
class AddStudent(Resource):

	def post(self):
		data = request.get_json()
		if session.query(Student).filter_by(username=data["username"]).first() is not None:
			return jsonify({"message" : "Username already exists"})
		try:
			stud = Student(name=data["name"], lastname = data["lastname"], username=data["username"], password=data["password"], image=data["image"], master_id=data["master_id"])
			session.add(stud)
			session.commit()
			return status.HTTP_200_OK
		except:
			session.rollback()
			return status.HTTP_500_INTERNAL_SERVER_ERROR

@api.resource("/add/teacher")
class AddTeacher(Resource):

	def post(self):
		data = request.get_json()
		if session.query(Teacher).filter_by(username=data["username"]).first() is not None:
			return jsonify({"message" : "Username already exists"})
		try:
			teacher = Teacher(name=data["name"], lastname=data["lastname"], username=data["username"], password=data["password"], email=data["email"], master_id=data["master_id"])
			session.add(teacher)
			session.commit()
			return status.HTTP_200_OK
		except:
			session.rollback()
			return status.HTTP_500_INTERNAL_SERVER_ERROR

@api.resource("/add/class")
class AddClass(Resource):

	def post(self):
		data = request.get_json()
		try:
			classd = Class(department=data["department"], year=data["year"], div=data["div"], master_id=data["master_id"])
			session.add(classd)
			session.commit()
			return status.HTTP_200_OK
		except:
			session.rollback()
			return status.HTTP_500_INTERNAL_SERVER_ERROR

@api.resource("/add/subject")
class AddSubject(Resource):

	def post(self):
		data = request.get_json()
		try:
			subject = Subject(name=data["name"], master_id=data["master_id"])
			session.add(subject)
			session.commit()
			return status.HTTP_200_OK
		except:
			session.rollback()
			return status.HTTP_500_INTERNAL_SERVER_ERROR

@api.resource("/add/timetable")
class AddTimetable(Resource):

	def post(self):
		data = request.get_json()
		try:
			class_id = session.query(Class).filter(and_(Class.department==data["department"], Class.year==data["year"], Class.div==data["div"], Class.master_id==data["master_id"])).one()
		except:
			session.rollback()
			return jsonify({"message" : "Invalid data"})
		try:
			timetable = Timetable(day=data["day"], start_time=data["start"], end_time=data["end"], class_id=class_id, teacher_id=data["teacher_id"], subject_id=data["subject_id"], master_id=data["master_id"])
			session.add(timetable)
			session.commit()
			return status.HTTP_200_OK
		except:
			session.rollback()
			return status.HTTP_401_UNAUTHORIZED

@api.resource("/edit/master")
class EditMaster(Resource):

	def post(self):
		data = request.get_json()
		try:
			master = session.query(Master).filter_by(id=data["id"]).one()
		except:
			return jsonify({"message" : "Master doesn't exist !"})

		try:	
			if data["name"] is not None:
				master.name = data["name"]
			if data["lastname"] is not None:
				master.lastname = data["lastname"]
			if data["newpassword"] is not None:
				if data["oldpassword"] == master.password:
					master.password = data["newpassword"]
				else:
					session.rollback()
					return jsonify({"message" : "Wrong password"})
			if data["email"] is not None:
				master.email = data["email"]
			session.add(master)
			session.commit()
			return status.HTTP_200_OK
		except:
			session.rollback()
			return status.HTTP_500_INTERNAL_SERVER_ERROR

@api.resource("/edit/student")
class EditStudent(Resource):

	def post(self):
		data = request.get_json()
		try:
			stud = session.query(Student).filter_by(id=data["id"]).one()
		except:
			return jsonify({"message" : "Student doesn't exist !"})

		try:	
			if data["name"] is not None:
				stud.name = data["name"]
			if data["lastname"] is not None:
				stud.lastname = data["lastname"]
			if data["newpassword"] is not None:
				if data["oldpassword"] == stud.password:
					stud.password = data["newpassword"]
				else:
					session.rollback()
					return jsonify({"message" : "Wrong password"})
			session.add(stud)
			session.commit()
			return status.HTTP_200_OK
		except:
			session.rollback()
			return status.HTTP_500_INTERNAL_SERVER_ERROR

@api.resource("/edit/teacher")
class EditTeacher(Resource):

	def post(self):
		data = request.get_json()
		try:
			teacher = session.query(Teacher).filter_by(id=data["id"]).one()
		except:
			return jsonify({"message" : "Teacher doesn't exist !"})

		try:	
			if data["name"] is not None:
				teacher.name = data["name"]
			if data["lastname"] is not None:
				teacher.lastname = data["lastname"]
			if data["newpassword"] is not None:
				if data["oldpassword"] == teacher.password:
					teacher.password = data["newpassword"]
				else:
					session.rollback()
					return jsonify({"message" : "Wrong password"})
			if data["email"] is not None:
				teacher.email = data["email"]
			session.add(teacher)
			session.commit()
			return status.HTTP_200_OK
		except:
			session.rollback()
			return status.HTTP_500_INTERNAL_SERVER_ERROR

@api.resource("/edit/subject")
class EditSubject(Resource):

	pass

@api.resource("/edit/class")
class EditClass(Resource):

	pass

@api.resource("/edit/timetable")
class EditTimetable(Resource):

	pass

@api.resource("/delete/master")
class DeleteMaster(Resource):

	def post(self):
		data = request.get_json()
		try:
			master = session.query(Master).filter_by(id=data["id"]).one()
		except:
			return jsonify({"message" : "Master doesn't exist !"})

		try:
			session.delete(master)
			session.commit()
			return status.HTTP_200_OK
		except: 
			session.rollback()
			return status.HTTP_500_INTERNAL_SERVER_ERROR

@api.resource("/delete/student")
class DeleteStudent(Resource):

	def post(self):
		data = request.get_json()
		try:
			stud = session.query(Student).filter_by(id=data["id"]).one()
		except:
			return jsonify({"message" : "Student doesn't exist !"})

		try:
			session.delete(stud)
			session.commit()
			return status.HTTP_200_OK
		except: 
			session.rollback()
			return status.HTTP_500_INTERNAL_SERVER_ERROR

@api.resource("/delete/teacher")
class DeleteTeacher(Resource):

	def post(self):
		data = request.get_json()
		try:
			teacher = session.query(Teacher).filter_by(id=data["id"]).one()
		except:
			return jsonify({"message" : "Teacher doesn't exist !"})

		try:
			session.delete(teacher)
			session.commit()
			return status.HTTP_200_OK
		except: 
			session.rollback()
			return status.HTTP_500_INTERNAL_SERVER_ERROR

@api.resource("/upload/file")
class Upload(Resource):
	
	def post(self):
		data = request.get_json()
		if session.query(Teacher).filter_by(id=data["teacher_id"]).first() is None:
			return status.HTTP_401_UNAUTHORIZED
		try:
			file = Moodle(filename=data["filename"], ftype=data["ftype"], path=data["path"], uploaded_by=data["teacher_id"])
			session.add(file)
			session.commit()
			return status.HTTP_200_OK
		except:
			session.rollback()
			return status.HTTP_500_INTERNAL_SERVER_ERROR

@api.resource("/delete/file")
class DeleteFile(Resource):

	def post(self):
		data = request.get_json()
		try:
			file = session.query(Moodle).filter_by(id=data["id"]).first()
			if file.uploaded_by != data["teacher_id"]:
				return jsonify({"message" : "You are not allowed to delete this file"})
			session.delete(file)
			session.commit()
			return status.HTTP_200_OK
		except:
			session.rollback()
			return status.HTTP_500_INTERNAL_SERVER_ERROR

@api.resource("/delete/subject")
class DeleteSubject(Resource):

	pass

@api.resource("/delete/class")
class DeleteClass(Resource):

	pass

@api.resource("/delete/timetable")
class DeleteTimetable(Resource):

	pass

@api.resource("/get/file")
class GetFile(Resource):

	def post(self):
		data = request.get_json()
		try:
			path = data["path"]
			files = session.query(Moodle).filter_by(path=path).all()
			return jsonify(data=[file.serialize for file in files ])
		except:
			session.rollback()
			return status.HTTP_500_INTERNAL_SERVER_ERROR

@api.resource("/login/student")
class StudentLogin(Resource):

	def post(self):
		data = request.authorization
		try:
			student = session.query(Student).filter_by(username=data["username"]).one()
		except:
			return jsonify({"message" : "Invalid username"})
		
		if student.password == data["password"]:
			return jsonify({"message" : "Successfully logged in"})
		else:
			return jsonify({"message" : "Wrong password"})

@api.resource("/login/teacher")
class TeacherLogin(Resource):

	def post(self):
		data = request.authorization
		try:
			teacher = session.query(Teacher).filter_by(username=data["username"]).one()
		except:
			return jsonify({"message" : "Invalid username"})
		
		if teacher.password == data["password"]:
			return jsonify({"message" : "Successfully logged in"})
		else:
			return jsonify({"message" : "Wrong password"})

@api.resource("/login/master")
class MasterLogin(Resource):

	def post(self):
		data = request.authorization
		master = session.query(Master).filter_by(username=data["username"])
		try:	
			if master.one().password == data["password"]:
				return jsonify({"message" : "Successfully logged in"})
			else:
				return jsonify({"message" : "Password Incorrect."}) 
		except:
			return  jsonify({"message" : "Invalid Username."})

if __name__ == '__main__':
	# stud = Student(username="shadiest", password="xyz")
	# db.session.add(stud)
	# db.session.commit()
	port = int(os.environ.get('PORT', 8080))
	app.run(host='0.0.0.0', port=port, debug=True)