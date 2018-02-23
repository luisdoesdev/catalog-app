
#!/usr/bin/env python


from flask import Flask

# Initialize the APP
app = Flask(__name__)

# Loads the routes
from app import routes



