import unittest.mock as mock

from model.static import StaticModel
from model.utils import Graph


@mock.patch('model.base.Persistence')
def test_initialization(persistence):
    config = mock.Mock()
    model = StaticModel(config)

    assert model._persistence is persistence.return_value
    assert model._configuration is config


@mock.patch('model.static.text_to_stacks', return_value=['dummy', 'stack'])
@mock.patch('model.static.parse_stack', return_value=Graph(nodes='dummy_nodes', edges='dummy_edges'))
@mock.patch('model.base.Persistence')
def test_load_text(persistence, parse_stack, text_to_stacks):
    model = StaticModel(None)

    model.load_text('dummy text')

    text_to_stacks.assert_called_once()
    text_to_stacks.assert_called_with('dummy text')

    assert parse_stack.call_args_list == [mock.call('dummy'), mock.call('stack')]
    assert parse_stack.call_count == 2

    assert persistence.return_value.load_edges.call_args == mock.call('dummy_edges')
    assert persistence.return_value.load_edges.call_count == 2

    assert persistence.return_value.load_nodes.call_args == mock.call('dummy_nodes')
    assert persistence.return_value.load_nodes.call_count == 2