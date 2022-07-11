import argparse
import sys
import time
from plan_graphs.relaxed_plan_graph import RelaxedPlanGraph
from pddl.parse_visitor import Parser

if __name__ == "__main__":
    """
    This script uses the RelaxedPlanGraph class.
    First it parses the PDDL domain and problem files.
    Then it builds the relaxed plan graph.
    """

    # ground command line arguments
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("pddl_file", help="PDDL domain file, problem file (2 files)", nargs=2)
    args = arg_parser.parse_args()

    if len(args.pddl_file) != 2: 
        arg_parser.print_help()
        sys.exit(0)
    
    # parse PDDL domain and problem files
    pddl_parser = Parser()
    print("Parsing PDDL domain file...")
    start_time = time.time()
    for file in args.pddl_file:
        pddl_parser.parse_file(file)
    print("Parsing PDDL files took %.2f seconds." % (time.time() - start_time))

    # after parsing, prepare the grounded representation
    print("Preparing grounded representation...")
    start_time = time.time()
    pddl_parser.grounding.ground_problem(pddl_parser.domain, pddl_parser.problem)
    print("Preparing grounded representation took %.2f seconds." % (time.time() - start_time))
        
    # build a relaxed plan graph
    print("Building relaxed plan graph...")
    start_time = time.time()
    rpg = RelaxedPlanGraph(pddl_parser.domain, pddl_parser.problem, pddl_parser.grounding)
    rpg.build_graph(stop_at_goal=True)
    print("Building relaxed plan graph took %.2f seconds." % (time.time() - start_time))