#!/usr/bin/env python3

import os
from src.settings import Settings

class EncodeAminoAcids:

    def __init__(self, pdb_id):
        self.pdb_id = pdb_id

    def read_seq(self):
        #dssp_path = os.listdir(Settings.dssp_path)
        pass