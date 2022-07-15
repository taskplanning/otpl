import numpy as np
from pddl.atomic_formula import AtomicFormula, TypedParameter
from pddl.domain import Domain
from pddl.effect import Effect, EffectType
from pddl.goal_descriptor import GoalDescriptor, GoalType, TimedGoal
from pddl.operator import Operator
from pddl.problem import Problem
from pddl.symbol_table import SymbolTable
from pddl.time_spec import TimeSpec


class Grounding:

    def __init__(self):

        self.domain  : Domain  = None
        self.problem : Problem = None

        # symbol tables for domain and problem
        self.operator_table = SymbolTable()
        self.predicate_table = SymbolTable()
        self.function_table = SymbolTable()
        self.type_symbol_tables : dict[str, SymbolTable] = {}

        # true if the problem has been grounded
        self.grounded = False

        # beginning ID of each symbol
        self.predicate_heads = {}
        self.function_heads = {}
        self.operator_heads = {}

        # total counts
        self.last_symbol_count = 0 
        self.proposition_count = 0
        self.function_count = 0
        self.action_count = 0

        # number of objects and constants of each type
        self.type_counts = {}

        # cached spike representations of action effects and conditions
        self.action_add_effect_spikes = {}
        self.action_del_effect_spikes = {}
        self.action_condition_spikes = {}
        self.action_negative_condition_spikes = {}

    #======================#
    # Setting heads values #
    #======================#

    def prepare_symbol_tables(self, domain : Domain, problem : Problem):

        for name, _ in domain.operators.items():
            self.operator_table.add_symbol(name)
        for name, _ in domain.predicates.items():
            self.predicate_table.add_symbol(name)
        for name, _ in domain.functions.items():
            self.function_table.add_symbol(name)
        for type in domain.type_tree.keys():
            self.type_symbol_tables[type] = SymbolTable()
            # TODO replace with map
            for obj in problem.type_objects_map[type]:
                self.type_symbol_tables[type].add_symbol(obj)
            for obj in domain.type_constants_map[type]:
                self.type_symbol_tables[type].add_symbol(obj)

    def ground_problem(self, domain : Domain, problem : Problem):

        if self.grounded:
            return

        self.domain = domain
        self.problem = problem

        self.grounded = True
        self.ground_object_list()
        self.ground_symbol_list(self.predicate_table, self.domain.predicates, self.predicate_heads)
        self.proposition_count = self.last_symbol_count
        self.ground_symbol_list(self.function_table, self.domain.functions, self.function_heads)
        self.function_count = self.last_symbol_count
        op_formulae = { op.formula.name: op.formula for op in domain.operators.values() }
        self.ground_symbol_list(self.operator_table, op_formulae, self.operator_heads)
        self.action_count = self.last_symbol_count

    def ground_object_list(self):
        self.type_counts["object"] = len(self.problem.objects_type_map) + len(self.domain.constants_type_map)
        for type in self.domain.type_tree.keys():
            self.type_counts[type] = len(self.type_symbol_tables[type].symbol_list)

    def ground_symbol_list(self, symbol_table : SymbolTable, formulae : dict[str, AtomicFormula], heads : dict[str, int]):
        head = 0
        for name in symbol_table.symbol_list:
            ground_formulae = 0
            for param in formulae[name].typed_parameters:
                type = param.type
                count = len(self.type_symbol_tables[type].symbol_list) if type in self.type_symbol_tables else 0
                if ground_formulae == 0:
                    ground_formulae = count
                else:
                    ground_formulae = ground_formulae * count
                # no objects can bind to this parameter so there are no ground symbols
                if count==0: break
            # special case for formula with no parameters
            if len(formulae[name].typed_parameters)==0:
                ground_formulae = 1
            heads[name] = (head, head + ground_formulae)
            self.last_symbol_count = head + ground_formulae
            head = head + ground_formulae
    
    #====================#
    # Get ID from object #
    #====================#

    def get_id_from_proposition(self, formula : AtomicFormula) -> int:
        id = self.predicate_heads[formula.name][0]
        id += self.get_id_from_parameters(formula.typed_parameters)
        return id

    def get_id_from_pne(self, formula : AtomicFormula) -> int:
        id = self.function_heads[formula.name][0]
        id += self.get_id_from_parameters(formula.typed_parameters)
        return id

    def get_id_from_action_formula(self, formula : AtomicFormula) -> int:
        id = self.operator_heads[formula.name][0]
        id += self.get_id_from_parameters(formula.typed_parameters)
        return id

    def get_id_from_action(self, action : Operator) -> int:
        return self.get_id_from_action_formula(action.formula)

    def get_id_from_parameters(self, params : list[TypedParameter]) -> int:
        id = 0
        obj_count = 1
        for param in params[::-1]:
            obj_count = self.type_counts[param.type]
            id = id * obj_count + self.type_symbol_tables[param.type].get_symbol_id(param.value)
        return id

    #=====================#
    # Get objects from ID #
    #=====================#

    def get_proposition_from_id(self, id : int) -> AtomicFormula:
        for name in self.predicate_heads:
            if self.predicate_heads[name][0] <= id and id < self.predicate_heads[name][1]:
                id = id - self.predicate_heads[name][0]
                params = self.domain.predicates[name].typed_parameters
                return AtomicFormula(name, self.get_parameters_from_id(id, params), True)

    def get_pne_from_id(self, id : int) -> AtomicFormula:
        for name in self.function_heads:
            if self.function_heads[name][0] <= id and id < self.function_heads[name][1]:
                id = id - self.function_heads[name][0]
                params = self.domain.functions[name].typed_parameters
                return AtomicFormula(name, self.get_parameters_from_id(id, params), True)

    def get_action_from_id(self, id : int) -> AtomicFormula:
        for name in self.operator_heads:
            if self.operator_heads[name][0] <= id and id < self.operator_heads[name][1]:
                id = id - self.operator_heads[name][0]
                op_params = self.domain.operators[name].formula.typed_parameters
                params = self.get_parameters_from_id(id, op_params)
                op = self.domain.operators[name].bind_parameters(params)
                return op

    def get_parameters_from_id(self, id : int, params : list[TypedParameter]) -> list[TypedParameter]:
        ground_parameters = []
        for param in params:
            obj_count = self.type_counts[param.type]
            param_id = id % obj_count
            value  = self.type_symbol_tables[param.type].get_symbol(param_id)
            id = id // obj_count
            ground_parameters.append(TypedParameter(param.type, param.label, value))
        return ground_parameters


    #===============#
    # spike methods #
    #===============#

    def get_initial_state_spike(self):
        """
        return numpy array of propositional initial state
        """
        if not self.grounded:
            return None

        init_spike = np.zeros(self.proposition_count, dtype=np.bool)
        init_spike[[ self.get_id_from_proposition(p) for p in self.problem.propositions ]] = True
        return init_spike

    def get_action_condition_spike_from_id(self, id : int, time_spec : TimeSpec = TimeSpec.AT_START) -> tuple[np.ndarray]:
        """
        Returns positive and negative spikes for the action condition, first returning the cached spike if it exists.
        If not, it will create a new spike and cache it.
        return numpy array of propositional action conditions.
        """
        if (id, time_spec) in self.action_condition_spikes and (id, time_spec) in self.action_negative_condition_spikes:
            return self.action_condition_spikes[(id, time_spec)], self.action_negative_condition_spikes[(id, time_spec)]
        else:
            action = self.get_action_from_id(id)
            pos, neg = self.get_action_condition_spike(action, time_spec)
            self.action_condition_spikes[(id, time_spec)] = pos
            self.action_negative_condition_spikes[(id, time_spec)] = neg
            return pos, neg

    def get_action_condition_spike(self, action : Operator, time_spec : TimeSpec = TimeSpec.AT_START) -> tuple[np.ndarray]:
        """
        return tuple of numpy arrays, one positive and one negative propositional precondition.
        Only looks at simple and negative conditions.
        """
        if not self.grounded:
            return None

        positive_conditions = np.zeros(self.proposition_count, dtype=np.bool)
        negative_conditions = np.zeros(self.proposition_count, dtype=np.bool)
        self.get_simple_conditions(action.condition, positive_conditions, negative_conditions, time_spec)
        return positive_conditions, negative_conditions

    def get_simple_conditions(self, condition : GoalDescriptor,
                                    positive_conditions : np.ndarray,
                                    negative_conditions : np.ndarray,
                                    time_spec : TimeSpec = TimeSpec.AT_START,
                                    is_negative : bool = False) -> None:
        """
        Sets the values of the positive_conditions and negative_conditions arrays to True
        for each simple condition in the conditions.
        """
        if condition.goal_type == GoalType.SIMPLE:
            id = self.get_id_from_proposition(condition.atomic_formula)
            if is_negative: 
                negative_conditions[id] = True
            else:
                positive_conditions[id] = True
        elif condition.goal_type == GoalType.NEGATIVE:
            self.get_simple_conditions(condition.goal, positive_conditions, negative_conditions, time_spec, not is_negative)
        elif condition.goal_type == GoalType.CONJUNCTION:
            for c in condition.goals:
                self.get_simple_conditions(c, positive_conditions, negative_conditions, time_spec)
        elif condition.goal_type == GoalType.TIMED:
            if condition.time_spec == time_spec:
                self.get_simple_conditions(condition.goal, positive_conditions, negative_conditions, time_spec)
        else:
            # comparison, disjunction, implication, universal, existential, and empty
            return

    def get_action_effect_spike_from_id(self, id : int, time_spec : TimeSpec = TimeSpec.AT_START) -> tuple[np.ndarray]:
        """
        Returns positive and negative spikes for the action effect, first returning the cached spike if it exists.
        If not, it will create a new spike and cache it.
        return numpy array of propositional action simple effects.
        """
        if (id, time_spec) in self.action_add_effect_spikes and (id, time_spec) in self.action_del_effect_spikes:
            return self.action_add_effect_spikes[(id, time_spec)], self.action_del_effect_spikes[(id, time_spec)]
        else:
            action = self.get_action_from_id(id)
            pos, neg = self.get_action_effect_spike(action, time_spec)
            self.action_add_effect_spikes[(id, time_spec)] = pos
            self.action_del_effect_spikes[(id, time_spec)] = neg
            return pos, neg

    def get_action_effect_spike(self, action : Operator, time_spec : TimeSpec = TimeSpec.AT_START) -> tuple[np.ndarray]:      
        """
        return tuple of numpy arrays, one adding and one deleting propositional effect.
        """
        if not self.grounded:
            return None

        positive_effects = np.zeros(self.proposition_count, dtype=np.bool)
        negative_effects = np.zeros(self.proposition_count, dtype=np.bool)
        self.get_simple_effects(action.effect, positive_effects, negative_effects, time_spec)
        return positive_effects, negative_effects  

    def get_simple_effects(self, effect : Effect,
                                positive_effects : np.ndarray,
                                negative_effects : np.ndarray,
                                time_spec : TimeSpec = TimeSpec.AT_START) -> None:
        """
        Sets the values of the positive_effects and negative_effects arrays to True
        for each simple effect in the effect.
        """
        if effect.effect_type == EffectType.SIMPLE:
            id = self.get_id_from_proposition(effect.formula)
            positive_effects[id] = True
        elif effect.effect_type == EffectType.NEGATIVE:
            id = self.get_id_from_proposition(effect.formula)
            negative_effects[id] = True
        elif effect.effect_type == EffectType.CONJUNCTION:
            for e in effect.effects:
                self.get_simple_effects(e, positive_effects, negative_effects, time_spec)
        elif effect.effect_type == EffectType.TIMED:
            if effect.time_spec == time_spec:
                self.get_simple_effects(effect.effect, positive_effects, negative_effects, time_spec)
        else:
            # forall, numeric, continuous, conditional, and empty
            return