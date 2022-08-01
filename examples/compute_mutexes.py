import numpy as np
from pddl.parser import Parser
from time import time
from plan_graphs.relaxed_plan_graph import RelaxedPlanGraph

"""
This file is testing computing mutex relations.
The implementation for this is currently work in progress, and
not very fast. It computes only mutex relations between actions.
"""

# parse files
domain_file = "./pddl/test_domains/logistics_domain.pddl"
problem_file = "./pddl/test_domains/logistics_problem.pddl"
pddl_parser = Parser()
pddl_parser.parse_file(domain_file)
pddl_parser.parse_file(problem_file)
problem = pddl_parser.problem

print("Grounding the problem...")
start_time = time()
problem.ground()
print("Grounding took {:0.2f} seconds.".format(time() - start_time))

# Generating relaxed plan graph
print("Generating relaxed plan graph...")
start_time = time()
relaxed_plan_graph = RelaxedPlanGraph(pddl_parser.domain, problem)
relaxed_plan_graph.build_graph(stop_at_goal=False)
print("Generating took {:0.2f} seconds.".format(time() - start_time))

# time checking action mutexes in problem
print("Checking action mutexes for {:0.0f} actions...".format(problem.grounding.action_count))
start_time = time()
problem.grounding.compute_action_mutexes(relaxed_plan_graph.all_actions)
print("Checking action mutexes took {:0.2f} seconds.".format(time() - start_time))

# print an example mutex relation
print("Mutex relation:")
nonzero = np.nonzero(problem.grounding.action_mutexes)
action_a = nonzero[0][0] # A action first pair
action_b = nonzero[1][0] # B action first pair
print("Action A")
print(problem.grounding.get_action_from_id(action_a))
print("Action B")
print(problem.grounding.get_action_from_id(action_b))
