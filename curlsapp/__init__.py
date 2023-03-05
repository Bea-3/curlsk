#initialize the app
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect

app=Flask(__name__,instance_relative_config=True)
csrf =CSRFProtect(app)

#load the config
app.config.from_pyfile('config.py',silent=False)
db=SQLAlchemy(app)

#load the routes
from curlsapp import adminroutes,vendorroutes,custroutes