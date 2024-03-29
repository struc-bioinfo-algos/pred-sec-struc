#!/usr/bin/env python3

import csv
import numpy as np
import logging
from sklearn import preprocessing
from src.read_dssp import ReadDSSP
from src.settings import Settings

logger = logging.getLogger(__name__)

class Residue:
    def __init__(self, pdb_id: str = None, window_length: int = int(Settings.window_length)):
        self.pdb_id: str = pdb_id
        self.window_length: int = window_length
        self.central_aa_pos = int(np.ceil(self.window_length / 2))
        AminoAcid.get_table()
        self.amino_acids = AminoAcid.mapping
        Target.get_table()
        self.targets = Target.mapping
        self.is_setup: bool = False
        self.read_seq = ReadDSSP
        self.residue_and_structure: list[tuple] = []
        self.residue_count: int = 0
        self.category_frequencies: dict = {target: 0 for target in self.targets.keys()}
        self.X_data: np.array = None
        self.Y_data: np.array = None

    def set_residue_and_structure(self) -> None:
        self.residue_and_structure = self.read_seq.read(pdb_id=self.pdb_id)
        self.residue_count = len(self.residue_and_structure)
        self.is_setup = True

    def get_category_frequencies(self) -> None:
        if not self.is_setup:
            pass
        for category in Target.sec_structure.values():
            count = self._get_frequency(category)
            try:
                self.category_frequencies[category] = count / self.residue_count
            except ZeroDivisionError:
                self.category_frequencies[category] = 0

    def _get_frequency(self, category: str) -> int:
        count: int = 0
        for residue in self.residue_and_structure:
            if residue.category == category:
                count += 1
        return count

    def get_X_and_Y_arrays(self):
        """This constructs the X array that holds the features. Each row is of window length and
        referred to as a group. The number of groups in X corresponds to the number of residues in the
        protein, minus the window length."""
        if self.residue_count <= 0:
            return
        input_group_units = np.array(list(self.amino_acids.keys()))
        input_group_units_length = input_group_units.shape[0]

        ouput_units = np.array(list(self.targets.keys()))

        self.X_data = np.zeros((self.residue_count - self.window_length, self.window_length * input_group_units_length))
        self.Y_data = np.zeros((self.residue_count - self.window_length, len(ouput_units)))
        residue_counter = self.central_aa_pos # 0
        first_iteration = True
        while residue_counter < (self.residue_count - self.window_length):
            start = residue_counter - self.central_aa_pos
            stop = start + self.window_length
            unit_index = 0
            if first_iteration:
                for idx in range(start, stop):
                    current_aa = self.residue_and_structure[idx].amino_acid
                    current_units = self.get_onehot_encoded_label(target_units=input_group_units, label=current_aa)

                    x_start_range = unit_index * input_group_units_length
                    x_end_range = x_start_range + input_group_units_length

                    self.X_data[residue_counter][x_start_range:x_end_range] = current_units
                    unit_index += 1
                    first_iteration = False
            else:
                current_aa = self.residue_and_structure[idx].amino_acid
                current_units = self.get_onehot_encoded_label(target_units=input_group_units, label=current_aa)

                self.X_data[residue_counter] = np.append(
                    self.X_data[residue_counter-1][input_group_units_length:],
                    current_units
                )
            
            # Get Y-data:
            category = self.residue_and_structure[residue_counter].category
            self.Y_data[residue_counter] = self.get_onehot_encoded_label(target_units=ouput_units, label=category)

            residue_counter += 1

    def _get_numerical_val_for_amino_acid(self, index: int) -> int:
        """Returns numerical value for an amino acid as defined in amino_acids.csv."""
        return self.amino_acids[self.residue_and_structure[index].amino_acid]

    def _get_numerical_val_for_category(self, index: int) -> int:
        """Returns numerical value for category as defined in target.csv."""
        return self.targets[self.residue_and_structure[index].category]

    def get_onehot_encoded_label(self, target_units: np.ndarray, label: str) -> np.ndarray:
        return np.where(target_units == label, 1, 0)


class ResidueFactory:
    """Returns a dictionary of Residue instances for a list PDB IDs."""
    def __init__(self, pdb_id_lst: list = None):
        self.instance_names: list = pdb_id_lst

    def construct(self) -> dict:
        residues: dict = {}
        for instance_name in self.instance_names:
            try:
                residue_instance = Residue(pdb_id=instance_name) 
                residue_instance.set_residue_and_structure()
                residue_instance.get_category_frequencies()
                residue_instance.get_X_and_Y_arrays()
                residues[instance_name] = residue_instance
            except:
                logger.info(f'Error creating residue {instance_name}')
                continue

        return residues


class AminoAcid:
    mapping: dict = {}

    @classmethod
    def get_table(cls) -> None:
        with open(Settings.amino_acids, 'r') as csvfile:
            rows = csv.DictReader(csvfile)
            for row in rows:
                cls.mapping[row['Single-letter-abbreviation']] = int(row['Encoding'])


class Target:
    sec_structure: dict = {}
    mapping: dict = {}
    encoding: preprocessing.LabelEncoder
    ohe2label: dict = {
        (1, 0, 0): 'a',
        (0, 1, 0): 'b',
        (0, 0, 1): 'c'
    }

    @classmethod
    def get_table(cls) -> None:
        # Todo: check whether it is advantageous to use sklearn's LabelEncoder here
        with open(Settings.target, 'r') as csvfile:
            rows = csv.DictReader(csvfile)
            for row in rows:
                cls.sec_structure[row['Structure']] = row['Abbreviation']
                cls.mapping[row['Abbreviation']] = int(row['Encoding'])
        cls.encoding = preprocessing.LabelEncoder()
        cls.encoding.fit(list(cls.mapping.keys()))

