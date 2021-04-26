#!/usr/bin/env python3

import sys
import logging
import argparse
import time
from src.training import Training


def main():

    logger = initiate_logging()
    logger.info("Welcome to pred-sec-struc!")

    args = argparser()

    if args.generate:
        start = time.time()
        dataset_type = 'q_s_tab1'  # Quian and Sejnowski data set from their table 1
        model = Training(dataset_type=dataset_type)
        try:
            model.get_pdb_lst()
            model.preprocess()
            model.train()
        except TypeError:
            logger.error('option -g requires a PDB ID as argument')
            sys.exit()

        logger.info('Generated multi-layer neural network model...')
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

    return parser.parse_args()



def initiate_logging() -> logging.Logger:
    logfile_name = 'main.log'
    logging.basicConfig(filename=logfile_name, format = '%(asctime)s - %(message)s', level = logging.INFO)
    return logging.getLogger(__name__)


def get_elapsed_time(start_time):
        return round((time.time() - start_time) / 60)


if __name__ == "__main__":
    main()