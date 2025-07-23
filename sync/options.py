#!/usr/bin/env python3
'''
Runtime options
'''
import argparse


def parser():
    '''
    Load and parse command line arguments
    '''
    # Template
    parser = argparse.ArgumentParser(
            usage='python3 -m sync [-h] [actions] <options>',
            description='Synchronize sober.page data to/from various sources',
            epilog='[*] At least one script action must be specified.',
            formatter_class=lambda prog: argparse.HelpFormatter(
                prog, max_help_position=30))

    # Actions
    actions = parser.add_argument_group('actions[*]')
    actions.add_argument(
        '-c',
        dest='collect',
        action='store_true',
        help='Collect meeting data from remote feeds')
    actions.add_argument(
        '-n',
        dest='mapfile',
        action='store',
        metavar='<path>',
        help='Create an nginx map file and store at <path>')
    actions.add_argument(
        '-z',
        dest='zonefile',
        action='store',
        metavar='<path>',
        help='Create a bind9 zone file and store at <path>')

    # Options
    parser.add_argument(
        '-H',
        dest='hugo_data',
        action='store',
        metavar='<path>',
        default='./data/domains.yaml',
        help='Path to hugo file containing DNS data')
    parser.add_argument(
        '-w',
        dest='local_data',
        action='store',
        metavar='<path>',
        default='./_workspace',
        help='Local workspace used for importing/caching data')
    parser.add_argument(
        '-l',
        dest='loglevel',
        action='store',
        metavar='<level>',
        default='WARNING',
        help='Log level (DEBUG, INFO, WARNING*, ERROR)')

    return parser
