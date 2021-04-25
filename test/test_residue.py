#!/usr/bin/env python3

import unittest
from unittest.mock import patch, PropertyMock
from src.residue import Residue, ResidueFactory, AminoAcid, Target


class TestResidue(unittest.TestCase):
    def setUp(self) -> None:
        self.dssp_test_filename = '1tes'
        self.dssp_path = './test'

    def test_set_residue_and_structure(self):
        with patch('src.settings.Settings.dssp_path', new_callable=PropertyMock) as prop:
            prop.return_value = self.dssp_path
            residue = Residue(pdb_id=self.dssp_test_filename)
            residue.set_residue_and_structure()
            self.assertEqual(len(residue.residue_and_structure), 509)
            self.assertEqual(residue.residue_and_structure[384].amino_acid, 'K')
            self.assertEqual(residue.residue_and_structure[176].category, 'c')


class TestResidueFactory(unittest.TestCase):
    def setUp(self) -> None:
        self.pdb_ids = ['1foo', '2bar', '3baz']
        self.factory = ResidueFactory()

    def test_construct(self):
        self.instance_dct = self.factory.construct(instance_names=self.pdb_ids)
        for key, val in self.instance_dct.items():
            #print(f'Instance name: {key}, Instance: {val}')
            self.assertIsInstance(val, Residue)

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
            'A': 0, 'C': 1, 'D': 2, 'E': 3, 'F': 4, 'G': 5, 'H': 6, 'I': 7, 'K': 8, 'L': 9, 'M': 10,
            'N': 11, 'P': 12, 'Q': 13, 'R': 14, 'S': 15, 'T': 16, 'V': 17, 'W': 18, 'Y': 19
        }
        AminoAcid.get_table()
        self.assertEqual(expected, AminoAcid.mapping)
        self.assertEqual(AminoAcid.mapping['S'], 15)


class TestTarget(unittest.TestCase):
    def test_get_table(self):
        Target.get_table()
        expected = ['a', 'b', 'c']
        self.assertEqual(list(Target.encoding.classes_), expected)
        self.assertEqual(Target.encoding.transform(['c'])[0], 2)


if __name__ == '__main__':
    unittest.main()
