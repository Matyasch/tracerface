#!/usr/bin/env python3
#TODO: Count function calls, which is the subtotal of each call is each stack
import re


def get_caller_pattern(fn_name):
    return re.compile('\s+([0-9]|,)+\s\s\<\s.*\:{}\s\('.format(fn_name))


def get_called(functions):
    for function in functions:
        fn_name = re.search('^^\s+([0-9]|,)+\s\s\*\s\s.*\:(.*)\s\[', function)
        if fn_name:
            return fn_name.group(2)


def get_calls(function_name, stacks):
    called_functions = []
    for stack in stacks:
        functions = stack.split('\n')
        for function in functions:
            if get_caller_pattern(function_name).match(function):
                called_functions.append(get_called(functions))
    return called_functions


def parse_from_file(file, from_fn):
    text = file.read_text()
    return parse_from_strng(text, from_fn)


def parse_from_strng(text, from_fn):
    call_stack = [[from_fn, 'None']]
    searching = [from_fn]
    stacks = text.split('\n\n')

    while searching:
        caller_function = searching.pop(0)
        called_functions = get_calls(caller_function, stacks)
        for called_function in called_functions:
            call_stack.append([called_function, caller_function])
            searching.append(called_function)
    for call in call_stack:
        print(call)
    return call_stack