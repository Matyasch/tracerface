EXPECTED_NODES = [
    {'name': '__libc_start_main', 'count': 0, 'source': 'libc-2.27.so'},
    {'name': 'func1', 'count': 2, 'source': 'test_application'},
    {'name': 'func2', 'count': 1, 'source': 'test_application'},
    {'name': 'func3', 'count': 5, 'source': 'test_application'},
    {'name': 'func6', 'count': 0, 'source': 'test_application'},
    {'name': 'main', 'count': 0, 'source': 'test_application'}
]

EXPECTED_EDGES = [
    {'call_count': 2, 'called_name': 'func1', 'caller_name': 'func6', 'params': '...'},
    {'call_count': 1, 'called_name': 'func2', 'caller_name': 'func6', 'params': '3'},
    {'call_count': 5, 'called_name': 'func3', 'caller_name': 'func6', 'params': ''},
    {'call_count': 0, 'called_name': 'func6', 'caller_name': 'main', 'params': ''},
    {'call_count': 0, 'called_name': 'main', 'caller_name': '__libc_start_main', 'params': ''}
]

def assert_results(result_nodes, result_edges):
    assert len(result_nodes) == len(EXPECTED_NODES)
    assert len(result_edges) == len(EXPECTED_EDGES)

    sorted_nodes = sorted(result_nodes, key = lambda i: i['data']['name'])
    # we can sort like this because no node is called from two different nodes
    sorted_edges = sorted(result_edges, key = lambda i: i['data']['called_name'])

    for result, expected in zip(sorted_nodes, EXPECTED_NODES):
        assert result['data']['name'] == expected['name']
        assert result['data']['count'] == expected['count']
        assert result['data']['source'] == expected['source']
    for result, expected in zip(sorted_edges, EXPECTED_EDGES):
        assert result['data']['call_count'] == expected['call_count']
        assert result['data']['called_name'] == expected['called_name']
        assert result['data']['caller_name'] == expected['caller_name']
        assert result['data']['params'] == expected['params']
