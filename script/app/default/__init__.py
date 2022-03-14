import os
from flask import Blueprint, current_app
#from config import Config

default = Blueprint('cast', __name__, static_folder='',static_url_path='')
from . import routes
