from unittest.mock import call, Mock, patch

from model.base import BaseModel


def test_empty_model():
    model = BaseModel()

    assert model.get_edges() == {}
    assert model.get_nodes() == {}


@patch('model.base.Persistence')
def test_get_nodes_gets_nodes_from_persistence(persistence):
    model = BaseModel()

    model.get_nodes()

    persistence.return_value.get_nodes.assert_called_once()


@patch('model.base.Persistence')
def test_get_edges_gets_edges_from_persistence(persistence):
    model = BaseModel()

    model.get_edges()

    persistence.return_value.get_edges.assert_called_once()


@patch('model.base.Persistence')
def test_yellow_count_gets_range_from_persistence(persistence):
    model = BaseModel()

    model.yellow_count()

    persistence.return_value.get_yellow.assert_called_once()


@patch('model.base.Persistence')
def test_red_count_gets_range_from_persistence(persistence):
    model = BaseModel()

    model.red_count()

    persistence.return_value.get_red.assert_called_once()


@patch('model.base.Persistence.get_nodes')
def test_max_count_gets_with_no_nodes(get_nodes):
    model = BaseModel()

    assert model.max_count() == 0


@patch('model.base.Persistence.get_nodes', return_value={
        'dummy_hash1': {'name': 'dummy_name1', 'source': 'dummy_source1', 'call_count': 2},
        'dummy_hash2': {'name': 'dummy_name2', 'source': 'dummy_source2', 'call_count': 5}
    })
def test_max_count_gets_with_nodes(get_nodes):
    model = BaseModel()

    assert model.max_count() == 5


@patch('model.base.Persistence')
def test_set_range_calls_persistence_with_right_params(persistence):
    model = BaseModel()

    model.set_range('dummy_yellow', 'dummy_red')

    persistence.return_value.update_colors.assert_called_once()
    persistence.return_value.update_colors.assert_called_with('dummy_yellow', 'dummy_red')


@patch('model.base.Persistence')
def test_init_colors(persistence):
    model = BaseModel()
    model.max_count = Mock(return_value=8)

    model.init_colors()

    assert model.max_count.call_count == 2
    persistence.return_value.update_colors.assert_called_once()
    persistence.return_value.update_colors.assert_called_with(3, 5)
