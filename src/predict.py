#!/usr/bin/env python3

from src.residue import Residue


class Predict:
    def __init__(self, pdb_id, model):
        self.pdb_id = pdb_id
        self.model = model
        self.Y_data = None

    def predict(self):
        residue = Residue(pdb_id=self.pdb_id)
        residue.set_residue_and_structure()
        residue.get_category_frequencies()
        residue.get_X_and_Y_arrays()
        self.Y_data = residue.Y_data

    def accuracy(self):
        print(self.Y_data)
