#!/usr/bin/env python3
from argparse import ArgumentParser
import sys

from tracerface.startup import start


def parse_args(args):
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('--debug', action='store_true', help='Start server in debug mode')
    parser.add_argument('--routes-logging', action='store_true', help='Show routes access logging in the console')
    return parser.parse_args(args)


# Create resources and start application
def main(args):
    parsed_args = parse_args(args)
    start(debug=parsed_args.debug, logging=parsed_args.routes_logging)


if __name__ == '__main__':
    main(sys.argv[1:])
