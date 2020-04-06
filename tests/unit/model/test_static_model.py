from unittest.mock import call, Mock, patch

from model.static import StaticModel
from model.parse_stack import Stack
from persistence.persistence import Persistence


def test_empty_model():
    persistence = Persistence()
    model = StaticModel(persistence)

    assert model._persistence == persistence


@patch('model.static.parse_stack', return_value=Stack(nodes='dummy_nodes', edges='dummy_edges'))
def test_load_text(parse_stack):
    persistence = Mock()
    persistence.get_nodes.return_value = {}
    model = StaticModel(persistence)

    model.load_text('first\nstack\n\nsecond\nstack')

    assert persistence.load_edges.call_args == call('dummy_edges')
    assert persistence.load_edges.call_count == 2
    assert persistence.load_nodes.call_args == call('dummy_nodes')
    assert persistence.load_nodes.call_count == 2
