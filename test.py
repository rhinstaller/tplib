#!/bin/env python3

import sys
import argparse
import logging
import yaml
import pprint
from testcases.structures.testcase import TestCase

def main(*in_args):
    parser = argparse.ArgumentParser(description='My awesome app.')
    parser.add_argument(
        'testcase_file',
        help="Some positional argument",
    )
    parser.add_argument(
        '-o', '--optional',
        action="store_true",
        help="Some optional switch.",
    )
    ...
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
    args = parser.parse_args(in_args)
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
    with open(args.testcase_file) as testcase_file:
        tc = TestCase(yaml.safe_load(testcase_file))
    print(tc.dump())
    #pprint.pprint(tc.data)

if __name__ == "__main__":
    sys.exit(main(*sys.argv[1:]))
