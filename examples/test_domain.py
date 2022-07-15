from pddl.atomic_formula import AtomicFormula, TypedParameter
from pddl.domain import Domain
from pddl.problem import Problem
from pddl.duration import DurationInequality
from pddl.effect import EffectConjunction, EffectNegative, EffectSimple, TimedEffect
from pddl.expression import ExprBase, ExprComposite
from pddl.goal_descriptor import GoalConjunction, GoalSimple
from pddl.goal_descriptor_inequality import Inequality
from pddl.operator import Operator
from pddl.time_spec import TimeSpec

domain = Domain("match_domain")

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
op.add_simple_effect_from_str("unused", {"?m" : "match"}, time_spec=TimeSpec.AT_START, is_delete=True)
op.add_simple_effect_from_str("light", {"?m" : "match"}, time_spec=TimeSpec.AT_START)
op.add_simple_effect_from_str("unused", {"?m" : "match"}, time_spec=TimeSpec.AT_START, is_delete=True)

# mend fuse
domain.add_operator_from_str("mend_fuse", {"?f" : "fuse", "?m" : "match"}, durative=True)
op = domain.operators['mend_fuse']
op.set_constant_duration(5)
op.add_simple_condition_from_str("light", {"?m" : "match"}, time_spec=TimeSpec.OVER_ALL)
op.add_simple_condition_from_str("handempty")
op.add_simple_effect_from_str("handempty", time_spec=TimeSpec.AT_START, is_delete=True)
op.add_simple_effect_from_str("mended", {"?f" : "fuse"}, time_spec=TimeSpec.AT_END)
op.add_simple_effect_from_str("handempty", time_spec=TimeSpec.AT_END)

print(domain)

problem = Problem("match_problem", "match_domain")

# objects
problem.add_object("match1", "match")
problem.add_object("match2", "match")
problem.add_object("fuse1", "fuse")
problem.add_object("fuse2", "fuse")

# initial state
problem.propositions.append(AtomicFormula("handempty"))
problem.propositions.append(AtomicFormula("unused", [TypedParameter("match", "?m", "match1")]))
problem.propositions.append(AtomicFormula("unused", [TypedParameter("match", "?m", "match2")]))

# goal
problem.goal = GoalConjunction([
    GoalSimple(AtomicFormula("handempty"))
])

print(problem)