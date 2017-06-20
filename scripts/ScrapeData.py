"""ScrapeData.py CLI app to pull data directly from data.seattle.gov"""

from os import path
import logging
import configparser

import requests
from plumbum import cli
from sodapy import Socrata

## vv TODO vv
# import logging
## ^^ TODO ^^
HERE = path.abspath(path.dirname(__file__))

def build_logger(
        log_name,
        log_path,
        verbose=False
    ):
    """create a logger object for easier debug/logging

    Args:
        log_name (str): name of logfile
        log_path (str): path to dump log to
        verbose (bool, optional): enable logging to STDOUT

    Returns:
        (:obj:`logging.logger`)

    """
    pass

def parse_configfile(
        path_to_config
):
    """parse config file for program defaults

    Args:
        path_to_config (str): path to configfile

    Returns:
        (:obj:`configparser.ConfigParser)

    """
    pass

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
        pass


if __name__ == '__main__':
    ScrapeSeattle.run()
