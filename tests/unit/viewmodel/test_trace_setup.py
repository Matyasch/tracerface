from unittest.mock import patch

from pytest import fixture, raises
from yaml.parser import ParserError

from model.dynamic import ProcessException
from viewmodel.trace_setup import Setup

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


@patch('viewmodel.trace_setup.check_output', return_value=b'func1\nfunc2\nfunc3\n')
def test_initialize_app(nm):
    setup = Setup()

    setup.initialize_app('app')

    assert setup._setup == {
        'app': {
            'func1': {'traced': False, 'parameters': {}},
            'func2': {'traced': False, 'parameters': {}},
            'func3': {'traced': False, 'parameters': {}}
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


def test_add_function(init_setup):
    setup = Setup()
    setup._setup = init_setup

    setup.add_function('app1', 'func1')

    assert setup._setup == {
        'app1': {
            'func1': {'traced': True, 'parameters': {}},
            'func3': {'traced': False, 'parameters': {}}
        },
        'app2': {
            'func2': {'traced': False, 'parameters': {}},
        }
    }


def test_remove_function(init_setup):
    setup = Setup()
    setup._setup = init_setup

    setup.add_function('app1', 'func1')
    setup.remove_function('app1', 'func1')

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


def test_generate_bcc_args_raises_exception_on_empty_dict():
    setup = Setup()

    with raises(ProcessException) as e:
        setup.generate_bcc_args()
    assert str(e.value) == 'No functions to trace'


def test_generate_bcc_args_raises_exception_on_only_apps():
    setup = Setup()
    setup._setup = {'app1': {}, 'app2': {}}

    with raises(ProcessException) as e:
        setup.generate_bcc_args()
    assert str(e.value) == 'No functions to trace'


def test_generate_bcc_args_raises_exception_with_only_untraced_functions():
    setup = Setup()
    setup._setup = {'app': {'func': {'traced': False, 'parameters': {}}}}

    with raises(ProcessException) as e:
        setup.generate_bcc_args()
    assert str(e.value) == 'No functions to trace'


def test_generate_bcc_args_with_multiple_values():
    setup = Setup()
    setup._setup = {
        'app1': {
            'func1': {'traced': True, 'parameters':{4: '%s', 2: '%d'}},
            'func2': {'traced': False, 'parameters':{}}
        },
        'app2': {
            'func3': {'traced': True, 'parameters':{1: '%s', 5: '%d'}},
            'func4': {'traced': True, 'parameters':{1: '%s', 2: '%f'}}
        }
    }
    result = setup.generate_bcc_args()
    assert result == [
        'app1:func1 "%s %d", arg4, arg2',
        'app2:func3 "%s %d", arg1, arg5',
        'app2:func4 "%s %f", arg1, arg2',
    ]


@patch('viewmodel.trace_setup.Path.read_text')
def test_load_from_file_raises_exception_if_file_not_found(read):
    def side_effect():
        raise FileNotFoundError

    read.side_effect = side_effect
    setup = Setup()
    with raises(ValueError):
        setup.load_from_file('.non/existent/path')


@patch('viewmodel.trace_setup.Path.read_text')
def test_load_from_file_raises_exception_if_file_is_directory(read):
    def side_effect():
        raise IsADirectoryError

    read.side_effect = side_effect
    setup = Setup()
    with raises(ValueError):
        setup.load_from_file('.non/existent/path')


@patch('viewmodel.trace_setup.yaml.safe_load')
@patch('viewmodel.trace_setup.Path.read_text')
def test_load_from_file_raises_exception_if_not_yaml_format(read, load):
    def side_effect(content):
        raise ParserError

    load.side_effect = side_effect
    setup = Setup()
    with raises(ValueError):
        setup.load_from_file('dummy/path')


@patch('viewmodel.trace_setup.yaml.safe_load', return_value={'.non/existent/path' : {}})
@patch('viewmodel.trace_setup.Path.read_text')
def test_load_from_file_raises_exception_if_not_yaml_format(read, load):
    setup = Setup()
    with raises(ValueError):
        setup.load_from_file('dummy/path')
