#!/bin/env python3

import sys
import argparse
import logging
from pprint import pprint

import testcases.library

def cli_parser():
    parser = argparse.ArgumentParser(description='My awesome app.')
    parser.add_argument(
        'old',
        help="Directory containing old library (previous state)",
    )
    parser.add_argument(
        'new',
        help="Directory containing new library (desired state)",
    )
    verbosity = parser.add_mutually_exclusive_group()
    verbosity.add_argument(
        '-d', '--debug',
        action="store_true",
        help="Turn on debugging.",
    )
    verbosity.add_argument(
        '-q', '--quiet',
        action="store_true",
        help="Run in quiet mode: show errors and failures only.",
    )
    return parser

def main(*in_args):
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
    ...
    o = testcases.library.Library(args.old)
    n = testcases.library.Library(args.new)
    pprint(testcases.library.diff(o, n))

if __name__ == "__main__":
    sys.exit(main(*sys.argv[1:]))
