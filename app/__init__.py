
#!/usr/bin/env python


from flask import Flask

# Initialize the APP
app = Flask(__name__)
app.config.from_pyfile('flask.cfg')
app.debug = True



# Loads the routes
from app import routes


## Blueprints
from app.crud.views import crud_blueprint

## Register the blueprints
app.register_blueprints(user_blueprint)


