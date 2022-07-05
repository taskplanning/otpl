import sys
import argparse
from typing import Tuple
from antlr4 import CommonTokenStream, FileStream
from pddl.domain import Domain
from pddl.grammar.pddl22Lexer import pddl22Lexer
from pddl.grammar.pddl22Parser import pddl22Parser
from pddl.parse_visitor import Parser
from pddl.problem import Problem

if __name__ == "__main__":  
    
    # parse command line arguments
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("pddl_file", help="PDDL domain file, problem file, or both (max 2 files)", nargs='+')
    arg_parser.add_argument("-p","--print", action="store_true", help="Immediately print parsed PDDL.")
    arg_parser.add_argument("-v","--verbose", action="store_true", help="Verbose parsing (not yet implemented).")
    args = arg_parser.parse_args()

    if len(args.pddl_file) > 2 or len(args.pddl_file) == 0:: 
        arg_parser.print_help()
        sys.exit(0)
    
    for file in args.pddl_file:
        
        pddl_parser = Parser()
        pddl_parser.parse_file(file)
        
        if pddl_parser.domain and args.print: print(pddl_parser.domain)
        if pddl_parser.problem and args.print: print(pddl_parser.problem)