from examples.remove_types import remove_types_from_domain
from pddl.atomic_formula import AtomicFormula, TypedParameter
from pddl.domain import Domain
from pddl.effect import Effect, EffectConditional, EffectConjunction, EffectForall, EffectNegative, EffectSimple
from pddl.goal_descriptor import GoalConjunction, GoalDescriptor, GoalDisjunction, GoalImplication, GoalNegative, GoalQuantified, GoalSimple

def normalise_domain(domain : Domain):
    """
    Normalise a domain by:
    1. Removing types from the domain.
    2. Simpliyfying conditions.
    3. Simplifying effects.
    Following the procedure presented in:
    "Concise finite-domain representations for PDDL planning tasks"
    Malte Helmert, Artificial Intelligence, 2009
    https://doi.org/10.1016/j.artint.2008.10.013
    """
    remove_types_from_domain(domain)
    _simplify_conditions(domain)
    _simplify_effects(domain)

# ========= #
# condition #
# ========= #

def _simplify_conditions(domain : Domain):
    """
    Simplifies the conditions in the domain.
    1. Implications are removed.
    2. Conditions are transformed into first-order negation normal form.
    3. Universal quantifiers are removed.
    4. Disjunctions are moved to the outside.
    5. Structures are split to eliminate disjunctions.
    """
    for op in domain.operators.values():

        # remove implications
        if not isinstance(op.condition, GoalConjunction):
            op.condition = GoalConjunction([op.condition])
        _remove_all_implications(op.condition)

        # transform into negation normal form
        for sub_condition in op.condition.goals:
            _transform_into_negation_normal_form(sub_condition, [op.condition], False)

# ============ #
# implications #
# ============ #

def _replace_implication(condition : GoalDescriptor) -> GoalDescriptor:
    """
    Replaces an implication with a disjunction of the antecedent and consequent.
    """
    if isinstance(condition, GoalImplication):
        return GoalDisjunction([
            GoalNegative(condition.antecedent),
            condition.consequent
            ])
    return condition

def _remove_all_implications(parent_condition : GoalDescriptor):
    """
    Removes all implications in the effect tree using the rule:
        A implies B -> (not A) or B
    """
    if isinstance(parent_condition, GoalConjunction) or isinstance(parent_condition, GoalDisjunction):

        # recurse on the sub-conditions
        for sub_condition in parent_condition.goals:
            _remove_all_implications(sub_condition)

        # check and possibly replace each sub-condition
        new_conditions = []
        for condition in parent_condition.goals:
            new_conditions.append(_replace_implication(condition))
        parent_condition.goals = new_conditions

    elif isinstance(parent_condition, GoalNegative) or isinstance(parent_condition, GoalQuantified):
        _remove_all_implications(parent_condition.goal)
        parent_condition.goal = _replace_implication(parent_condition.goal)

    elif isinstance(parent_condition, GoalImplication):
        _remove_all_implications(parent_condition.antecedent)
        _remove_all_implications(parent_condition.consequent)
        parent_condition.antecedent = _replace_implication(parent_condition.antecedent)
        parent_condition.consequent = _replace_implication(parent_condition.consequent)

# === #
# NNF #
# === #

def _transform_into_negation_normal_form(condition : GoalDescriptor, path : list[GoalDescriptor], negate : bool):
    """
    Uses DeMorgan's laws to transform the condition into negation normal form.
    Assumes that implications have already been removed and the path contains a single conjunction.
    param condition: Condition to transform.
    param path: Path through condition tree to this condition.
    param negate: True if the condition should be negated.
    """
    new_condition = None
    if negate and (isinstance(condition, GoalConjunction) or isinstance(condition, GoalDisjunction)):

        # negate each sub-condition
        sub_conditions = []
        for sub_condition in condition.goals:
            if isinstance(sub_condition, GoalNegative):
                sub_conditions.append(sub_condition.goal)
            else: sub_conditions.append(GoalNegative(sub_condition))

        # create the alternate condition
        if isinstance(condition, GoalConjunction):
            new_condition = GoalDisjunction(sub_conditions)
        elif isinstance(condition, GoalDisjunction):
            new_condition = GoalConjunction(sub_conditions)

        # toggle negation
        negate = False

    elif negate and isinstance(condition, GoalNegative):

        # negate the sub-condition
        new_condition = condition.goal
        negate = False

    # set parent's condition to the new condition
    if new_condition is not None:
        if isinstance(path[-1], GoalConjunction) or isinstance(path[-1], GoalDisjunction):
            path[-1].goals.remove(condition)
            path[-1].goals.append(new_condition)
        elif isinstance(path[-1], GoalQuantified):
            path[-1].goal = new_condition
        elif isinstance(path[-1], GoalNegative):
            # eliminate the negative parent
            if isinstance(path[-2], GoalConjunction) or isinstance(path[-2], GoalDisjunction):
                path[-2].goals.remove(path[-1])
                path[-2].goals.append(new_condition)
            elif isinstance(path[-2], GoalQuantified) or isinstance(path[-2], GoalNegative):
                path[-2].goal = new_condition
        condition = new_condition

    # recurse on the sub-conditions
    if isinstance(condition, GoalConjunction) or isinstance(condition, GoalDisjunction):
        for sub_condition in condition.goals:
            new_path = path.copy()
            new_path.append(condition)
            _transform_into_negation_normal_form(sub_condition, new_path, negate)
    elif isinstance(condition, GoalQuantified):
        path.append(condition)
        _transform_into_negation_normal_form(condition.goal, path, negate)
    elif isinstance(condition, GoalNegative):
        path.append(condition)
        _transform_into_negation_normal_form(condition.goal, path, True)

# ======= #
# effects #
# ======= #

def _simplify_effects(domain : Domain):
    """
    Simplifies effects in the domain.
    1. Universal and conditional effects are moved into conjunctive effects.
    2. Conditional effects are moved into universal effects.
    3. Nested effects of the same type are flattened.
    4. Dummy effects are added to make form consistent.
    """
    for op in domain.operators.values():

        # Move everything into conjunctive effects
        new_effects = _expand_effect(op.effect)
        if len(new_effects) > 1: op.effect = EffectConjunction(new_effects)
        _expand_all_effects(op.effect)

        # Move conditional effects into universal effects
        op.effect = _nest_conditional(op.effect)
        _nest_all_conditionals(op.effect)

        # Flatten nested effects of the same type
        _flatten_all_effects(op.effect)

        # Add dummy effects
        if not isinstance(op.effect, EffectConjunction):
            op.effect = EffectConjunction([op.effect])
        _normalise_all_effects(op.effect)

# ============== #
# expand effects #
# ============== #

def _expand_effect(effect) -> list[Effect]:
    """
    Expands effect to multiple effects and returns a list.
    If the effect does not need to be expanded, the list is of length one.
    param effect: Effect to expand.
    """
    # we are only expanding effects of this form
    if not isinstance(effect, EffectForall) and not isinstance(effect, EffectConditional):
        return [effect]

    # only need to expand if the sub-effect is conjunction
    if not isinstance(effect.effect, EffectConjunction):
        return [effect]

    # expand the sub-effect
    sub_effects = []
    for sub_effect in effect.effect.effects:
        if isinstance(effect, EffectForall):
            sub_effects.append(EffectForall(effect.typed_parameters, sub_effect))
        elif isinstance(effect, EffectConditional):
            sub_effects.append(EffectConditional(effect.condition.copy(), sub_effect))
    return sub_effects

def _expand_all_effects(parent_effect : Effect):
    """
    Recursively expands all effects in the effect tree.
    Universal effects are expanded following the rule:
        forall(x): A && B -> forall(x): A && forall(x): B
    Conditional effects are expanded following the rule:
        if(x): B -> if(x): A && if(x): B
    """
    if isinstance(parent_effect, EffectConjunction):

        # recurse on the sub-effects
        for sub_effect in parent_effect.effects:
            _expand_all_effects(sub_effect)

        # check and possibly expand each sub-effect
        new_effects = []
        for effect in parent_effect.effects:
            if isinstance(effect, EffectConjunction):
                # flatten conjunctions
                new_effects.extend(effect.effects)
            else: new_effects.extend(_expand_effect(effect))
        parent_effect.effects = new_effects

    elif isinstance(parent_effect, EffectForall) or isinstance(parent_effect, EffectConditional):

        # recurse on the sub-effect
        _expand_all_effects(parent_effect.effect)

        # possibly expand the sub-effect
        new_effects = _expand_effect(parent_effect.effect)
        if len(new_effects) > 1: parent_effect.effect = EffectConjunction(new_effects)

# ============ #
# nest effects #
# ============ #

def _nest_conditional(effect : Effect) -> Effect:
    """
    Checks if the effect is a conditional over a universal and if so, nests it.
    """
    if isinstance(effect, EffectConditional) and isinstance(effect.effect, EffectForall):
        forall = effect.effect
        effect.effect = forall.effect
        forall.effect = effect
        return forall
    else:
        return effect

def _nest_all_conditionals(parent_effect : Effect):
    """
    Moves conditional effects into universal effects using the following rule:
        if(x): forall(y): A -> forall(y): if(x): A
    """
    if isinstance(parent_effect, EffectConjunction):

        # recurse on sub-effects
        for sub_effect in parent_effect.effects:
            _nest_all_conditionals(sub_effect)

        # check and possibly nest each sub-effect
        new_effects = []
        for sub_effect in parent_effect.effects:
            new_effects.append(_nest_conditional(sub_effect))
        parent_effect.effects = new_effects

# =============== #
# flatten effects #
# =============== #

def _flatten_all_effects(parent_effect : Effect):
    """
    Flattens effects in the effect tree.
    Nested Conjunctions are flattened into a single conjunction.
    Nested Universals are flattened into a single universal using the rule:
        forall(x): forall(y): A -> forall(x,y): A
    Nested Conditionals are flattened into a single conditional using the rule:
        if(x): if(y): A -> if(x && y): A
    """
    if isinstance(parent_effect, EffectConjunction):

        # recurse on sub-effects
        for sub_effect in parent_effect.effects:
            _flatten_all_effects(sub_effect)

        # check and possibly flatten each sub-effect
        new_effects = []
        for sub_effect in parent_effect.effects:
            if isinstance(sub_effect, EffectConjunction):
                # flatten conjunctions
                new_effects.extend(sub_effect.effects)
            else: new_effects.append(sub_effect)
        parent_effect.effects = new_effects

    elif isinstance(parent_effect, EffectForall):

        # recurse on sub-effect
        _flatten_all_effects(parent_effect.effect)

        # check and possibly flatten the sub-effect
        if isinstance(parent_effect.effect, EffectForall):
            # flatten universals
            parent_effect.typed_parameters.extend(parent_effect.effect.typed_parameters)
            parent_effect.effect = parent_effect.effect.effect

    elif isinstance(parent_effect, EffectConditional):

        # recurse on sub-effect
        _flatten_all_effects(parent_effect.effect)

        # check and possibly flatten the sub-effect
        if isinstance(parent_effect.effect, EffectConditional):
            # flatten conditionals
            if not isinstance(parent_effect.condition, GoalConjunction):
                parent_effect.condition = GoalConjunction([parent_effect.condition])
            parent_effect.condition.goals.append(parent_effect.effect.condition)
            parent_effect.effect = parent_effect.effect.effect

# ================= #
# normalise effects #
# ================= #

def _normalise_all_effects(effect : EffectConjunction):
    """
    Add dummy effects to ensuring that all effects are in the form:
    conjunction -> universal -> conditional -> simple
    The conjunctive effect is already assumed to be expanded, nested, and flattened.
    """
    new_effects = []
    for sub_effect in effect.effects:

        if isinstance(sub_effect, EffectSimple):
            # wrap simple effect in universal and conditional
            new_effects.append(EffectForall([], EffectConditional(GoalDescriptor(), sub_effect)))
        
        elif isinstance(sub_effect, EffectConditional):
            # wrap conditional effect in universal
            new_effects.append(EffectForall([], sub_effect))
        
        elif isinstance(sub_effect, EffectForall) and not isinstance(sub_effect.effect, EffectConditional):
            # wrap inner effect in a conditional
            sub_effect.effect = EffectConditional(GoalDescriptor(), sub_effect.effect)
            new_effects.append(sub_effect)

        elif isinstance(sub_effect, EffectForall) and isinstance(sub_effect.effect, EffectConditional):
            # already in proper form
            new_effects.append(sub_effect)

    effect.effects = new_effects

# ======= #   
# testing #
# ======= #

def _create_nonsimple_domain():
    domain = Domain("nonsimple_domain")

    domain.add_type("block")
    domain.add_type("table")

    domain.add_predicate_from_str("on_table", {"?b" : "block", "?t" : "table"})
    domain.add_predicate_from_str("on_block", {"?b1" : "block", "?b2" : "block"})
    domain.add_predicate_from_str("clear", {"?b" : "block"})
    domain.add_predicate_from_str("destroyed", {"?b" : "block"})
    domain.add_predicate_from_str("handempty")
    
    domain.add_operator_from_str("clear_one_block", {"?b" : "block", "?t" : "table"})
    op = domain.operators['clear_one_block']

    op.condition = GoalImplication(
        antecedent=GoalConjunction([
            GoalSimple(AtomicFormula.from_string("on_table", {"?b" : "block", "?t" : "table"})),
            GoalSimple(AtomicFormula.from_string("on_table", {"?b" : "block", "?t" : "table"})),
            GoalSimple(AtomicFormula.from_string("on_table", {"?b" : "block", "?t" : "table"}))
            ]),
        consequent=GoalSimple(AtomicFormula.from_string("handempty"))
        )

    op.effect = EffectConditional(
            condition = GoalSimple(AtomicFormula.from_string("on_table", {"?b" : "block", "?t" : "table"})),
            effect = EffectConjunction([
                EffectSimple(AtomicFormula.from_string("clear", {"?b" : "block"})),
                EffectForall(
                    typed_parameters = [TypedParameter("table", "?t2")],
                    effect = EffectConjunction([EffectConjunction([
                        EffectNegative(AtomicFormula.from_string("on_table", {"?b" : "block", "?t" : "table"})),
                        EffectNegative(AtomicFormula.from_string("on_table", {"?b" : "block", "?t2" : "table"}))
                    ])])
                ),
                EffectConditional(
                    condition = GoalSimple(AtomicFormula.from_string("handempty")),
                    effect = EffectNegative(AtomicFormula.from_string("handempty"))
                )
            ])
    )
    return domain

if __name__ == "__main__":

    domain = _create_nonsimple_domain()
    normalise_domain(domain)
    print(domain)
