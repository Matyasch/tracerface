from queue import Empty
import unittest.mock as mock

from model.dynamic import DynamicModel
import model.utils as utils


def test_empty_model():
    model = DynamicModel()

    assert not model._thread_enabled
    assert model._thread_error == None
    assert model._process_error == None
    assert model.get_edges() == {}
    assert model.get_nodes() == {}


def test_monitor_tracing_without_thread_enabled_with_process_alive():
    model = DynamicModel()
    queue = mock.Mock()
    process = mock.Mock()
    process.is_alive = mock.Mock(return_value=True)

    model.monitor_tracing(queue, process)

    process.is_alive.assert_called()
    process.terminate.assert_called()
    assert not queue.get_nowait.called


def test_monitor_tracing_without_thread_enabled_without_process_alive():
    model = DynamicModel()
    queue = mock.Mock()
    process = mock.Mock()
    process.is_alive = mock.Mock(return_value=False)

    model.monitor_tracing(queue, process)

    process.is_alive.assert_called()
    assert not process.terminate.called
    assert not queue.get_nowait.called


def test_monitor_tracing_with_thread_enabled_without_process_alive():
    model = DynamicModel()
    model._thread_enabled = True
    queue = mock.Mock()
    process = mock.Mock()
    process.is_alive = mock.Mock(return_value=False)

    model.monitor_tracing(queue, process)

    assert model._thread_error == 'Tracing stopped unexpectedly'


@mock.patch('model.base.Persistence')
@mock.patch('model.dynamic.utils.parse_stack', return_value=utils.Graph(nodes='dummy_nodes', edges='dummy_edges'))
def test_monitor_tracing_with_thread_enabled_with_process_alive_at_stack_end(parse_stack, persistence):
    def side_effect(*argv):
        model._thread_enabled = False
        return True

    model = DynamicModel()
    model._thread_enabled = True
    queue = mock.Mock()
    queue.get_nowait.return_value = utils.STACK_END_PATTERN
    process = mock.Mock()
    process.is_alive = mock.Mock(side_effect=side_effect)

    model.monitor_tracing(queue, process)

    persistence.return_value.load_edges.assert_called_with('dummy_edges')


@mock.patch('model.base.Persistence')
@mock.patch('model.dynamic.utils.parse_stack', return_value=utils.Graph(nodes='dummy_nodes', edges='dummy_edges'))
def test_monitor_tracing_with_thread_enabled_with_process_alive_at_middle_of_stack(parse_stack, persistence):
    def side_effect(*argv):
        model._thread_enabled = False
        return True

    model = DynamicModel()
    model._thread_enabled = True
    queue = mock.Mock()
    queue.get_nowait.return_value = 'dummy value'
    process = mock.Mock()
    process.is_alive = mock.Mock(side_effect=side_effect)

    model.monitor_tracing(queue, process)

    assert not persistence.return_value.load_edges.called


def test_monitor_tracing_handles_empty_exception():
    def side_effect(*argv):
        model._thread_enabled = False
        return True

    model = DynamicModel()
    model._thread_enabled = True
    queue = mock.Mock()
    queue.get_nowait.side_effect = Empty
    process = mock.Mock()
    process.is_alive = mock.Mock(side_effect=side_effect)

    model.monitor_tracing(queue, process)

    process.terminate.assert_called()


@mock.patch('model.dynamic.utils.flatten_trace_dict', return_value='dummy_functions')
def test_trace_dict_without_exception(flatten_trace_dict):
    model = DynamicModel()
    model.start_trace = mock.Mock()

    model.trace_dict('dummy_dict')

    flatten_trace_dict.assert_called_once()
    flatten_trace_dict.assert_called_with('dummy_dict')
    model.start_trace.assert_called_once()
    model.start_trace.assert_called_with('dummy_functions')


@mock.patch('model.dynamic.utils.flatten_trace_dict', side_effect=utils.ProcessException('Dummy Error'))
def test_trace_dict_with_exception(flatten_trace_dict):
    model = DynamicModel()
    model.start_trace = mock.Mock()

    model.trace_dict('dummy_dict')

    flatten_trace_dict.assert_called_once()
    flatten_trace_dict.assert_called_with('dummy_dict')
    assert model._process_error == 'Dummy Error'


@mock.patch('model.dynamic.utils.extract_config', return_value='dummy_functions')
def test_trace_yaml_without_exception(extract_config):
    model = DynamicModel()
    model.start_trace = mock.Mock()

    model.trace_yaml('dummy_dict')

    extract_config.assert_called_once()
    extract_config.assert_called_with('dummy_dict')
    model.start_trace.assert_called_once()
    model.start_trace.assert_called_with('dummy_functions')


@mock.patch('model.dynamic.utils.extract_config', side_effect=utils.ProcessException('Dummy Error'))
def test_trace_yaml_with_exception(extract_config):
    model = DynamicModel()
    model.start_trace = mock.Mock()

    model.trace_yaml('dummy_dict')

    extract_config.assert_called_once()
    extract_config.assert_called_with('dummy_dict')
    assert model._process_error == 'Dummy Error'


@mock.patch('model.dynamic.Thread')
@mock.patch('model.dynamic.TraceProcess')
def test_start_trace(process, thread):
    model = DynamicModel()

    model.start_trace(['dummy', 'functions'])

    assert model._thread_error == None
    assert model._process_error == None
    assert model._thread_enabled
    thread.assert_called_once()
    thread.return_value.start.assert_called_once()
    process.assert_called_once()
    process.return_value.start.assert_called_once()


@mock.patch('model.base.Persistence')
def test_stop_trace(persistence):
    model = DynamicModel()
    model._thread_enabled = True
    model.init_colors = mock.Mock()

    model.stop_trace()

    assert not model._thread_enabled
    model.init_colors.assert_called_once()


def test_thread_error_returns_error():
    model = DynamicModel()
    model._thread_error = 'Dummy Error'

    assert model.thread_error() == 'Dummy Error'


def test_process_error_returns_error():
    model = DynamicModel()
    model._process_error = 'Dummy Error'

    assert model.process_error() == 'Dummy Error'


def test_trace_active_returns_thread_enabled():
    model = DynamicModel()
    model._thread_enabled = True

    assert model.trace_active()
