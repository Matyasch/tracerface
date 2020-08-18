#!/usr/bin/env python3
from unittest import main, TestCase

from tracerface.parse_stack import parse_stack


class TestParseStack(TestCase):
    def test_parse_stack_returns_empty_graph_for_empty_stack(self):
        result = parse_stack([])

        self.assertDictEqual(result.nodes, {})
        self.assertDictEqual(result.edges, {})

    def test_parse_stack_returns_empty_graph_for_stack_with_no_calls_in_right_format(self):
        result = parse_stack(['no calls'])

        self.assertDictEqual(result.nodes, {})
        self.assertDictEqual(result.edges, {})

    def test_parse_stack_returns_nodes_for_stack_with_one_call(self):
        stack = [
            "19059  19059  dummy_source1 func1",
            "-14",
            "b'func1+0x0 [dummy_source1]'"
        ]

        expected_nodes = [{'call_count': 1, 'name': 'func1', 'source': 'dummy_source1'}]
        result = parse_stack(stack)
        self.assertListEqual(list(result.nodes.values()), expected_nodes)
        self.assertListEqual(list(result.edges.values()), [])

    def test_parse_stack_returns_nodes_for_stack_with_no_params(self):
        stack = [
            "19059  19059  dummy_source1 func1",
            "-14",
            "b'func1+0x0 [dummy_source1]'",
            "b'func2+0x26 [dummy_source1]'",
            "b'func3+0x17 [dummy_source2]'",
            "b'[unknown]'"
        ]

        result = parse_stack(stack)
        self.assertListEqual(
            sorted(list(result.nodes.values()), key = lambda i: i['name']),
            [
                {'call_count': 1, 'name': 'func1', 'source': 'dummy_source1'},
                {'call_count': 0, 'name': 'func2', 'source': 'dummy_source1'},
                {'call_count': 0, 'name': 'func3', 'source': 'dummy_source2'},
            ]
        )
        self.assertListEqual(
            sorted(list(result.edges.values()), key = lambda i: i['call_count']),
            [{'call_count': 0, 'param': []}, {'call_count': 1, 'param': []}]
        )

    def test_parse_stack_returns_nodes_for_stack_with_params(self):
        stack = [
            "19059  19059  dummy_source1 func1        b'param1' b'param2'",
            "-14",
            "b'func1+0x0 [dummy_source1]'",
            "b'func2+0x26 [dummy_source1]'",
            "b'func3+0x17 [dummy_source2]'",
        ]

        result = parse_stack(stack)

        self.assertListEqual(
            sorted(list(result.nodes.values()), key = lambda i: i['name']),
            [
                {'call_count': 1, 'name': 'func1', 'source': 'dummy_source1'},
                {'call_count': 0, 'name': 'func2', 'source': 'dummy_source1'},
                {'call_count': 0, 'name': 'func3', 'source': 'dummy_source2'},
            ]
        )
        self.assertListEqual(
            sorted(list(result.edges.values()), key = lambda i: i['call_count']),
            [{'call_count': 0, 'param': []}, {'call_count': 1, 'param': ['param1', 'param2']}]
        )

    def test_parse_stack_returns_nodes_for_stack_with_header(self):
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
        self.assertListEqual(
            sorted(list(result.nodes.values()), key = lambda i: i['name']),
            [
                {'call_count': 1, 'name': 'func1', 'source': 'dummy_source1'},
                {'call_count': 0, 'name': 'func2', 'source': 'dummy_source1'},
                {'call_count': 0, 'name': 'func3', 'source': 'dummy_source2'},
            ]
        )
        self.assertListEqual(
            sorted(list(result.edges.values()), key = lambda i: i['call_count']),
            [{'call_count': 0, 'param': []}, {'call_count': 1, 'param': []}]
        )

    def test_parse_stack_returns_empty_stack_for_header_only(self):
        stack = [
            "PID    TID    COMM         FUNC             ",
        ]

        result = parse_stack(stack)

        self.assertDictEqual(result.nodes, {})
        self.assertDictEqual(result.edges, {})


if __name__ == '__main__':
    main()
