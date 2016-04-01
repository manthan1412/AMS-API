from settings import *

class Student(db.Model):
	__tablename__ = 'student'
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(80), unique=True)
	password = db.Column(db.String(20), nullable=False)
	image = db.Column(db.String)

	def __init__(self, username, password, image=None):
		self.username = username
		self.password = password
		if not image: 
			self.image = 'null'
		else:
			self.image = image

# class Teacher(db.Model):
# 	__tablename__ = 'teacher'
# 	id = db.Column(db.Integer, primary_key=True)
# 	username = db.Column(db.String(80), unique=True)
# 	password = db.Column(db.String(20), nullable=False)
# 	departments = db.Column(db.String, nullable=False)


# 	def __init__(self, username, password, table, image=None):
# 		self.username = username
# 		self.password = password
# 		if not image:
# 			self.image = null
# 		else:
# 			self.image = image

