from settings import *
from models import *
# use .get()
mid = 1
# @api.representation('application/json')
# def output_json(data, code, headers=None):
# 	resp = make_response(json.dumps(data), code)
# 	return resp 

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

		return {"name" : data["name"]} , 201

@api.resource("/teachers/<int:pageid>/<int:pagesize>")
class Teachers(Resource):

	def get(self,pageid, pagesize):
		try:
			teachers = session.query(Teacher).filter_by(master_id=mid).limit(pagesize)
			students = students.offset(pagesize*pageid)
			return jsonify(teacher=[teacher.serialize for teacher in teachers])
		except:
			return {"message" : "You are not allowed"} , 401

@api.resource("/students/<int:pageid>/<int:pagesize>")
class Students(Resource):

	def get(self,pageid, pagesize):
		try:
			students = session.query(Student).filter_by(master_id=mid).limit(pagesize)
			students = students.offset(pagesize*pageid)
			return jsonify(student=[student.serialize for student in students])
		except:
			return {"message" : "You are not allowed"} , 401

@api.resource("/masters/<int:pageid>/<int:pagesize>")
class Masters(Resource):

	def get(self,pageid, pagesize):
		try:
			masters = session.query(Master).limit(pagesize)
			students = students.offset(pagesize*pageid)
			return jsonify(master=[master.serialize for master in masters])
		except:
			return {"message" : "You are not allowed"} , 401

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
			return {"message" : "Username already exists"}, 409
		try:
			master = Master(name=data["name"], username=data["username"], lastname=data["lastname"], password=data["password"], email=data["email"])
			session.add(master)
			session.commit()
			return {"message" : "Successfully added"} , 200
		except:
			session.rollback()
			return {"message" : "Error"}, 401

@api.resource("/add/student")
class AddStudent(Resource):

	def post(self):
		data = request.get_json()
		if session.query(Student).filter_by(username=data["username"]).first() is not None:
			return {"message" : "Username already exists"} , 409
		try:
			stud = Student(name=data["name"], lastname = data["lastname"], username=data["username"], password=data["password"], image=data["image"], master_id=data["master_id"])
			session.add(stud)
			session.commit()
			return {"message" : "Successfully added"} , 200
		except:
			session.rollback()
			return {"message" : "Error"}, 401

@api.resource("/add/teacher")
class AddTeacher(Resource):

	def post(self):
		data = request.get_json()
		if session.query(Teacher).filter_by(username=data["username"]).first() is not None:
			return {"message" : "Username already exists"} , 409
		try:
			teacher = Teacher(name=data["name"], lastname=data["lastname"], username=data["username"], password=data["password"], email=data["email"], master_id=data["master_id"])
			session.add(teacher)
			session.commit()
			return {"message" : "Successfully added"} , 200
		except:
			session.rollback()
			return {"message" : "Error"}, 401

@api.resource("/add/class")
class AddClass(Resource):

	def post(self):
		data = request.get_json()
		try:
			classd = Class(department=data["department"], year=data["year"], div=data["div"], master_id=data["master_id"])
			session.add(classd)
			session.commit()
			return {"message" : "Successfully added"} , 200
		except:
			session.rollback()
			return {"message" : "Error"}, 401

@api.resource("/add/subject")
class AddSubject(Resource):

	def post(self):
		data = request.get_json()
		try:
			subject = Subject(name=data["name"], master_id=data["master_id"])
			session.add(subject)
			session.commit()
			return {"message" : "Successfully added"} , 200
		except:
			session.rollback()
			return {"message" : "Error"}, 401

@api.resource("/add/timetable")
class AddTimetable(Resource):

	def post(self):
		data = request.get_json()
		try:
			class_id = session.query(Class).filter(and_(Class.department==data["department"], Class.year==data["year"], Class.div==data["div"], Class.master_id==data["master_id"])).one()
		except:
			session.rollback()
			return {"message" : "Invalid data"}, 403
		try:
			timetable = Timetable(day=data["day"], start_time=data["start"], end_time=data["end"], class_id=class_id, teacher_id=data["teacher_id"], subject_id=data["subject_id"], master_id=data["master_id"])
			session.add(timetable)
			session.commit()
			return {"message" : "Successfully added"} , 200
		except:
			session.rollback()
			return {"message" : "Error"}, 401

@api.resource("/edit/master")
class EditMaster(Resource):

	def put(self):
		data = request.get_json()
		try:
			master = session.query(Master).get(data["id"])
			if master is None:
				return {"message" : "You are not allowed"} , 403
	
			if data["name"] is not None:
				master.name = data["name"]
			if data["lastname"] is not None:
				master.lastname = data["lastname"]
			if data["newpassword"] is not None:
				if data["oldpassword"] == master.password:
					master.password = data["newpassword"]
				else:
					session.rollback()
					return {"message" : "Wrong password"} , 403
			if data["email"] is not None:
				master.email = data["email"]
			session.add(master)
			session.commit()
			return {"message" : "Successfully edited"} , 200
		except:
			session.rollback()
			return {"message" : "Error"} , 401

@api.resource("/edit/student")
class EditStudent(Resource):

	def put(self):
		data = request.get_json()
		try:
			stud = session.query(Student).get(data["id"])
			if stud is None:
				return {"message" : "You are not allowed"} , 403

			if data["name"] is not None:
				stud.name = data["name"]
			if data["lastname"] is not None:
				stud.lastname = data["lastname"]
			if data["newpassword"] is not None:
				if data["oldpassword"] == stud.password:
					stud.password = data["newpassword"]
				else:
					session.rollback()
					return {"message" : "Wrong password"} , 403
			session.add(stud)
			session.commit()
			return {"message" : "Successfully edited"} , 200
		except:
			session.rollback()
			return {"message" : "Error"} , 401

@api.resource("/edit/teacher")
class EditTeacher(Resource):

	def put(self):
		data = request.get_json()
		try:
			teacher = session.query(Teacher).get(data["id"])
			if teacher is None:
				return {"message" : "You are not allowed"}, 403

			if data["name"] is not None:
				teacher.name = data["name"]
			if data["lastname"] is not None:
				teacher.lastname = data["lastname"]
			if data["newpassword"] is not None:
				if data["oldpassword"] == teacher.password:
					teacher.password = data["newpassword"]
				else:
					session.rollback()
					return {"message" : "Wrong password"} , 403
			if data["email"] is not None:
				teacher.email = data["email"]
			session.add(teacher)
			session.commit()
			return {"message" : "Successfully edited"} , 200
		except:
			session.rollback()
			return {"message" : "Error"} , 401

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

	def delete(self):
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

	def delete(self):
		data = request.get_json()
		try:
			stud = session.query(Student).get(data["id"])
			if stud is None:
				return {"message" : "Student doesn't exist !"} , 404
			session.delete(stud)
			session.commit()
			return {"message" : "Successfully deleted"} , 200
		except: 
			session.rollback()
			return {"message" : "Error"} , 404

@api.resource("/delete/teacher")
class DeleteTeacher(Resource):

	def delete(self):
		data = request.get_json()
		try:
			teacher = session.query(Teacher).get(data["id"])
			if teacher is None:
				return {"message" : "Teacher doesn't exist !"} , 404

			session.delete(teacher)
			session.commit()
			return {"message" : "Successfully deleted"} , 200
		except: 
			session.rollback()
			return {"message" : "Error"} , 404

@api.resource("/delete/subject")
class DeleteSubject(Resource):

	pass

@api.resource("/delete/class")
class DeleteClass(Resource):

	pass

@api.resource("/delete/timetable")
class DeleteTimetable(Resource):

	pass

@api.resource("/upload/file")
class Upload(Resource):
	
	def post(self):
		data = request.get_json()
		if session.query(Teacher).get(data["teacher_id"]) is None:
			return {"message" : "You are not allowed"} , 401
		try:
			file = Moodle(filename=data["filename"], ftype=data["ftype"], path=data["path"], uploaded_by=data["teacher_id"])
			session.add(file)
			session.commit()
			return {"message" : "Successfully uploaded"} , 200
		except:
			session.rollback()
			return {"message" : "Error"} , 401

@api.resource("/delete/file")
class DeleteFile(Resource):

	def delete(self):
		data = request.get_json()
		try:
			file = session.query(Moodle).get(data["id"])
			if file is None:
				return {"message" : "File not found"}, 404
			if file.uploaded_by != data["teacher_id"]:
				return {"message" : "You are not allowed"} , 401
			session.delete(file)
			session.commit()
			return {"message" : "Deleted successfully"}, 200
		except:
			session.rollback()
			return {"message" : "Error"} , 401

@api.resource("/give/attendance")
class GiveAttendance(Resource):
	pass

@api.resource("/take/attendance")
class TakeAttendance(Resource):
	pass

@api.resource("/get/file")
class GetFile(Resource):

	def get(self):
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

	def get(self):
		data = request.authorization
		try:
			student = session.query(Student).filter_by(username=data["username"]).one()
		except:
			return {"message" : "Invalid username"} , 404
		
		if student.password == data["password"]:
			return {"message" : "Successfully logged in"} , 200
		else:
			return {"message" : "Wrong password"}, 404

@api.resource("/login/teacher")
class TeacherLogin(Resource):

	def get(self):
		data = request.authorization
		try:
			teacher = session.query(Teacher).filter_by(username=data["username"]).one()
		except:
			return {"message" : "Invalid username"} , 404
		
		if teacher.password == data["password"]:
			return {"message" : "Successfully logged in"} , 200
		else:
			return {"message" : "Wrong password"}, 404

@api.resource("/login/master")
class MasterLogin(Resource):

	def post(self):
		data = request.authorization
		master = session.query(Master).filter_by(username=data["username"])
		try:	
			if master.one().password == data["password"]:
				return {"message" : "Successfully logged in"} , 200
				return {"message" : "Wrong password"}, 404
		except:
			return  {"message" : "Invalid username"} , 404

if __name__ == '__main__':
	# stud = Student(username="shadiest", password="xyz")
	# db.session.add(stud)
	# db.session.commit()
	port = int(os.environ.get('PORT', 8080))
	app.run(host='0.0.0.0', port=port, debug=True)