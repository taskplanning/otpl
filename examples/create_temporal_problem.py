from numpy import negative
from examples.create_temporal_domain import create_temporal_domain
from pddl.problem import Problem

def create_temporal_problem() -> Problem:

    domain = create_temporal_domain()
    problem = Problem("match_problem", domain)

    # objects
    problem.add_object("match1", "match")
    problem.add_object("match2", "match")
    problem.add_object("fuse1", "fuse")
    problem.add_object("fuse2", "fuse")

    # initial state
    problem.add_proposition_from_str("unused", ["match1"])
    problem.add_proposition_from_str("unused", ["match2"])
    problem.add_proposition_from_str("unused", ["match2"])

    # ...function assignments
    problem.add_assignment_from_str(0.0, "fuses_mended")

    # ...TILs
    problem.add_til_from_str(10.0, "handempty")
    problem.add_til_from_str(20.0, "handempty", negative=True)

    # goal
    problem.add_simple_goal_from_str("mended", ["fuse1"])
    problem.add_simple_goal_from_str("mended", ["fuse2"])

    return problem

if __name__ == "__main__":
    
    problem = create_temporal_problem()
    print(problem)