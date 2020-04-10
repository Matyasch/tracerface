from pathlib import Path
from unittest.mock import call, Mock, patch

from model.static import StaticModel
from model.parse_stack import Stack


def test_model_initialization():
    persistence = Mock()
    model = StaticModel(persistence)

    assert model._persistence == persistence


def test_load_output():
    test_file_path = Path.cwd().joinpath(
        'tests', 'integration', 'resources', 'test_static_output'
    )
    persistence = Mock()
    persistence.get_nodes.return_value = {}
    model = StaticModel(persistence)

    model.load_output(str(test_file_path))

    assert persistence.load_edges.call_count == 8
    assert persistence.load_nodes.call_count == 8
