from pathlib import Path
import subprocess
import time

from pytest import fixture

from tests.integration.asserts import assert_results
from viewmodel.trace_setup import Setup
from viewmodel.viewmodel import ViewModel


@fixture
def functions_to_trace():
    return {
        'func1': {'arg1': '%s', 'arg2': '%s'},
        'func2': {'arg1': '%d'},
        'func3': {}
    }


def test_dynamic_model_with_trace_dict(functions_to_trace):
    test_app = str(Path.cwd().joinpath('tests/integration/resources/test_application'))

    viewmodel = ViewModel(Setup())
    viewmodel.add_app(test_app)
    viewmodel.add_function(test_app, 'func1')
    viewmodel.add_function(test_app, 'func2')
    viewmodel.add_function(test_app, 'func3')
    viewmodel.add_parameter(test_app, 'func1', '1', '%s')
    viewmodel.add_parameter(test_app, 'func1', '2', '%s')
    viewmodel.add_parameter(test_app, 'func2', '1', '%d')

    viewmodel.trace_with_ui_elements() # start monitoring
    time.sleep(5) # BCC trace needs a bit of time to setup
    subprocess.run(test_app) # run monitored application
    viewmodel.trace_btn_turned_off() # stop monitoring

    assert_results(viewmodel.get_nodes(), viewmodel.get_edges())
