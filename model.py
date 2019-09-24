from pathlib import Path
import subprocess

from parsers.bcc_parser import BccParser

# Manages logic and persistence
class Model():
    def __init__(self, persistence):
        self.persistence = persistence
        self.parser = BccParser()


    # Returns a list of nodes and their call count
    def get_nodes(self):
        return self.persistence.nodes


    # Returns a list of edges and their frequency
    def get_edges(self):
        return self.persistence.edges


    def initialize_from_output(self, output_file):
        self.parser.parse(output_file.read_text())
        self.persistence.edges = self.parser.edges
        self.persistence.nodes = [edge[0] for edge in self.parser.edges]