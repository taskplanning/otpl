class Problem:
    """
    A class that describes a PDDL instance, including:
    - current objects
    - current state
    - goals & metric
    """

    def __init__(self, domain_name : str, problem_name : str) -> None:
        self.problem_name = problem_name       
        self.objects = []
        self.propositions = []
        self.functions = []
        self.timed_initial_literals = []
        self.timed_initial_functions = []
        self.goal = []
        self.metric = []
        self.one_of_constraints = []

    def print_problem(self):
        pass