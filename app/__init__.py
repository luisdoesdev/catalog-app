# app/__init__.py


from flask import Flask

app  = Flask(__name__)

# Loads the routes
from app import routes


#Loads Config

app.config.from_object('config')