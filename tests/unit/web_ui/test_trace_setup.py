#!/usr/bin/env python3
from unittest import main, TestCase
from unittest.mock import patch

from yaml.parser import ParserError, ScannerError

from tracerface.web_ui.trace_setup import (
    BinaryAlreadyAddedError,
    BinaryNotExistsError,
    ConfigFileError,
    FunctionNotInBinaryError,
    BuiltInNotExistsError,
    Setup
)


def dummy_setup():
    return {
        'app1': {
            'func1': {'traced': False, 'parameters': {}, 'mangled': 'mangledfunc1', 'offset': 0},
            'func3': {'traced': False, 'parameters': {}, 'mangled': 'mangledfunc3', 'offset': 0}
        },
        'app2': {
            'func2': {'traced': False, 'parameters': {}, 'mangled': 'mangledfunc2', 'offset': 0}
        }
    }


class TestInitBinary(TestCase):
    @patch('tracerface.web_ui.trace_setup.check_output', return_value=b'func1\nfunc2\nfunc3\n')
    def test_initialize_binary(self, nm):
        setup = Setup()

        setup.initialize_binary('app')

        expected = {
            'app': {
                'func1': {'mangled': 'func1', 'traced': False, 'parameters': {}, 'offset': 0},
                'func2': {'mangled': 'func2', 'traced': False, 'parameters': {}, 'offset': 0},
                'func3': {'mangled': 'func3', 'traced': False, 'parameters': {}, 'offset': 0}
            }
        }
        self.assertEqual(setup._setup, expected)

    def test_init_binary_raises_error_if_binary_already_added(self):
        setup = Setup()
        setup._setup = dummy_setup()
        with self.assertRaises(BinaryAlreadyAddedError):
            setup.initialize_binary('app1')

    def test_init_binary_raises_error_if_binary_not_exists(self):
        setup = Setup()
        with self.assertRaises(BinaryNotExistsError):
            setup.initialize_binary('non_existent_app')


class TestRemoveApp(TestCase):
    def test_remove_app(self):
        setup = Setup()
        setup._setup = dummy_setup()

        setup.remove_app('app2')

        expected = {
            'app1': {
                'func1': {'traced': False, 'parameters': {}, 'mangled': 'mangledfunc1', 'offset': 0},
                'func3': {'traced': False, 'parameters': {}, 'mangled': 'mangledfunc3', 'offset': 0}
            }
        }
        self.assertEqual(setup._setup, expected)


class TestInitBuiltin(TestCase):
    @patch('tracerface.web_ui.trace_setup.Setup.get_offset_for_built_in', return_value=12)
    def test_initialize_built_in(self, get_offset_for_built_in):
        setup = Setup()

        setup.initialize_built_in('app')

        expected = {'built-ins': {'app': {'traced': True, 'parameters': {}, 'offset': 12}}}
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
            'func1': {'traced': False, 'parameters': {}, 'mangled': 'mangledfunc1', 'offset': 0},
            'func3': {'traced': False, 'parameters': {}, 'mangled': 'mangledfunc3', 'offset': 0}
        }
        self.assertEqual(result, expected)


class TestSetupFunctionToTrace(TestCase):
    @patch('tracerface.web_ui.trace_setup.Setup.get_offset_for_function', return_value=8)
    def test_setup_function_to_trace_with_demangled_name(self, get_offset_for_function):
        setup = Setup()
        setup._setup = dummy_setup()

        setup.setup_function_to_trace('app1', 'func1')

        expected = {
            'app1': {
                'func1': {'traced': True, 'parameters': {}, 'mangled': 'mangledfunc1', 'offset': 8},
                'func3': {'traced': False, 'parameters': {}, 'mangled': 'mangledfunc3', 'offset': 0}
            },
            'app2': {
                'func2': {'traced': False, 'parameters': {}, 'mangled': 'mangledfunc2', 'offset': 0}
            }
        }
        self.assertEqual(setup._setup, expected)

    @patch('tracerface.web_ui.trace_setup.Setup.get_offset_for_function', return_value=10)
    def test_setup_function_to_trace_with_mangled_name(self, get_offset_for_function):
        setup = Setup()
        setup._setup = dummy_setup()

        setup.setup_function_to_trace('app1', 'mangledfunc1')

        expected = {
            'app1': {
                'func1': {'traced': True, 'parameters': {}, 'mangled': 'mangledfunc1', 'offset': 10},
                'func3': {'traced': False, 'parameters': {}, 'mangled': 'mangledfunc3', 'offset': 0}
            },
            'app2': {
                'func2': {'traced': False, 'parameters': {}, 'mangled': 'mangledfunc2', 'offset': 0}
            }
        }
        self.assertEqual(setup._setup, expected)

    def test_setup_function_to_trace_raises_error_if_function_not_exists(self):
        setup = Setup()
        setup._setup = dummy_setup()
        with self.assertRaises(FunctionNotInBinaryError):
            setup.setup_function_to_trace('app1', 'func4')


class TestRemoveFunctionFromTrace(TestCase):
    @patch('tracerface.web_ui.trace_setup.Setup.get_offset_for_function', return_value=8)
    def test_remove_function_from_trace_with_demangled_name(self, get_offset_for_function):
        setup = Setup()
        setup._setup = dummy_setup()

        setup.setup_function_to_trace('app1', 'func1')
        setup.remove_function_from_trace('app1', 'func1')

        expected_setup = dummy_setup()
        expected_setup['app1']['func1']['offset'] = 8

        self.assertEqual(setup._setup, expected_setup)

    @patch('tracerface.web_ui.trace_setup.Setup.get_offset_for_function', return_value=8)
    def test_remove_function_from_trace_with_mangled_name(self, get_offset_for_function):
        setup = Setup()
        setup._setup = dummy_setup()

        setup.setup_function_to_trace('app1', 'func1')
        setup.remove_function_from_trace('app1', 'mangledfunc1')

        expected_setup = dummy_setup()
        expected_setup['app1']['func1']['offset'] = 8

        self.assertEqual(setup._setup, expected_setup)

    def test_remove_function_from_trace_raises_error_if_function_not_exists(self):
        setup = Setup()
        setup._setup = dummy_setup()
        with self.assertRaises(FunctionNotInBinaryError):
            setup.remove_function_from_trace('app1', 'func4')


class TestParameters(TestCase):
    def test_get_parameters(self):
        setup = Setup()
        setup._setup = {'app': {'func': {'traced': False, 'parameters': {1: '%s', 4: '%d'}, 'offset': 0}}}

        result = setup.get_parameters('app', 'func')

        self.assertEqual(result, {1: '%s', 4: '%d'})

    def test_add_parameter(self):
        setup = Setup()
        setup._setup = dummy_setup()

        setup.add_parameter('app1', 'func3', 2, '%s')

        expected = {
            'app1': {
                'func1': {'traced': False, 'parameters': {}, 'mangled': 'mangledfunc1', 'offset': 0},
                'func3': {'traced': False, 'parameters': {2: '%s'}, 'mangled': 'mangledfunc3', 'offset': 0}
            },
            'app2': {
                'func2': {'traced': False, 'parameters': {}, 'mangled': 'mangledfunc2', 'offset': 0}
            }
        }
        self.assertEqual(setup._setup, expected)

    def test_remove_parameter(self):
        setup = Setup()
        setup._setup = {'app': {'func': {'traced': False, 'parameters': {1: '%s', 4: '%d'}, 'offset': 0}}}

        setup.remove_parameter('app', 'func', 4)

        expected = {'app': {'func': {'traced': False, 'parameters': {1: '%s'}, 'offset': 0}}}
        self.assertEqual(setup._setup, expected)

class TestGenerateBCCArgs(TestCase):
    def test_generate_bcc_args_with_multiple_values(self):
        setup = Setup()
        setup._setup = {
            'app1': {
                'func1': {'mangled': 'mangled1', 'traced': True, 'parameters':{4: '%s', 2: '%d'}, 'offset': 8},
                'func2': {'mangled': 'mangled2', 'traced': False, 'parameters':{}, 'offset': 0}
            },
            'app2': {
                'func3': {'mangled': 'mangled3', 'traced': True, 'parameters':{1: '%s', 5: '%d'}, 'offset': 11},
                'func4': {'mangled': 'mangled4', 'traced': True, 'parameters':{1: '%s', 2: '%f'}, 'offset': 16}
            }
        }
        result = setup.generate_bcc_args()
        expected = [
            'app1:mangled1+0x8 "%s %d", arg4, arg2',
            'app2:mangled3+0xB "%s %d", arg1, arg5',
            'app2:mangled4+0x10 "%s %f", arg1, arg2'
        ]
        self.assertEqual(result, expected)


class TestLoadFromFile(TestCase):
    @patch('tracerface.web_ui.trace_setup.Path.read_text')
    def test_load_from_file_raises_exception_if_file_not_found(self, read):
        def side_effect():
            raise FileNotFoundError

        read.side_effect = side_effect
        setup = Setup()
        with self.assertRaises(ConfigFileError):
            setup.load_from_file('/dummy/path')

    @patch('tracerface.web_ui.trace_setup.Path.read_text')
    def test_load_from_file_raises_exception_if_file_is_directory(self, read):
        def side_effect():
            raise IsADirectoryError

        read.side_effect = side_effect
        setup = Setup()
        with self.assertRaises(ConfigFileError) as ctx:
            setup.load_from_file('/dummy/path')

    @patch('tracerface.web_ui.trace_setup.yaml.safe_load')
    @patch('tracerface.web_ui.trace_setup.Path.read_text')
    def test_load_from_file_raises_exception_on_yaml_parse_error(self, read, load):
        def side_effect(content):
            raise ParserError

        load.side_effect = side_effect
        setup = Setup()
        with self.assertRaises(ConfigFileError) as ctx:
            setup.load_from_file('/dummy/path')

    @patch('tracerface.web_ui.trace_setup.yaml.safe_load')
    @patch('tracerface.web_ui.trace_setup.Path.read_text')
    def test_load_from_file_raises_exception_on_yaml_scan_error(self, read, load):
        def side_effect(content):
            raise ScannerError

        load.side_effect = side_effect
        setup = Setup()
        with self.assertRaises(ConfigFileError) as ctx:
            setup.load_from_file('/dummy/path')

    @patch('tracerface.web_ui.trace_setup.yaml.safe_load', return_value={'dummy_built_in' : {}})
    @patch('tracerface.web_ui.trace_setup.Path.read_text')
    @patch('tracerface.web_ui.trace_setup.Setup.get_offset_for_built_in', return_value=8)
    def test_load_from_file_adds_built_in_if_binary_not_found(self, read, load, get_offset_for_built_in):
        setup = Setup()
        setup.load_from_file('dummy/path')
        self.assertIn('built-ins', setup._setup)
        self.assertIn('dummy_built_in', setup._setup['built-ins'])


class TestGetOffsetForBuiltIn(TestCase):
    @patch('tracerface.web_ui.trace_setup.check_output', side_effect=[b'0\n10', b'push %rbp\nmov %rsp,%rbp\n0x8'])
    def test_get_offset_for_built_in_existing(self, check_output):
        setup = Setup()
        result = setup.get_offset_for_built_in('builtin_func')
        expected = 8
        self.assertEqual(result, expected)

    @patch('tracerface.web_ui.trace_setup.check_output', side_effect=[b'0\n10', b'line1\nline2'])
    def test_get_offset_for_built_in_no_match(self, check_output):
        setup = Setup()
        result = setup.get_offset_for_built_in('builtin_func')
        expected = 0
        self.assertEqual(result, expected)

    def test_get_offset_for_built_in_non_existing(self):
        setup = Setup()
        with self.assertRaises(BuiltInNotExistsError):
            setup.get_offset_for_built_in('no_such_built_in')


class TestGetOffsetForFunction(TestCase):
    @patch('tracerface.web_ui.trace_setup.check_output', return_value=b'push %rbp\nmov %rsp,%rbp\n<func1+0x1a>')
    def test_get_offset_for_function_hexadecimal(self, check_output):
        setup = Setup()
        result = setup.get_offset_for_function('app', 'func1')
        expected = 26
        self.assertEqual(result, expected)

    @patch('tracerface.web_ui.trace_setup.check_output', return_value=b'extra1\npush %rbp\nextra2\nmov %rsp,%rbp\nextra3\n<func2+0x8>')
    def test_get_offset_for_function_extra_lines(self, check_output):
        setup = Setup()
        result = setup.get_offset_for_function('app', 'func2')
        expected = 8
        self.assertEqual(result, expected)

    @patch('tracerface.web_ui.trace_setup.check_output', return_value=b'line1\nline2')
    def test_get_offset_for_function_no_match(self, check_output):
        setup = Setup()
        result = setup.get_offset_for_function('app', 'func')
        expected = 0
        self.assertEqual(result, expected)

if __name__ == '__main__':
    main()
