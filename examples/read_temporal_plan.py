import argparse
from pddl.parser import Parser
from pddl.grounding import Grounding
from plans.temporal_plan import PlanTemporalNetwork

if __name__ == "__main__":
    """
    This script uses the PlanTemporalNetwork class.
    First it parses the PDDL domain and problem files.
    Then it loads a temporal plan from file and generates a temporal network.
    It checks thge consistency of the network and makes the network minimal for execution.
    Finally it prints the network as a DOT graph.
    """

    # command line arguments
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("domain", help="path to PDDL domain file")
    arg_parser.add_argument("problem", help="path to PDDL problem file")
    arg_parser.add_argument("plan", help="path to plan file")
    args = arg_parser.parse_args()
    
    # parse PDDL domain and problem files
    print("Parsing PDDL domain and problem file...")
    pddl_parser = Parser()
    pddl_parser.parse_file(args.domain)
    pddl_parser.parse_file(args.problem)
    
    print("Parsing PDDL plan file...")
    plan = PlanTemporalNetwork(pddl_parser.domain, pddl_parser.problem)
    plan.read_from_file(args.plan)

    print("Plan is temporally consistent:", plan.temporal_network.floyd_warshall())
    plan.temporal_network.make_minimal()
    plan.temporal_network.print_dot_graph()