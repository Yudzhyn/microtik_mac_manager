# for logging
from modules import logger

# configs
from configs import *

# flaskr app
from app import app

if __name__ == '__main__':
    app.run(
        host=FLASK_HOST,
        port=FLASK_PORT,
        debug=FLASK_DEBUG
    )
