from settings import *


# class Test(Base):
# 	def __init__(self, username, password):
# 		self.username = username
# 		self.password = password
# tname  = ["diva", "divb"11]

# for t in tname:
# 	timetable = Table(
# 					t,metadata,
# 					Column('id',Integer,primary_key=True),
# 					Column('name',String)
# 				)
# 	metadata.create_all()
# mapper(TimeTable, timetable)
	# s = create_sess

class Master(Base):

	__tablename__ = 'master'

	id = Column(Integer, primary_key=True)
	name = Column(String, nullable=False)
	lastname = Column(String, nullable=False)
	username = Column(String, nullable=False)
	password = Column(String, nullable=False)
	email = Column(String, nullable=False)

	@property
	def serialize(self):
	    return {
	    	'id' : self.id,
	    	'name' : self.name,
	    	'lastname' : self.lastname,
	    	'username' : self.username,
	    	'email' : self.email
	    }
	

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

	@property
	def serialize(self):
	    return {
	    	'id' : self.id,
	    	'name' : self.name,
	    	'lastname' : self.lastname,
	    	'username' : self.username,
	    	'image' : self.image,
	    }
	

class Teacher(Base):
	__tablename__ = 'teacher'

	id = Column(Integer, primary_key=True)
	name = Column(String, nullable=False)
	lastname = Column(String, nullable=False)
	username = Column(String, nullable=False)
	password = Column(String, nullable=False)
	email = Column(String, nullable=False)
	master_id = Column(Integer, ForeignKey('master.id'))
	master = relationship(Master)
	
	@property
	def serialize(self):
	    return {
	    	'id' : self.id,
	    	'name' : self.name,
	    	'lastname' : self.lastname,
	    	'username' : self.username,
	    	'email' : self.email,
	    }
	

class Moodle(Base):
	__tablename__ ='moodle'

	id = Column(Integer, primary_key=True)
	filename = Column(String, nullable=False)
	path = Column(String, nullable=False)
	ftype = Column(Integer, nullable=False)
	uploaded_by = Column(Integer, ForeignKey('teacher.id'))
	time = Column(DateTime, default=datetime.datetime.now)
	teacher = relationship(Teacher)

	@property
	def serialize(self):
	    return {
	    	'id' : self.id,
	    	'filename' : self.filename,
	    	'ftype' : self.ftype,
	    	'uploaded_by' : self.uploaded_by,
	    	'time' : self.time,
	    }

class Subject(Base):
	__tablename__ = 'subject'

	id = Column(Integer, primary_key=True)
	name = Column(String, nullable=False) 
	master_id = Column(Integer, ForeignKey('master.id'))
	master = relationship(Master)
	@property
	def serialize(self):
	    return {
	    	'id' : self.id,
	    	'name' : self.name,
	    }

class Class(Base):
	__tablename__ ='class'

	id=Column(Integer, primary_key=True)
	department = Column(String, nullable=False)
	year = Column(Integer, nullable=False)
	div = Column(String, nullable=False)
	master_id = Column(Integer, ForeignKey('master.id'))
	master = relationship(Master)

class TimeTable(Base):
	__tablename__ = 'timetable'

	id=Column(Integer, primary_key=True)
	day = Column(Integer, nullable=False)
	start_time = Column(DateTime, nullable=False)
	end_time = Column(DateTime, nullable=False)
	class_id = Column(Integer, ForeignKey('class.id'))
	teacher_id = Column(Integer, ForeignKey('teacher.id'))
	subject_id = Column(Integer, ForeignKey('subject.id'))
	master_id = Column(Integer, ForeignKey('master.id'))
	classr = relationship(Class)
	master = relationship(Master)
	subject = relationship(Subject)
	teacher = relationship(Teacher)

string ="00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000"

class Attendance(Base):
	__tablename__ = 'attendance'

	id=Column(Integer, primary_key=True)
	start_time = Column(String, default=time.time())
	a_string = Column(String, default=string)
	key = Column(String, nullable=False)
	class_id = Column(Integer, ForeignKey('class.id'))
	classr = relationship(Class) 
	

# class Timetable(Base):
# 	pass

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