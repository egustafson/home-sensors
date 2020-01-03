# -*- coding: utf-8 -*-
""" REST API Factory
    Uses:  Flask-RESTPlus (https://flask-restplus.readthedocs.io/en/stable/index.html)
    Core API definition in the 'apis' package.
"""

from flask import Flask
from codex.apis import api


class ProdConfig(object):
    ENV = 'production'
    DEBUG = False

class DevConfig(object):
    ENV = 'development'
    DEBUG = True

class TestConfig(object):
    ENV = 'testing'
    TESTING = True
    DEBUG = True



def create_app(cfg_obj=ProdConfig):

    app = Flask(__name__.split('.')[0])
    app.url_map.strict_slashes = False
    app.config.from_object(cfg_obj)

    api.init_app(app)  ## from 'codex.apis' package

    return app


## Note:  This package (when tested) obviates the following
##   settings.py
##   webapp.py

