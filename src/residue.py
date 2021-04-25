#!/usr/bin/env python3
import csv
from sklearn import preprocessing
from src.read_dssp import ReadDSSP
from src.settings import Settings

class Residue:

    def __init__(self, pdb_id: str = None):
        self.pdb_id: str = pdb_id
        self.read_seq = ReadDSSP
        self.residue_and_structure: list[tuple]

    def set_residue_and_structure(self):
        self.residue_and_structure = self.read_seq.read(pdb_id=self.pdb_id)


class ResidueFactory:
    def __init__(self):
        self.class_name = 'Residue'
        self.residue_lst: list = []

    def construct(self, instance_names: list) -> dict:
        return {instance_name: Residue(pdb_id=instance_name) for instance_name in instance_names}


class AminoAcid:
    mapping: dict = {}

    @classmethod
    def get_table(cls) -> dict:
        with open(Settings.amino_acids, 'r') as csvfile:
            rows = csv.DictReader(csvfile)
            for row in rows:
                cls.mapping[row['Single-letter-abbreviation']] = int(row['Encoding'])

class Target:
    mapping: dict = {}
    encoding: preprocessing.LabelEncoder

    @classmethod
    def get_table(cls) -> dict:
        # Todo: check whether it is advantageous to use sklearn's LabelEncoder here
        with open(Settings.target, 'r') as csvfile:
            rows = csv.DictReader(csvfile)
            for row in rows:
                cls.mapping[row['Abbreviation']] = row['Encoding']
        cls.encoding = preprocessing.LabelEncoder()
        cls.encoding.fit(list(cls.mapping.keys()))

