from settings import *

class Master(Base):

	__tablename__ = 'master'

	id = Column(Integer, primary_key=True)
	name = Column(String, nullable=False)
	lastname = Column(String, nullable=False)
	username = Column(String, nullable=False)
	password = Column(String, nullable=False)
	email = Column(String, nullable=False)

class Student(Base):
	__tablename__ = 'student'

	id = Column(Integer, primary_key=True)
	name = Column(String, nullable=False)
	lastname = Column(String, nullable=False)
	username = Column(String(80), unique=True)
	password = Column(String(20), nullable=False)
	image = Column(String, nullable=True)
	master_id = Column(Integer, ForeignKey('master.id'))
	master = relationship(Master)

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

