# -*- coding: utf-8 -*-
""" healthz endpoint """

from flask import Blueprint
from flask import jsonify

###

class Healthz():

    def status(self):
        return { 'status': "ok" }

###

_healthz = Healthz()

def get_healthz():
    return _healthz


blueprint = Blueprint('healthz', __name__)

@blueprint.route('/healthz')
def healthz():
    status = get_healthz().status()
    return jsonify(status)


