from unittest.mock import patch

from pytest import fixture, raises
from yaml.parser import ParserError, ScannerError

from tracerface.web_ui.trace_setup import Setup, SetupError


@fixture
def init_setup():
    return {
        'app1': {
            'func1': {'traced': False, 'parameters': {}},
            'func3': {'traced': False, 'parameters': {}}
        },
        'app2': {
            'func2': {'traced': False, 'parameters': {}},
        }
    }


def test_empty_setup():
    setup = Setup()

    assert setup._setup == {}


@patch('tracerface.web_ui.trace_setup.check_output', return_value=b'func1\nfunc2\nfunc3\n')
def test_initialize_binary(nm):
    setup = Setup()

    setup.initialize_binary('app')

    assert setup._setup == {
        'app': {
            'func1': {'mangled': 'func1', 'traced': False, 'parameters': {}},
            'func2': {'mangled': 'func2', 'traced': False, 'parameters': {}},
            'func3': {'mangled': 'func3', 'traced': False, 'parameters': {}}
        }
    }


def test_remove_app(init_setup):
    setup = Setup()
    setup._setup = init_setup

    setup.remove_app('app2')

    assert setup._setup == {
        'app1': {
            'func1': {'traced': False, 'parameters': {}},
            'func3': {'traced': False, 'parameters': {}}
        }
    }


def test_initialize_built_in():
    setup = Setup()

    setup.initialize_built_in('app')

    assert setup._setup == {
        'built-ins': {
            'app': {'traced': True, 'parameters': {}},
        }
    }


def test_get_apps(init_setup):
    setup = Setup()
    setup._setup = init_setup

    result = setup.get_apps()

    assert result == ['app1', 'app2']


def test_get_setup_of_app(init_setup):
    setup = Setup()
    setup._setup = init_setup

    result = setup.get_setup_of_app('app1')

    assert result == {
        'func1': {'traced': False, 'parameters': {}},
        'func3': {'traced': False, 'parameters': {}}
    }


def test_setup_function_to_trace(init_setup):
    setup = Setup()
    setup._setup = init_setup

    setup.setup_function_to_trace('app1', 'func1')

    assert setup._setup == {
        'app1': {
            'func1': {'traced': True, 'parameters': {}},
            'func3': {'traced': False, 'parameters': {}}
        },
        'app2': {
            'func2': {'traced': False, 'parameters': {}},
        }
    }


def test_remove_function_from_trace(init_setup):
    setup = Setup()
    setup._setup = init_setup

    setup.setup_function_to_trace('app1', 'func1')
    setup.remove_function_from_trace('app1', 'func1')

    assert setup._setup == {
        'app1': {
            'func1': {'traced': False, 'parameters': {}},
            'func3': {'traced': False, 'parameters': {}}
        },
        'app2': {
            'func2': {'traced': False, 'parameters': {}},
        }
    }


def test_get_parameters():
    setup = Setup()
    setup._setup = {
        'app': {
            'func': {'traced': False, 'parameters': {1: '%s', 4: '%d'}}
        }
    }

    result = setup.get_parameters('app', 'func')

    assert result == {1: '%s', 4: '%d'}


def test_add_parameter(init_setup):
    setup = Setup()
    setup._setup = init_setup

    setup.add_parameter('app1', 'func3', 2, '%s')

    assert setup._setup == {
        'app1': {
            'func1': {'traced': False, 'parameters': {}},
            'func3': {'traced': False, 'parameters': {2: '%s'}}
        },
        'app2': {
            'func2': {'traced': False, 'parameters': {}},
        }
    }


def test_remove_parameter():
    setup = Setup()
    setup._setup = {
        'app': {
            'func': {'traced': False, 'parameters': {1: '%s', 4: '%d'}}
        }
    }

    setup.remove_parameter('app', 'func', 4)

    assert setup._setup == {
        'app': {
            'func': {'traced': False, 'parameters': {1: '%s'}}
        }
    }


def test_generate_bcc_args_with_multiple_values():
    setup = Setup()
    setup._setup = {
        'app1': {
            'func1': {'mangled': 'mangled1', 'traced': True, 'parameters':{4: '%s', 2: '%d'}},
            'func2': {'mangled': 'mangled2', 'traced': False, 'parameters':{}}
        },
        'app2': {
            'func3': {'mangled': 'mangled3', 'traced': True, 'parameters':{1: '%s', 5: '%d'}},
            'func4': {'mangled': 'mangled4', 'traced': True, 'parameters':{1: '%s', 2: '%f'}}
        }
    }
    result = setup.generate_bcc_args()
    assert result == [
        'app1:mangled1 "%s %d", arg4, arg2',
        'app2:mangled3 "%s %d", arg1, arg5',
        'app2:mangled4 "%s %f", arg1, arg2',
    ]


@patch('tracerface.web_ui.trace_setup.Path.read_text')
def test_load_from_file_raises_exception_if_file_not_found(read):
    def side_effect():
        raise FileNotFoundError

    read.side_effect = side_effect
    setup = Setup()
    with raises(SetupError) as err:
        setup.load_from_file('.non/existent/path')
    assert err.value.error_cause == SetupError.ErrorCauses.WRONG_CONFIG_FILE


@patch('tracerface.web_ui.trace_setup.Path.read_text')
def test_load_from_file_raises_exception_if_file_is_directory(read):
    def side_effect():
        raise IsADirectoryError

    read.side_effect = side_effect
    setup = Setup()
    with raises(SetupError) as err:
        setup.load_from_file('.non/existent/path')
    assert err.value.error_cause == SetupError.ErrorCauses.WRONG_CONFIG_FILE


@patch('tracerface.web_ui.trace_setup.yaml.safe_load')
@patch('tracerface.web_ui.trace_setup.Path.read_text')
def test_load_from_file_raises_exception_on_yaml_parse_error(read, load):
    def side_effect(content):
        raise ParserError

    load.side_effect = side_effect
    setup = Setup()
    with raises(SetupError) as err:
        setup.load_from_file('dummy/path')
    assert err.value.error_cause == SetupError.ErrorCauses.WRONG_CONFIG_FILE


@patch('tracerface.web_ui.trace_setup.yaml.safe_load')
@patch('tracerface.web_ui.trace_setup.Path.read_text')
def test_load_from_file_raises_exception_on_yaml_scan_error(read, load):
    def side_effect(content):
        raise ScannerError

    load.side_effect = side_effect
    setup = Setup()
    with raises(SetupError) as err:
        setup.load_from_file('dummy/path')
    assert err.value.error_cause == SetupError.ErrorCauses.WRONG_CONFIG_FILE


@patch('tracerface.web_ui.trace_setup.yaml.safe_load', return_value={'built_in' : {}})
@patch('tracerface.web_ui.trace_setup.Path.read_text')
def test_load_from_file_adds_built_in_if_binary_not_found(read, load):
    setup = Setup()
    setup.load_from_file('dummy/path')
    assert 'built-ins' in setup._setup
    assert 'built_in' in setup._setup['built-ins']
