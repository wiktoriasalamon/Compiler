import argparse
from lexer import CompilerLexer
from parser import CompilerParser
from compiler import Compiler


def parse_arguments():
    parser = argparse.ArgumentParser(description='Compiler')
    parser.add_argument(
        'infile',
        type=argparse.FileType('r'),
        help='.imp file containing code'
    )
    parser.add_argument(
        'outfile',
        type=argparse.FileType('w'),
        help='output file for compilation results',
    )
    return parser.parse_args()


def start_compiler(input_file, output_file):
    lexer = CompilerLexer()

    with open(input_file, 'r') as file:
        code = file.read()

    tokens = lexer.tokenize(code)
    parser = CompilerParser()
    tree = parser.parse(tokens)
    compiler = Compiler(tree)
    code = compiler.compile()

    with open(output_file, 'w') as file:
        file.write(code)


def main():
    arguments = parse_arguments()
    start_compiler(arguments.infile.name, arguments.outfile.name)


if __name__ == "__main__":
    main()
