#!/usr/bin/env python3

import unittest
import numpy as np
from unittest.mock import patch, PropertyMock
from src.residue import Residue, ResidueFactory, AminoAcid, Target


class TestResidue(unittest.TestCase):
    def setUp(self) -> None:
        self.dssp_test_filename = '1tes'
        self.dssp_path = './test'
        Target.get_table()
        with patch('src.settings.Settings.dssp_path', new_callable=PropertyMock) as prop:
            prop.return_value = self.dssp_path
            self.residue = Residue(pdb_id=self.dssp_test_filename)
            self.residue.set_residue_and_structure()
            self.residue.get_category_frequencies()
            self.residue.get_X_and_Y_arrays()

    def test_set_residue_and_structure(self):
            self.assertEqual(len(self.residue.residue_and_structure), 506)
            self.assertEqual(self.residue.residue_and_structure[384].amino_acid, 'V')
            self.assertEqual(self.residue.residue_and_structure[176].category, 'a')

    def test_get_category_frequencies(self):
        self.assertTrue(self.residue.category_frequencies['a'] > 0.5)
        self.assertTrue(self.residue.category_frequencies['b'] == 0)
        self.assertTrue(self.residue.category_frequencies['c'] < 0.5)

    def test_X_array(self):
        self.assertTrue(isinstance(self.residue.X_data, np.ndarray))
        self.assertEqual(len(self.residue.X_data), 506)

    def test_Y_array(self):
        self.assertTrue(isinstance(self.residue.Y_data, np.ndarray))
        self.assertEqual(len(self.residue.Y_data), 506)


class TestResidueFactory(unittest.TestCase):
    def setUp(self) -> None:
        pdb_ids = ['1foo', '2bar', '3baz']
        self.factory = ResidueFactory(pdb_id_lst=pdb_ids)

    def test_construct(self):
        self.instance_dct = self.factory.construct()
        for residue_instance in self.instance_dct.values():
            #print(f'Instance name: {key}, Instance: {val}')
            self.assertIsInstance(residue_instance, Residue)

    def tearDown(self) -> None:
        del self.factory
        for inst in self.instance_dct.values():
            try:
                inst
            except NameError:
                continue
            else:
                del inst


class TestAminoAcid(unittest.TestCase):
    def test_get_table(self):
        expected = {
            '-': 0, 'A': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6, 'H': 7, 'I': 8, 'K': 9, 'L': 10, 'M': 11, 'N': 12,
            'P': 13, 'Q': 14, 'R': 15, 'S': 16, 'T': 17, 'V': 18, 'W': 19, 'Y': 20
        }
        AminoAcid.get_table()
        self.assertEqual(expected, AminoAcid.mapping)
        self.assertEqual(AminoAcid.mapping['S'], 16)


class TestTarget(unittest.TestCase):
    def test_get_table(self):
        Target.get_table()
        expected = ['a', 'b', 'c']
        self.assertEqual(list(Target.encoding.classes_), expected)
        self.assertEqual(Target.encoding.transform(['c'])[0], 2)


if __name__ == '__main__':
    unittest.main()
