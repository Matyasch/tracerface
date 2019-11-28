from pathlib import Path
import subprocess
import time

from pytest import fixture

from persistence.configuration import Configuration
from tests.integration.asserts import assert_results
from viewmodel.viewmodel import ViewModel


@fixture
def functions_to_trace():
    return {
        'func1': {'arg1': '%s', 'arg2': '%s'},
        'func2': {'arg1': '%d'},
        'func3': {}
    }


def test_dynamic_model_with_trace_dict(functions_to_trace):
    test_application_path = Path.cwd().joinpath('tests/integration/resources/test_application')
    to_trace = {}
    to_trace[str(test_application_path)] = functions_to_trace
    print(to_trace)

    configuration = Configuration()
    viewmodel = ViewModel(configuration)

    viewmodel.trace_with_ui_elements(to_trace) # start monitoring
    time.sleep(1) # BCC trace needs a bit of time to setup
    subprocess.run(str(test_application_path)) # run monitored application
    viewmodel.trace_btn_turned_off() # stop monitoring

    assert_results(viewmodel.get_nodes(), viewmodel.get_edges())
