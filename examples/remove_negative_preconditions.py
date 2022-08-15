from examples.create_temporal_domain import create_temporal_domain
from examples.normalise_domain import _simplify_conditions
from pddl.domain import Domain
from pddl.effect import Effect, EffectConditional, EffectConjunction, EffectForall, EffectNegative, EffectSimple, EffectType, TimedEffect
from pddl.goal_descriptor import GoalConjunction, GoalDescriptor, GoalDisjunction, GoalNegative, GoalQuantified, GoalSimple, TimedGoal

def _negate_negative_precondition(condition : GoalNegative, negative_predicate_map : dict) -> GoalDescriptor:
    """
    Negate a negative precondition.
    The negative precondition is assumed to be a negated simple precondition.
    param condition: The condition to negate.
    param negative_predicate_map: A map from predicate names to the negated predicate.
    """
    if not isinstance(condition.goal, GoalSimple):
        raise ValueError("Negative precondition must be simple")   
       
    # map negation
    pred_name = condition.goal.atomic_formula.name
    if pred_name not in negative_predicate_map:
        negative_predicate_map[pred_name] = "not_" + pred_name
        negative_predicate_map[negative_predicate_map[pred_name]] = pred_name

    # create positive precondition
    formula = condition.goal.atomic_formula.copy()
    formula.name = negative_predicate_map[formula.name]
    return GoalSimple(formula)

def _negate_all_negative_preconditions(parent_condition : GoalDescriptor, negative_predicate_map : dict) -> None:
    """
    Negate all negative preconditions in the condition.
    Precoditions are assumed to be in negated normal form.
    param condition: The condition to negate.
    param negative_predicate_map: A map from predicate names to the negated predicate.
    """
    if isinstance(parent_condition, GoalConjunction) or isinstance(parent_condition, GoalDisjunction):

        # recurse on subconditions
        for subcondition in parent_condition.goals:
            _negate_all_negative_preconditions(subcondition, negative_predicate_map)

        # check and possibly negate subconditions
        new_conditions = []
        for subcondition in parent_condition.goals:
            if isinstance(subcondition, GoalNegative):
                new_conditions.append(_negate_negative_precondition(subcondition, negative_predicate_map))
            else:
                new_conditions.append(subcondition)
        parent_condition.goals = new_conditions

    elif isinstance(parent_condition, GoalQuantified) or isinstance(parent_condition, TimedGoal):

        # recurse on subcondition
        _negate_all_negative_preconditions(parent_condition.goal, negative_predicate_map)

        # check and possibly negate subcondition
        if isinstance(parent_condition.goal, GoalNegative):
            parent_condition.goal = _negate_negative_precondition(parent_condition.goal, negative_predicate_map)    

def _update_effect(effect : Effect, negative_precondition_map) -> Effect:
    """
    Update an effect so that each add and delete effect on a key of the negative_precondition_map is negated.
    param effect: The effect to update.
    param negative_precondition_map: A map from predicate names to the negated predicate.
    """
    if isinstance(effect, EffectConjunction):
            
        # recurse on subeffects
        for subeffect in effect.effects:
            _update_effect(subeffect, negative_precondition_map)

        # check and possibly negate subeffects
        new_effects = []
        for subeffect in effect.effects:
            if isinstance(subeffect, EffectSimple):
                new_effects.append(_update_effect(subeffect, negative_precondition_map))
        effect.effects.extend(new_effects)
    elif isinstance(effect, EffectSimple):
        if isinstance(effect.atomic_formula, GoalSimple):
            if effect.atomic_formula.name in negative_precondition_map:
                effect.atomic_formula.name = negative_precondition_map[effect.atomic_formula.name]
    return effect


def _update_all_effects(parent_effect : Effect, negative_predicate_map : dict) -> None:
    """
    Update effects so that each add and delete effect on a key of the negative_predicate_map is negated.
    param parent_effect: The effect to update.
    param negative_predicate_map: A map from predicate names to the negated predicate.
    """
    if isinstance(parent_effect, EffectConjunction):
            
        # recurse on subeffects
        for subeffect in parent_effect.effects:
            _update_all_effects(subeffect, negative_predicate_map)

        # check and possibly negate subeffects
        new_effects = []
        for subeffect in parent_effect.effects:
            if isinstance(subeffect, EffectNegative) and subeffect.formula.name in negative_predicate_map:
                new_effect = EffectSimple(subeffect.formula.copy())
                new_effect.formula.name = negative_predicate_map[subeffect.formula.name]
                new_effects.append(new_effect)
            elif isinstance(subeffect, EffectSimple) and subeffect.formula.name in negative_predicate_map:
                new_effect = EffectNegative(subeffect.formula.copy())
                new_effect.formula.name = negative_predicate_map[subeffect.formula.name]
                new_effects.append(new_effect)
        parent_effect.effects.extend(new_effects)

    if isinstance(parent_effect, EffectForall) or isinstance(parent_effect, EffectConditional) or isinstance(parent_effect, TimedEffect):

        # recurse on subeffect
        _update_all_effects(parent_effect.effect, negative_predicate_map)

        # check and possibly negate subeffect
        if isinstance(parent_effect.effect, EffectSimple) and parent_effect.effect.formula.name in negative_predicate_map:

            # make negated effect
            if parent_effect.effect.effect_type == EffectType.NEGATIVE:
                new_effect = EffectSimple(parent_effect.effect.formula.copy())
            else: new_effect = EffectNegative(parent_effect.effect.formula.copy())
            new_effect.formula.name = negative_predicate_map[parent_effect.effect.formula.name]

            # update parent effect
            parent_effect.effect = EffectConjunction([new_effect, parent_effect.effect])


def remove_negative_preconditions(domain: Domain) -> None:
    """
    Remove negative preconditions from the domain.
    param domain: The domain to remove negative preconditions from.
    """

    # put conditions in negated normal form
    _simplify_conditions(domain)

    # negate all negative preconditions
    negative_predicate_map = {}
    for _, operator in domain.operators.items():
        _negate_all_negative_preconditions(operator.condition, negative_predicate_map)


    print(negative_predicate_map)

    # add new predicates to the domain
    for predicate, other in negative_predicate_map.items():
        if other in domain.predicates: continue
        formula = domain.predicates[predicate].copy()
        formula.name = other
        domain.predicates[other] = formula

    # adjust all add and delete effects
    for _, operator in domain.operators.items():
        _update_all_effects(operator.effect, negative_predicate_map)
       

if __name__ == "__main__":
    domain = create_temporal_domain()
    print("Domain before:")
    print(domain)
    print()
    remove_negative_preconditions(domain)
    print("Domain after:")
    print(domain)

    