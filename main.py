#!/usr/bin/env python3
from model import Model
from persistence import Persistence
from viewmodel import ViewModel
from view import View


def main():
    persistence = Persistence()
    model = Model(persistence)
    view_model = ViewModel(model)
    view = View(view_model)
    view.app.run_server(debug=True)

if __name__ == '__main__':
    main()