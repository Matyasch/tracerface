from enum import Enum
from pathlib import Path
from subprocess import CalledProcessError, check_output
import yaml

import cxxfilt


class SetupError(Exception):
    class ErrorCauses(Enum):
        BINARY_ALREADY_ADDED = 1
        BINARY_NOT_FOUND = 2
        FUNCTION_NOT_EXISTS_IN_BINARY = 3
        WRONG_CONFIG_FILE = 4

    def __init__(self, message, cause):
        super().__init__(message)
        self._error_cause = cause

    @classmethod
    def init_binary_already_added(cls, message):
        return cls(message=message, cause=cls.ErrorCauses.BINARY_ALREADY_ADDED)

    @classmethod
    def init_binary_not_found(cls, message):
        return cls(message=message, cause=cls.ErrorCauses.BINARY_NOT_FOUND)

    @classmethod
    def init_function_not_exists_in_binary(cls, message):
        return cls(message=message, cause=cls.ErrorCauses.FUNCTION_NOT_EXISTS_IN_BINARY)

    @classmethod
    def init_wrong_config_file(cls, message):
        return cls(message=message, cause=cls.ErrorCauses.WRONG_CONFIG_FILE)

    @property
    def error_cause(self):
        return self._error_cause


class Setup:
    def __init__(self):
        self._setup = {}

    # initialize app and its functions for tracing
    def initialize_binary(self, path):
        if path in self._setup:
            raise SetupError.init_binary_already_added('Binary at {} already added'.format(path))

        try:
            symbols = check_output(['nm', path]).decode().rstrip().split('\n')
        except CalledProcessError:
            err_message = 'Could not find binary at {}, so it is assumed to be a built-in function'.format(path)
            raise SetupError.init_binary_not_found(err_message)

        functions = [symbol.split()[-1] for symbol in symbols]
        init_state = {}
        for function in functions:
            try:
                name = cxxfilt.demangle(function)
            except cxxfilt.InvalidName:
                name = function
            init_state[name] = {
                'mangled': function,
                'traced': False,
                'parameters': {}
            }
        self._setup[path] = init_state

    def initialize_built_in(self, func_name):
        if 'built-ins' not in self._setup:
            self._setup['built-ins'] = {}
        self._setup['built-ins'][func_name] = {
            'traced': True,
            'parameters': {}
        }

    # Remove application from getting traced
    def remove_app(self, app):
        del self._setup[app]

    # Returns apps currently saved
    def get_apps(self):
        return list(self._setup.keys())

    # Return functions and their state of a given application
    def get_setup_of_app(self, app):
        return self._setup[app]

    # Sets up a function to be traced
    def setup_function_to_trace(self, app, function):
        try:
            self._setup[app][function]['traced'] = True
        except KeyError:
            for func_name in self._setup[app]:
                if self._setup[app][func_name]['mangled'] == function:
                    self._setup[app][func_name]['traced'] = True
                    return
            err_message = 'No function named {} was found in {}'.format(function, app)
            raise SetupError.init_function_not_exists_in_binary(err_message)

    # Removes a function from traced ones
    def remove_function_from_trace(self, app, function):
        try:
            self._setup[app][function]['traced'] = False
        except KeyError:
            for func_name in self._setup[app]:
                if self._setup[app][func_name]['mangled'] == function:
                    self._setup[app][func_name]['traced'] = False
                    return
            err_message = 'No function named {} was found in {}'.format(function, app)
            raise SetupError.init_function_not_exists_in_binary(err_message)

    # Returns the indexes where a parameter is set for tracing
    def get_parameters(self, app, function):
        return self._setup[app][function]['parameters']

    # Sets up a parameter to be traced
    def add_parameter(self, app, function, index, format):
        self._setup[app][function]['parameters'][index] = format

    # Removes a parameter from traced ones
    def remove_parameter(self, app, function, index):
        del self._setup[app][function]['parameters'][index]

    # Convert dictionary of functions to trace into properly
    # structured list of args to be used by the trace tool
    def generate_bcc_args(self):
        arguments = []
        for app in self._setup:
            for function in self._setup[app]:
                if self._setup[app][function]['traced']:
                    if app == 'built-ins':
                        argument = function
                    else:
                        argument = '{}:{}'.format(app, self._setup[app][function]['mangled'])
                    params = self._setup[app][function]['parameters']
                    if params:
                        argument = '{} "{}", {}'.format(
                            argument,
                            ' '.join([params[index] for index in params]),
                            ', '.join(['arg{}'.format(index) for index in params]))
                    arguments.append(argument)
        return arguments

    def load_from_file(self, path):
        try:
            content = Path(path).read_text()
        except FileNotFoundError:
            raise SetupError.init_wrong_config_file('Could not find config file at {}'.format(path))
        except IsADirectoryError:
            raise SetupError.init_wrong_config_file('{} is a directory, not a file'.format(path))

        try:
            config = yaml.safe_load(content)
        except (yaml.parser.ParserError, yaml.scanner.ScannerError):
            raise SetupError.init_wrong_config_file('File needs to be yaml format')

        try:
            err_message = ''
            for app in config:
                try:
                    self.initialize_binary(app)
                    for function in config[app]:
                        self.setup_function_to_trace(app, function)
                        for index in config[app][function]:
                            self.add_parameter(app, function, index, config[app][function][index])
                except SetupError as err:
                    if err.error_cause == SetupError.ErrorCauses.BINARY_NOT_FOUND:
                        self.initialize_built_in(app)
                        for index in config[app]:
                            self.add_parameter('built-ins', app, index, config[app][index])
                        err_message = 'Some binaries were not found so they were assumed to be built-in functions'
                    else:
                        raise
            return err_message
        except TypeError:
            raise SetupError.init_wrong_config_file('File format is incorrect')
