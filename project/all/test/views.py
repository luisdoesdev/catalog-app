
from flask import Blueprint, render_template 
 # we will import much more later

# let's create the owners_blueprint to register in our __init__.py
test_blueprint = Blueprint(
    'test',
    __name__,
    template_folder='templates'
)
@test_blueprint.route('/')
def index():
    return render_template('index.html')