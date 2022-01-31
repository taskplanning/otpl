import sys
import argparse
from antlr4 import CommonTokenStream, FileStream
from pddl.grammar.pddl22Lexer import pddl22Lexer
from pddl.grammar.pddl22Parser import pddl22Parser
from pddl.parse_visitor import Parser

if __name__ == "__main__":  
    
    # parse command line arguments
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("pddl_file", help="PDDL domain file, problem file, or both (max 2 files)", nargs='+')
    arg_parser.add_argument("-p","--print", action="store_true", help="Immediately print parsed PDDL.")
    args = arg_parser.parse_args()

    if len(args.pddl_file) > 2: 
        arg_parser.print_help()
        sys.exit(0)

    for file in args.pddl_file:

        # lexer
        data = FileStream(file)
        lexer = pddl22Lexer(data)
        stream = CommonTokenStream(lexer)
        
        # parser
        arg_parser = pddl22Parser(stream)
        tree = arg_parser.pddl_file()
        if arg_parser.getNumberOfSyntaxErrors() > 0:
            print("PDDL Parser encountered syntax errors.")
            sys.exit(-1)

        # visitor
        visitor = Parser()
        visitor.visit(tree)
        if tree.domain() and args.print: print(visitor.domain)
        if tree.problem() and args.print: print(visitor.problem)