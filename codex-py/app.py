# -*- coding: utf-8 -*-
"""bootstrap the application"""

from flask.helpers import get_debug_flag

from codex.app import create_app
from codex.settings import DevConfig, ProdConfig

CONFIG = DevConfig if get_debug_flag() else ProdConfig

app = create_app(CONFIG)

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=get_debug_flag())
