#!/usr/bin/env python3

import logging

logger = logging.getLogger(__name__)


class GenerateModel:

    def __init__(self, pdb_id):
        self.pdb_id = pdb_id

    def generate(self) -> dict:
        logger.info(f'Generating model for PDB ID {self.pdb_id}')

        return {}


