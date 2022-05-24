#!/bin/env python3

import sys
import os
import argparse
import logging
import jinja2
from tplib.library import Library

def cli_parser():
    parser = argparse.ArgumentParser(
        description='Generate documents for testplans, requirements and/or testcases using jinja2 templates.',
        epilog="""
Examples:

 * Generate documents in the same directory where .j2 templates are:

  * ``./generate_documents.py path/to/library path/to/templates/dir``

 * Generate documents from .j2 templates in one directory and make them available in another directory:

  * ``./generate_documents.py path/to/library path/to/outdir``

""",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument(
        'library',
        help="Directory where requirements and testcases are located.",
    )
    parser.add_argument(
        'templates',
        help="Directory where jinja2 files are located.",
    )
    parser.add_argument(
        'outdir',
        nargs='?',
        help="Directory where generated documents should be stored. If not provided, the templates directory is used.",
    )
    verbosity = parser.add_mutually_exclusive_group()
    verbosity.add_argument(
        '-d', '--debug',
        action="store_true",
        help="Turn on debugging in tplib.",
    )
    verbosity.add_argument(
        '-q', '--quiet',
        action="store_true",
        help="Run logging in quiet mode: show tplib errors and failures only.",
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
    for fromfile, outfile in generate_documents(Library(args.library), args.templates, args.outdir or args.templates):
        print(f'Generating: "{outfile}" from "{fromfile}"')
    return 0

def generate_documents(library, templates_dir, outdir):
    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader([templates_dir])
    )
    for template_file in os.listdir(templates_dir):
        filename, extension = os.path.splitext(template_file)
        if extension != '.j2':
            continue
        yield template_file, filename
        rendered_filename = os.path.join(outdir, filename)
        template = env.get_template(template_file)
        with open(rendered_filename, 'w') as outfile:
            outfile.write(template.render(library=library))
