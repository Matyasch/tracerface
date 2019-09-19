#!/usr/bin/env python3
import argparse
import json
from pathlib import Path
import subprocess
import sys

import dash
import dash_html_components as html
from dash.dependencies import Input, Output, State

from persistence import Data
from model import Model
from viewmodel import ViewModel
import view.layout as layout
from webapp import WebApp


CALLGRIND_OUT_FILE_PATH = Path('assets/callgrind')
PARSED_OUT_FILE = Path('assets/parsed')

def parse_args(args):
    parser = argparse.ArgumentParser()
    parser.add_argument('--binary-path',
        type=Path,
        help='path to binary to be profiled',
        required=True)

    return parser.parse_args(args)


def main(args):
    parsed_args = parse_args(args)
    subprocess.run([
        'valgrind',
        '--tool=callgrind',
        '--dump-instr=yes',
        '--dump-line=yes',
        '--callgrind-out-file={}'.format(str(CALLGRIND_OUT_FILE_PATH)),
        './{}'.format(str(parsed_args.binary_path))
    ])
    data = Data()
    model = Model(data)
    view_model = ViewModel(model)
    web_app = WebApp(view_model)
    web_app.app.run_server(debug=True)

if __name__ == '__main__':
    main(sys.argv[1:])