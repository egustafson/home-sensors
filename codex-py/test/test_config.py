# -*- coding: utf-8 -*-
""" UnitTest for config objects """

import unittest

from codex.config import load

TEST_CONFIG = """
_identity: [ serial ]
serial: 10101
sensor:
  topic: topic-value
logging:
  mqtt-topic: logging-topic
"""

class TestConfig(unittest.TestCase):

    def test_load(self):
        c = load(TEST_CONFIG)
        self.assertIsNotNone(c)
        self.assertEqual(c["_identity"][0], "serial")
