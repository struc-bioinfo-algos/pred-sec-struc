#!/usr/bin/env python3

import os
import logging
import typing
from enum import Enum
from collections import namedtuple
from src.settings import Settings

logger = logging.getLogger(__name__)


class ReadDSSP:
    aa_single_letter_abbreviations: dict = {
        'A', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'W', 'Y'
    }
    structure_label_category_correspondence: dict = {'H': 'a', 'G': 'a', 'I': 'a', 'E': 'b'}
    header_line: str = '  #  RESIDUE AA STRUCTURE'
    aa_pos_start: int = 12
    aa_pos_end: int = 14
    struc_pos_start: int = 14
    struc_pos_end: int = 17
    ResidueAndCategory = typing.NamedTuple('ResidueAndStruc', [('amino_acid', str), ('category', str)])

    @classmethod
    def extract_info_from_line(cls, line: str) -> tuple:
        """Returns amino acid and corresponding structure from line in DSSP file."""
        aa = line[cls.aa_pos_start:cls.aa_pos_end].strip()
        structure = line[cls.struc_pos_start:cls.struc_pos_end].strip()

        if aa == '' or aa not in cls.aa_single_letter_abbreviations:
            tag = StructureTag.NO_AA
        elif aa == '!':
            tag = StructureTag.CHAIN_BREAK
        elif structure == '':
            tag = StructureTag.NO_STRUCTURE
        elif structure == '!*':
            tag = StructureTag.DISCONTINUITY
        elif aa == '' and structure == '':
            tag = StructureTag.NONE
        else:
            tag = StructureTag.OKAY

        return aa, structure, tag

    @classmethod
    def read(cls, pdb_id: str) -> list[namedtuple]:
        """Read DSSP file of PDB ID and return a list of (AA, structure label) tuples."""
        residue_and_category_lst = []
        filename = cls.get_filename(pdb_id=pdb_id)
        # logger.info(f'filename: {filename}')
        read_line = False
        try:
            with open(filename, 'r') as fp:
                for line in fp:
                    if line.startswith(cls.header_line):
                        read_line = True
                        continue
                    if read_line:
                        aa, structure, tag = cls.extract_info_from_line(line=line)
                        if tag.name == 'OKAY':
                            cat = cls.dssp_structure_to_category(structure_label=structure)
                            res_and_struc = cls.ResidueAndCategory(amino_acid=aa.strip().upper(), category=cat)
                            residue_and_category_lst.append(res_and_struc)
        except FileNotFoundError as err:
            logger.info(f'Error {err.errno}: File {filename} not found - check path in settings.ini')
            # logger.info(f'DSSP file {filename} may not be on disk')
            raise err

        return residue_and_category_lst

    @classmethod
    def dssp_structure_to_category(cls, structure_label: str) -> str:
        """Return DSSP label as one of three classes of alpha helix, beta strand, or coil.
        See https://swift.cmbi.umcn.nl/gv/dssp/ for details."""
        structure_label = structure_label.upper()
        if structure_label in cls.structure_label_category_correspondence.keys():
            return cls.structure_label_category_correspondence[structure_label]
        else:
            return 'c'

    @staticmethod
    def get_filename(pdb_id: str) -> str:
        return os.path.join(Settings.dssp_path, pdb_id) + Settings.dssp_extension

    @classmethod
    def handle_exceptions(cls, line):
        """Handles exceptions in line of DSSP file."""
        pass


class StructureTag(Enum):
    """For details: see https://swift.cmbi.umcn.nl/gv/dssp/"""
    OKAY = 0
    NO_AA = 1
    CHAIN_BREAK = 2
    DISCONTINUITY = 3
    NO_STRUCTURE = 4
    NONE = 5
