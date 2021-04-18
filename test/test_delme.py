#!/usr/bin/env python3

import unittest
from src.delme import DelMe


class TestDelMe(unittest.TestCase):

    def test_somedef(self):
        expected = 42
        observed = DelMe.somedef()
        self.assertEqual(expected, observed)


if __name__ == "__main__":
    unittest
