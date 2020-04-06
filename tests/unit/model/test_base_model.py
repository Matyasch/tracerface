from unittest.mock import call, Mock

from model.base import BaseModel
from persistence.persistence import Persistence


def test_empty_model():
    persistence = Mock()
    model = BaseModel(persistence)

    assert model._persistence == persistence


def test_get_nodes_gets_nodes_from_persistence():
    persistence = Mock()
    model = BaseModel(persistence)

    model.get_nodes()

    persistence.get_nodes.assert_called_once()


def test_get_edges_gets_edges_from_persistence():
    persistence = Mock()
    model = BaseModel(persistence)

    model.get_edges()

    persistence.get_edges.assert_called_once()


def test_yellow_count_gets_range_from_persistence():
    persistence = Mock()
    model = BaseModel(persistence)

    model.yellow_count()

    persistence.get_yellow.assert_called_once()


def test_red_count_gets_range_from_persistence():
    persistence = Mock()
    model = BaseModel(persistence)

    model.red_count()

    persistence.get_red.assert_called_once()


def test_max_count_gets_with_no_nodes():
    persistence = Mock()
    persistence.get_nodes.return_value = {}
    model = BaseModel(persistence)

    assert model.max_count() == 0


def test_max_count_gets_with_nodes():
    persistence = Mock()
    persistence.get_nodes.return_value = {
        'dummy_hash1': {'name': 'dummy_name1', 'source': 'dummy_source1', 'call_count': 2},
        'dummy_hash2': {'name': 'dummy_name2', 'source': 'dummy_source2', 'call_count': 5}
    }
    model = BaseModel(persistence)

    assert model.max_count() == 5


def test_set_range_calls_persistence_with_right_params():
    persistence = Mock()
    model = BaseModel(persistence)

    model.set_range('dummy_yellow', 'dummy_red')

    persistence.update_colors.assert_called_once()
    persistence.update_colors.assert_called_with('dummy_yellow', 'dummy_red')


def test_init_colors():
    persistence = Mock()
    model = BaseModel(persistence)
    model.max_count = Mock(return_value=8)

    model.init_colors()

    assert model.max_count.call_count == 2
    persistence.update_colors.assert_called_once()
    persistence.update_colors.assert_called_with(3, 5)
