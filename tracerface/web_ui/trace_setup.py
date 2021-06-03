from enum import Enum
from pathlib import Path
from subprocess import CalledProcessError, check_output
import yaml
import re

import cxxfilt


class BinaryAlreadyAddedError(Exception):
    def __init__(self, message=''):
        super().__init__(message)


class BinaryNotExistsError(Exception):
    def __init__(self, message=''):
        super().__init__(message)


class ConfigFileError(Exception):
    def __init__(self, message=''):
        super().__init__(message)


class FunctionNotInBinaryError(Exception):
    def __init__(self, message=''):
        super().__init__(message)


class BuiltInNotExistsError(Exception):
    def __init__(self, message=''):
        super().__init__(message)


class Setup:
    def __init__(self):
        self._setup = {}

    # initialize app and its functions for tracing
    def initialize_binary(self, path):
        if path in self._setup:
            raise BinaryAlreadyAddedError('Binary at {} already added'.format(path))

        try:
            symbols = check_output(['nm', path]).decode().rstrip().split('\n')
        except CalledProcessError:
            raise BinaryNotExistsError

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
                'parameters': {},
                'offset': 0
            }
        self._setup[path] = init_state

    # search offset after setting stack pointer for built-in function
    def get_offset_for_built_in(self, func_name):
        offset = 0
        try:
            # search address of function in symbol map
            sym_address = check_output(
                            ['sudo',
                             'grep',
                             '-A1',
                             '-w',
                             func_name,
                             '/proc/kallsyms']
                          ).decode().rstrip().split('\n')
            if len(sym_address) == 2:
                # address of given function
                start_address = -1
                start_address_match = re.search(r'^([a-f0-9]+)', sym_address[0])
                if start_address_match:
                    start_address = int(start_address_match.group(1), base=16)

                # address of following symbol
                stop_address = -1
                stop_address_match = re.search(r'^([a-f0-9]+)', sym_address[1])
                if stop_address_match:
                    stop_address = int(stop_address_match.group(1), base=16)

                if start_address >= 0 and stop_address >= 0:
                    # get instructions of function
                    objdump_out = check_output(
                                ['sudo',
                                    'objdump',
                                    '--prefix-addresses',
                                    '-d',
                                    '--start-address=0x{:X}'.format(start_address),
                                    '--stop-address=0x{:X}'.format(stop_address),
                                    '/proc/kcore']
                                ).decode().rstrip().split('\n')
                    # search first instruction after function prologue
                    first = False
                    second = False
                    for line in objdump_out:
                        if first and second:
                            func_offset = re.search(r'(0x[a-f0-9]+)', line)
                            if func_offset:
                                # needed offset is difference between function's base address and
                                # address of first instruction after function prologue
                                offset = int(func_offset.group(1), base=16) - start_address
                                break

                        # second instruction of function prologue
                        if first and re.search(r'mov\s+%rsp,%rbp', line):
                            second = True

                        # first instruction of function prologue
                        if not(first) and re.search(r'push\s+%rbp', line):
                            first = True
        except CalledProcessError:
            raise BuiltInNotExistsError
        return offset

    # initialize built-in function to be traced
    def initialize_built_in(self, func_name):
        if 'built-ins' not in self._setup:
            self._setup['built-ins'] = {}
        try:
            offset = self.get_offset_for_built_in(func_name)
            self._setup['built-ins'][func_name] = {
                'traced': True,
                'parameters': {},
                'offset': offset
            }
        except BuiltInNotExistsError:
            raise

    # Remove application from getting traced
    def remove_app(self, app):
        del self._setup[app]

    # Returns apps currently saved
    def get_apps(self):
        return list(self._setup.keys())

    # Return functions and their state of a given application
    def get_setup_of_app(self, app):
        return self._setup[app]

    # search offset after setting stack pointer for user function
    def get_offset_for_function(self, app_name, func_name):
        offset = 0
        # get instructions of function
        try:
            objdump_out = check_output(['objdump', "--disassemble="+func_name, "--prefix-addresses", app_name]).decode().rstrip().split('\n')
        except CalledProcessError:
            raise FunctionNotInBinaryError

        first = False
        second = False
        for line in objdump_out:
            if first and second:
                # first instruction after function prologue with offset
                func_offset = re.search(r'<'+func_name+r'\+(0x[a-f0-9]+)>', line)
                if func_offset:
                    offset = int(func_offset.group(1), base=16)
                    break

            # second instruction of function prologue
            if first and re.search(r'mov\s+%rsp,%rbp', line):
                second = True

            # first instruction of function prologue
            if not(first) and re.search(r'push\s+%rbp', line):
                first = True
        return offset

    # Sets up a function to be traced
    def setup_function_to_trace(self, app, function):
        try:
            self._setup[app][function]['traced'] = True
            offset = self.get_offset_for_function(app, function)
            self._setup[app][function]['offset'] = offset

        except KeyError:
            for func_name in self._setup[app]:
                if self._setup[app][func_name]['mangled'] == function:
                    self._setup[app][func_name]['traced'] = True
                    offset = self.get_offset_for_function(app, function)
                    self._setup[app][func_name]['offset'] = offset
                    return
            raise FunctionNotInBinaryError(
                'No function named {} was found in {}'.format(function, app)
            )

    # Removes a function from traced ones
    def remove_function_from_trace(self, app, function):
        try:
            self._setup[app][function]['traced'] = False
        except KeyError:
            for func_name in self._setup[app]:
                if self._setup[app][func_name]['mangled'] == function:
                    self._setup[app][func_name]['traced'] = False
                    return
            raise FunctionNotInBinaryError(
                'No function named {} was found in {}'.format(function, app)
            )

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
                        argument = '{}+0x{:X}'.format(function, self._setup[app][function]['offset'])
                    else:
                        argument = '{}:{}+0x{:X}'.format(app, self._setup[app][function]['mangled'], self._setup[app][function]['offset'])
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
            raise ConfigFileError('Could not find config file at {}'.format(path))
        except IsADirectoryError:
            raise ConfigFileError('{} is a directory, not a file'.format(path))

        try:
            config = yaml.safe_load(content)
        except (yaml.parser.ParserError, yaml.scanner.ScannerError):
            raise ConfigFileError('File needs to be yaml format')

        err_message = ''
        for app in config:
            try:
                self.initialize_binary(app)
                for function in config[app]:
                    self.setup_function_to_trace(app, function)
                    for index in config[app][function]:
                        self.add_parameter(app, function, index, config[app][function][index])
            except BinaryNotExistsError:
                try:
                    self.initialize_built_in(app)
                    for index in config[app]:
                        self.add_parameter('built-ins', app, index, config[app][index])
                    err_message = 'Some binaries were not found so they were assumed to be built-in functions'
                except BuiltInNotExistsError:
                    err_message = 'Some binaries were not found, and neither as built-in functions'
            except TypeError:
                raise ConfigFileError('File format is incorrect')
        return err_message
