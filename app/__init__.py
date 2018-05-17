
#!/usr/bin/env python


from flask import Flask

# Initialize the APP
app = Flask(__name__)
app.debug = True
# Loads the routes
from app import routes



