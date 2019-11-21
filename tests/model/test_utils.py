from pytest import raises

import model.utils as utils


def test_format_specs():
    assert utils.format_specs() == [
        ('char', '%c'),
        ('double/float', '%f'),
        ('int', '%d'),
        ('long', '%l'),
        ('long double', '%lF'),
        ('string/char *', '%s'),
        ('short', '%hi'),
        ('unsigned short', '%hi'),
        ('void *', '%p'),
    ]


def test_flatten_trace_dict_raises_exception_on_empty_dict():
    with raises(utils.ProcessException) as excinfo:
        utils.flatten_trace_dict({})
    assert str(excinfo.value) == 'No functions to trace'


def test_flatten_trace_dict_raises_exception_on_only_apps():
    with raises(utils.ProcessException) as excinfo:
        utils.flatten_trace_dict({'app1': {}, 'app2': {}})
    assert str(excinfo.value) == 'No functions to trace'


def test_flatten_trace_dict_single_app_single_func():
    result = utils.flatten_trace_dict({'app': {'func': {}}})
    assert result == ['app:func']


def test_flatten_trace_dict_single_app_multiple_funcs():
    result = utils.flatten_trace_dict({'app': {'func1': {}, 'func2': {}}})
    assert sorted(result) == ['app:func1', 'app:func2']


def test_flatten_trace_dict_multiple_apps_each_with_single_func():
    result = utils.flatten_trace_dict({
        'app1': {'func1': {}},
        'app2': {'func2': {}}})
    assert sorted(result) == ['app1:func1', 'app2:func2']


def test_flatten_trace_dict_multiple_apps_each_with_multiple_funcs():
    result = utils.flatten_trace_dict({
        'app1': {'func1': {}, 'func2': {}},
        'app2': {'func3': {}, 'func4': {}}})
    assert result == ['app1:func1', 'app1:func2', 'app2:func3', 'app2:func4']


def test_flatten_trace_dict_single_param_in_single_function():
    result = utils.flatten_trace_dict({'app': {'func': {'arg1': '%s'}}})
    assert result == ['app:func "%s", arg1']


def test_flatten_trace_dict_multiple_params_in_single_function():
    result = utils.flatten_trace_dict({'app': {'func': {'arg1': '%s', 'arg3': '%d'}}})
    assert result == ['app:func "%s %d", arg1, arg3']


def test_flatten_trace_dict_single_param_in_multiple_functions():
    result = utils.flatten_trace_dict({'app': {
        'func1': {'arg4': '%s'},
        'func2': {'arg2': '%f'}}})
    assert result == ['app:func1 "%s", arg4', 'app:func2 "%f", arg2']


def test_flatten_trace_dict_multiple_params_in_multiple_functions():
    result = utils.flatten_trace_dict({'app': {
        'func1': {'arg4': '%s', 'arg2': '%d'},
        'func2': {'arg2': '%f', 'arg1': '%hi'}}})
    assert result == ['app:func1 "%d %s", arg2, arg4', 'app:func2 "%hi %f", arg1, arg2']


def test_parse_stack_returns_empty_graph_for_empty_stack():
    result = utils.parse_stack([])

    assert result.nodes == {}
    assert result.edges == {}


def test_parse_stack_returns_empty_graph_for_stack_with_no_calls():
    result = utils.parse_stack(['no calls'])

    assert result.nodes == {}
    assert result.edges == {}


def test_parse_stack_returns_nodes_for_stack_with_one_call():
    stack = [
        '19059  19059  dummy_source1 func1        ',
        '        -14',
        '        func1+0x0 [dummy_source1]',
    ]

    result = utils.parse_stack(stack)
    assert list(result.nodes.values()) == [{'call_count': 1, 'name': 'func1', 'source': 'dummy_source1'}]
    assert list(result.edges.values()) == []


def test_parse_stack_returns_nodes_for_stack_with_no_params():
    stack = [
        '19059  19059  dummy_source1 func1        ',
        '        -14',
        '        func1+0x0 [dummy_source1]',
        '        func2+0x26 [dummy_source1]',
        '        func3+0x17 [dummy_source2]',
        '        [unknown]'
    ]

    result = utils.parse_stack(stack)

    assert sorted(list(result.nodes.values()), key = lambda i: i['name']) == [
        {'call_count': 1, 'name': 'func1', 'source': 'dummy_source1'},
        {'call_count': 0, 'name': 'func2', 'source': 'dummy_source1'},
        {'call_count': 0, 'name': 'func3', 'source': 'dummy_source2'},
    ]

    assert sorted(list(result.edges.values()), key = lambda i: i['call_count'], reverse=True) == [
        {'call_count': 1, 'param': []},
        {'call_count': 0, 'param': []},
    ]


def test_parse_stack_returns_nodes_for_stack_with_params():
    stack = [
        '19059  19059  dummy_source1 func1        param1 param2',
        '        -14',
        '        func1+0x0 [dummy_source1]',
        '        func2+0x26 [dummy_source1]',
        '        func3+0x17 [dummy_source2]',
    ]

    result = utils.parse_stack(stack)

    assert sorted(list(result.nodes.values()), key = lambda i: i['name']) == [
        {'call_count': 1, 'name': 'func1', 'source': 'dummy_source1'},
        {'call_count': 0, 'name': 'func2', 'source': 'dummy_source1'},
        {'call_count': 0, 'name': 'func3', 'source': 'dummy_source2'},
    ]

    assert sorted(list(result.edges.values()), key = lambda i: i['call_count'], reverse=True) == [
        {'call_count': 1, 'param': ['param1', 'param2']},
        {'call_count': 0, 'param': []},
    ]


def test_parse_stack_returns_nodes_for_stack_with_header():
    stack = [
        'PID    TID    COMM         FUNC             ',
        '19059  19059  dummy_source1 func1        ',
        '        -14',
        '        func1+0x0 [dummy_source1]',
        '        func2+0x26 [dummy_source1]',
        '        func3+0x17 [dummy_source2]',
        '        [unknown]'
    ]

    result = utils.parse_stack(stack)

    assert sorted(list(result.nodes.values()), key = lambda i: i['name']) == [
        {'call_count': 1, 'name': 'func1', 'source': 'dummy_source1'},
        {'call_count': 0, 'name': 'func2', 'source': 'dummy_source1'},
        {'call_count': 0, 'name': 'func3', 'source': 'dummy_source2'},
    ]

    assert sorted(list(result.edges.values()), key = lambda i: i['call_count'], reverse=True) == [
        {'call_count': 1, 'param': []},
        {'call_count': 0, 'param': []},
    ]


def test_text_to_stacks_returns_empty_stack_for_empty_string():
    assert utils.text_to_stacks('') == [['']]


def test_text_to_stacks_with_one_stack():
    stack = [
        '19059  19059  dummy_source1 func1        \n',
        '        -14\n',
        '        func1+0x0 [dummy_source1]\n',
        '        func2+0x26 [dummy_source1]\n',
        '        func3+0x17 [dummy_source2]'
    ]

    assert utils.text_to_stacks(''.join(stack)) == [[
        '19059  19059  dummy_source1 func1        ',
        '        -14',
        '        func1+0x0 [dummy_source1]',
        '        func2+0x26 [dummy_source1]',
        '        func3+0x17 [dummy_source2]'
    ]]


def test_text_to_stacks_with_multiple_stacks():
    stack = [
        '19059  19059  dummy_source1 func1        \n',
        '        -14\n',
        '        func1+0x0 [dummy_source1]\n',
        '        func2+0x26 [dummy_source1]\n',
        '        func3+0x17 [dummy_source2]\n',
        '\n'
        '19059  19059  dummy_source3 func4        \n',
        '        -14\n',
        '        func4+0x0 [dummy_source3]\n',
        '        func5+0x26 [dummy_source4]\n',
        '        func6+0x17 [dummy_source4]'
    ]

    assert utils.text_to_stacks(''.join(stack)) == [
        [
            '19059  19059  dummy_source1 func1        ',
            '        -14',
            '        func1+0x0 [dummy_source1]',
            '        func2+0x26 [dummy_source1]',
            '        func3+0x17 [dummy_source2]'
        ],
        [
            '19059  19059  dummy_source3 func4        ',
            '        -14',
            '        func4+0x0 [dummy_source3]',
            '        func5+0x26 [dummy_source4]',
            '        func6+0x17 [dummy_source4]'
        ]
    ]


def test_extract_config_raises_error_for_invalid_path_type():
    with raises(utils.ProcessException) as excinfo:
        utils.extract_config(None)

    assert str(excinfo.value) == 'Please provide a path to the configuration file'


def test_extract_config_raises_error_for_invalid_path_value():
    with raises(utils.ProcessException) as excinfo:
        utils.extract_config('.non/existent/path')

    assert str(excinfo.value) == 'Could not find configuration file at .non/existent/path'


def test_extract_config_raises_error_on_directory(tmp_path):
    with raises(utils.ProcessException) as excinfo:
        utils.extract_config(tmp_path)

    assert str(excinfo.value) == '{} is a directory, not a file'.format(str(tmp_path))


def test_extract_config_raises_error_on_invalid_yaml_format(tmp_path):
    config_file = tmp_path.joinpath('config')
    config_file.write_text('invalid:yaml:\ncontent')

    with raises(utils.ProcessException) as excinfo:
        utils.extract_config(config_file)

    assert str(excinfo.value) == 'Config file at {} has to be YAML format'.format(str(config_file))


def test_extract_config_raises_error_on_unknown_exception(tmp_path):
    config_file = tmp_path.joinpath('config')
    config_file.write_text('c:\n  - [- asd: dsa]')

    with raises(utils.ProcessException) as excinfo:
        utils.extract_config(config_file)

    assert str(excinfo.value) == 'Unknown error happened while processing config file'


def test_extract_config_raises_error_on_invalid_config_format(tmp_path):
    config_file = tmp_path.joinpath('config')
    config_file.write_text('app1:func1:func2:func3')

    with raises(utils.ProcessException) as excinfo:
        utils.extract_config(config_file)

    assert str(excinfo.value) == 'Could not process configuration file'


def test_extract_config_raises_error_if_no_functions_to_trace(tmp_path):
    config_file = tmp_path.joinpath('config')
    config_file.write_text('app1: []\napp2: []')

    with raises(utils.ProcessException) as excinfo:
        utils.extract_config(config_file)

    assert str(excinfo.value) == 'No functions to trace'


def test_extract_config_with_single_app_and_single_func(tmp_path):
    config_file = tmp_path.joinpath('config')
    config_file.write_text('app:\n  - func')

    result = utils.extract_config(config_file)

    assert result == ['app:func']


def test_extract_config_with_single_app_and_multiple_funcs(tmp_path):
    config_file = tmp_path.joinpath('config')
    config_file.write_text('app:\n  - func1\n  - func2')

    result = utils.extract_config(config_file)

    assert sorted(result) == ['app:func1','app:func2']


def test_extract_config_with_multiple_app_with_single_funcs(tmp_path):
    config_file = tmp_path.joinpath('config')
    config_file.write_text('app1:\n  - func1\napp2:\n  - func2')

    result = utils.extract_config(config_file)

    assert sorted(result) == ['app1:func1','app2:func2']


def test_extract_config_with_multiple_app_with_multiple_funcs(tmp_path):
    config_file = tmp_path.joinpath('config')
    config_file.write_text('app1:\n  - func1\n  - func2\napp2:\n  - func3\n  - func4')

    result = utils.extract_config(config_file)

    assert sorted(result) == ['app1:func1', 'app1:func2', 'app2:func3', 'app2:func4']


def test_extract_config_with_single_param(tmp_path):
    config_file = tmp_path.joinpath('config')
    config_file.write_text("app:\n  - func:\n    - '%type'")

    result = utils.extract_config(config_file)

    assert result == ['app:func "%type", arg1']


def test_extract_config_with_multiple_params(tmp_path):
    config_file = tmp_path.joinpath('config')
    config_file.write_text("app:\n  - func:\n    - '%type1'\n    - '%type2'")

    result = utils.extract_config(config_file)

    assert result == ['app:func "%type1 %type2", arg1, arg2']