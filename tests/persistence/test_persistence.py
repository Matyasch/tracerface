from tracerface.persistence.persistence import Persistence


def test_initial_persistence():
    persistence = Persistence()
    assert persistence.nodes == {}
    assert persistence.edges == {}
    assert persistence.yellow == 0
    assert persistence.red == 0


def test_load_single_node():
    persistence = Persistence()
    persistence.load_nodes({'dummy_hash': {'name': 'dummy_name', 'source': 'dummy_source', 'call_count': 1}})
    assert persistence.nodes == {'dummy_hash': {'name': 'dummy_name', 'source': 'dummy_source', 'call_count': 1}}


def test_single_load_different_nodes():
    persistence = Persistence()
    persistence.load_nodes({
        'dummy_hash1': {'name': 'dummy_name1', 'source': 'dummy_source1', 'call_count': 0},
        'dummy_hash2': {'name': 'dummy_name2', 'source': 'dummy_source2', 'call_count': 1}
    })
    assert persistence.nodes == {
        'dummy_hash1': {'name': 'dummy_name1', 'source': 'dummy_source1', 'call_count': 0},
        'dummy_hash2': {'name': 'dummy_name2', 'source': 'dummy_source2', 'call_count': 1}
    }


def test_multiple_load_different_nodes():
    persistence = Persistence()
    persistence.load_nodes({'dummy_hash1': {'name': 'dummy_name1', 'source': 'dummy_source1', 'call_count': 0}})
    persistence.load_nodes({'dummy_hash2': {'name': 'dummy_name2', 'source': 'dummy_source2', 'call_count': 1}})
    assert persistence.nodes == {
        'dummy_hash1': {'name': 'dummy_name1', 'source': 'dummy_source1', 'call_count': 0},
        'dummy_hash2': {'name': 'dummy_name2', 'source': 'dummy_source2', 'call_count': 1}
    }


def test_load_equal_nodes():
    persistence = Persistence()
    persistence.load_nodes({'dummy_hash': {'name': 'dummy_name', 'source': 'dummy_source', 'call_count': 1}})
    persistence.load_nodes({'dummy_hash': {'name': 'dummy_name', 'source': 'dummy_source', 'call_count': 1}})
    assert persistence.nodes == {'dummy_hash': {'name': 'dummy_name', 'source': 'dummy_source', 'call_count': 2}}


def test_load_single_edge_with_no_params():
    persistence = Persistence()
    persistence.load_edges({('node_hash1', 'node_hash2'): {'param': [], 'call_count': 8}})
    assert persistence.edges == {('node_hash1', 'node_hash2'): {'params': [], 'call_count': 8}}


def test_load_single_edge_with_params():
    persistence = Persistence()
    persistence.load_edges({('node_hash1', 'node_hash2'): {'param': ['dummy_param1', 'dummy_param2'], 'call_count': 8}})
    assert persistence.edges == {('node_hash1', 'node_hash2'): {'params': [['dummy_param1', 'dummy_param2']], 'call_count': 8}}


def test_single_load_different_edges():
    persistence = Persistence()
    persistence.load_edges({
        ('node_hash1', 'node_hash2'): {'param': [], 'call_count': 0},
        ('node_hash3', 'node_hash4'): {'param': ['dummy_param'], 'call_count': 3}
    })
    assert persistence.edges == {
        ('node_hash1', 'node_hash2'): {'params': [], 'call_count': 0},
        ('node_hash3', 'node_hash4'): {'params': [['dummy_param']], 'call_count': 3}
    }


def test_multiple_load_different_edges():
    persistence = Persistence()
    persistence.load_edges({('node_hash1', 'node_hash2'): {'param': [], 'call_count': 0}})
    persistence.load_edges({('node_hash3', 'node_hash4'): {'param': ['dummy_param'], 'call_count': 3}})
    assert persistence.edges == {
        ('node_hash1', 'node_hash2'): {'params': [], 'call_count': 0},
        ('node_hash3', 'node_hash4'): {'params': [['dummy_param']], 'call_count': 3}
    }


def test_multiple_load_equal_edges_with_no_params():
    persistence = Persistence()
    persistence.load_edges({('node_hash1', 'node_hash2'): {'param': [], 'call_count': 1}})
    persistence.load_edges({('node_hash1', 'node_hash2'): {'param': [], 'call_count': 3}})
    assert persistence.edges == {('node_hash1', 'node_hash2'): {'params': [], 'call_count': 4}}


def test_multiple_load_equal_edges_with_params():
    persistence = Persistence()
    persistence.load_edges({('node_hash1', 'node_hash2'): {'param': ['dummy_param1', 'dummy_param2'], 'call_count': 1}})
    persistence.load_edges({('node_hash1', 'node_hash2'): {'param': ['dummy_param3', 'dummy_param4'], 'call_count': 3}})
    assert persistence.edges == {('node_hash1', 'node_hash2'): {
            'params': [['dummy_param1', 'dummy_param2'], ['dummy_param3', 'dummy_param4']],
            'call_count': 4}
        }


def test_clear_empty_persistence():
    persistence = Persistence()
    persistence.clear()
    assert persistence.nodes == {}


def test_clear_for_only_nodes():
    persistence = Persistence()
    persistence.load_nodes({
        'dummy_hash1': {'name': 'dummy_name1', 'source': 'dummy_source1', 'call_count': 0},
        'dummy_hash2': {'name': 'dummy_name2', 'source': 'dummy_source2', 'call_count': 1}
    })
    persistence.clear()
    assert persistence.nodes == {}


def test_clear_for_only_edges():
    persistence = Persistence()
    persistence.load_edges({
        ('node_hash1', 'node_hash2'): {'param': [], 'call_count': 0},
        ('node_hash3', 'node_hash4'): {'param': ['dummy_param'], 'call_count': 3}
    })
    persistence.clear()
    assert persistence.edges == {}


def test_clear_for_nodes_and_edges():
    persistence = Persistence()
    persistence.load_nodes({
        'dummy_hash1': {'name': 'dummy_name1', 'source': 'dummy_source1', 'call_count': 0},
        'dummy_hash2': {'name': 'dummy_name2', 'source': 'dummy_source2', 'call_count': 1}
    })
    persistence.load_edges({
        ('node_hash1', 'node_hash2'): {'param': [], 'call_count': 0},
        ('node_hash3', 'node_hash4'): {'param': ['dummy_param'], 'call_count': 3}
    })
    persistence.clear()
    assert persistence.nodes == {}
    assert persistence.edges == {}


def test_max_calls_with_no_nodes():
    persistence = Persistence()
    assert persistence.max_calls() == 0


def test_max_calls_with_zero_call_count():
    persistence = Persistence()
    persistence.load_nodes({'dummy_hash': {'name': 'dummy_name', 'source': 'dummy_source', 'call_count': 0}})
    assert persistence.max_calls() == 0


def test_max_calls_with_single_node():
    persistence = Persistence()
    persistence.load_nodes({'dummy_hash': {'name': 'dummy_name', 'source': 'dummy_source', 'call_count': 3}})
    assert persistence.max_calls() == 3


def test_max_calls_with_single_load_different_nodes():
    persistence = Persistence()
    persistence.load_nodes({
        'dummy_hash1': {'name': 'dummy_name1', 'source': 'dummy_source', 'call_count': 3},
        'dummy_hash2': {'name': 'dummy_name2', 'source': 'dummy_source', 'call_count': 5},
        'dummy_hash3': {'name': 'dummy_name3', 'source': 'dummy_source', 'call_count': 2}})
    assert persistence.max_calls() == 5


def test_max_calls_with_multiple_loads_different_nodes():
    persistence = Persistence()
    persistence.load_nodes({'dummy_hash1': {'name': 'dummy_name1', 'source': 'dummy_source', 'call_count': 3}})
    assert persistence.max_calls() == 3
    persistence.load_nodes({'dummy_hash2': {'name': 'dummy_name2', 'source': 'dummy_source', 'call_count': 5}})
    assert persistence.max_calls() == 5
    persistence.load_nodes({'dummy_hash3': {'name': 'dummy_name3', 'source': 'dummy_source', 'call_count': 2}})
    assert persistence.max_calls() == 5


def test_max_calls_with_multiple_loads_equal_nodes():
    persistence = Persistence()
    persistence.load_nodes({'dummy_hash': {'name': 'dummy_name', 'source': 'dummy_source', 'call_count': 3}})
    assert persistence.max_calls() == 3
    persistence.load_nodes({'dummy_hash': {'name': 'dummy_name', 'source': 'dummy_source', 'call_count': 5}})
    assert persistence.max_calls() == 8
    persistence.load_nodes({'dummy_hash': {'name': 'dummy_name', 'source': 'dummy_source', 'call_count': 2}})
    assert persistence.max_calls() == 10


def test_init_colors_of_empty_persistence():
    persistence = Persistence()
    persistence.init_colors()
    assert persistence.yellow == 0
    assert persistence.red == 0


def test_init_colors_with_0_max_call_count():
    persistence = Persistence()
    persistence.load_nodes({'dummy_hash1': {'name': 'dummy_name1', 'source': 'dummy_source', 'call_count': 0}})
    persistence.init_colors()
    assert persistence.yellow == 0
    assert persistence.red == 0


def test_init_colors_with_three_divisible_call_count():
    persistence = Persistence()
    persistence.load_nodes({'dummy_hash1': {'name': 'dummy_name1', 'source': 'dummy_source', 'call_count': 9}})
    persistence.init_colors()
    assert persistence.yellow == 3
    assert persistence.red == 6


def test_init_colors_rounding():
    persistence = Persistence()
    persistence.load_nodes({'dummy_hash1': {'name': 'dummy_name1', 'source': 'dummy_source', 'call_count': 7}})
    persistence.init_colors()
    assert persistence.yellow == 2
    assert persistence.red == 5


def test_update_color_range():
    persistence = Persistence()
    persistence.update_color_range(yellow=2, red=3)
    assert persistence.yellow == 2
    assert persistence.red == 3


def test_get_range_with_empty_persistence():
    persistence = Persistence()
    result = persistence.get_range()
    assert result.yellow == 0
    assert result.red == 0
    assert result.top == 0


def test_get_range_with_nodes_but_not_set_colors():
    persistence = Persistence()
    persistence.load_nodes({'dummy_hash1': {'name': 'dummy_name1', 'source': 'dummy_source', 'call_count': 7}})
    result = persistence.get_range()
    assert result.yellow == 0
    assert result.red == 0
    assert result.top == 7


def test_get_range_with_no_nodes_but_set_colors():
    persistence = Persistence()
    persistence.yellow = 3
    persistence.red = 8
    result = persistence.get_range()
    assert result.yellow == 3
    assert result.red == 8
    assert result.top == 0


def test_get_range_with_nodes_and_set_colors():
    persistence = Persistence()
    persistence.load_nodes({'dummy_hash1': {'name': 'dummy_name1', 'source': 'dummy_source', 'call_count': 7}})
    persistence.yellow = 3
    persistence.red = 8
    result = persistence.get_range()
    assert result.yellow == 3
    assert result.red == 8
    assert result.top == 7
