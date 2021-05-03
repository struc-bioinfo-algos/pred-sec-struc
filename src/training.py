#!/usr/bin/env python3

import numpy as np
import logging
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.metrics import multilabel_confusion_matrix
from src.residue import ResidueFactory
from src.settings import Settings
from src.residue import Target


logger = logging.getLogger(__name__)


class Training:
    def __init__(self, dataset_type: str = 'q_s_tab1'):
        self.dataset_type = dataset_type
        self.X_data: np.ndarray = None
        self.Y_data: np.ndarray = None
        self.pdb_lst: list = []
        self.classifier = None
        self.model = None
        self.n_hidden_units = 5
        self.n_hidden_layers = 3
        self.split_test_frac = 0.25  # fraction of data to be used for testing
        self.X_train: np.ndarray = None
        self.X_test: np.ndarray = None
        self.Y_train: np.ndarray = None
        self.Y_test: np.ndarray = None

    def preprocess(self):
        """Fetch PDB IDs of the files to use in training. Load the DSSP data from each file,
        process it, and append to data array."""
        factory = ResidueFactory(pdb_id_lst=self.pdb_lst)
        data: dict = factory.construct()
        logger.info(f'Preprocessing {len(data)} DSSP files...')
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
        logger.info(f'Training multi-layer perceptron with {self.n_hidden_layers}')
        self.classifier = MLPClassifier(
            solver='lbfgs',
            alpha=1e-5,
            hidden_layer_sizes=(self.n_hidden_units, self.n_hidden_layers),
            max_iter=2000,
            activation='relu',
            random_state=1,
            warm_start=True
        )
        self.get_split_data()
        self.model = self.classifier.fit(self.X_train, self.Y_train)
        logger.info(f'Model: {self.model.__repr__()}')

    def validate_model(self):
        predictions = self.model.predict(self.X_test)
        predictions, bugs = self.decode_onehot(classifications=predictions)
        y_test = np.delete(self.Y_test, bugs, 0)
        ground_truth, bugs = self.decode_onehot(classifications=y_test)
        logger.info(f'{classification_report(ground_truth, predictions)}')
        print(classification_report(ground_truth, predictions))
        confusion_matrix = multilabel_confusion_matrix(ground_truth, predictions)
        print('CONFUSION MATRICES')
        print('Alpha helix:')
        self.print_cm(confusion_matrix[:][0], labels=['Y', 'N'])
        print('Beta sheet:')
        self.print_cm(confusion_matrix[:][1], labels=['Y', 'N'])
        print('Coil:')
        self.print_cm(confusion_matrix[:][2], labels=['Y', 'N'])


    def get_pdb_lst(self):
        filepath = Settings.q_s_tab1
        with open(file=filepath, mode='r') as fp:
            for line in fp.readlines():
                line = line.strip('\n')
                self.pdb_lst.append(line)

    def get_classifier(self):
        self.classifier = MLPClassifier(
            solver='lbfgs',
            alpha=1e-5,
            hidden_layer_sizes=(self.n_hidden_units, self.n_hidden_layers),
            max_iter=1000,
            activation='relu',
            random_state=1,
            warm_start=True
        )

    def get_split_data(self) -> None:
        self.X_train, self.X_test, self.Y_train, self.Y_test = train_test_split(
            self.X_data,
            self.Y_data,
            test_size=self.split_test_frac,
            random_state=1
        )

    def decode_onehot(self, classifications: np.ndarray) -> tuple[list, list]:
        """Returns a list of character labels from encoded labels."""
        out: list = []
        bugs: list = []
        # ToDo: there's a bug where tuple(classification) == (0, 0, 0) - use conditional breakpoint to verify
        for i, classification in enumerate(classifications):
            try:
                out.append(Target.ohe2label[tuple(classification)])
            except KeyError:
                bugs.append(i)

        return out, bugs


    # Taken from: https://gist.github.com/zachguo/10296432
    @staticmethod
    def print_cm(confusion_mat, labels, hide_zeroes=False, hide_diagonal=False, hide_threshold=None):
        """Pretty print confusion matrix."""
        columnwidth = max([len(x) for x in labels] + [5])  # 5 is value length
        empty_cell = " " * columnwidth

        # Begin CHANGES
        fst_empty_cell = (columnwidth - 3) // 2 * " " + "t/p" + (columnwidth - 3) // 2 * " "

        if len(fst_empty_cell) < len(empty_cell):
            fst_empty_cell = " " * (len(empty_cell) - len(fst_empty_cell)) + fst_empty_cell
        # Print header
        print("    " + fst_empty_cell, end=" ")
        # End CHANGES

        for label in labels:
            print("%{0}s".format(columnwidth) % label, end=" ")

        print()
        # Print rows
        for i, label1 in enumerate(labels):
            print("    %{0}s".format(columnwidth) % label1, end=" ")
            for j in range(len(labels)):
                cell = "%{0}.1f".format(columnwidth) % confusion_mat[i, j]
                if hide_zeroes:
                    cell = cell if float(confusion_mat[i, j]) != 0 else empty_cell
                if hide_diagonal:
                    cell = cell if i != j else empty_cell
                if hide_threshold:
                    cell = cell if confusion_mat[i, j] > hide_threshold else empty_cell
                print(cell, end=" ")
            print()
