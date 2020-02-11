from pytest import raises
from queue import Empty
import unittest.mock as mock

from model.dynamic import DynamicModel, ProcessException
from model.base import Stack
from model.trace_utils import STACK_END_PATTERN


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
def test_monitor_tracing_with_thread_enabled_with_process_alive_at_stack_end(persistence):
    def side_effect(*argv):
        model._thread_enabled = False
        return True

    model = DynamicModel()
    model.parse_stack = mock.Mock(return_value=Stack(nodes='dummy_nodes', edges='dummy_edges'))
    model._thread_enabled = True
    queue = mock.Mock()
    queue.get_nowait.return_value = STACK_END_PATTERN
    process = mock.Mock()
    process.is_alive = mock.Mock(side_effect=side_effect)

    model.monitor_tracing(queue, process)

    persistence.return_value.load_edges.assert_called_with('dummy_edges')


@mock.patch('model.base.Persistence')
def test_monitor_tracing_with_thread_enabled_with_process_alive_at_middle_of_stack(persistence):
    def side_effect(*argv):
        model._thread_enabled = False
        return True

    model = DynamicModel()
    model.parse_stack = mock.Mock(return_value=Stack(nodes='dummy_nodes', edges='dummy_edges'))
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


@mock.patch('model.dynamic.DynamicModel.parse_args_from_dict', return_value='dummy_functions')
def test_trace_dict_without_exception(parse_args_from_dict):
    model = DynamicModel()
    model.start_trace = mock.Mock()

    model.trace_dict('dummy_dict')

    parse_args_from_dict.assert_called_once()
    parse_args_from_dict.assert_called_with('dummy_dict')
    model.start_trace.assert_called_once()
    model.start_trace.assert_called_with('dummy_functions')


@mock.patch('model.dynamic.DynamicModel.parse_args_from_dict', side_effect=ProcessException('Dummy Error'))
def test_trace_dict_with_exception(parse_args_from_dict):
    model = DynamicModel()
    model.start_trace = mock.Mock()

    model.trace_dict('dummy_dict')

    parse_args_from_dict.assert_called_once()
    parse_args_from_dict.assert_called_with('dummy_dict')
    assert model._process_error == 'Dummy Error'


@mock.patch('model.dynamic.DynamicModel.parse_args_from_file', return_value='dummy_functions')
def test_trace_yaml_without_exception(parse_args_from_file):
    model = DynamicModel()
    model.start_trace = mock.Mock()

    model.trace_yaml('dummy_dict')

    parse_args_from_file.assert_called_once()
    parse_args_from_file.assert_called_with('dummy_dict')
    model.start_trace.assert_called_once()
    model.start_trace.assert_called_with('dummy_functions')


@mock.patch('model.dynamic.DynamicModel.parse_args_from_file', side_effect=ProcessException('Dummy Error'))
def test_trace_yaml_with_exception(parse_args_from_file):
    model = DynamicModel()
    model.start_trace = mock.Mock()

    model.trace_yaml('dummy_dict')

    parse_args_from_file.assert_called_once()
    parse_args_from_file.assert_called_with('dummy_dict')
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


def test_parse_args_from_dict_raises_exception_on_empty_dict():
    with raises(ProcessException) as excinfo:
        DynamicModel.parse_args_from_dict({})
    assert str(excinfo.value) == 'No functions to trace'


def test_parse_args_from_dict_raises_exception_on_only_apps():
    with raises(ProcessException) as excinfo:
        DynamicModel.parse_args_from_dict({'app1': {}, 'app2': {}})
    assert str(excinfo.value) == 'No functions to trace'


def test_parse_args_from_dict_single_app_single_func():
    result = DynamicModel.parse_args_from_dict({'app': {'func': {}}})
    assert result == ['app:func']


def test_parse_args_from_dict_single_app_multiple_funcs():
    result = DynamicModel.parse_args_from_dict({'app': {'func1': {}, 'func2': {}}})
    assert sorted(result) == ['app:func1', 'app:func2']


def test_parse_args_from_dict_multiple_apps_each_with_single_func():
    result = DynamicModel.parse_args_from_dict({
        'app1': {'func1': {}},
        'app2': {'func2': {}}})
    assert sorted(result) == ['app1:func1', 'app2:func2']


def test_parse_args_from_dict_multiple_apps_each_with_multiple_funcs():
    result = DynamicModel.parse_args_from_dict({
        'app1': {'func1': {}, 'func2': {}},
        'app2': {'func3': {}, 'func4': {}}})
    assert result == ['app1:func1', 'app1:func2', 'app2:func3', 'app2:func4']


def test_parse_args_from_dict_single_param_in_single_function():
    result = DynamicModel.parse_args_from_dict({'app': {'func': {'arg1': '%s'}}})
    assert result == ['app:func "%s", arg1']


def test_parse_args_from_dict_multiple_params_in_single_function():
    result = DynamicModel.parse_args_from_dict({'app': {'func': {'arg1': '%s', 'arg3': '%d'}}})
    assert result == ['app:func "%s %d", arg1, arg3']


def test_parse_args_from_dict_single_param_in_multiple_functions():
    result = DynamicModel.parse_args_from_dict({'app': {
        'func1': {'arg4': '%s'},
        'func2': {'arg2': '%f'}}})
    assert result == ['app:func1 "%s", arg4', 'app:func2 "%f", arg2']


def test_parse_args_from_dict_multiple_params_in_multiple_functions():
    result = DynamicModel.parse_args_from_dict({'app': {
        'func1': {'arg4': '%s', 'arg2': '%d'},
        'func2': {'arg2': '%f', 'arg1': '%hi'}}})
    assert result == ['app:func1 "%d %s", arg2, arg4', 'app:func2 "%hi %f", arg1, arg2']


def test_parse_args_from_file_raises_error_for_invalid_path_type():
    with raises(ProcessException) as excinfo:
        DynamicModel.parse_args_from_file(None)

    assert str(excinfo.value) == 'Please provide a path to the configuration file'


def test_parse_args_from_file_raises_error_for_invalid_path_value():
    with raises(ProcessException) as excinfo:
        DynamicModel.parse_args_from_file('.non/existent/path')

    assert str(excinfo.value) == 'Could not find configuration file at .non/existent/path'


def test_parse_args_from_file_raises_error_on_directory(tmp_path):
    with raises(ProcessException) as excinfo:
        DynamicModel.parse_args_from_file(tmp_path)

    assert str(excinfo.value) == '{} is a directory, not a file'.format(str(tmp_path))


def test_parse_args_from_file_raises_error_on_invalid_yaml_format(tmp_path):
    config_file = tmp_path.joinpath('config')
    config_file.write_text('invalid:yaml:\ncontent')

    with raises(ProcessException) as excinfo:
        DynamicModel.parse_args_from_file(config_file)

    assert str(excinfo.value) == 'Config file at {} has to be YAML format'.format(str(config_file))


def test_parse_args_from_file_raises_error_on_unknown_exception(tmp_path):
    config_file = tmp_path.joinpath('config')
    config_file.write_text('c:\n  - [- asd: dsa]')

    with raises(ProcessException) as excinfo:
        DynamicModel.parse_args_from_file(config_file)

    assert str(excinfo.value) == 'Unknown error happened while processing config file'


def test_parse_args_from_file_raises_error_on_invalid_config_format(tmp_path):
    config_file = tmp_path.joinpath('config')
    config_file.write_text('app1:func1:func2:func3')

    with raises(ProcessException) as excinfo:
        DynamicModel.parse_args_from_file(config_file)

    assert str(excinfo.value) == 'Could not process configuration file'


def test_parse_args_from_file_raises_error_if_no_functions_to_trace(tmp_path):
    config_file = tmp_path.joinpath('config')
    config_file.write_text('app1: []\napp2: []')

    with raises(ProcessException) as excinfo:
        DynamicModel.parse_args_from_file(config_file)

    assert str(excinfo.value) == 'No functions to trace'


def test_parse_args_from_file_with_single_app_and_single_func(tmp_path):
    config_file = tmp_path.joinpath('config')
    config_file.write_text('app:\n  - func')

    result = DynamicModel.parse_args_from_file(config_file)

    assert result == ['app:func']


def test_parse_args_from_file_with_single_app_and_multiple_funcs(tmp_path):
    config_file = tmp_path.joinpath('config')
    config_file.write_text('app:\n  - func1\n  - func2')

    result = DynamicModel.parse_args_from_file(config_file)

    assert sorted(result) == ['app:func1','app:func2']


def test_parse_args_from_file_with_multiple_app_with_single_funcs(tmp_path):
    config_file = tmp_path.joinpath('config')
    config_file.write_text('app1:\n  - func1\napp2:\n  - func2')

    result = DynamicModel.parse_args_from_file(config_file)

    assert sorted(result) == ['app1:func1','app2:func2']


def test_parse_args_from_file_with_multiple_app_with_multiple_funcs(tmp_path):
    config_file = tmp_path.joinpath('config')
    config_file.write_text('app1:\n  - func1\n  - func2\napp2:\n  - func3\n  - func4')

    result = DynamicModel.parse_args_from_file(config_file)

    assert sorted(result) == ['app1:func1', 'app1:func2', 'app2:func3', 'app2:func4']


def test_parse_args_from_file_with_single_param(tmp_path):
    config_file = tmp_path.joinpath('config')
    config_file.write_text("app:\n  - func:\n    - '%type'")

    result = DynamicModel.parse_args_from_file(config_file)

    assert result == ['app:func "%type", arg1']


def test_parse_args_from_file_with_multiple_params(tmp_path):
    config_file = tmp_path.joinpath('config')
    config_file.write_text("app:\n  - func:\n    - '%type1'\n    - '%type2'")

    result = DynamicModel.parse_args_from_file(config_file)

    assert result == ['app:func "%type1 %type2", arg1, arg2']
