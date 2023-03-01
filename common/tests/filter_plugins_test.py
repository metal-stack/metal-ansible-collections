import unittest

from plugins.filter.common import parse_size, transpile_ignition_config
from plugins.filter.common import FilterModule


class UtilsFilterTest(unittest.TestCase):
    def test_all_filters_present(self):
        filters = FilterModule().filters()

        expected_filters = ["metal_lb_conf", "humanfriendly", "transpile_ignition_config"]

        for expected_filter in expected_filters:
            self.assertIn(expected_filter, filters)


class HumanfriendlyTest(unittest.TestCase):
    def test_parsing_size(self):
        actual = parse_size("1MB", binary=False)

        expected = 1000000

        self.assertEqual(expected, actual)

    def test_parsing_size_binary(self):
        actual = parse_size("1KB", binary=True)

        expected = 1024

        self.assertEqual(expected, actual)


class TranspileIgnitionTest(unittest.TestCase):
    def test_transpile_ignition_config(self):
        userdata = """
  storage:
    files:
     - path: /etc/sudoers.d/metal
       filesystem: root
       mode: 0600
       contents:
         inline: |
            metal ALL=(ALL) NOPASSWD: ALL
"""

        actual = transpile_ignition_config(userdata)

        expected = """
{"ignition":{"config":{},"security":{"tls":{}},"timeouts":{},"version":"2.2.0"},"networkd":{},"passwd":{},"storage":{"files":[{"filesystem":"root","path":"/etc/sudoers.d/metal","contents":{"source":"data:,metal%20ALL%3D(ALL)%20NOPASSWD%3A%20ALL%0A","verification":{}},"mode":384}]},"systemd":{}}
"""

        self.assertEqual(expected.strip(), actual.strip())
