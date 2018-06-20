
#!/usr/bin/env python


from flask import Flask, Blueprint
import random
import string
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, User, Category, Item
from flask import session as login_session


engine = create_engine('sqlite:///models.db?check_same_thread=False')
Base.metadata.bind = engine
Session = sessionmaker(bind=engine)
session = Session()




# Initialize the APP
app = Flask(__name__)
app.debug = True



# anti forgery Token
state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                for x in range(32))




# RPUTES
from project import routes
from project.auth.views import auth_blueprint
from project.api.views import api_blueprint

# API ROUTES


# API ROUTES
app.register_blueprint(api_blueprint, url_prefix='/api')
app.register_blueprint(auth_blueprint, url_prefix='/auth')



