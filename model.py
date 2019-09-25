import itertools
from pathlib import Path
import subprocess

from parser import Parser

# Manages logic and persistence
class Model():
    def __init__(self, persistence):
        self.persistence = persistence
        self.parser = Parser()

    # Returns a list of nodes and their call count
    def get_nodes(self):
        return self.persistence.nodes

    # Returns a list of edges and their frequency
    def get_edges(self):
        return self.persistence.edges

    def green_count(self):
        return 0

    def yellow_count(self):
        return int(self.persistence.max_count/3)

    def red_count(self):
        return int(self.persistence.max_count*2/3)

    def initialize_from_output(self, output_file):
        self.parser.parse(output_file.read_text())
        self.persistence.load_edges(self.parser.edges)
        self.persistence.load_nodes(self.parser.nodes)