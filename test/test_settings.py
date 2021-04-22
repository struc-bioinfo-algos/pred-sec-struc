#!/usr/bin/env python3

import os
import unittest
from src.settings import Settings


class TestSettings(unittest.TestCase):
    def test_settings(self):
        self.assertTrue(os.path.exists(Settings.dssp_path))
        self.assertEqual('.dssp', Settings.dssp_extension)


if __name__ == '__main__':
    unittest.main()
