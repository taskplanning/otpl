import argparse
from queue import PriorityQueue
import sys
import time

from pddl.parser import Parser
from pddl.domain import Domain
from pddl.problem import Problem
from pddl.grounding import Grounding
from plan_graphs.relaxed_plan_graph import RelaxedPlanGraph
from plans.sequential_plan import PlanSequential

class PriorityState:

    def __init__(self, hval, gval, action_id, state, applicable_actions, parent):
        """
        :param hval: heuristic value of parent node
        :param gval: cummulative cost
        :param action_id: action id that achieved this node
        :param state: propositional state
        :param applicable_actions: list of applicable action_ids
        :param parent: parent node
        """
        self.hval : int = hval
        self.gval : int  = gval
        self.action_id : int = action_id
        self.state = state
        self.parent = parent
        self.applicable_actions = applicable_actions

    def __lt__(self, other):
        return self.hval + self.gval < other.hval + other.gval

    def __eq__(self, other):
        return self.hval == other.hval

class Planner(): 
        
    def __init__(self):
        self.domain = None
        self.problem = None

    def find_sequential_plan(self, domain : Domain, problem : Problem, optimal : bool = False, verbosity : int = 1) -> PlanSequential:

        self.domain = domain
        self.problem = problem

        self.grounding = Grounding()
        self.grounding.ground_problem(domain, problem)
        initial_state = self.grounding.get_initial_state_spike()

        # check if the goal is achieved in the initial state
        if self.grounding.simple_goal_achieved(initial_state):
            return PlanSequential(domain, problem)

        # create the relaxed plan graph and determine unreachable actions
        rpg = RelaxedPlanGraph(pddl_parser.domain, pddl_parser.problem, self.grounding)

        # setup the search queue
        queue = PriorityQueue()
        hval = rpg.build_graph()
        queue.put(PriorityState(
                hval=hval,
                gval=0,
                action_id=None,
                state=initial_state,
                applicable_actions=rpg.all_actions,
                parent=None))
        
        # begin best-first search (or A* if optimal)
        goal_achieved = False
        while not queue.empty() and not goal_achieved:

            pstate = queue.get()

            # compute heuristic for selected node
            rpg.build_graph(pstate.state)
            _, relaxed_action_count = rpg.get_relaxed_plan()

            # get next states
            for id in rpg.helpful_actions:
                if not self.grounding.check_simple_conditions(id, pstate.state):
                    continue

                # action is applicable 
                new_state = self.grounding.apply_simple_effects(id, pstate.state)

                # check goal
                if self.grounding.simple_goal_achieved(new_state):
                    goal_achieved = True
                    # select child immediately
                    pstate = PriorityState(
                        hval=0,
                        gval=pstate.gval+1 if optimal else 0,
                        action_id=id,
                        state=new_state,
                        applicable_actions=None,
                        parent=pstate)
                else:
                    # add child to queue
                    queue.put(PriorityState(
                        hval=relaxed_action_count,
                        gval=pstate.gval+1 if optimal else 0,
                        action_id=id,
                        state=new_state,
                        applicable_actions=rpg.all_actions,
                        parent=pstate))

        # reconstruct plan
        plan = PlanSequential(domain, problem)
        while pstate and pstate.action_id:
            plan.action_list.insert(0, self.grounding.get_action_from_id(pstate.action_id))
            pstate = pstate.parent

        return plan        

if __name__ == "__main__":
    
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

    # find sequential plan
    print("Finding sequential plan...")
    start_time = time.time()
    planner = Planner()
    plan = planner.find_sequential_plan(pddl_parser.domain, pddl_parser.problem, verbosity=0)
    print("Finding sequential plan took %.2f seconds." % (time.time() - start_time))
    
    plan.print_plan()
    print("Plan valid:", plan.check_plan())