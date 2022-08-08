from collections import Counter
from itertools import chain, combinations
from typing import Type
from examples.create_temporal_problem import create_temporal_problem
from examples.remove_types import remove_types_from_domain, remove_types_from_problem
from pddl.atomic_formula import AtomicFormula, TypedParameter
from pddl.domain import Domain
from pddl.effect import EffectForall, EffectSimple, EffectType
from pddl.goal_descriptor import GoalDescriptor, GoalDisjunction, GoalImplication, GoalNegative, GoalQuantified, GoalSimple, GoalType
from pddl.operator import Operator

def create_simple_domain():

    domain = Domain("simple_domain")

    domain.add_type("car")
    domain.add_type("city")

    domain.add_predicate_from_str("at", {"?c" : "car", "?y" : "city"})

    domain.add_operator_from_str("drive", {"?c" : "car", "?from" : "city", "?to" : "city"})
    op = domain.operators['drive']
    op.add_simple_condition_from_str("at", {"?c" : "car", "?from" : "city"})
    op.add_simple_effect_from_str("at", {"?c" : "car", "?from" : "city"}, is_delete=True)
    op.add_simple_effect_from_str("at", {"?c" : "car", "?to" : "city"})

    return domain


def create_nonsimple_domain():

    domain = Domain("nonsimple_domain")

    domain.add_type("block")
    domain.add_type("table")

    domain.add_predicate_from_str("on_table", {"?b" : "block", "?t" : "table"})
    domain.add_predicate_from_str("on_block", {"?b1" : "block", "?b2" : "block"})
    domain.add_predicate_from_str("clear", {"?b" : "block"})
    domain.add_predicate_from_str("destroyed", {"?b" : "block"})
    domain.add_predicate_from_str("handempty")

    domain.add_operator_from_str("destroy_all_blocks", {})
    op = domain.operators['destroy_all_blocks']
    
    op.condition = GoalImplication(
        antecedent=GoalQuantified(
            [TypedParameter("block", "?b")],
            GoalSimple(AtomicFormula.from_string("clear", {"?b" : "block"})),
            GoalType.UNIVERSAL
        ),
        consequent=GoalSimple(AtomicFormula.from_string("handempty"))
    )
    
    op.effect = EffectForall(
        [TypedParameter("block", "?b")],
        EffectSimple(AtomicFormula.from_string("destroyed", {"?b" : "block"}))
    )
    
    return domain

def simplify_implication_conditions(condition : GoalImplication, operator : Operator) -> None:
    """
    Simplifies implied conditions.
    """
    new_condition = GoalDisjunction([GoalNegative(condition.antecedent), condition.consequent])
    operator.condition = new_condition

# =================== #
# invariant synthesis #
# =================== #

class CandidateInvariant():
    def __init__(self, pred_name : str, counted_labels : list[str]):
        self.pred_name = pred_name
        self.counted_labels = counted_labels

    def __repr__(self) -> str:
        return "forall" + ",".join([str(i) for i in self.counted_labels]) + ":" + self.pred_name


def get_modifiable_predicates(effect : EffectSimple, modifiable_predicates : list):
    """
    Returns the list of modifiable predicates in the effect.
    """
    modifiable_predicates.add(effect.formula.name)
    
def get_modified_predicates(effect : EffectSimple, pred_name : str, added_predicates : list, deleted_predicates : list):
    """
    Returns the list of modified predicates in the effect.
    """
    if effect.formula.name != pred_name: return
    if effect.effect_type == EffectType.NEGATIVE:
        deleted_predicates.append(effect.formula)
    else:
        added_predicates.append(effect.formula)

if __name__ == "__main__":

    domain = create_simple_domain()

    # Normalise the problem, removing types and simplifying conditions
    remove_types_from_domain(domain)
    for _, op in domain.operators.items():
        op.visit(simplify_implication_conditions, valid_types=(GoalImplication), args=(op,))

    print("Modifiable Predicates")
    modifiable_predicates = set()
    domain.visit(get_modifiable_predicates, valid_types=(EffectSimple), args=(modifiable_predicates,))
    print(modifiable_predicates)

    print("Initial Candidates")
    candidates = []
    for pred in modifiable_predicates:
        predicate = domain.predicates[pred]
        powerset = list(chain.from_iterable(combinations(range(len(predicate.typed_parameters)), r) for r in range(1,len(predicate.typed_parameters)+1)))
        for combination in powerset:
            candidates.append(CandidateInvariant(pred, [p for p in combination]))
    print(candidates)

    print("Proving Invariants")
    proved_candidates = []
    for candidate in candidates:
        balanced = True
        for operator in domain.operators.values():
            adds, dels = [], []
            operator.visit(get_modified_predicates, valid_types=(EffectSimple), args=(candidate.pred_name, adds, dels))
            for prop in dels:
                for other in adds:
                    if prop.name != other.name:
                        continue
                    match = True
                    for index in candidate.counted_labels:
                        if prop.typed_parameters[index].label != other.typed_parameters[index].label:
                            match = False
                            break
                    if not match: continue
                    adds.remove(other)
                    break
            if len(adds) > 0:
                balanced = False
                break
        if balanced: proved_candidates.append(candidate)
    print(proved_candidates)