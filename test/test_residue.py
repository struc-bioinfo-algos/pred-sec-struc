#!/usr/bin/env python3

import unittest
from src.residue import Residue, ResidueFactory


class TestResidue(unittest.TestCase):
    pass


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


if __name__ == '__main__':
    unittest.main()
