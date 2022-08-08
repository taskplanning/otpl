from examples.remove_types import remove_types_from_domain
from pddl.atomic_formula import AtomicFormula, TypedParameter
from pddl.domain import Domain
from pddl.effect import Effect, EffectConditional, EffectConjunction, EffectForall, EffectNegative, EffectSimple
from pddl.goal_descriptor import GoalConjunction, GoalDescriptor, GoalSimple

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
    pass

# ======= #
# effects #
# ======= #

def _simplify_effects(domain : Domain):
    """
    Normalises effects in the domain.
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
