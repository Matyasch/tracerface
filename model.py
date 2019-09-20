from pathlib import Path
import re
import subprocess

# Parses output provided by callgrind_annotate
class Parser():
    # Pattern of caller functions
    def caller_pattern(self, fn_name):
        return '^\s*([0-9]|,)+\s\s\<\s.*\:{}\s\(([0-9]+)x\)'.format(fn_name)


    # Pattern of called functions, at the bottom of the stack
    def called_pattern(self):
        return '^\s*[0-9]+\,?[0-9]+\s\s\*\s\s.*\:(.*)\s\['


    # Get function name from last line of calls stack
    def get_called(self, functions):
        return re.search(self.called_pattern(), functions[-1]).group(1)


    # Collect all calls from given function
    def calls(self, caller_function, stacks):
        edges = []
        for stack in stacks:
            functions = stack.split('\n')
            for function in functions:
                if re.compile(self.caller_pattern(caller_function)).match(function):
                    number_of_calls = re.search(self.caller_pattern(caller_function), function).group(2)
                    edges.append([self.get_called(functions), caller_function, number_of_calls])
        return edges


    # Parse output from given function
    def parse(self, text, from_fn):
        call_stack = [[from_fn, 'None', 0]]
        nodes = [from_fn]
        search_ind = 0
        stacks = text.split('\n\n')

        while search_ind < len(nodes):
            caller_function = nodes[search_ind]
            search_ind += 1
            edges = self.calls(caller_function, stacks)
            call_stack += edges
            nodes += [edge[0] for edge in edges if edge[0] not in nodes]
        return call_stack


# Manages logic and persistence
class Model():
    def __init__(self, persistence):
        self.persistence = persistence
        self.callgrind_output = Path('assets/callgrind_out')
        self.parser = Parser()


    # Returns a list of nodes and their call count
    def get_nodes(self):
        return self.persistence.nodes


    # Returns a list of edges and their frequency
    def get_edges(self):
        return self.persistence.edges


    # Runs valgrind process of given binary
    def run_valgrind(self, binary):
        subprocess.run([
            'valgrind',
            '--tool=callgrind',
            '--dump-instr=yes',
            '--dump-line=yes',
            '--callgrind-out-file={}'.format(str(self.callgrind_output)),
            './{}'.format(str(binary))
        ])


    # Runs callgrind_annotate on output
    def run_annotate(self):
        return subprocess.Popen([
            'callgrind_annotate',
            '--threshold=100',
            '--inclusive=yes',
            '--tree=caller',
            str(self.callgrind_output)
        ], stdout=subprocess.PIPE)


    def load_persistence(self, annotated_text, from_fn):
        parsed_output = self.parser.parse(annotated_text, from_fn)
        for edge in parsed_output:
            if edge[0] in self.persistence.nodes:
                self.persistence.nodes[edge[0]] += int(edge[2])
            else:
                self.persistence.nodes[edge[0]] = int(edge[2])
        self.persistence.edges = set(tuple(edge) for edge in parsed_output)


    # Initializes persistence with by profiling given binary
    def initialize_from_binary(self, binary, from_fn):
        run_valgrind(binary)
        pipe = run_annotate()
        annotated_text = pipe.communicate()[0].decode("utf-8")
        self.load_persistence(annotated_text, from_fn)


    # Initializes persistence by parsing annotated output
    def initialize_from_output(self, annotated_file, from_fn):
        annotated_text = annotated_file.read_text()
        self.load_persistence(annotated_text, from_fn)