# -*- coding: utf-8 -*-
""" Daemon / Service for the Codex CMDB """

import click
import logging

from flask.helpers import get_debug_flag

from codex.cmdb import init_cmdb
from codex.webapp import create_app
from codex.mcast import McastThread
from codex.settings import DevConfig, ProdConfig
from codex.config import load as load_config

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

_mcast_thread = None
_webapp = None

def config_logging(cfg):
    ##
    ## TODO - actually config logging.
    ##
    ##   Assume logging.basicConfig was previously invoked and that
    ##  handlers do exist.
    pass

def start_mcast(cfg):
    global _mcast_thread
    _mcast_thread = McastThread(cfg)
    _mcast_thread.start()


def start_webapp(cfg):
    global _webapp
    CONFIG = DevConfig if get_debug_flag() else ProdConfig
    _webapp = create_app(CONFIG)
    addr = cfg.get("rest.listen", "0.0.0.0")
    port = cfg.get("rest.port", 5000)
    _webapp.run(host=addr, port=port, debug=get_debug_flag())


@click.command()
@click.option('-c','--config', default='codexd.yml', type=click.File('r'))
def main(config):
    try:
        logger.info("Codex CMDB initializing...")
        cfg = load_config(config)
        config_logging(cfg)
        logger.info("Codex CMDB running.")
        init_cmdb(cfg)
        start_mcast(cfg)
        start_webapp(cfg)
    except:
        logger.exception("Unanticipated exception - shutdown.")
    finally:
        logger.info("Codex CMDB exited.")

