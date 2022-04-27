#!/bin/env python3

import sys
import argparse
import logging
from tclib.library import Library

# ordered dict

def cli_parser():
    parser = argparse.ArgumentParser(
        description='Validate testplan data by trying to create testcase library.',
    )
    parser.add_argument(
        'directory',
        help="Directory where requirements and testcases are located.",
    )
    verbosity = parser.add_mutually_exclusive_group()
    verbosity.add_argument(
        '-d', '--debug',
        action="store_true",
        help="Turn on debugging in tclib.",
    )
    verbosity.add_argument(
        '-q', '--quiet',
        action="store_true",
        help="Run logging in quiet mode: show tclib errors and failures only.",
    )
    return parser

def main():
    in_args=sys.argv[1:]
    args = cli_parser().parse_args(in_args)
    loglevel = logging.INFO
    logformat = "%(levelname)-8s: %(message)s"
    if args.debug:
        loglevel = logging.DEBUG
        logformat = "%(name)s(%(levelname)s): %(message)s"
    elif args.quiet:
        loglevel = logging.ERROR
    logging.basicConfig(
        level=loglevel,
        format=logformat,
    )
    Library(args.directory)
    return 0
