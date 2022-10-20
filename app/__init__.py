# flaskr
from flask import Flask
from flask_cors import CORS

# blueprints
from .blueprints import *

# - Flask App -----------------------------------------------------------------

app: Flask = Flask(__name__,
                   static_folder="./templates/public",
                   template_folder="./templates")

# Cross-Origin Resource Sharing
CORS(app, supports_credentials=True)

# - Blueprints ----------------------------------------------------------------
app.register_blueprint(locations_blueprint)
