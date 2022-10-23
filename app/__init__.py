# flaskr
from flask import Flask
from flask_cors import CORS

# db
from .database import db

# blueprints
from .blueprints import *

# configs
from configs import SQLALCHEMY_DATABASE_URI

# - Flask App -----------------------------------------------------------------

app: Flask = Flask(__name__,
                   static_folder="./templates/public",
                   template_folder="./templates")

# Cross-Origin Resource Sharing
CORS(app, supports_credentials=True)

# - Blueprints ----------------------------------------------------------------
app.register_blueprint(host_group_bp)

# - DataBase ------------------------------------------------------------------
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()
