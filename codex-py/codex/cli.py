# -*- coding: utf-8 -*-
"""CLI for Codex CMDB"""

import click
import json
import requests
import yaml

import codex.config
from codex.client import Client

DEFAULT_URL = "http://localhost:5000"

def print_json(j):
    click.echo(json.dumps(j, indent=2))


@click.group()
@click.option('-c','--config', default="codex.yml", type=click.File('r'))
@click.pass_context
def cli(ctx, config):
    ctx.ensure_object(dict)
    cfg = codex.config.load(config)
    ctx.obj['CONFIG'] = cfg
    ctx.obj['CLIENT'] = Client(cfg)

@click.command()
@click.pass_context
def reset(ctx):
    config = ctx.obj["CONFIG"]
    base_url = config.get('service-url', DEFAULT_URL)
    url = "{}/reset".format(base_url)
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

@click.command()
@click.pass_context
def dump(ctx):
    client = ctx.obj["CLIENT"]
    dd = []
    r = client.list()
    for cid in r:
        ci = client.get_config(cid)
        dd.append(ci)
    print_json(dd)

@click.command()
@click.argument('loadfile', type=click.File('r'))
@click.pass_context
def load(ctx, loadfile):
    client = ctx.obj["CLIENT"]
    loaddata = yaml.load(loadfile)
    for ci in loaddata:
        cid = ci.get("_id", None)
        if cid is not None:
            client.update_config(cid, ci)
        else:
            client.add_config(ci)
    click.echo("OK")

## Commands
#
# discover "{json: value}"
# list     ## return a list of the CI id's
# get      <oid>
# put      single-config.yml <oid>
# create   single-config.yml
## del      <oid>
# healthz
#
# dump     # dump the entire CMDB as vector of CI's
# load     dump-file.json

cli.add_command(reset)
cli.add_command(list)
cli.add_command(create)
cli.add_command(get)
cli.add_command(put)
cli.add_command(discover)
cli.add_command(healthz)
cli.add_command(dump)
cli.add_command(load)
