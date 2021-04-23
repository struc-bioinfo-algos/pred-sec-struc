#!/usr/bin/env python3

import os
import sys
import logging
from enum import Enum
from src.settings import Settings

logger = logging.getLogger(__name__)

class ReadDSSP():

    header_line = '  #  RESIDUE AA STRUCTURE'

    @classmethod
    def extract_info_from_line(cls, line: str) -> tuple:
        """Returns amino acid and corresponding structure from line in DSSP file."""
        aa = line[12:14]
        structure = line[14:17]

        if aa == '':
            tag = StructureTag.NO_AA.name
        elif structure == '':
            tag = StructureTag.NO_STRUCTURE.name
        elif aa == '' and structure == '':
            tag = StructureTag.NONE.name
        else:
            tag = StructureTag.OKAY.name

        return aa, structure, tag

    @classmethod
    def read(cls, pdb_id: str) -> list:
        """Read DSSP file of PDB ID"""
        aa_lst = []  # ToDo: make this a class (-> issue 12)
        filename = cls.get_filename(pdb_id=pdb_id)
        logger.info(f'filename: {filename}')
        read_line = False
        try:
            with open(filename, 'r') as fp:
                for line in fp:
                    if line.startswith(cls.header_line):
                        read_line = True
                        continue
                    if read_line:
                        aa_lst.append(line)
        except FileNotFoundError as err:
            logger.error(f'Error {err.errno}: File {filename} not found - please check path in settings.ini')
            sys.exit()

        return aa_lst

    @classmethod
    def dssp_structure_to_category(cls, label: str) -> str:
        """Return DSSP label as one of three classes of alpha helix, beta strand, or coil."""
        # https://swift.cmbi.umcn.nl/gv/dssp/
        label = label.upper()
        dct = cls.get_structure_label_category_correspondence()
        if label in dct.keys():
            return dct[label]
        else:
            return 'c'

    @staticmethod
    def get_filename(pdb_id: str) -> str:
        return os.path.join(Settings.dssp_path, pdb_id) + Settings.dssp_extension

    @classmethod
    def handle_exceptions(cls, line):
        """Handles exceptions in line of DSSP file."""
        pass

    @staticmethod
    def get_structure_label_category_correspondence() -> dict:
        """Returns a dictionary to map structure labels to the
        three classes we are interested in."""
        return {'H': 'a', 'G': 'a', 'I': 'a', 'E': 'b'}


class StructureTag(Enum):
    OKAY = 0
    NO_AA = 1
    NO_STRUCTURE = 2
    NONE = 3