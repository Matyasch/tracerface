from model.base import BaseModel
from model.utils import parse_stack, text_to_stacks


# Model for graph creation with static text
class StaticModel(BaseModel):
    def __init__(self, configuration):
         super().__init__(configuration)

    # Load raw bcc trace input
    def load_text(self, raw_text):
        self._persistence.clear()
        stacks = text_to_stacks(raw_text)
        for stack in stacks:
            graph = parse_stack(stack)
            self._persistence.load_edges(graph.edges)
            self._persistence.load_nodes(graph.nodes)
        self.init_colors()
