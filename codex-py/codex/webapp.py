# -*- coding: utf-8 -*-
""" Web-App defnition and factory
     Uses: Flask & Flask-RESTFul
"""

from flask import Flask
from flask_restful import abort, Api, Resource

from codex import view, healthz
from codex.settings import ProdConfig

class CodexResourceList(Resource):
    def get(self):
        return {}

class CodexResource(Resource):
    def get(self, rid):
        return { 'placeholder': 'todo' }

class CodexLinkList(Resource):
    def get(self):
        return {}

class CodexLink(Resource):
    def get(self, lid):
        return { 'placeholder': 'todo-link-attr' }



def create_app(config_object=ProdConfig):
    """Flask applicaton factory
    """
    webapp = Flask(__name__.split('.')[0])
    restapi = Api(webapp)

#    webapp.url_map.strict_slashes = False
    webapp.config.from_object(config_object)

    restapi.add_resource(CodexResourceList, '/resource')
    restapi.add_resource(CodexResource, '/resource/<uuid:rid>')
    ##
    ## ...
    ##

#    webapp.register_blueprint(view.blueprint)
#    webapp.register_blueprint(healthz.blueprint)
    return webapp


