from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, create_engine, and_, or_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from flask.ext.api import status
import os
import datetime

Base = declarative_base()

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:ams@localhost:5432/ams'
# db = SQLAlchemy(app)
api = Api(app)

engine = create_engine('postgresql://postgres:ams@localhost:5432/ams')
# engine = create_engine('postgres://qogoqipkzqtylc:VZNm-dB2SiYTlc7uezU7NbW_fJ@ec2-54-163-254-231.compute-1.amazonaws.com:5432/d164pdjkve1t6d')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()