"""ScrapeData.py CLI app to pull data directly from data.seattle.gov"""

from os import path
import logging      # https://docs.python.org/3/library/logging.html
from logging.handlers import TimedRotatingFileHandler
import configparser # https://docs.python.org/3/library/configparser.html

import requests
from plumbum import cli     # http://plumbum.readthedocs.io/en/latest/cli.html
from sodapy import Socrata  # https://github.com/xmun0x/sodapy
import pandas as pd         # http://pandas.pydata.org/

HERE = path.abspath(path.dirname(__file__))
LOGGER = logging.getLogger('NULL')
LOGGER.addHandler(logging.NullHandler())
CONFIG = configparser.ConfigParser()

def build_logger(
        log_name,
        log_path,
        verbose=False
    ):
    """create a logger object for easier debug/logging

    Note:
        Temporary only, get more generic library later
        https://github.com/EVEprosper/ProsperCommon

    Args:
        log_name (str): name of logfile
        log_path (str): path to dump log to
        verbose (bool, optional): enable logging to STDOUT

    Returns:
        (:obj:`logging.logger`)

    """
    logger = logging.getLogger(log_name)

    log_abspath = path.join(log_path, log_name + '.log')
    general_handler = TimedRotatingFileHandler(
        log_abspath,
        when='midnight',
        interval=1,
        backupCount=30
    )
    formatter = logging.Formatter(
        '[%(asctime)s;%(levelname)s;%(filename)s;%(funcName)s;%(lineno)s] %(message)s'
    )
    general_handler.setFormatter(formatter)
    logger.addHandler(general_handler)
    logger.setLevel('INFO')

    if verbose:
        verbose_handler = logging.StreamHandler()
        verbose_formatter = logging.Formatter(
            '[%(levelname)s:%(filename)s--%(funcName)s:%(lineno)s] %(message)s'
        )
        verbose_handler.setFormatter(verbose_formatter)
        verbose_handler.setLevel('DEBUG')

        logger.addHandler(verbose_handler)

    return logger

def parse_configfile(
        path_to_config
):
    """parse config file for program defaults

    Args:
        path_to_config (str): path to configfile

    Returns:
        (:obj:`configparser.ConfigParser)

    """
    config_path = path_to_config
    local_config = path_to_config.replace('.cfg', '_local.cfg')
    if path.isfile(local_config):
        config_path = local_config

    config = configparser.ConfigParser(
        interpolation=configparser.ExtendedInterpolation(),
        allow_no_value=True,
        delimiters=('='),
        inline_comment_prefixes=('#')
    )

    with open(config_path, 'r') as cfg_fh:
        config.read_file(cfg_fh)

    return config

class ScrapeSeattle(cli.Application):
    """application to scrape data from data.seattle.gov

    MORE INFO: http://plumbum.readthedocs.io/en/latest/cli.html
    """

    debug = cli.Flag(
        ['d', '--debug'],
        help='debug mode: do not write to live database'
    )
    verbose = cli.Flag(
        ['v', '--verbose'],
        help='Enable verbose messaging'
    )

    config_path = path.join(HERE, 'my_config.cfg')
    @cli.switch(
        ['-c', '--config'],
        str,
        help='config file'
    )
    def update_config_file(self, config_path):
        """overwrite config_path"""
        self.config_path = config_path

    def main(self):
        """core app logic goes here"""
        global LOGGER
        global CONFIG

        LOGGER = build_logger(
            'scrapedata',
            HERE,
            self.verbose
        )
        CONFIG = parse_configfile(self.config_path)

        LOGGER.info('hello world')
        LOGGER.info('username=%s', CONFIG.get('AUTH', 'username'))

if __name__ == '__main__':
    ScrapeSeattle.run()
