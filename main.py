#!/usr/bin/env python3
import argparse
import json
from pathlib import Path
import sys

from model import Model
from persistence import Persistence
from viewmodel import ViewModel
from view import View


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


if __name__ == '__main__':
    view.app.run_server(debug=True)