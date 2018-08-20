# -*- coding: utf-8 -*-
"""bootstrap the application"""

from flask.helpers import get_debug_flag

from codex.webapp import create_app
from codex.settings import DevConfig, ProdConfig


if __name__ == '__main__':
    CONFIG = DevConfig if get_debug_flag() else ProdConfig
    webapp = create_app(CONFIG)
    webapp.run(host="0.0.0.0", debug=get_debug_flag())
