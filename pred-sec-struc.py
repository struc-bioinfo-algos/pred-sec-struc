#!/usr/bin/env python3

import os
import sys
import logging
import argparse
import time
from src.settings import Settings
from src.training import Training
from src.predict import Predict
from joblib import dump, load


def main():

    logger = initiate_logging()
    logger.info("Welcome to pred-sec-struc!")
    logger.info(f'Window length: {Settings.window_length}')

    args = argparser()

    if args.train or args.train_predict:
        start = time.time()
        dataset_type = 'q_s_tab1'  # Quian and Sejnowski data set from their table 1
        model = Training(dataset_type=dataset_type)
        model.get_pdb_lst()
        model.preprocess()
        model.train()
        model.validate_model()

        # Persist model.
        model_dir = Settings.model_path
        if not os.path.exists(model_dir):
            os.makedirs(model_dir)
        filename = os.path.join(model_dir, 'neural_net.model')
        logger.info(f'Writing model to {filename}')
        dump(model, filename)

        logger.info('Generated multi-layer neural network model...')
        logger.info(f'That took {get_elapsed_time(start_time=start)} s')

    if args.train_predict or args.predict:
        if args.predict:
            if not 'model' in locals():  # load model from disk
                try:
                    model_dir = Settings.model_path
                    filename = os.path.join(model_dir, 'neural_net.model')
                    model = load(filename=filename)
                    logger.info(f'Loading model {filename} into memory.')
                except FileNotFoundError:
                    msg = 'No model found on disk. Run training first.'
                    print(msg)
                    sys.exit(logger.info(msg))

        try:
            predict = Predict(pdb_id=args.pdb.lower(), model=model.model)
        except AttributeError as err:
            msg = f'{err.__repr__()}: flag -tp requires a PDB ID as argument'
            logger.error(msg)
            sys.exit(msg)
        predict.predict()
        predict.accuracy()


def argparser():
    parser = argparse.ArgumentParser(
        description='pred-sec-struc: API to predict the secondary structure of an amino acid sequence.'
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        '-t', '--train-model', default=False, action='store_true', dest='train',
        help='train a neural network model and write to disk'
    )
    group.add_argument(
        '-tp', '--train-predict', default=False, action='store_true', dest='train_predict',
        help='train a neural network model and predict structure (requires [pdb])'
    )
    group.add_argument(
        '-p', '--predict', default=False, action='store_true', dest='predict',
        help='predict structure using the neural network model on disk (requires [pdb])'
    )
    parser.add_argument(
        'pdb', nargs='?', help='a PDB ID whose structure is predicted'
    )

    return parser.parse_args()


def initiate_logging() -> logging.Logger:
    logfile_name = 'main.log'
    # Include filemode='w' in next command?
    logging.basicConfig(filename=logfile_name, format='%(asctime)s - %(message)s', level=logging.INFO)
    return logging.getLogger(__name__)


def get_elapsed_time(start_time):
    return round(time.time() - start_time)


if __name__ == "__main__":
    main()
