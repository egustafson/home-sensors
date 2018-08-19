# -*- coding: utf-8 -*-
"""App factory for Flask"""

##
## -- DEPRECATED in favor of webapp.py --
##

from flask import Flask

from codex import view, healthz
from codex.settings import ProdConfig

def create_app(config_object=ProdConfig):
    """Flask applicaton factory
    """
    app = Flask(__name__.split('.')[0])

    app.url_map.strict_slashes = False
    app.config.from_object(config_object)

    app.register_blueprint(view.blueprint)
    app.register_blueprint(healthz.blueprint)
    return app

