# -*- coding: utf-8 -*-
"""Configuration definitions"""

class Config(object):
    """Base Configuration"""

    BOGUS_DETAIL = "bogus value"


class ProdConfig(Config):
    ENV = 'prod'
    DEBUG = False


class DevConfig(Config):
    ENV = 'dev'
    DEBUG = True


class TestConfig(Config):
    ENV = 'testing'
    TESTING = True
    DEBUG = True
