#!/usr/bin/env python3

import os
import logging
import argparse
import time
from src.training import Training
from src.predict import Predict
from joblib import dump


def main():

    logger = initiate_logging()
    logger.info("Welcome to pred-sec-struc!")

    args = argparser()

    if args.train or args.train_predict or args.train_write:
        start = time.time()
        dataset_type = 'q_s_tab1'  # Quian and Sejnowski data set from their table 1
        model = Training(dataset_type=dataset_type)
        model.get_pdb_lst()
        model.preprocess()
        model.train()
        if args.train_write:
            model_dir = './models'
            if not os.path.exists(model_dir):
                os.makedirs(model_dir)
            filename = os.path.join(model_dir, 'neural_net.model')
            logger.info(f'Writing model to {filename}')
            dump(model, filename)

        logger.info('Generated multi-layer neural network model...')
        logger.info(f'That took {get_elapsed_time(start_time=start)} min')

    if args.train_predict:
        predict = Predict(pdb_id=args.pdb.lower(), model=model)
        predict.predict()
        predict.accuracy()


def argparser():
    parser = argparse.ArgumentParser(
        description='pred-sec-struc: API to predict the secondary structure of an amino acid sequence.'
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        '-t', '--train-model', default=False, action='store_true', dest='train',
        help='train a neural network model'
    )
    group.add_argument(
        '-tw', '--train-write', default=False, action='store_true', dest='train_write',
        help='train a neural network model and write model to disk'
    )
    group.add_argument(
        '-tp', '--train-predict', default=False, action='store_true', dest='train_predict',
        help='train a neural network model and predict structure (requires [pdb])'
    )
    parser.add_argument(
        'pdb', nargs='?', help='a PDB ID whose structure is predicted'
    )


    return parser.parse_args()



def initiate_logging() -> logging.Logger:
    logfile_name = 'main.log'
    logging.basicConfig(filename=logfile_name, filemode='w', format = '%(asctime)s - %(message)s', level = logging.INFO)
    return logging.getLogger(__name__)


def get_elapsed_time(start_time):
    return round((time.time() - start_time) / 60)


if __name__ == "__main__":
    main()