from flask import Flask, jsonify
import logging
from flask_cors import CORS
from src.blueprints.honeycomb import honeycomb_blueprint

logging.getLogger('flask_cors').level = logging.DEBUG

# init Flask app
app = Flask(__name__)
app.logger.setLevel(logging.INFO)
CORS(app)

# register blueprints. ensure that all paths are versioned!
app.register_blueprint(honeycomb_blueprint, url_prefix="/api/v1/honeycomb")
