#!/usr/bin/python3
"""
    Python API Module To Handle API requests
                                            """
from models import storage
from api.ports import app_ports
from flask import Flask, make_response, jsonify
from flasgger import Swagger
from flasgger.utils import swag_from


app = Flask(__name__)
app.register_blueprint(app_ports)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

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
    return jsonify({'error': '500 - Server Error'})

@app.errorhandler(404)
def port_404(error):
    """
        Handles error codes 404 for resources not found
                                                        """
    return jsonify({'error': '404 - Resource Not Found'})

app.config['SWAGGER'] = {
        'title': 'ALX PORTFOLIO WEBSITE',
        'api_version': '1.0'
        }

Swagger(app)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, threaded=True)
