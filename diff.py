#!/bin/env python3

import sys
import argparse
import logging
from pprint import pprint

import tclib.library

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
    parser.add_argument(
        '--no-headers',
        help="Print only diffed items. This is useful when using both --only- switches",
        action="store_true",
    )
    items_group = parser.add_mutually_exclusive_group()
    items_group.add_argument(
        '--only-testplans',
        action='store_const',
        dest='items',
        const=('testplans',),
        default=('testplans', 'requirements', 'testcases',),
        help="Print information about testplans only",
    )
    items_group.add_argument(
        '--only-requirements',
        action='store_const',
        dest='items',
        const=('requirements',),
        default=('testplans', 'requirements', 'testcases',),
        help="Print information about requirements only",
    )
    items_group.add_argument(
        '--only-testcases',
        action='store_const',
        dest='items',
        const=('testcases',),
        default=('testplans', 'requirements', 'testcases',),
        help="Print information about testcases only",
    )
    states_group = parser.add_mutually_exclusive_group()
    states_group.add_argument(
        '--only-added',
        action='store_const',
        dest='states',
        const=('added',),
        default=('added', 'modified', 'unchanged', 'removed',),
        help="Print added items only",
    )
    states_group.add_argument(
        '--only-modified',
        action='store_const',
        dest='states',
        const=('modified',),
        default=('added', 'modified', 'unchanged', 'removed',),
        help="Print modified items only",
    )
    states_group.add_argument(
        '--only-unchanged',
        action='store_const',
        dest='states',
        const=('unchanged',),
        default=('added', 'modified', 'unchanged', 'removed',),
        help="Print unchanged items only",
    )
    states_group.add_argument(
        '--only-removed',
        action='store_const',
        dest='states',
        const=('removed',),
        default=('added', 'modified', 'unchanged', 'removed',),
        help="Print removed items only",
    )
    states_group.add_argument(
        '--only-added-modified',
        action='store_const',
        dest='states',
        const=('added', 'modified',),
        default=('added', 'modified', 'unchanged', 'removed',),
        help="Print added and modified items only",
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
    o = tclib.library.Library(args.old)
    n = tclib.library.Library(args.new)

    diff = tclib.library.diff(o, n)
    if args.no_headers:
        fmt = '{}'
    else:
        fmt = ' {}'
    for state in args.states:
        for item in args.items:
            if not args.no_headers:
                print(f'{state.upper()} {item}:')
            for entry in diff[state][item]:
                print(fmt.format(entry))

if __name__ == "__main__":
    sys.exit(main(*sys.argv[1:]))
