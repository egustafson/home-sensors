# -*- coding: utf-8 -*-
""" UnitTest the /healthz endpoint """

import pytest

import json
#from codex.restapp import create_app
#
#@pytest.fixture
#def app():
#    app = create_app({'TESTING': True})
#    return app
#
#@pytest.fixture
#def client(app):
#    return app.test_client()



def test_healthz(client):
    response = client.get('/healthz/')
    msg = response.get_json()
    assert msg.get('status') == 'ok'

def test_healthz_noslash(client):
    response = client.get('/healthz')
    msg = response.get_json()
    assert msg.get('status') == 'ok'
