#!/usr/bin/env python3

import logging


def main():

    logger = initiate_logging()
    logger.info("Welcome to pred-sec-struc!")


def initiate_logging() -> logging.Logger:
    logfile_name = 'main.log'
    logging.basicConfig(filename=logfile_name, format = '%(asctime)s - %(message)s', level = logging.INFO)
    return logging.getLogger(__name__)


if __name__ == "__main__":
    main()