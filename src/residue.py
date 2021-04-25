#!/usr/bin/env python3

import csv
from sklearn import preprocessing
from src.read_dssp import ReadDSSP
from src.settings import Settings


class Residue:
    def __init__(self, pdb_id: str = None):
        self.pdb_id: str = pdb_id
        self.is_setup: bool = False
        self.read_seq = ReadDSSP
        self.residue_and_structure: list[tuple] = []
        self.residue_count: int = 0
        self.category_frequencies: dict = {'a': 0, 'b': 0, 'c': 0}

    def set_residue_and_structure(self) -> list[tuple]:
        self.residue_and_structure = self.read_seq.read(pdb_id=self.pdb_id)
        self.residue_count = len(self.residue_and_structure)
        self.is_setup = True

    def get_category_frequencies(self):
        if not self.is_setup:
            pass
        for category in Target.sec_structure.values():
            count = self._get_frequency(category)
            self.category_frequencies[category] = count / self.residue_count

    def _get_frequency(self, category: str) -> int:
        count: int = 0
        for residue in self.residue_and_structure:
            if residue.category == category:
                count += 1
        return count

class ResidueFactory:
    def __init__(self, pdb_id_lst: list = []):
        self.instance_names: list = pdb_id_lst

    def construct(self) -> dict:
        return {instance_name: Residue(pdb_id=instance_name) for instance_name in self.instance_names}


class AminoAcid:
    mapping: dict = {}

    @classmethod
    def get_table(cls):
        with open(Settings.amino_acids, 'r') as csvfile:
            rows = csv.DictReader(csvfile)
            for row in rows:
                cls.mapping[row['Single-letter-abbreviation']] = int(row['Encoding'])


class Target:
    sec_structure: dict = {}
    mapping: dict = {}
    encoding: preprocessing.LabelEncoder

    @classmethod
    def get_table(cls):
        # Todo: check whether it is advantageous to use sklearn's LabelEncoder here
        with open(Settings.target, 'r') as csvfile:
            rows = csv.DictReader(csvfile)
            for row in rows:
                cls.sec_structure[row['Structure']] = row['Abbreviation']
                cls.mapping[row['Abbreviation']] = row['Encoding']
        cls.encoding = preprocessing.LabelEncoder()
        cls.encoding.fit(list(cls.mapping.keys()))

