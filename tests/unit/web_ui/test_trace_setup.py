#!/usr/bin/env python3
from unittest import main, TestCase
from unittest.mock import patch

from yaml.parser import ParserError, ScannerError

from tracerface.web_ui.trace_setup import Setup, SetupError


def dummy_setup():
    return {
        'app1': {
            'func1': {'traced': False, 'parameters': {}, 'mangled': 'mangledfunc1'},
            'func3': {'traced': False, 'parameters': {}, 'mangled': 'mangledfunc3'},
        },
        'app2': {
            'func2': {'traced': False, 'parameters': {}, 'mangled': 'mangledfunc2'},
        }
    }


class TestInitBinary(TestCase):
    @patch('tracerface.web_ui.trace_setup.check_output', return_value=b'func1\nfunc2\nfunc3\n')
    def test_initialize_binary(self, nm):
        setup = Setup()

        setup.initialize_binary('app')

        expected = {
            'app': {
                'func1': {'mangled': 'func1', 'traced': False, 'parameters': {}},
                'func2': {'mangled': 'func2', 'traced': False, 'parameters': {}},
                'func3': {'mangled': 'func3', 'traced': False, 'parameters': {}}
            }
        }
        self.assertEqual(setup._setup, expected)


class TestRemoveApp(TestCase):
    def test_remove_app(self):
        setup = Setup()
        setup._setup = dummy_setup()

        setup.remove_app('app2')

        expected = {
            'app1': {
                'func1': {'traced': False, 'parameters': {}, 'mangled': 'mangledfunc1'},
                'func3': {'traced': False, 'parameters': {}, 'mangled': 'mangledfunc3'}
            }
        }
        self.assertEqual(setup._setup, expected)


class TestInitBuiltin(TestCase):
    def test_initialize_built_in(self):
        setup = Setup()

        setup.initialize_built_in('app')

        expected = {'built-ins': {'app': {'traced': True, 'parameters': {}}}}
        self.assertEqual(setup._setup, expected)


class TestGetApps(TestCase):
    def test_get_apps(self):
        setup = Setup()
        setup._setup = dummy_setup()

        result = setup.get_apps()

        self.assertEqual(result, ['app1', 'app2'])


class TestGetAppSetup(TestCase):
    def test_get_setup_of_app(self):
        setup = Setup()
        setup._setup = dummy_setup()

        result = setup.get_setup_of_app('app1')

        expected = {
            'func1': {'traced': False, 'parameters': {}, 'mangled': 'mangledfunc1'},
            'func3': {'traced': False, 'parameters': {}, 'mangled': 'mangledfunc3'}
        }
        self.assertEqual(result, expected)


class TestSetupFunctionToTrace(TestCase):
    def test_setup_function_to_trace_with_demangled_name(self):
        setup = Setup()
        setup._setup = dummy_setup()

        setup.setup_function_to_trace('app1', 'func1')

        expected = {
            'app1': {
                'func1': {'traced': True, 'parameters': {}, 'mangled': 'mangledfunc1'},
                'func3': {'traced': False, 'parameters': {}, 'mangled': 'mangledfunc3'}
            },
            'app2': {
                'func2': {'traced': False, 'parameters': {}, 'mangled': 'mangledfunc2'},
            }
        }
        self.assertEqual(setup._setup, expected)

    def test_setup_function_to_trace_with_mangled_name(self):
        setup = Setup()
        setup._setup = dummy_setup()

        setup.setup_function_to_trace('app1', 'mangledfunc1')

        expected = {
            'app1': {
                'func1': {'traced': True, 'parameters': {}, 'mangled': 'mangledfunc1'},
                'func3': {'traced': False, 'parameters': {}, 'mangled': 'mangledfunc3'}
            },
            'app2': {
                'func2': {'traced': False, 'parameters': {}, 'mangled': 'mangledfunc2'},
            }
        }
        self.assertEqual(setup._setup, expected)

    def test_setup_function_to_trace_raises_error_if_function_not_exists(self):
        setup = Setup()
        setup._setup = dummy_setup()
        with self.assertRaises(SetupError) as ctx:
            setup.setup_function_to_trace('app1', 'func4')
        error_cause = ctx.exception.error_cause
        self.assertEqual(error_cause, SetupError.ErrorCauses.FUNCTION_NOT_EXISTS_IN_BINARY)


class TestRemoveFunctionFromTrace(TestCase):
    def test_remove_function_from_trace_with_demangled_name(self):
        setup = Setup()
        setup._setup = dummy_setup()

        setup.setup_function_to_trace('app1', 'func1')
        setup.remove_function_from_trace('app1', 'func1')

        self.assertEqual(setup._setup, dummy_setup())

    def test_remove_function_from_trace_with_mangled_name(self):
        setup = Setup()
        setup._setup = dummy_setup()

        setup.setup_function_to_trace('app1', 'func1')
        setup.remove_function_from_trace('app1', 'mangledfunc1')

        self.assertEqual(setup._setup, dummy_setup())

    def test_remove_function_from_trace_raises_error_if_function_not_exists(self):
        setup = Setup()
        setup._setup = dummy_setup()
        with self.assertRaises(SetupError) as ctx:
            setup.remove_function_from_trace('app1', 'func4')
        error_cause = ctx.exception.error_cause
        self.assertEqual(error_cause, SetupError.ErrorCauses.FUNCTION_NOT_EXISTS_IN_BINARY)


class TestParameters(TestCase):
    def test_get_parameters(self):
        setup = Setup()
        setup._setup = {'app': {'func': {'traced': False, 'parameters': {1: '%s', 4: '%d'}}}}

        result = setup.get_parameters('app', 'func')

        self.assertEqual(result, {1: '%s', 4: '%d'})

    def test_add_parameter(self):
        setup = Setup()
        setup._setup = dummy_setup()

        setup.add_parameter('app1', 'func3', 2, '%s')

        expected = {
            'app1': {
                'func1': {'traced': False, 'parameters': {}, 'mangled': 'mangledfunc1'},
                'func3': {'traced': False, 'parameters': {2: '%s'}, 'mangled': 'mangledfunc3'}
            },
            'app2': {
                'func2': {'traced': False, 'parameters': {}, 'mangled': 'mangledfunc2'},
            }
        }
        self.assertEqual(setup._setup, expected)

    def test_remove_parameter(self):
        setup = Setup()
        setup._setup = {'app': {'func': {'traced': False, 'parameters': {1: '%s', 4: '%d'}}}}

        setup.remove_parameter('app', 'func', 4)

        expected = {'app': {'func': {'traced': False, 'parameters': {1: '%s'}}}}
        self.assertEqual(setup._setup, expected)

class TestGenerateBCCArgs(TestCase):
    def test_generate_bcc_args_with_multiple_values(self):
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
        expected = [
            'app1:mangled1 "%s %d", arg4, arg2',
            'app2:mangled3 "%s %d", arg1, arg5',
            'app2:mangled4 "%s %f", arg1, arg2',
        ]
        self.assertEqual(result, expected)


class TestLoadFromFile(TestCase):
    @patch('tracerface.web_ui.trace_setup.Path.read_text')
    def test_load_from_file_raises_exception_if_file_not_found(self, read):
        def side_effect():
            raise FileNotFoundError

        read.side_effect = side_effect
        setup = Setup()
        with self.assertRaises(SetupError) as ctx:
            setup.load_from_file('/dummy/path')
        error_cause = ctx.exception.error_cause
        self.assertEqual(error_cause, SetupError.ErrorCauses.WRONG_CONFIG_FILE)

    @patch('tracerface.web_ui.trace_setup.Path.read_text')
    def test_load_from_file_raises_exception_if_file_is_directory(self, read):
        def side_effect():
            raise IsADirectoryError

        read.side_effect = side_effect
        setup = Setup()
        with self.assertRaises(SetupError) as ctx:
            setup.load_from_file('/dummy/path')
        error_cause = ctx.exception.error_cause
        self.assertEqual(error_cause, SetupError.ErrorCauses.WRONG_CONFIG_FILE)

    @patch('tracerface.web_ui.trace_setup.yaml.safe_load')
    @patch('tracerface.web_ui.trace_setup.Path.read_text')
    def test_load_from_file_raises_exception_on_yaml_parse_error(self, read, load):
        def side_effect(content):
            raise ParserError

        load.side_effect = side_effect
        setup = Setup()
        with self.assertRaises(SetupError) as ctx:
            setup.load_from_file('/dummy/path')
        error_cause = ctx.exception.error_cause
        self.assertEqual(error_cause, SetupError.ErrorCauses.WRONG_CONFIG_FILE)

    @patch('tracerface.web_ui.trace_setup.yaml.safe_load')
    @patch('tracerface.web_ui.trace_setup.Path.read_text')
    def test_load_from_file_raises_exception_on_yaml_scan_error(self, read, load):
        def side_effect(content):
            raise ScannerError

        load.side_effect = side_effect
        setup = Setup()
        with self.assertRaises(SetupError) as ctx:
            setup.load_from_file('/dummy/path')
        error_cause = ctx.exception.error_cause
        self.assertEqual(error_cause, SetupError.ErrorCauses.WRONG_CONFIG_FILE)

    @patch('tracerface.web_ui.trace_setup.yaml.safe_load', return_value={'dummy_built_in' : {}})
    @patch('tracerface.web_ui.trace_setup.Path.read_text')
    def test_load_from_file_adds_built_in_if_binary_not_found(self, read, load):
        setup = Setup()
        setup.load_from_file('dummy/path')
        self.assertIn('built-ins', setup._setup)
        self.assertIn('dummy_built_in', setup._setup['built-ins'])


if __name__ == '__main__':
    main()
