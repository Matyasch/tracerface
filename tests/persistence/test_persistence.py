from persistence.persistence import Persistence


def test_initial_persistence():
    persistence = Persistence()
    assert persistence._nodes == {}
    assert persistence._edges == {}
    assert persistence._yellow == 0
    assert persistence._red == 0


def test_load_node_single_to_empty_nodes():
    persistence = Persistence()

    persistence.load_nodes({'dummy_hash': {'name': 'dummy_name', 'source': 'dummy_source', 'call_count': 1}})

    assert persistence._nodes == {'dummy_hash': {'name': 'dummy_name', 'source': 'dummy_source', 'call_count': 1}}


def test_load_node_multiple_to_empty_nodes():
    persistence = Persistence()

    persistence.load_nodes({
        'dummy_hash1': {'name': 'dummy_name1', 'source': 'dummy_source1', 'call_count': 0},
        'dummy_hash2': {'name': 'dummy_name2', 'source': 'dummy_source2', 'call_count': 1}
    })

    assert persistence._nodes == {
        'dummy_hash1': {'name': 'dummy_name1', 'source': 'dummy_source1', 'call_count': 0},
        'dummy_hash2': {'name': 'dummy_name2', 'source': 'dummy_source2', 'call_count': 1}
    }


def test_load_node_to_different_nodes():
    persistence = Persistence()
    persistence._nodes = {'dummy_hash1': {'name': 'dummy_name1', 'source': 'dummy_source1', 'call_count': 3}}

    persistence.load_nodes({'dummy_hash2': {'name': 'dummy_name2', 'source': 'dummy_source2', 'call_count': 1}})

    assert persistence._nodes == {
        'dummy_hash1': {'name': 'dummy_name1', 'source': 'dummy_source1', 'call_count': 3},
        'dummy_hash2': {'name': 'dummy_name2', 'source': 'dummy_source2', 'call_count': 1}
    }


def test_load_node_to_same_nodes():
    persistence = Persistence()
    persistence._nodes = {'dummy_hash': {'name': 'dummy_name', 'source': 'dummy_source', 'call_count': 1}}

    persistence.load_nodes({'dummy_hash': {'name': 'dummy_name', 'source': 'dummy_source', 'call_count': 1}})

    assert persistence._nodes == {'dummy_hash': {'name': 'dummy_name', 'source': 'dummy_source', 'call_count': 2}}


def test_load_edge_with_no_params():
    persistence = Persistence()

    persistence.load_edges({('node_hash1', 'node_hash2'): {'param': [], 'call_count': 8}})

    assert persistence._edges == {('node_hash1', 'node_hash2'): {'params': [], 'call_count': 8}}


def test_load_edge_with_params():
    persistence = Persistence()

    persistence.load_edges({('node_hash1', 'node_hash2'): {'param': ['dummy_param1', 'dummy_param2'], 'call_count': 8}})

    assert persistence._edges == {('node_hash1', 'node_hash2'): {'params': [['dummy_param1', 'dummy_param2']], 'call_count': 8}}


def test_single_load_different_edges():
    persistence = Persistence()

    persistence.load_edges({
        ('node_hash1', 'node_hash2'): {'param': [], 'call_count': 0},
        ('node_hash3', 'node_hash4'): {'param': ['dummy_param'], 'call_count': 3}
    })

    assert persistence._edges == {
        ('node_hash1', 'node_hash2'): {'params': [], 'call_count': 0},
        ('node_hash3', 'node_hash4'): {'params': [['dummy_param']], 'call_count': 3}
    }


def test_load_edge_to_different_edges():
    persistence = Persistence()
    persistence._edges = {('node_hash1', 'node_hash2'): {'params': [], 'call_count': 0}}

    persistence.load_edges({('node_hash3', 'node_hash4'): {'param': ['dummy_param'], 'call_count': 3}})

    assert persistence._edges == {
        ('node_hash1', 'node_hash2'): {'params': [], 'call_count': 0},
        ('node_hash3', 'node_hash4'): {'params': [['dummy_param']], 'call_count': 3}
    }


def test_load_edge_to_same_edges():
    persistence = Persistence()
    persistence._edges = {('node_hash1', 'node_hash2'): {'params': [], 'call_count': 1}}

    persistence.load_edges({('node_hash1', 'node_hash2'): {'param': [], 'call_count': 3}})

    assert persistence._edges == {('node_hash1', 'node_hash2'): {'params': [], 'call_count': 4}}


def test_load_edge_to_same_edges_with_params():
    persistence = Persistence()
    persistence._edges = {('node_hash1', 'node_hash2'): {
        'params': [['dummy_param1', 'dummy_param2']],
        'call_count': 1}
    }

    persistence.load_edges({('node_hash1', 'node_hash2'): {'param': ['dummy_param3', 'dummy_param4'], 'call_count': 3}})

    assert persistence._edges == {('node_hash1', 'node_hash2'): {
            'params': [['dummy_param1', 'dummy_param2'], ['dummy_param3', 'dummy_param4']],
            'call_count': 4}
        }


def test_get_nodes_returns_empty_dict_for_empty_persistence():
    persistence = Persistence()

    assert persistence.get_nodes() == {}


def test_get_edges_returns_empty_dict_for_empty_persistence():
    persistence = Persistence()

    assert persistence.get_edges() == {}


def test_get_nodes_return_nodes_for_filled_persistence():
    persistence = Persistence()
    persistence._nodes = {
        'dummy_hash1': {'name': 'dummy_name1', 'source': 'dummy_source1', 'call_count': 3},
        'dummy_hash2': {'name': 'dummy_name2', 'source': 'dummy_source2', 'call_count': 1}
    }

    assert persistence.get_nodes() == {
        'dummy_hash1': {'name': 'dummy_name1', 'source': 'dummy_source1', 'call_count': 3},
        'dummy_hash2': {'name': 'dummy_name2', 'source': 'dummy_source2', 'call_count': 1}
    }


def test_get_edges_return_edges_for_filled_persistence():
    persistence = Persistence()
    persistence._edges = {
        ('node_hash1', 'node_hash2'): {'params': [], 'call_count': 0},
        ('node_hash3', 'node_hash4'): {'params': [['dummy_param']], 'call_count': 3}
    }

    assert persistence.get_edges() == {
        ('node_hash1', 'node_hash2'): {'params': [], 'call_count': 0},
        ('node_hash3', 'node_hash4'): {'params': [['dummy_param']], 'call_count': 3}
    }


def test_clear_empty_persistence():
    persistence = Persistence()

    persistence.clear()

    assert persistence._nodes == {}


def test_clear_for_only_nodes():
    persistence = Persistence()
    persistence._nodes = {
        'dummy_hash1': {'name': 'dummy_name1', 'source': 'dummy_source1', 'call_count': 3},
        'dummy_hash2': {'name': 'dummy_name2', 'source': 'dummy_source2', 'call_count': 1}
    }

    persistence.clear()

    assert persistence._nodes == {}


def test_clear_for_only_edges():
    persistence = Persistence()
    persistence._edges = {
        ('node_hash1', 'node_hash2'): {'params': [], 'call_count': 0},
        ('node_hash3', 'node_hash4'): {'params': [['dummy_param']], 'call_count': 3}
    }

    persistence.clear()

    assert persistence._edges == {}


def test_clear_for_nodes_and_edges():
    persistence = Persistence()
    persistence._nodes = {
        'dummy_hash1': {'name': 'dummy_name1', 'source': 'dummy_source1', 'call_count': 3},
        'dummy_hash2': {'name': 'dummy_name2', 'source': 'dummy_source2', 'call_count': 1}
    }
    persistence._edges = {
        ('node_hash1', 'node_hash2'): {'params': [], 'call_count': 0},
        ('node_hash3', 'node_hash4'): {'params': [['dummy_param']], 'call_count': 3}
    }

    persistence.clear()

    assert persistence._nodes == {}
    assert persistence._edges == {}


def test_update_colors():
    persistence = Persistence()
    persistence._yellow = 0
    persistence._red = 0

    persistence.update_colors(yellow=2, red=3)

    assert persistence._yellow == 2
    assert persistence._red == 3


def test_get_yellow_with_empty_persistence():
    persistence = Persistence()

    assert persistence.get_yellow() == 0


def test_get_red_with_empty_persistence():
    persistence = Persistence()

    assert persistence.get_red() == 0


def test_get_yellow_with_nodes_but_not_set_colors():
    persistence = Persistence()
    persistence._nodes = {'dummy_hash': {'name': 'dummy_name', 'source': 'dummy_source', 'call_count': 7}}

    assert persistence.get_yellow() == 0


def test_get_red_with_nodes_but_not_set_colors():
    persistence = Persistence()
    persistence._nodes = {'dummy_hash': {'name': 'dummy_name', 'source': 'dummy_source', 'call_count': 7}}

    assert persistence.get_red() == 0


def test_get_yellow_with_no_nodes_but_set_color():
    persistence = Persistence()
    persistence._yellow = 3

    assert persistence.get_yellow() == 3
