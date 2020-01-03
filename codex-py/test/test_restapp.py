# -*- coding: utf-8 -*-
""" UnitTest for constructing the Flask-RESTPlus app """

import unittest

from codex.restapp import create_app


class TestRestApp(unittest.TestCase):

    def test_restapp(self):
        rapp = create_app()
        self.assertIsNotNone(rapp)
