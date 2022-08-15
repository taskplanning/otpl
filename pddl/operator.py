from pddl.duration import Duration, DurationInequality
from pddl.atomic_formula import AtomicFormula, TypedParameter
from pddl.effect import Effect, EffectConjunction, EffectNegative, EffectSimple, EffectType, TimedEffect
from pddl.effect_assignment import Assignment, AssignmentType
from pddl.expression import ExprBase, ExprComposite
from pddl.goal_descriptor import GoalConjunction, GoalDescriptor, GoalNegative, GoalSimple, GoalType, TimedGoal
from pddl.goal_descriptor_inequality import Inequality
from pddl.time_spec import TimeSpec


class Operator:
    """ 
    A class used to represent an operator in the domain.
    """

    def __init__(self,
            formula  : AtomicFormula,
            durative : bool,
            duration : Duration = None,
            condition : GoalDescriptor = None,
            effect : Effect = None,
            ) -> None:
        self.formula : AtomicFormula = formula
        self.durative : bool = durative
        self.duration : Duration = duration if duration else Duration()
        self.condition : GoalDescriptor = condition if condition else GoalDescriptor()
        self.effect : Effect = effect if effect else Effect()

    # ======= #
    # cloning #
    # ======= #

    def copy(self) -> 'Operator':
        """
        Returns a deep copy of this operator.
        """
        return Operator(
            formula=self.formula.copy(),
            durative=self.durative,
            duration=self.duration.copy(),
            condition=self.condition.copy(),
            effect=self.effect.copy()
        )

    # ======== #
    # visiting #
    # ======== #

    def visit(self, visit_function : callable, valid_types : set[type] = None, args=(), kwargs={}):
        """
        Calls the visit function on self and recurses through the visit methods of members.
        param visit_function: the function to call on self.
        param valid_types: a set of types to visit. If None, all types are visited.
        """
        if valid_types is None or isinstance(self, valid_types):
            visit_function(self, *args, **kwargs)

        self.formula.visit(visit_function, valid_types, args, kwargs)
        self.duration.visit(visit_function, valid_types, args, kwargs)
        self.condition.visit(visit_function, valid_types, args, kwargs)
        self.effect.visit(visit_function, valid_types, args, kwargs)

    # ================== #
    # setters : duration #
    # ================== #

    def set_constant_duration(self, duration : float):
        lhs = ExprComposite([ExprBase(expr_type=ExprBase.ExprType.SPECIAL, special_type=ExprBase.SpecialType.DURATION)])
        rhs = ExprComposite([ExprBase(expr_type=ExprBase.ExprType.CONSTANT, constant=duration)])
        self.duration = DurationInequality(Inequality(comparison_type=Inequality.ComparisonType.EQUALS, lhs=lhs, rhs=rhs))

    # ==================== #
    # setters : conditions #
    # ==================== #

    def add_simple_condition_from_str(self, name : str,
                                            parameters : dict[str,str] = {},
                                            constants : dict[str,str] = {}, 
                                            time_spec : TimeSpec = TimeSpec.AT_START, 
                                            is_negative : bool = False
                                            ):
        """
        Adds a propositional condition from string using AtomicFormula.from_string()
        param name: the name of the predicate to add.
        param parameters: dictionary mapping label to type.
        param constants: dictionary mapping label to constant value.
        param time_spec: timing of condition, if durative action.
        param is_negative: True if the condition is a negative condition.
        """
        self.add_simple_condition(AtomicFormula.from_string(name, parameters, constants), time_spec, is_negative)

    def add_simple_condition(self, predicate : AtomicFormula, time_spec : TimeSpec = TimeSpec.AT_START, is_negative : bool = False):
        """
        Adds a propositional condition.
        If the operator already has a non-conjunctive condition then the new and existing
        conditions will be wrapped together within a new conjunctive condition.
        param predicate: the predicate to add.
        param time_spec: timing of condition, if durative action.
        param is_negative: True if the condition is a negative condition.
        """
        condition = GoalSimple(predicate)
        if is_negative: condition = GoalNegative(condition)
        if self.durative: condition = TimedGoal(time_spec, condition)
        if isinstance(self.condition, GoalConjunction):
            self.condition.goals.append(condition)
        elif self.condition.goal_type == GoalType.EMPTY:
            self.condition = condition
        else:
            self.condition = GoalConjunction(goals=[self.condition, condition])

    # ================= #
    # setters : effects #
    # ================= #

    def add_simple_effect_from_str(self, name : str,
                                        parameters : dict[str,str] = {},
                                        constants : dict[str,str] = {}, 
                                        time_spec : TimeSpec = TimeSpec.AT_START,
                                        is_delete : bool = False
                                        ):
        """
        Adds a propositional effect from string using AtomicFormula.from_string()
        param name: the name of the predicate to add.
        param parameters: dictionary mapping label to type.
        param constants: dictionary mapping label to constant value.
        param time_spec: timing of effect, if durative action.
        param is_delete: True if the effect is a delete effect.
        """
        self.add_simple_effect(AtomicFormula.from_string(name, parameters, constants), time_spec, is_delete)

    def add_simple_effect(self, predicate : AtomicFormula, time_spec : TimeSpec = TimeSpec.AT_START, is_delete : bool = False):
        """
        Adds a propositional effect.
        If the operator already has a non-conjunctive effect then the new and existing
        effects will be wrapped together within a new conjunctive effect.
        """
        effect = EffectNegative(predicate) if is_delete else EffectSimple(predicate)
        if self.durative: effect = TimedEffect(time_spec, effect)
        if self.effect.effect_type == EffectType.CONJUNCTION:
            self.effect : EffectConjunction
            self.effect.effects.append(effect)
        elif self.effect.effect_type == EffectType.EMPTY:
            self.effect = effect
        else:
            self.effect = EffectConjunction(effects=[self.effect, effect])

    def add_assign_effect_from_str(self, name : str,
                                        parameters : dict[str,str] = {},
                                        constants : dict[str,str] = {}, 
                                        time_spec : TimeSpec = TimeSpec.AT_START,
                                        assign_type : AssignmentType = AssignmentType.ASSIGN,
                                        value : float = 1.0
                                        ):
        """
        Adds a numeric effect from string using AtomicFormula.from_string()
        param name: the name of the predicate to add.
        param parameters: dictionary mapping label to type.
        param constants: dictionary mapping label to constant value.
        param time_spec: timing of effect, if durative action.
        param assign_type: the type of numeric assignment (assign, increase, decrease, etc)
        param value: The amount to be applied.
        """
        self.add_assign_effect(AtomicFormula.from_string(name, parameters, constants), time_spec, assign_type, value)

    def add_assign_effect(self, function : AtomicFormula,
                                time_spec : TimeSpec = TimeSpec.AT_START,
                                assign_type : AssignmentType = AssignmentType.ASSIGN,
                                value : float = 1.0):
        """
        Adds a numeric effect.
        If the operator already has a non-conjunctive effect then the new and existing
        effects will be wrapped together within a new conjunctive effect.
        """
        value_expr = ExprComposite([ExprBase(expr_type=ExprBase.ExprType.CONSTANT, constant=value)])
        effect = Assignment(assign_type, function, value_expr)
        if self.durative: effect = TimedEffect(time_spec, effect)
        if self.effect.effect_type == EffectType.CONJUNCTION:
            self.effect : EffectConjunction
            self.effect.effects.append(effect)
        elif self.effect.effect_type == EffectType.EMPTY:
            self.effect = effect
        else:
            self.effect = EffectConjunction(effects=[self.effect, effect])

    # ======== #
    # printing #
    # ======== #

    def __str__(self) -> str:
        # TODO checking for empty parameters and conditions
        return ("(durative-action " if self.durative else "(action ") \
                + self.formula.name + "\n" \
                + "  :parameters (" + self.formula.print_pddl(include_types=True).partition(' ')[2][:-1] + ")\n" \
                + ("  :duration " + str(self.duration) + "\n" if self.durative else "") \
                + ("  :condition " if self.durative else "  :precondition ") \
                + str(self.condition) + "\n" \
                + "  :effect " \
                + str(self.effect) + "\n" \
                + ")"
    
    def print_pddl(self) -> str:
        return self.formula.print_pddl(include_types=False)

    # ========= #
    # grounding #
    # ========= #
    
    def bind_parameters(self, parameters : list[TypedParameter]) -> 'Operator':
        """
        parameters: list of TypedParameter whose type and label must match the type and label of the operator.
        returns a copy of the operator whose conditions and effects have been grounded with the given values.
        """
        return Operator(
            self.formula.bind_parameters(parameters),
            durative=self.durative,
            duration=self.duration.bind_parameters(parameters),
            condition=self.condition.bind_parameters(parameters),
            effect=self.effect.bind_parameters(parameters)
        )