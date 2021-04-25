#!/usr/bin/env python3

import unittest
from unittest.mock import patch, PropertyMock
from src.read_dssp import ReadDSSP


class TestReadDSSP(unittest.TestCase):

    def setUp(self) -> None:
        self.dssp_test_filename = '1tes'
        self.dssp_path = './test'
        self.dssp_line0 = '   77   77 A P  H  > S+     0   0   71      0, 0.0     4,-0.5     0, 0.0    -1,-0.2   0.929 113.9  31.6 -45.4 -53.8  106.3   51.0    1.3                A         A         77         77          0          0          0          4          0         -1\n'
        self.dssp_line2 = '    1  307 A A    >         0   0   56      0, 0.0     3,-0.7     0, 0.0    58,-0.0   0.000 360.0 360.0 360.0 -50.8   15.6  -14.4  -34.4                A         A          1        307          0          0          0          3          0         58\n'

    def test_extract_info_from_line_happy(self):
        aa, structure, tag = ReadDSSP.extract_info_from_line(self.dssp_line0)
        self.assertTrue('P' in aa)
        self.assertTrue('H' in structure)
        self.assertTrue('OKAY' in tag.name)

    def test_extract_info_from_line_no_structure(self):
        aa, structure, tag = ReadDSSP.extract_info_from_line(self.dssp_line2)
        self.assertTrue('A' in aa)
        self.assertTrue(structure.isspace())
        self.assertTrue('NO_STRUCTURE' in tag.name)

    def test_read_happy(self):
        with patch('src.settings.Settings.dssp_path', new_callable=PropertyMock) as prop:
            prop.return_value = self.dssp_path
            lst = ReadDSSP.read(self.dssp_test_filename)
            self.assertFalse(lst == [])
            self.assertTrue(isinstance(lst[0], tuple))
            self.assertTrue(lst[0].amino_acid == 'P')
            self.assertTrue(lst[0].category == 'c')

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
