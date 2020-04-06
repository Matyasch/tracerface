from pathlib import Path

from pytest import fixture

from tests.integration.asserts import assert_results
from viewmodel.trace_setup import Setup
from viewmodel.viewmodel import ViewModel


@fixture
def static_output():
    static_output_path = 'tests/integration/resources/test_static_output'
    return Path.cwd().joinpath(static_output_path).read_text()


def test_static_model(static_output):
    viewmodel = ViewModel(Setup())

    viewmodel.output_submit_btn_clicked(static_output)

    assert_results(viewmodel.get_nodes(), viewmodel.get_edges())
