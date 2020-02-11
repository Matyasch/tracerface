from unittest.mock import call, Mock, patch

from model.base import BaseModel


def test_empty_model():
    model = BaseModel()

    assert model.get_edges() == {}
    assert model.get_nodes() == {}


@patch('model.base.Persistence')
def test_get_nodes_gets_nodes_from_persistence(persistence):
    model = BaseModel()

    model.get_nodes()

    persistence.return_value.get_nodes.assert_called_once()


@patch('model.base.Persistence')
def test_get_edges_gets_edges_from_persistence(persistence):
    model = BaseModel()

    model.get_edges()

    persistence.return_value.get_edges.assert_called_once()


@patch('model.base.Persistence')
def test_yellow_count_gets_range_from_persistence(persistence):
    model = BaseModel()

    model.yellow_count()

    persistence.return_value.get_yellow.assert_called_once()


@patch('model.base.Persistence')
def test_red_count_gets_range_from_persistence(persistence):
    model = BaseModel()

    model.red_count()

    persistence.return_value.get_red.assert_called_once()


@patch('model.base.Persistence.get_nodes')
def test_max_count_gets_with_no_nodes(get_nodes):
    model = BaseModel()

    assert model.max_count() == 0


@patch('model.base.Persistence.get_nodes', return_value={
        'dummy_hash1': {'name': 'dummy_name1', 'source': 'dummy_source1', 'call_count': 2},
        'dummy_hash2': {'name': 'dummy_name2', 'source': 'dummy_source2', 'call_count': 5}
    })
def test_max_count_gets_with_nodes(get_nodes):
    model = BaseModel()

    assert model.max_count() == 5


@patch('model.base.Persistence')
def test_set_range_calls_persistence_with_right_params(persistence):
    model = BaseModel()

    model.set_range('dummy_yellow', 'dummy_red')

    persistence.return_value.update_colors.assert_called_once()
    persistence.return_value.update_colors.assert_called_with('dummy_yellow', 'dummy_red')


@patch('model.base.Persistence')
def test_init_colors(persistence):
    model = BaseModel()
    model.max_count = Mock(return_value=8)

    model.init_colors()

    assert model.max_count.call_count == 2
    persistence.return_value.update_colors.assert_called_once()
    persistence.return_value.update_colors.assert_called_with(3, 5)


def test_parse_stack_returns_empty_graph_for_empty_stack():
    result = BaseModel.parse_stack([])

    assert result.nodes == {}
    assert result.edges == {}


def test_parse_stack_returns_empty_graph_for_stack_with_no_calls_in_right_format():
    result = BaseModel.parse_stack(['no calls'])

    assert result.nodes == {}
    assert result.edges == {}


def test_parse_stack_returns_nodes_for_stack_with_one_call():
    stack = [
        "19059  19059  dummy_source1 func1",
        "-14",
        "b'func1+0x0 [dummy_source1]'"
    ]

    result = BaseModel.parse_stack(stack)
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

    result = BaseModel.parse_stack(stack)

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

    result = BaseModel.parse_stack(stack)

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

    result = BaseModel.parse_stack(stack)

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

    result = BaseModel.parse_stack(stack)

    assert result.nodes == {}
    assert result.edges == {}

