import unittest.mock as mock

from model.static import StaticModel
from model.utils import Graph


def test_empty_model():
    model = StaticModel()

    assert model.get_edges() == {}
    assert model.get_nodes() == {}


@mock.patch('model.static.text_to_stacks', return_value=['dummy', 'stack'])
@mock.patch('model.static.parse_stack', return_value=Graph(nodes='dummy_nodes', edges='dummy_edges'))
@mock.patch('model.base.Persistence')
def test_load_text(persistence, parse_stack, text_to_stacks):
    model = StaticModel()

    model.load_text('dummy text')

    text_to_stacks.assert_called_once()
    text_to_stacks.assert_called_with('dummy text')

    assert parse_stack.call_args_list == [mock.call('dummy'), mock.call('stack')]
    assert parse_stack.call_count == 2

    assert persistence.return_value.load_edges.call_args == mock.call('dummy_edges')
    assert persistence.return_value.load_edges.call_count == 2

    assert persistence.return_value.load_nodes.call_args == mock.call('dummy_nodes')
    assert persistence.return_value.load_nodes.call_count == 2
