import os
from flask import Flask
from flask_restful import Api
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

DIRNAME = os.path.abspath(os.path.dirname(__name__))
DB_NAME = 'audioFileServer.db'
PATH = os.path.join(DIRNAME, DB_NAME) 

#Init the app
app = Flask(__name__)

#Init the API 
api = Api(app)

#Init the database
try:
    engine = create_engine('sqlite:///'+PATH)
    Base = declarative_base()
except:
    print('Could not find the database, Please make sure it is in the same directory from where you are running this code ie Run.py')

from curd_api_package import model
from curd_api_package import route