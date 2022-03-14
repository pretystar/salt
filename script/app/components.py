# from flask_sqlalchemy import SQLAlchemy
from flask import g, current_app
from app.utils.salt import SaltApi

def get_saltapi():
    if 'saltapi' not in g:
        g.saltapi = SaltApi(current_app.config["SALT_URL"],current_app.config["SALT_USER"],current_app.config["SALT_PASS"])
        # g.db.row_factory = sqlite3.Row

    return g.saltapi

