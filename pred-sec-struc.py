#!/usr/bin/env python3

import sys
import logging
import argparse
import time
from src.residue import AminoAcid, Target
from src.generate_model import GenerateModel


def main():

    logger = initiate_logging()
    logger.info("Welcome to pred-sec-struc!")

    # Set up input and target encoding.
    AminoAcid.get_table()
    Target.get_table()

    args = argparser()

    if args.generate:
        start = time.time()
        model = GenerateModel(args.PDBID)
        try:
            data = model.generate()
        except TypeError:
            logger.error('option -g requires a PDB ID as argument')
            sys.exit()

        logger.info(f'That took {get_elapsed_time(start_time=start)} min')


def argparser():
    parser = argparse.ArgumentParser(
        description='pred-sec-struc: API to predict the secondary structure of an amino acid sequence.'
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        '-g', '--generate-model', default=False, action='store_true', dest='generate',
        help='generate a model (requires Training Data Set)'
    )
    parser.add_argument(
        'train', nargs='?', help='Training Data Set'
    )


    return parser.parse_args()



def initiate_logging() -> logging.Logger:
    logfile_name = 'main.log'
    logging.basicConfig(filename=logfile_name, format = '%(asctime)s - %(message)s', level = logging.INFO)
    return logging.getLogger(__name__)


def get_elapsed_time(start_time):
        return round((time.time() - start_time) / 60)


if __name__ == "__main__":
    main()