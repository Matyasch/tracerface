#!/usr/bin/env python3
import argparse
import json
import sys

import dash
import dash_html_components as html
from dash.dependencies import Input, Output, State

from model import Model
from pathlib import Path
from persistence import Persistence
from viewmodel import ViewModel
import view.layout as layout
from webapp import WebApp


def parse_args(args):
    parser = argparse.ArgumentParser()
    parser.add_argument('--binary',
        type=Path,
        help='path to binary to be profiled')
    parser.add_argument('--output',
        type=Path,
        help='path to callgrind output-file')

    return parser.parse_args(args)

parsed_args = parse_args(sys.argv[1:])
persistence = Persistence()
model = Model(persistence)

if parsed_args.binary:
    model.initialize_from_binary(parsed_args.binary, 'main')
else:
    model.initialize_from_output(parsed_args.output, 'main')

view_model = ViewModel(model)
WEB_APP = WebApp(view_model)


if __name__ == '__main__':
    WEB_APP.app.run_server(debug=True)