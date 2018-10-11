# -*- coding: utf-8 -*-
""" Daemon / Service for the Codex CMDB """

import click
import logging

from flask.helpers import get_debug_flag

from codex.webapp import create_app
from codex.settings import DevConfig, ProdConfig

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_config():
    pass

def config_logging():
    ##
    ## TODO - actually config logging.
    ##
    ##   Assume logging.basicConfig was previously invoked and that
    ##  handlers do exist.
    pass


def start_webapp():
    CONFIG = DevConfig if get_debug_flag() else ProdConfig
    webapp = create_app(CONFIG)
    webapp.run(host="0.0.0.0", debug=get_debug_flag())


@click.command()
def main():
    try:
        logger.info("Codex CMDB initializing...")
        load_config()
        config_logging()
        logger.info("Codex CMDB running.")
        start_webapp()
    except:
        logger.exception("Unanticipated exception - shutdown.")
    finally:
        logger.info("Codex CMDB exited.")

