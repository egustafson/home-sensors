# -*- coding: utf-8 -*-
""" pytest fixtures """


import pytest

from codex.restapp import create_app

@pytest.fixture
def app():
    app = create_app({'TESTING': True,
                      'DEBUG': True,
                      'ENV': 'testing' })
    return app

@pytest.fixture
def client(app):
    return app.test_client()

