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

    def predict(self):
        logger.info(f'Predicting structure of {self.pdb_id} using {self.model.__repr__()}')
        residue = Residue(pdb_id=self.pdb_id)
        residue.set_residue_and_structure()
        residue.get_category_frequencies()
        residue.get_X_and_Y_arrays()
        self.X_data = residue.X_data
        self.Y_data = residue.Y_data
        self.Y_data_pred = self.model.predict(self.X_data)

    def accuracy(self):
        n_elements: int = len(self.Y_data) - 1
        predicate_arr: list[bool] = []
        for i in range(n_elements):
            predicate_arr.append(all(self.Y_data[i] == self.Y_data_pred[i]))
        hits: int = sum(predicate_arr)
        perc_correct: float = round(((hits / n_elements) * 100), 2)
        logger.info(f'Model correctly predicted structure for {self.pdb_id} by {perc_correct}%')
