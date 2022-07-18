from pddl.domain import Domain
from pddl.problem import Problem
from pddl.grounding import Grounding
from pddl.time_spec import TimeSpec
from plans.temporal_plan import PlanTemporalNetwork

def create_temporal_domain() -> Domain:
        
    domain = Domain("match_domain")

    # types
    domain.add_type("match")
    domain.add_type("fuse")

    # predicates
    domain.add_predicate_from_str("light", {"?m" : "match"})
    domain.add_predicate_from_str("unused", {"?m" : "match"})
    domain.add_predicate_from_str("mended", {"?f" : "fuse"})
    domain.add_predicate_from_str("handempty")

    # light match
    domain.add_operator_from_str("light_match", {"?m" : "match"}, durative=True)
    op = domain.operators['light_match']
    op.set_constant_duration(8)
    op.add_simple_condition_from_str("unused", {"?m" : "match"})
    op.add_simple_effect_from_str("unused", {"?m" : "match"}, is_delete=True)
    op.add_simple_effect_from_str("light", {"?m" : "match"})
    op.add_simple_effect_from_str("unused", {"?m" : "match"}, is_delete=True)

    # mend fuse
    domain.add_operator_from_str("mend_fuse", {"?f" : "fuse", "?m" : "match"}, durative=True)
    op = domain.operators['mend_fuse']
    op.set_constant_duration(5)
    op.add_simple_condition_from_str("light", {"?m" : "match"}, time_spec=TimeSpec.OVER_ALL)
    op.add_simple_condition_from_str("handempty")
    op.add_simple_effect_from_str("handempty", is_delete=True)
    op.add_simple_effect_from_str("mended", {"?f" : "fuse"}, time_spec=TimeSpec.AT_END)
    op.add_simple_effect_from_str("handempty", time_spec=TimeSpec.AT_END)

    return domain

if __name__ == "__main__":
    domain = create_temporal_domain()
    print(domain)
