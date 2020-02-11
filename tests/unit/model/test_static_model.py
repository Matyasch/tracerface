import unittest.mock as mock

from model.static import StaticModel
from model.base import Stack


def test_empty_model():
    model = StaticModel()

    assert model.get_edges() == {}
    assert model.get_nodes() == {}


@mock.patch('model.base.Persistence')
def test_load_text(persistence):
    model = StaticModel()
    model.parse_stack = mock.Mock(return_value=Stack(nodes='dummy_nodes', edges='dummy_edges'))

    model.load_text('first\nstack\n\nsecond\nstack')

    assert persistence.return_value.load_edges.call_args == mock.call('dummy_edges')
    assert persistence.return_value.load_edges.call_count == 2

    assert persistence.return_value.load_nodes.call_args == mock.call('dummy_nodes')
    assert persistence.return_value.load_nodes.call_count == 2
