#!/usr/bin/env python3

import re
import sys

from_fn = sys.argv[1]
caller_pattern = re.compile('{}')

call_stack = [[from_fn, 'None']]
searching = [from_fn]


def get_caller_pattern(fn_name):
    return re.compile('\s+[0-9]+\s\s\<\s.*\:{}\s\('.format(fn_name))


def get_called(functions):
    for function in functions:
        fn_name = re.search('^\s+[0-9]+\s\s\*\s\s.*\:(.*)\s', function)
        if fn_name:
            return fn_name.group(1)


def get_calls(function_name, stacks):
    called_functions = []
    for stack in stacks:
        functions = stack.split('\n')
        for function in functions:
            if get_caller_pattern(function_name).match(function):
                called_functions.append(get_called(functions))
    return called_functions



with open('teststack.txt') as infile:
    stacks = infile.read().split('\n\n')

while searching:
    caller_function = searching.pop(0)
    called_functions = get_calls(caller_function, stacks)
    for called_function in called_functions:
        call_stack.append([called_function, caller_function])
        searching.append(called_function)


for call in call_stack:
    print(call)
#from_pattern = re.compile('\s\s\s\s[0-9]+\s\s\*\s\(([0-9]+)\)\s{}$'.format(from_fn))