# -*- coding: utf-8 -*-
""" UnitTest load() of config objects """

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

class TestConfigLoad(unittest.TestCase):

    def test_load(self):
        c = load(TEST_CONFIG)
        self.assertIsNotNone(c)
        self.assertEqual(c["serial"], 10101)
        self.assertEqual(c["_identity"][0], "serial")
        # self.assertEqual(c["_identity[0]"], "serial")
        self.assertEqual(c["sensor.topic"], "topic-value")
        self.assertEqual(c["logging"]["mqtt-topic"], "logging-topic")
