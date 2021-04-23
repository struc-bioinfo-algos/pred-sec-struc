#!/usr/bin/env python3

import unittest
from unittest.mock import patch
from src.settings import Settings
from src.read_dssp import ReadDSSP


class TestReadDSSP(unittest.TestCase):

    def setUp(self) -> None:
        #self.dssp_path = './test/1tes.dssp'
        self.dssp_line2 = '    1  307 A A    >         0   0   56      0, 0.0     3,-0.7     0, 0.0    58,-0.0   0.000 360.0 360.0 360.0 -50.8   15.6  -14.4  -34.4                A         A          1        307          0          0          0          3          0         58\n'

    def test_extract_info_from_line_no_structure(self):
        aa, dssp_classification, tag = ReadDSSP.extract_info_from_line(self.dssp_line2)

        print(aa, dssp_classification, tag)

    def test_read(self):
        #MockSettingsDsspPath.return_value = './test'
        lst = ReadDSSP.read('6vjd')
        for item in lst:
            #print(item)
            pass

    def test_dssp_label_to_category_alpha_helix(self):
        self.assertEqual(ReadDSSP.dssp_structure_to_category('H'), 'a')
        self.assertEqual(ReadDSSP.dssp_structure_to_category('I'), 'a')
        self.assertEqual(ReadDSSP.dssp_structure_to_category('G'), 'a')

    def test_dssp_label_to_category_beta_strand(self):
        self.assertEqual(ReadDSSP.dssp_structure_to_category('E'), 'b')

    def test_dssp_label_to_category_coil(self):
        self.assertEqual(ReadDSSP.dssp_structure_to_category('c'), 'c')


if __name__ == "__main__":
    unittest
