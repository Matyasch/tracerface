#!/usr/bin/env python3
from argparse import ArgumentParser
import sys

from dash import Dash
from dash_bootstrap_components.themes import BOOTSTRAP

from tracerface.init_resources import initialize


def parse_args(args):
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('--debug', action='store_true', help='Start server in debug mode')
    parser.add_argument('--routes-logging', action='store_true', help='Show routes access logging in the console')
    return parser.parse_args(args)


# Create resources and start application
def main(args):
    parsed_args = parse_args(args)
    app = Dash(__name__, external_stylesheets=[BOOTSTRAP])
    initialize(app)
    silent = not parsed_args.routes_logging
    app.run_server(debug=parsed_args.debug, dev_tools_silence_routes_logging=silent)


if __name__ == '__main__':
    main(sys.argv[1:])
