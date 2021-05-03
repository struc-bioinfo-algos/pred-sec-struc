#!/usr/bin/env python3

from sklearn.neural_network import MLPClassifier
from src.residue import Residue
import numpy as np
import logging

logger = logging.getLogger(__name__)


class Predict:
    def __init__(self, pdb_id: str, model: MLPClassifier):
        self.pdb_id = pdb_id
        self.model = model
        self.X_data: np.ndarray = None
        self.Y_data: np.ndarray = None
        self.Y_data_pred: np.ndarray = None
        self.n_samples = None

    def predict(self):
        logger.info(f'Predicting structure of {self.pdb_id} using {self.model.__repr__()}')
        residue = Residue(pdb_id=self.pdb_id)
        residue.set_residue_and_structure()
        residue.get_category_frequencies()
        residue.get_X_and_Y_arrays()
        # Print secondary structure fractions:
        print('FREQUENCIES:')
        print(f'alpha helix: {round(residue.category_frequencies["a"], 2) * 100}')
        print(f'beta sheet: {round(residue.category_frequencies["b"], 2) * 100}')
        print(f'coil: {round(residue.category_frequencies["c"], 2) * 100}')
        self.X_data = residue.X_data
        self.Y_data = residue.Y_data
        self.Y_data_pred = self.model.predict(self.X_data)

    def accuracy(self):
        predicate_arr: list[bool] = []
        self.n_samples = self._get_n_samples()
        for i in range(self.n_samples):
            predicate_arr.append(all(self.Y_data[i] == self.Y_data_pred[i]))
        hits: int = sum(predicate_arr)
        perc_correct: float = round(((hits / self.n_samples) * 100), 2)
        msg = f'Model correctly predicted structure for {self.pdb_id} by {perc_correct}%'
        logger.info(msg=msg)
        print(msg)

    def _get_n_samples(self):
        return len(self.Y_data) - 1
