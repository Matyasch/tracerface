#!/usr/bin/env python3
import argparse
import json
from pathlib import Path
import sys

import dash
from dash.dependencies import Input, Output, State

from model import Model
from persistence import Persistence
from viewmodel import ViewModel
import view.layout as layout
from webapp import WebApp


def parse_args(args):
    parser = argparse.ArgumentParser()
    parser.add_argument('--output',
        type=Path,
        help='path to callgrind output-file')
    return parser.parse_args(args)


parsed_args = parse_args(sys.argv[1:])
persistence = Persistence()
model = Model(persistence)

model.initialize_from_output(parsed_args.output)

view_model = ViewModel(model)
web_app = WebApp(view_model)


@web_app.app.callback(Output('info-box', 'children'),
              [Input('graph', 'tapNodeData')])
def displayTapNodeData(data):
    return json.dumps(data, indent=2)


if __name__ == '__main__':
    web_app.app.run_server(debug=True)