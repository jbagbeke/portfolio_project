#!/usr/bin/python3
"""
    Python API Module To Handle API requests
                                            """
from models import storage
from api.ports import app_ports
from flask import Flask, make_response, jsonify, render_template
from flasgger import Swagger
from flasgger.utils import swag_from
from flask_cors import CORS 
from uuid import uuid4


app = Flask(__name__)
app.register_blueprint(app_ports)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

CORS(app, resources={r"/api/*": {"origins": "*"}})

@app.route('/', strict_slashes=False)
def port_home():
    """
        Returns Index.html [The home Page of the website
                                                        """
    return render_template('index.html')

@app.teardown_appcontext
def port_close_session(self):
    """
        Terminates current session/connection to the database
                                                            """
    storage.close()

@app.errorhandler(500)
def port_500(error):
    """
        Handles server errors by the server
                                            """
    return make_response({'error': '500 - Server Error'}, 500)

@app.errorhandler(404)
def port_404(error):
    """
        Handles error codes 404 for resources not found
                                                        """
    return make_response({'error': '404 - Resource Not Found'}, 404)

app.config['SWAGGER'] = {
        'title': 'ALX PORTFOLIO WEBSITE',
        'api_version': '1.0'
        }

Swagger(app)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, threaded=True)
