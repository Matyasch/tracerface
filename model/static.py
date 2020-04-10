from pathlib import Path

from model.base import BaseModel
from model.parse_stack import parse_stack


# Model for graph creation with static text
class StaticModel(BaseModel):
    def __init__(self, persistence):
         super().__init__(persistence)

    def load_output(self, path):
        try:
            text = Path(path).read_text()
        except FileNotFoundError:
            raise ValueError('Could not find output file at {}'.format(path))
        except IsADirectoryError:
            raise ValueError('{} is a directory, not a file'.format(path))

        stacks = [stack.split('\n') for stack in text.split('\n\n')]
        for stack in stacks:
            graph = parse_stack(stack)
            self._persistence.load_edges(graph.edges)
            self._persistence.load_nodes(graph.nodes)
        self.init_colors()
