from pathlib import Path

from pytest import fixture

from persistence.configuration import Configuration
from tests.integration.asserts import assert_results
from viewmodel.viewmodel import ViewModel


@fixture
def static_output():
    static_output_path = 'tests/integration/resources/test_static_output'
    return Path.cwd().joinpath(static_output_path).read_text()


def test_static_model(static_output):
    configuration = Configuration()
    viewmodel = ViewModel(configuration)

    viewmodel.output_submit_btn_clicked(static_output)

    assert_results(viewmodel.get_nodes(), viewmodel.get_edges())
