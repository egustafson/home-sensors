# -*- coding: utf-8 -*-
"""CLI for Codex CMDB"""

import click
import json
import requests
import yaml

CODEX_URL = "http://localhost:5000"

@click.group()
def cli():
    pass

@click.command()
def info():
    click.echo("Codex-CMDB CLI")

@click.command()
def reset():
    url = "{}/reset".format(CODEX_URL)
    r = requests.get(url)
    if r.status_code == requests.codes.ok:
        click.echo("OK")
    else:
        r.raise_for_status()

@click.command()
def list():
    url = "{}/resource".format(CODEX_URL)
    r = requests.get(url)
    if r.status_code == requests.codes.ok:
        click.echo(r.text)
    else:
        r.raise_for_status()

@click.command()
@click.argument('id')
def get(id):
    url = "{}/resource/{}/config".format(CODEX_URL, id)
    r = requests.get(url)
    if r.status_code == requests.codes.ok:
        click.echo(r.text)
    elif r.status_code == 404:
        click.echo("CI(id:{}) does not exist".format(id))
    else:
        r.raise_for_status()

@click.command()
@click.argument('cfgfile', type=click.File('r'))
@click.argument('id')
def put(cfgfile, id):
    cfgdata = yaml.load(cfgfile)
    cfg = json.dumps(cfgdata, separators=(',',':'))
    print("PUT: {}".format(id))
    print("     {}".format(cfg))
    ##
    url = "{}/resource/{}/config".format(CODEX_URL, id)
    r = requests.put(url, json=cfgdata)
    if r.status_code == requests.codes.ok:
        click.echo(r.text)
    elif r.status_code == 404:
        click.echo("CI(id:{}) does not exist".format(id))
    else:
        r.raise_for_status()


## Commands
#
# discover "{json: value}"
# get      <oid>
# post     -f single-config.yml
# put      single-config.yml <oid>
# del      <oid>
# healthz
#
# list     ## return a list of the CI id's
# getci    <oid>
#

cli.add_command(info)
cli.add_command(reset)
cli.add_command(list)
cli.add_command(get)
cli.add_command(put)

if __name__ == '__main__':
    cli()
