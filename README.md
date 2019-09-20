# call-graph-visualisation

An interactive web-app tool for call-graph visualisation

# Usage:
Binary: ./main.py --binary <path to binary> 
Binary should be compiled like: gcc -ggdb3 -O0  -fno-omit-frame-pointer

Output: ./main.py --output <path to output-file>
Output should be created with:
    - valgrind --tool=callgrind --dump-instr=yes --dump-line=yes --callgrind-out-file=<callgrind-output-file> ./<binary>
    - callgrind_annotate --threshold=100 --inclusive=yes --tree=caller <callgrind-output-file> > <output-file>