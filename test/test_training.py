#!/usr/bin/env python3

import unittest
import numpy as np
from src.training import Training


class TestTraining(unittest.TestCase):
    def setUp(self) -> None:
        self.training = Training(dataset_type='q_s_tab1')
        self.training.get_pdb_lst()
        self.training.preprocess()

    def test_get_pdb_lst(self):
        self.assertTrue(isinstance(self.training.pdb_lst, list))
        self.assertEqual(self.training.pdb_lst[0], '1acx')
        self.assertEqual(len(self.training.pdb_lst), 105)

    @unittest.skip("skip test")
    def test_preprocess(self):
        self.assertEqual(self.training.X_data.size, 4192461)
        self.assertEqual(self.training.Y_data.size, 46071)

    def test_decode_onehot(self):
        classifications = np.array([[0, 0, 1], [1, 0, 0], [0, 1, 0], [0, 1, 0], [0, 0, 1]])
        observed, _ = self.training.decode_onehot(classifications=classifications)
        expected = ['c', 'a', 'b', 'b', 'c']
        self.assertEqual(expected, observed)

    @unittest.skip
    def test_train(self):
        self.training.train()


if __name__ == '__main__':
    unittest.main()
