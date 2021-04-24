#!/usr/bin/env python3

import os
from src.read_dssp import ReadDSSP
from src.settings import Settings

class Residue:

    def __init__(self, pdb_id: str):
        self.pdb_id: str = pdb_id
        self.read_seq = ReadDSSP
        self.residue_and_structure: list[tuple]

    def set_residue_and_structure(self):
        residue_and_structure = self.read_seq.read()
        #dssp_path = os.listdir(Settings.dssp_path)
        pass


class ResidueFactory:
    def __init__(self):
        self.class_name = 'Residue'
        self.residue_lst: list = []

    def construct(self, instance_names: list) -> dict:
        return {instance_name: Residue(pdb_id=instance_name) for instance_name in instance_names}
