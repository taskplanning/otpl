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
    """
    This class defines a simple planner that can be used as the basis for some experimentation.
    """

    def __init__(self):
        self.domain = None
        self.problem = None

    def find_sequential_plan(self, domain : Domain, problem : Problem, optimal : bool = False, verbose : bool = False) -> PlanSequential:
        """
        Searches for a sequential plan in the given a propositional domain and problem.
        By default the search algorithm is best first search.
        If optimal is True, the search algorithm is A* instead of best first.
        The number of actions in the relaxed plan is the heuristic. 
        The search uses lazy evaluation, i.e. heuristic values are only computed for nodes when they are selected from the priority queue.
        Only helpful actions are considered when expanding a node!
        """

        self.domain = domain
        self.problem = problem
        self.grounding = problem.grounding
        initial_state = self.problem.get_initial_state()

        # check if the goal is achieved in the initial state
        if self.grounding.check_simple_goal(initial_state, problem.goal):
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
        expanded = 0
        while not queue.empty() and not goal_achieved:

            pstate = queue.get()
            expanded += 1

            # compute heuristic for selected node
            rpg.build_graph(pstate.state)
            _, relaxed_action_count = rpg.get_relaxed_plan()

            if verbose and expanded%1000==0: print("(n: %d; h: %d; q: %d" % (expanded, relaxed_action_count, queue.qsize()))

            # get next states
            for id in rpg.helpful_actions:
                if not self.grounding.check_simple_conditions(id, pstate.state):
                    continue

                # action is applicable 
                new_state = pstate.state.copy()
                self.grounding.apply_simple_action_effects(id, new_state)

                # check goal
                if self.grounding.check_simple_goal(new_state, problem.goal):
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
    
    # command line arguments
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("domain", help="path to PDDL domain file")
    arg_parser.add_argument("problem", help="path to PDDL problem file")
    args = arg_parser.parse_args()
    
    # parse PDDL domain and problem files
    pddl_parser = Parser()
    pddl_parser.parse_file(args.domain)
    pddl_parser.parse_file(args.problem)

    # find sequential plan
    planner = Planner()
    plan = planner.find_sequential_plan(pddl_parser.domain, pddl_parser.problem, optimal=False, verbose=True)
    plan.print_plan()