# ...user/views.py

# IMPORTS
from flask import Blueprint 
from project.models import User

# Blueprints
user_blueprint = Blueprint(
    'user',
    __name__,
    template_folder='templates'
)
