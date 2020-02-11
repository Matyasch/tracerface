from model.base import BaseModel


# Model for graph creation with static text
class StaticModel(BaseModel):
    def __init__(self):
         super().__init__()

    # Load raw bcc trace input
    def load_text(self, raw_text):
        self._persistence.clear()
        stacks = [stack.split('\n') for stack in raw_text.split('\n\n')]
        for stack in stacks:
            graph = self.parse_stack(stack)
            self._persistence.load_edges(graph.edges)
            self._persistence.load_nodes(graph.nodes)
        self.init_colors()
