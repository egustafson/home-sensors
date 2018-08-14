#!/usr/bin/env python3
#
#
##

from flask import Flask
from flask import jsonify

app = Flask(__name__)


@app.route("/", methods=['GET'])
def landing():
    return "Codex CMDB"

## ##########

@app.route("/resource", methods=['GET'])
def resources():
    return "list resources"

@app.route("/resource/<uuid:rid>", methods=['GET'])
def get_resource(rid):
    return "resource({})".format(rid)

@app.route("/resource/<uuid:rid>/config")
def get_config(rid):
    return "resource config <{}>".format(rid)

## ##########

@app.route("/link", methods=['GET'])
def links():
    return "list links"

@app.route("/link/<uuid:lid>", methods=['GET'])
def get_link(lid):
    return "link({})".format(lid)

## ##########

@app.route("/query", methods=['POST'])
def query():
    return "query cmdb"

@app.route("/lookup", methods=['POST'])
def lookup():
    return "cmdb resource lookup."

## ####

@app.route("/healthz", methods=['GET'])
def healthz():
    return jsonify(status="OK")
