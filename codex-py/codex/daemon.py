# -*- coding: utf-8 -*-
""" Daemon / Service for the Codex CMDB """

import click
import logging

from flask.helpers import get_debug_flag

from codex.cmdb import init_cmdb
from codex.webapp import create_app
from codex.mcast import McastThread
from codex.settings import DevConfig, ProdConfig

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

_mcast_thread = None
_webapp = None

def load_config():
    pass

def config_logging():
    ##
    ## TODO - actually config logging.
    ##
    ##   Assume logging.basicConfig was previously invoked and that
    ##  handlers do exist.
    pass

def start_mcast():
    global _mcast_thread
    _mcast_thread = McastThread()
    _mcast_thread.start()


def start_webapp():
    global _webapp
    CONFIG = DevConfig if get_debug_flag() else ProdConfig
    _webapp = create_app(CONFIG)
    _webapp.run(host="0.0.0.0", debug=get_debug_flag())


@click.command()
def main():
    try:
        logger.info("Codex CMDB initializing...")
        load_config()
        config_logging()
        logger.info("Codex CMDB running.")
        init_cmdb()
        start_mcast()
        start_webapp()
    except:
        logger.exception("Unanticipated exception - shutdown.")
    finally:
        logger.info("Codex CMDB exited.")

