#!/usr/bin/python3
from flask import Blueprint

app_ports = Blueprint('app_ports', __name__, url_prefix='/api')


from api.ports.users import *
from api.ports.messages import *
from api.ports.recipients import *
from api.ports.index import *
from api.ports.api import *
