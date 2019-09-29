#!/usr/bin/env python3
import argparse
import json
from pathlib import Path
import sys

import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc

from model import Model
from persistence import Persistence
from viewmodel import ViewModel
from webapp import WebApp


def parse_args(args):
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(help='Modes of usage', dest='mode')
    static_parser = subparsers.add_parser("static", help='Create call graph from output')
    realtime_parser = subparsers.add_parser("realtime", help='Profile given functions dinamically')
    static_parser.add_argument('--output',
        type=Path,
        help='Path to callgrind output-file'
    )
    realtime_parser.add_argument('--functions',
        help='Functions to profile',
        nargs='+'
    )
    return parser.parse_args(args)


parsed_args = parse_args(sys.argv[1:])
persistence = Persistence()
model = Model(persistence)

if parsed_args.mode == 'static':
    model.initialize_from_output(parsed_args.output)
else:
    model.start_trace(parsed_args.functions)

view_model = ViewModel(model)
web_app = WebApp(view_model)


@web_app.app.callback(Output('info-box', 'children'),
              [Input('interval-component', 'n_intervals')])
def update_metrics(n):
    return json.dumps(view_model.get_nodes()+[persistence.max_count], indent=2)

@web_app.app.callback(Output('graph', 'elements'),
              [Input('interval-component', 'n_intervals')])
def update_elements(n):
    return view_model.get_nodes() + view_model.get_edges()


if __name__ == '__main__':
    web_app.app.run_server(debug=True)