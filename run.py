import argparse
from lexer import CompilerLexer
from parser import CompilerParser


def parse_arguments():
    parser = argparse.ArgumentParser(description='Compiler')
    parser.add_argument(
        '--infile',
        type=argparse.FileType('r'),
        help='.imp file containing code'
    )
    parser.add_argument(
        '--outfile',
        type=argparse.FileType('w'),
        help='output file for compilation results',
        default='a.out'
    )
    return parser.parse_args()


def start_compiler(input_file, output_file):
    print(input_file, output_file)
    lexer = CompilerLexer()


    with open(input_file, 'r') as file:
        code = file.read()
        tokens = lexer.tokenize(code)
        parser = CompilerParser()
        parsed_code = parser.parse(tokens)

        print(parsed_code)

        '''      for t in tokens:
            print(t)'''


        '''with open(output_file, 'w') as file:
            tokens = lexer.tokenize(code)
            for t in tokens:
                #file.write(str(t)+"\n")
                print(t)'''


def main():
    arguments = parse_arguments()
    start_compiler(arguments.infile.name, arguments.outfile.name)


if __name__ == "__main__":
    main()
