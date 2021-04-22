#!/usr/bin/env python3

import os
import configparser

PROJECT_ROOT = os.path.dirname(os.getcwd())


config = configparser.ConfigParser()
config.read(os.path.join(PROJECT_ROOT, 'settings.ini'))


class Settings:
    """Static class to read settings.ini"""
    config = config
    dssp_path = config['DEFAULT']['DsspPath']
    dssp_extension = config['DEFAULT']['DsspExtension']
