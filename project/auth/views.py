# ...auth/views.py

# IMPORTS
from flask import redirect, render_template, request, url_for, Blueprint
from project.models import db, User
from project.user.forms import UserForm, DeleteForm


# Blueprints
auth_blueprint = Blueprint(
    'auth',
    __name__,
    template_folder='templates'
)

@auth_blueprint.route('/gconnect', methods=['GET', 'POST'])
def gconnect():
    return "/gconnect"

@auth_blueprint.route('/gdisconnect', methods=['GET', 'POST'])
def gdisconnect():
    return "/gdisconnect"