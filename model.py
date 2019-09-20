from pathlib import Path
import re
import subprocess

class Parser():
    def caller_pattern(self, fn_name):
        return re.compile('\s+([0-9]|,)+\s\s\<\s.*\:{}\s\('.format(fn_name))


    def get_called(self, functions):
        for function in functions:
            fn_name = re.search('^^\s+([0-9]|,)+\s\s\*\s\s.*\:(.*)\s\[', function)
            if fn_name:
                return fn_name.group(2)


    def get_calls(self, function_name, stacks):
        called_functions = []
        for stack in stacks:
            functions = stack.split('\n')
            for function in functions:
                if self.caller_pattern(function_name).match(function):
                    called_functions.append(self.get_called(functions))
        return called_functions


    def parse(self, text, from_fn):
        call_stack = [[from_fn, 'None']]
        searching = [from_fn]
        stacks = text.split('\n\n')

        while searching:
            caller_function = searching.pop(0)
            called_functions = self.get_calls(caller_function, stacks)
            for called_function in called_functions:
                call_stack.append([called_function, caller_function])
                searching.append(called_function)
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
        self.persistence.load(parsed_output)