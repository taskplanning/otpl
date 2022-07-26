from plans.temporal_plan import PlanTemporalNetwork
from examples.create_temporal_domain import create_temporal_domain
from examples.create_temporal_problem import create_temporal_problem

if __name__ == "__main__":
    """
    This script uses the PlanTemporalNetwork class.
    First it creates the PDDL domain and problem files.
    Then it loads a temporal plan from file and generates a temporal network.
    Then it simulates the execution of the temporal plan for some time, storing the current
    state and the remaining TILs. Some TILs represent the effects of ongoing actinos.
    Finally, it prints the current state as a new problem file.
    """

    domain = create_temporal_domain()
    problem = create_temporal_problem()
    
    print("Printing the original problem...")
    print(problem)
    print("")

    print("Parsing plan file...")
    plan_file = "pddl/test_domains/match_plan.pddl"
    plan = PlanTemporalNetwork(domain, problem)
    plan.read_from_file(plan_file)
    
    # print the plan file
    with open(plan_file, "r") as f: print(f.read())
    print("")

    time = 13.0
    print("Printing the problem at time {:0.2f}".format(time))
    state, ongoing_action_tils = plan.simulate_execution(until_time=time)

    # update the problem to the current state and time
    problem.update_with_state(state)
    
    # add new TILs to the problem that represent the end effects of ongoing actions
    for til in ongoing_action_tils: problem.add_til(til)
    
    print(problem)
