#!/usr/bin/env python3

import configparser


config = configparser.ConfigParser()
config.read('settings.ini')


class Settings:
    """Static class to read settings.ini"""
    config = config
    dssp_path = config.get(section='PATHS', option='DsspPath')
    dssp_extension = config.get(section='PATHS', option='DsspExtension')
    amino_acids = config.get(section='PATHS', option='AminoAcidTable')
    target = config.get(section='LABELS', option='Target')
    q_s_tab1 = config.get(section='TRAINING', option='Q_S_1') # table 1 from Qian & Sejnowsky, 1988
