import unittest.mock as mock

import pexpect

from model.dynamic import DynamicModel
import model.utils as utils


@mock.patch('model.base.Persistence')
def test_initialization(persistence):
    config = mock.Mock()
    model = DynamicModel(config)

    assert model._persistence is persistence.return_value
    assert model._configuration is config
    assert not model._thread_enabled
    assert model._thread_error == None
    assert model._process_error == None


@mock.patch('model.dynamic.pexpect.spawn')
def test_run_command_without_thread_enabled(spawn):
    model = DynamicModel(None)

    model._run_command('dummy_command')

    spawn.assert_called_once()
    spawn.assert_called_with('dummy_command', timeout=None)
    spawn.return_value.close.assert_called_once()


@mock.patch('model.dynamic.pexpect.spawn')
def test_run_command_with_thread_enabled(spawn):
    def side_effect(*argv):
        model._thread_enabled = False

    model = DynamicModel(None)
    model._process_output = mock.Mock(side_effect=side_effect)
    model._thread_enabled = True

    model._run_command('dummy_command')

    spawn.assert_called_once()
    spawn.assert_called_with('dummy_command', timeout=None)
    spawn.return_value.close.assert_called_once()
    model._process_output.assert_called_once()
    model._process_output.assert_called_with(spawn.return_value, [])


@mock.patch('model.dynamic.pexpect.spawn')
def test_run_command_EOF_exception(spawn):
    model = DynamicModel(None)
    model._process_output = mock.Mock(side_effect=pexpect.EOF('Dummy Error'))
    model._thread_enabled = True

    model._run_command('dummy_command')

    spawn.assert_called_once()
    spawn.assert_called_with('dummy_command', timeout=None)
    model._process_output.assert_called_once()
    model._process_output.assert_called_with(spawn.return_value, [])
    assert not model._thread_enabled


@mock.patch('model.dynamic.pexpect.spawn')
def test_run_command_ExceptionPexpect_exception(spawn):
    model = DynamicModel(None)
    model._process_output = mock.Mock(side_effect=pexpect.exceptions.ExceptionPexpect('Dummy Error'))
    model._thread_enabled = True

    model._run_command('dummy_command')

    spawn.assert_called_once()
    spawn.assert_called_with('dummy_command', timeout=None)
    model._process_output.assert_called_once()
    model._process_output.assert_called_with(spawn.return_value, [])
    assert not model._thread_enabled
    assert model._thread_error == 'Dummy Error'


def test_process_output_inside_stack():
    model = DynamicModel(None)
    child = mock.Mock()
    stack = mock.Mock()

    model._process_output(child, stack)

    child.expect.assert_called_once()
    child.expect.assert_called_with('\n')
    stack.append.assert_called_once()
    stack.append.assert_called_with(child.before.decode())


@mock.patch('model.dynamic.parse_stack', return_value=utils.Graph(nodes='dummy_nodes', edges='dummy_edges'))
@mock.patch('model.dynamic.pexpect')
@mock.patch('model.base.Persistence')
def test_process_output_end_of_stack(persistence, pexpect, parse_stack):
    model = DynamicModel(None)
    child = mock.Mock()
    child.before.decode.return_value = '\r'
    stack = mock.Mock()

    model._process_output(child, stack)

    child.expect.assert_called_once()
    child.expect.assert_called_with('\n')
    parse_stack.assert_called_once()
    parse_stack.assert_called_with(stack)
    persistence.return_value.load_edges.assert_called_once()
    persistence.return_value.load_edges.assert_called_with('dummy_edges')
    persistence.return_value.load_nodes.assert_called_once()
    persistence.return_value.load_nodes.assert_called_with('dummy_nodes')
    stack.clear.assert_called_once()


@mock.patch('model.dynamic.flatten_trace_dict', return_value='dummy_functions')
def test_trace_dict_without_exception(flatten_trace_dict):
    config = mock.Mock()
    model = DynamicModel(config)
    model.start_trace = mock.Mock()

    model.trace_dict('dummy_dict')

    flatten_trace_dict.assert_called_once()
    flatten_trace_dict.assert_called_with('dummy_dict')
    model.start_trace.assert_called_once()
    model.start_trace.assert_called_with('dummy_functions')


@mock.patch('model.dynamic.flatten_trace_dict', side_effect=utils.ProcessException('Dummy Error'))
def test_trace_dict_with_exception(flatten_trace_dict):
    config = mock.Mock()
    model = DynamicModel(config)
    model.start_trace = mock.Mock()

    model.trace_dict('dummy_dict')

    flatten_trace_dict.assert_called_once()
    flatten_trace_dict.assert_called_with('dummy_dict')
    assert model._process_error == 'Dummy Error'


@mock.patch('model.dynamic.extract_config', return_value='dummy_functions')
def test_trace_yaml_without_exception(extract_config):
    config = mock.Mock()
    model = DynamicModel(config)
    model.start_trace = mock.Mock()

    model.trace_yaml('dummy_dict')

    extract_config.assert_called_once()
    extract_config.assert_called_with('dummy_dict')
    model.start_trace.assert_called_once()
    model.start_trace.assert_called_with('dummy_functions')


@mock.patch('model.dynamic.extract_config', side_effect=utils.ProcessException('Dummy Error'))
def test_trace_yaml_with_exception(extract_config):
    config = mock.Mock()
    model = DynamicModel(config)
    model.start_trace = mock.Mock()

    model.trace_yaml('dummy_dict')

    extract_config.assert_called_once()
    extract_config.assert_called_with('dummy_dict')
    assert model._process_error == 'Dummy Error'


@mock.patch('model.dynamic.Thread')
def test_start_trace(thread):
    config = mock.Mock()
    config.get_command.return_value = 'dummy_command'
    model = DynamicModel(config)

    model.start_trace(['dummy', 'functions'])

    assert model._thread_error == None
    assert model._process_error == None
    assert model._thread_enabled
    thread.assert_called_once()
    thread.assert_called_with(target=model._run_command, args=["dummy_command -UK 'dummy' 'functions'"])
    thread.return_value.start.assert_called_once()


@mock.patch('model.base.Persistence')
def test_stop_trace(persistence):
    model = DynamicModel(None)
    model._thread_enabled = True
    model.init_colors = mock.Mock()

    model.stop_trace()

    assert not model._thread_enabled
    model.init_colors.assert_called_once()


def test_thread_error_returns_error():
    model = DynamicModel(None)
    model._thread_error = 'Dummy Error'

    assert model.thread_error() == 'Dummy Error'


def test_process_error_returns_error():
    model = DynamicModel(None)
    model._process_error = 'Dummy Error'

    assert model.process_error() == 'Dummy Error'


def test_trace_active_returns_thread_enabled():
    model = DynamicModel(None)
    model._thread_enabled = True

    assert model.trace_active()