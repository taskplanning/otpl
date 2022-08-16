import itertools
from examples.remove_types import remove_types_from_domain
from pddl.atomic_formula import AtomicFormula, TypedParameter
from pddl.derived_predicate import DerivedPredicate
from pddl.domain import Domain
from pddl.effect import Effect, EffectConditional, EffectConjunction, EffectForall, EffectNegative, EffectSimple
from pddl.goal_descriptor import GoalConjunction, GoalDescriptor, GoalDisjunction, GoalImplication, GoalNegative, GoalQuantified, GoalSimple, GoalType
from pddl.operator import Operator

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
    new_operators : list[Operator] = []
    remove_operators = set()
    for op in domain.operators.values():

        # 1. remove implications
        if not isinstance(op.condition, GoalConjunction):
            op.condition = GoalConjunction([op.condition])
        _remove_all_implications(op.condition)

        # 2. transform into negation normal form
        op.condition = _transform_into_negation_normal_form(op.condition, False)

        # 3. remove universal quantifiers
        op.condition = _remove_universal_conditions(op.condition, domain)

        # 4. move disjunctions to the outside
        op.condition = _move_disjunctive_condition(op.condition)

        # 5. split structures to eliminate disjunctions
        op.condition = _flatten_disjunctive_conditions(op.condition)
        if isinstance(op.condition, GoalDisjunction):
            count = 0
            for disj in op.condition.goals:
                # create new operator
                new_formula = op.formula.copy()
                new_formula.name = op.formula.name + "_" + str(count)
                new_op = Operator(new_formula, durative=False)
                new_op.condition = disj
                new_op.effect = op.effect.copy()
                new_operators.append(new_op)
                count += 1
            remove_operators.add(op.formula.name)

    # add all new split operators to the domain
    for op in new_operators: domain.operators[op.formula.name] = op
    # remove all old operators
    for name in remove_operators: domain.operators.pop(name)

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

def _transform_into_negation_normal_form(condition : GoalDescriptor, negate : bool) -> GoalDescriptor:
    """
    Uses DeMorgan's laws to transform the condition into negation normal form.
    Assumes that implications have already been removed and the path contains a single conjunction.
    param condition: Condition to transform.
    param negate: True if the condition should be negated.
    returns: The transformed condition.
    """
    if isinstance(condition, GoalConjunction) or isinstance(condition, GoalDisjunction):

        # possibly negate the condition
        if negate: new_condition = GoalDisjunction([]) if isinstance(condition, GoalConjunction) else GoalConjunction([])
        else: new_condition = GoalConjunction([]) if isinstance(condition, GoalConjunction) else GoalDisjunction([])

        # recurse on the sub-conditions
        for sub_condition in condition.goals:
            new_condition.goals.append(_transform_into_negation_normal_form(sub_condition, negate))
        return new_condition

    elif isinstance(condition, GoalQuantified):

        # possibly negate the quantifier and recurse
        if negate: condition.goal_type = GoalType.EXISTENTIAL if condition.goal_type == GoalType.UNIVERSAL else GoalType.UNIVERSAL
        condition.goal = _transform_into_negation_normal_form(condition.goal, negate)
        return condition

    elif isinstance(condition, GoalNegative):

        # eliminate the negative goal and recurse
        if negate: return _transform_into_negation_normal_form(condition.goal, False)
        else: return _transform_into_negation_normal_form(condition.goal, True)

    else:

        # possibly negate the condition
        if negate: return GoalNegative(condition)
        else: return condition

# =========================== #
# remove universal conditions #
# =========================== #

def _collect_typed_parameters(condition : GoalSimple, params : list[TypedParameter]):
    """
    Collects all typed parameters in the condition.
    """
    for param in condition.atomic_formula.typed_parameters:
        match = False
        for other in params:
            if other.type == param.type and other.label == param.label:
                match = True
                break
        if not match: params.append(param)

def _remove_universal_conditions(condition : GoalDescriptor, domain : Domain) -> GoalDescriptor:
    """
    Eliminates universal conditions. If a universal is found during traversal
    through the condition tree, then it is replaced using the following rule:
        forall x: phi -> not exists x not phi -> not new_pred
    where new_pred is a new derived predicate: exists x not phi.
    """
    if isinstance(condition, GoalQuantified) and condition.goal_type == GoalType.UNIVERSAL:

        # create new derived predicate
        pred_name = "derived_predicate_" + str(len(domain.derived_predicates))
        typed_parameters = []
        condition.visit(_collect_typed_parameters, valid_types=(GoalSimple,), kwargs={"params" : typed_parameters})
        derived_predicate = AtomicFormula(pred_name, typed_parameters)
        derived_condition = GoalQuantified(
            typed_parameters=condition.typed_parameters,
            quantification=GoalType.EXISTENTIAL,
            goal=_transform_into_negation_normal_form(condition.goal, True))
        domain.derived_predicates.append(DerivedPredicate(derived_condition, derived_predicate))

        # create new condition
        return GoalNegative(GoalSimple(derived_predicate))

    elif isinstance(condition, GoalConjunction) or isinstance(condition, GoalDisjunction):

        # recurse on the sub-conditions
        new_subconditions = []
        for sub_condition in condition.goals:
            new_subconditions.append(_remove_universal_conditions(sub_condition, domain))
        condition.goals = new_subconditions

    elif isinstance(condition, GoalNegative):
        condition.goal = _remove_universal_conditions(condition.goal, domain)
    
    return condition

# ================= #
# move disjunctions #
# ================= #

def _move_disjunctive_condition(condition : GoalDescriptor) -> GoalDescriptor:
    """
    Moves disjunctions to the root of the condition tree using the following rules:
        exists x (phi or psi) -> exists x phi or exists x psi
        xi and (phi or psi) -> (xi and phi) or (xi and psi)
    Assumes that universals and implications have already been removed.
    """
    if isinstance(condition, GoalConjunction):

        # recurse on the sub-conditions
        subgoals = []
        disjunctions = []
        for subgoal in condition.goals:
            subgoal = _move_disjunctions(subgoal)
            if isinstance(subgoal, GoalDisjunction):
                disjunctions.append(subgoal)
            else: subgoals.append(subgoal)

        if len(disjunctions) > 0:
            # create root disjunction
            new_condition = GoalDisjunction([])
            # prepare conjunctive part (xi)
            conjunction = GoalConjunction(subgoals)
            # loop through permutations of disjunctive parts
            perms = list(itertools.product(*[d.goals for d in disjunctions]))
            for perm in perms:
                # cop the conjunctive part (xi)
                new_subgoal = conjunction.copy()
                # add the disjunctive parts (phi) or (psi)
                for goal in perm: new_subgoal.goals.append(goal)
                # add the new subgoal to the root disjunction
                new_condition.goals.append(new_subgoal)
            return new_condition
        else:
            # no disjunctions to move
            return GoalConjunction(subgoals)

    elif isinstance(condition, GoalQuantified):

        # recurse on the sub-condition
        condition.goal = _move_disjunctions(condition.goal)
        
        # move disjunctions to the root
        if isinstance(condition.goal, GoalDisjunction):
            new_condition = GoalDisjunction([])
            for subgoal in condition.goal.goals:
                new_condition.goals.append(GoalQuantified(
                    typed_parameters=condition.typed_parameters,
                    quantification=condition.goal_type,
                    goal=subgoal))
            return new_condition
        else: 
            # no disjunction to move
            return condition
    
    return condition

def _flatten_disjunctive_conditions(condition : GoalDescriptor) -> GoalDescriptor:
    if not isinstance(condition, GoalDisjunction): return condition
    new_goals = []
    for goal in condition.goals:
        if not isinstance(goal, GoalDisjunction): new_goals.append(goal)
        else: new_goals.extend(goal.goals)
    return GoalDisjunction(new_goals)

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
        op.effect = _move_disjunctions(op.effect)
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

def _move_disjunctions(effect : Effect) -> Effect:
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
            new_effects.append(_move_disjunctions(sub_effect))
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
        antecedent=GoalQuantified(
            typed_parameters=[TypedParameter("table", "?t2")],
            quantification=GoalType.EXISTENTIAL,
            goal=GoalConjunction([
                GoalSimple(AtomicFormula.from_string("on_table", {"?b" : "block", "?t" : "table"})),
                GoalSimple(AtomicFormula.from_string("on_table", {"?b" : "block", "?t" : "table"})),
                GoalSimple(AtomicFormula.from_string("on_table", {"?b" : "block", "?t" : "table"}))
            ])
        ),
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
    