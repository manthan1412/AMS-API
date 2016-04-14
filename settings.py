from flask import Flask, jsonify, request, make_response
from flask_restful import Api, Resource
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, create_engine, and_, or_, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
import os
import datetime
from datetime import timedelta
import time
import json
import urllib3
urllib3.disable_warnings()

Base = declarative_base()

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:ams@localhost:5432/ams'
# db = SQLAlchemy(app)
api = Api(app)
app.permanent_session_lifetime = timedelta(seconds=10)
# api = Api(app, catch_all_404s=True)

# engine = create_engine('postgresql://postgres:ams@localhost:5432/ams')
engine = create_engine('postgres://qogoqipkzqtylc:VZNm-dB2SiYTlc7uezU7NbW_fJ@ec2-54-163-254-231.compute-1.amazonaws.com:5432/d164pdjkve1t6d')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()