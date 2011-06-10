# -*- coding: utf-8 -*-

import parser
import unittest
from testdata import testdata

class test(unittest.TestCase):
    def setUp(self):
        self.p = parser.Parser('data/nmea.yaml')

    def test_good(self):
        for sentence, nmea_id in testdata:
            data = self.p.parse(sentence)
            self.assertEqual(data['Type'], nmea_id)

    def test_fail(self):
        pass

if __name__ == '__main__':
    unittest.main()

