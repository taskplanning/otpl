import argparse
import sys
import time
from pddl.grounding import Grounding
from plan_graphs.relaxed_plan_graph import RelaxedPlanGraph
from pddl.parser import Parser

if __name__ == "__main__":
    """
    This script uses the RelaxedPlanGraph class.
    First it parses the PDDL domain and problem files.
    Then it builds the relaxed plan graph.
    """

    # ground command line arguments
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("domain", help="path to PDDL domain file")
    arg_parser.add_argument("problem", help="path to PDDL problem file")
    args = arg_parser.parse_args()

    # parse PDDL domain and problem files
    print("Parsing PDDL domain file...")
    pddl_parser = Parser()
    pddl_parser.parse_file(args.domain)
    pddl_parser.parse_file(args.problem)

    # build a relaxed plan graph
    print("Building relaxed plan graph...")
    start_time = time.time()
    rpg = RelaxedPlanGraph(pddl_parser.domain, pddl_parser.problem)
    layer_count = rpg.build_graph(stop_at_goal=True)
    relaxed_plan, action_count = rpg.get_relaxed_plan()
    print("Building relaxed plan graph took %.2f seconds." % (time.time() - start_time))

    # print the relaxed plan
    print("Relaxed plan graph has %d layers." % layer_count)
    print("Relaxed plan has %d actions." % action_count)
    rpg.print_relaxed_plan()
