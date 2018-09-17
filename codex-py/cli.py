# -*- coding: utf-8 -*-
"""CLI for Codex CMDB"""

import click
import json
import requests
import yaml

from codex.client import Client

CODEX_URL = "http://localhost:5000"

def print_json(j):
    click.echo(json.dumps(j, indent=2))


@click.group()
@click.pass_context
def cli(ctx):
    ctx.obj['CLIENT'] = Client()

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
@click.pass_context
def list(ctx):
    client = ctx.obj["CLIENT"]
    r = client.list()
    if len(r) < 1:
        click.echo("[]")
    else:
        click.echo("[")
        for id in r:
            click.echo("  {}".format(id))
        click.echo("]")

@click.command()
@click.argument('cfgfile', type=click.File('r'))
@click.pass_context
def create(ctx, cfgfile):
    client = ctx.obj["CLIENT"]
    cfgdata = yaml.load(cfgfile)
    r = client.add_config(cfgdata)
    print_json(r)

@click.command()
@click.argument('id')
@click.pass_context
def get(ctx, id):
    client = ctx.obj["CLIENT"]
    r = client.get_config(id)
    if r is None:
        click.echo("No such CI")
    else:
        print_json(r)

@click.command()
@click.argument('cfgfile', type=click.File('r'))
@click.argument('id')
@click.pass_context
def put(ctx, cfgfile, id):
    client = ctx.obj["CLIENT"]
    cfgdata = yaml.load(cfgfile)
    r = client.update_config(id, cfgdata)
    print_json(r)

@click.command()
@click.argument('pattern')
@click.pass_context
def discover(ctx, pattern):
    client = ctx.obj["CLIENT"]
    p = json.loads(pattern)
    r = client.discover(p)
    print_json(r)

@click.command()
@click.pass_context
def healthz(ctx):
    client = ctx.obj["CLIENT"]
    r = client.healthz()
    print_json(r)

## Commands
#
# discover "{json: value}"
# get      <oid>
# post     single-config.yml
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
cli.add_command(create)
cli.add_command(get)
cli.add_command(put)
cli.add_command(discover)
cli.add_command(healthz)

if __name__ == '__main__':
    cli(obj={})
