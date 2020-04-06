from model.parse_stack import parse_stack


def test_parse_stack_returns_empty_graph_for_empty_stack():
    result = parse_stack([])

    assert result.nodes == {}
    assert result.edges == {}


def test_parse_stack_returns_empty_graph_for_stack_with_no_calls_in_right_format():
    result = parse_stack(['no calls'])

    assert result.nodes == {}
    assert result.edges == {}


def test_parse_stack_returns_nodes_for_stack_with_one_call():
    stack = [
        "19059  19059  dummy_source1 func1",
        "-14",
        "b'func1+0x0 [dummy_source1]'"
    ]

    result = parse_stack(stack)
    assert list(result.nodes.values()) == [{'call_count': 1, 'name': 'func1', 'source': 'dummy_source1'}]
    assert list(result.edges.values()) == []


def test_parse_stack_returns_nodes_for_stack_with_no_params():
    stack = [
        "19059  19059  dummy_source1 func1",
        "-14",
        "b'func1+0x0 [dummy_source1]'",
        "b'func2+0x26 [dummy_source1]'",
        "b'func3+0x17 [dummy_source2]'",
        "b'[unknown]'"
    ]

    result = parse_stack(stack)

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
        "19059  19059  dummy_source1 func1        b'param1' b'param2'",
        "-14",
        "b'func1+0x0 [dummy_source1]'",
        "b'func2+0x26 [dummy_source1]'",
        "b'func3+0x17 [dummy_source2]'",
    ]

    result = parse_stack(stack)

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
        "PID    TID    COMM         FUNC             ",
        "19059  19059  dummy_source1 func1        ",
        "        -14",
        "b'func1+0x0 [dummy_source1]'",
        "b'func2+0x26 [dummy_source1]'",
        "b'func3+0x17 [dummy_source2]'",
        "b'[unknown]'"
    ]

    result = parse_stack(stack)

    assert sorted(list(result.nodes.values()), key = lambda i: i['name']) == [
        {'call_count': 1, 'name': 'func1', 'source': 'dummy_source1'},
        {'call_count': 0, 'name': 'func2', 'source': 'dummy_source1'},
        {'call_count': 0, 'name': 'func3', 'source': 'dummy_source2'},
    ]

    assert sorted(list(result.edges.values()), key = lambda i: i['call_count'], reverse=True) == [
        {'call_count': 1, 'param': []},
        {'call_count': 0, 'param': []},
    ]


def test_parse_stack_returns_empty_stack_for_header_only():
    stack = [
        "PID    TID    COMM         FUNC             ",
    ]

    result = parse_stack(stack)

    assert result.nodes == {}
    assert result.edges == {}

