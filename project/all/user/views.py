from flask import Blueprint, render_template 
from project.models import User
 # we will import much more later

# let's create the owners_blueprint to register in our __init__.py
user_blueprint = Blueprint(
    'user',
    __name__,
    template_folder='templates'
)
@user_blueprint.route('/')
def index():
    return "hello user"