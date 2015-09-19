from flask import Flask
from controllers.data import mod_data
from models import db
from app.config import configure_app

import helpers

# Set up the app
app = Flask(__name__)
app.register_blueprint(mod_data)

# Json errors for common errors
@app.errorhandler(405)
def not_allowed(error):
    return helpers.make_error(405, 1001, "Route not found.")

@app.errorhandler(404)
def not_found(error):
    return helpers.make_error(404, 1002, "Route not found.")

# Configure app
configure_app(app)

# Initialize mongo
db.init_app(app)
