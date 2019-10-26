from model.base import BaseModel
from model.parser import text_to_stacks, process_stack

# Manages logic and persistence
class StaticModel(BaseModel):
    def __init__(self):
         super().__init__()

    def load_text(self, raw_text):
        self._persistence.clear()
        stacks = text_to_stacks(raw_text)
        for stack in stacks:
            graph = process_stack(stack)
            self._persistence.load_edges(graph.edges)
            self._persistence.load_nodes(graph.nodes)
        self._persistence.init_colors()