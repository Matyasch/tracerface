from pathlib import Path
from pytest import raises
from queue import Empty
from unittest import mock

from model.model import Model
from model.parse_stack import Stack

def test_get_nodes_gets_nodes_from_persistence():
    persistence = mock.Mock()
    model = Model(persistence)

    model.get_nodes()

    persistence.get_nodes.assert_called_once()


def test_get_edges_gets_edges_from_persistence():
    persistence = mock.Mock()
    model = Model(persistence)

    model.get_edges()

    persistence.get_edges.assert_called_once()


def test_yellow_count_gets_range_from_persistence():
    persistence = mock.Mock()
    model = Model(persistence)

    model.yellow_count()

    persistence.get_yellow.assert_called_once()


def test_red_count_gets_range_from_persistence():
    persistence = mock.Mock()
    model = Model(persistence)

    model.red_count()

    persistence.get_red.assert_called_once()


def test_max_count_gets_with_no_nodes():
    persistence = mock.Mock()
    persistence.get_nodes.return_value = {}
    model = Model(persistence)

    assert model.max_count() == 0


def test_max_count_gets_with_nodes():
    persistence = mock.Mock()
    persistence.get_nodes.return_value = {
        'dummy_hash1': {'name': 'dummy_name1', 'source': 'dummy_source1', 'call_count': 2},
        'dummy_hash2': {'name': 'dummy_name2', 'source': 'dummy_source2', 'call_count': 5}
    }
    model = Model(persistence)

    assert model.max_count() == 5


def test_set_range_calls_persistence_with_right_params():
    persistence = mock.Mock()
    model = Model(persistence)

    model.set_range('dummy_yellow', 'dummy_red')

    persistence.update_colors.assert_called_once()
    persistence.update_colors.assert_called_with('dummy_yellow', 'dummy_red')


def test_init_colors():
    persistence = mock.Mock()
    model = Model(persistence)
    model.max_count = mock.Mock(return_value=8)

    model.init_colors()

    assert model.max_count.call_count == 2
    persistence.update_colors.assert_called_once()
    persistence.update_colors.assert_called_with(3, 5)


def test_empty_model():
    persistence = mock.Mock()
    model = Model(persistence)

    assert not model._thread_enabled
    assert model._thread_error == None
    assert model._persistence == persistence


@mock.patch('model.model.Thread')
@mock.patch('model.model.TraceProcess')
def test_start_trace(process, thread):
    model = Model(mock.Mock())

    model.start_trace(['dummy', 'functions'])

    assert model._thread_error == None
    assert model._thread_enabled
    thread.assert_called_once()
    thread.return_value.start.assert_called_once()
    process.assert_called_once()
    process.return_value.start.assert_called_once()


def test_start_trace_without_functions():
    model = Model(mock.Mock())
    model.start_trace([])

    assert model._thread_error == 'No functions to trace'


def test_stop_trace():
    model = Model(mock.Mock())
    model._thread_enabled = True
    model.init_colors = mock.Mock()

    model.stop_trace()

    assert not model._thread_enabled
    model.init_colors.assert_called_once()


def test_thread_error_returns_error():
    model = Model(mock.Mock())
    model._thread_error = 'Dummy Error'

    assert model.thread_error() == 'Dummy Error'


def test_trace_active_returns_thread_enabled():
    model = Model(mock.Mock())
    model._thread_enabled = True

    assert model.trace_active()


def test_load_output():
    test_file_path = Path.cwd().joinpath(
        'tests', 'integration', 'resources', 'test_static_output'
    )
    text = test_file_path.read_text()
    persistence = mock.Mock()
    persistence.get_nodes.return_value = {}
    model = Model(persistence)

    model.load_output(text)

    assert persistence.load_edges.call_count == 8
    assert persistence.load_nodes.call_count == 8
