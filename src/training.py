#!/usr/bin/env python3

import numpy as np
import logging
from sklearn.neural_network import MLPClassifier
from src.residue import ResidueFactory
from src.settings import Settings

logger = logging.getLogger(__name__)


class Training:
    def __init__(self, dataset_type: str = 'q_s_tab1'):
        self.dataset_type = dataset_type
        self.X_data: np.ndarray = None
        self.Y_data: np.ndarray = None
        self.pdb_lst: list = []
        self.classifier = None

    def preprocess(self):
        """Fetch PDB IDs of the files to use in training. Load the DSSP data from each file,
        process it, and append to data array."""
        factory = ResidueFactory(pdb_id_lst=self.pdb_lst)
        data: dict = factory.construct()
        logger.info(f'Preprocessing {len(data)} DSSP files...')
        # data = self.triage_residue_instances(data=data)
        first = True
        for obj in data.values():
            if first:
                self.X_data = obj.X_data
                self.Y_data = obj.Y_data
                first = False
            else:
                self.X_data = np.concatenate((self.X_data, obj.X_data))
                self.Y_data = np.concatenate((self.Y_data, obj.Y_data))

    def train(self):
        number_hidden_units = 13
        number_hidden_layers = 2
        self.classifier = MLPClassifier(
            solver='lbfgs',
            alpha=1e5,
            hidden_layer_sizes=(number_hidden_units, number_hidden_layers),
            random_state=1
        )
        self.classifier.fit(self.X_data, self.Y_data)

    def get_pdb_lst(self):
        filepath = Settings.q_s_tab1
        with open(file=filepath, mode='r') as fp:
            for line in fp.readlines():
                line = line.strip('\n')
                self.pdb_lst.append(line)

    def triage_residue_instances(self, data: dict) -> dict:
        """Removes residues instances from data that (for reasons unknown to me) have no data in their
        X_data or Y_data. I didn't pursue the reasons for it any further. Even without the triaged data
        there are >70 proteins in left to train on..."""
        triage_lst = []
        for name, object in data.items():
            if object.residue_count == 0:
                logger.info(f'Instance {name} contains {object.residue_count} residue - triaging')
                triage_lst.append(name)
        for obj in triage_lst:
            data.pop(obj)
        return data