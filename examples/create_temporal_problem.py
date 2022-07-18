from examples.create_temporal_domain import create_temporal_domain
from pddl.problem import Problem

def create_temporal_problem() -> Problem:

    problem = Problem("match_problem", domain)

    # objects
    problem.add_object("match1", "match")
    problem.add_object("match2", "match")
    problem.add_object("fuse1", "fuse")
    problem.add_object("fuse2", "fuse")

    # initial state
    problem.add_proposition_from_str("handempty")
    problem.add_proposition_from_str("unused", ["match1"])
    problem.add_proposition_from_str("unused", ["match2"])

    # goal
    problem.add_simple_goal_from_str("mended", ["fuse1"])
    problem.add_simple_goal_from_str("mended", ["fuse2"])

    return problem

if __name__ == "__main__":
    
    domain = create_temporal_domain()
    problem = create_temporal_problem()
    
    print(problem)