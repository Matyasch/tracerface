from pathlib import Path
import re
import subprocess

class Parser():
    def caller_pattern(self, fn_name):
        return '^\s*([0-9]|,)+\s\s\<\s.*\:{}\s\(([0-9]+)x\)'.format(fn_name)


    def called_pattern(self):
        return '^\s*[0-9]+\,?[0-9]+\s\s\*\s\s.*\:(.*)\s\['


# Get function name from last line of calls stack
    def get_called(self, functions):
        return re.search(self.called_pattern(), functions[-1]).group(1)


    def get_edges_from_caller(self, caller_function, stacks):
        edges = []
        for stack in stacks:
            functions = stack.split('\n')
            for function in functions:
                if re.compile(self.caller_pattern(caller_function)).match(function):
                    number_of_calls = re.search(self.caller_pattern(caller_function), function).group(2)
                    edges.append([self.get_called(functions), caller_function, number_of_calls])
        return edges


    def parse(self, text, from_fn):
        call_stack = [[from_fn, 'None', 0]]
        nodes = [from_fn]
        search_ind = 0
        stacks = text.split('\n\n')

        while search_ind < len(nodes):
            caller_function = nodes[search_ind]
            search_ind += 1
            edges = self.get_edges_from_caller(caller_function, stacks)
            call_stack += edges
            nodes += [edge[0] for edge in edges if edge[0] not in nodes]
        return call_stack


class Model():
    def __init__(self, persistence):
        self.persistence = persistence
        self.callgrind_output = Path('assets/callgrind_out')
        self.parser = Parser()


    def get_nodes(self):
        return self.persistence.nodes


    def get_edges(self):
        return self.persistence.edges


    def run_valgrind(self, binary):
        subprocess.run([
            'valgrind',
            '--tool=callgrind',
            '--dump-instr=yes',
            '--dump-line=yes',
            '--callgrind-out-file={}'.format(str(self.callgrind_output)),
            './{}'.format(str(binary))
        ])


    def run_annotate(self):
        return subprocess.Popen([
            'callgrind_annotate',
            '--threshold=100',
            '--inclusive=yes',
            '--tree=caller',
            str(self.callgrind_output)
        ], stdout=subprocess.PIPE)


    def initialize_from_binary(self, binary, from_fn):
        run_valgrind(binary)
        pipe = run_annotate()
        text = pipe.communicate()[0].decode("utf-8")
        parsed_output = self.parser.parse(text, from_fn)
        self.persistence.load(parsed_output)


    def initialize_from_output(self, annotated_file, from_fn):
        text = annotated_file.read_text()
        parsed_output = self.parser.parse(text, from_fn)
        for edge in parsed_output:
            if edge[0] in self.persistence.nodes:
                self.persistence.nodes[edge[0]] += int(edge[2])
            else:
                self.persistence.nodes[edge[0]] = int(edge[2])
        self.persistence.load(parsed_output)