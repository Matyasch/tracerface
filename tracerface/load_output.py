#!/usr/bin/env python3

from pathlib import Path

from tracerface.parse_stack import parse_stack


def load_trace_output_from_file_to_call_graph(file_path, call_graph):
    text = Path(file_path).read_text()
    call_graph.clear()
    stacks = [stack.split('\n') for stack in text.split('\n\n')]
    for stack in stacks:
        graph = parse_stack(stack)
        call_graph.load_edges(graph.edges)
        call_graph.load_nodes(graph.nodes)
    call_graph.init_colors()
