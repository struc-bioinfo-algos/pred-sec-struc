#!/usr/bin/env python3

import configparser

config = configparser.ConfigParser()
config.read('settings.ini')


class Settings:
    """Static class to read settings.ini"""

    dssp_path = config.get('DEFAULT', 'DSSP_PATH')

