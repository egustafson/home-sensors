# -*- coding: utf-8 -*-
""" Codex (CMDB) endpoints -- main app """

from flask import Blueprint


blueprint = Blueprint('codex', __name__)


@blueprint.route("/", methods=['GET'])
def landing():
    return "Codex CMDB"

## ##########

@blueprint.route("/resource", methods=['GET'])
def resources():
    return "list resources"

@blueprint.route("/resource/<uuid:rid>", methods=['GET'])
def get_resource(rid):
    return "resource({})".format(rid)

@blueprint.route("/resource/<uuid:rid>/config")
def get_config(rid):
    return "resource config <{}>".format(rid)

## ##########

@blueprint.route("/link", methods=['GET'])
def links():
    return "list links"

@blueprint.route("/link/<uuid:lid>", methods=['GET'])
def get_link(lid):
    return "link({})".format(lid)

## ##########

@blueprint.route("/query", methods=['POST'])
def query():
    return "query cmdb"

@blueprint.route("/lookup", methods=['POST'])
def lookup():
    return "cmdb resource lookup."
