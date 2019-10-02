#!/usr/bin/env python3
import argparse
import json
from pathlib import Path
import sys

import dash
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

from model import Model
from persistence import Persistence
from viewmodel import ViewModel
from view import View
from webapp import WebApp


def parse_args(args):
    parser = argparse.ArgumentParser()
    parser.add_argument('--functions',
        help='Functions to profile',
        nargs='+',
    )
    return parser.parse_args(args)


parsed_args = parse_args(sys.argv[1:])
persistence = Persistence()
model = Model(persistence)

if parsed_args.functions:
    model.start_trace(parsed_args.functions)

view_model = ViewModel(model)
view = View(view_model)
web_app = WebApp(view)


@web_app.app.callback(Output('info-box', 'children'),
    [Input('output-button', 'n_clicks')],
    [State('output-textarea', 'value')])
def update_info(n, value):
    if not n:
        raise PreventUpdate
    else:
        model.initialize_from_text(value)
    return json.dumps(view_model.get_nodes()+[persistence.max_count], indent=2)


@web_app.app.callback(Output('graph', 'elements'),
    [Input('output-button', 'n_clicks'), Input('interval-component', 'n_intervals')],
    [State('output-textarea', 'value')])
def update_elements(n_click, n_int, value):
    if not n_click:
        raise PreventUpdate
    else:
        model.initialize_from_text(value)
    return view_model.get_nodes() + view_model.get_edges()


if __name__ == '__main__':
    web_app.app.run_server(debug=True)