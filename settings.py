from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from sqlalchemy import Column, String, Integer, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker


Base = declarative_base()

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:ams@localhost:5432/ams'
# db = SQLAlchemy(app)
api = Api(app)

engine = create_engine('postgresql://postgres:ams@localhost:5432/ams')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()