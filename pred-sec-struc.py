#!/usr/bin/env python3

import sys
import logging
import argparse
import time
from src.generate_model import GenerateModel


def main():

    logger = initiate_logging()
    logger.info("Welcome to pred-sec-struc!")
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
        help='generate a model (requires PDB ID)'
    )
    parser.add_argument(
        'PDBID', nargs='?', help='PDB ID of protein'
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