
#!/usr/bin/env python


from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, User, Category, Item

# Initialize the APP
app = Flask(__name__)
app.debug = True


# import a blueprint that we will create
from project.test.views import test_blueprint

# register our blueprints with the application
app.register_blueprint(test_blueprint, url_prefix='/catalog')



# Root
@app.route('/')
def root():
    return "Hello"


'''
## Blueprints
from app.crud.views import crud_blueprint

## Register the blueprints
app.register_blueprints(user_blueprint)
'''

