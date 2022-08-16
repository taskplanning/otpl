import numpy as np

from pddl.atomic_formula import AtomicFormula, TypedParameter
from pddl.domain import Domain
from pddl.effect import Effect, EffectType
from pddl.goal_descriptor import GoalDescriptor, GoalType
from pddl.operator import Operator
from pddl.state import State
from pddl.symbol_table import SymbolTable
from pddl.time_spec import TimeSpec
from pddl.timed_initial_literal import TimedInitialLiteral

class Grounding:

    def __init__(self):

        self.domain  : Domain  = None

        # symbol tables for domain and problem
        self.operator_table  : SymbolTable = SymbolTable()
        self.predicate_table : SymbolTable = SymbolTable()
        self.function_table  : SymbolTable = SymbolTable()
        self.type_symbol_tables : dict[str, SymbolTable] = {}

        # true if the problem has been grounded
        self.grounded = False

        # beginning ID of each symbol
        self.predicate_heads : dict[str,int] = {}
        self.function_heads : dict[str,int] = {}
        self.operator_heads : dict[str,int] = {}

        # total counts
        self.last_symbol_count : int = 0 
        self.proposition_count : int  = 0
        self.function_count : int  = 0
        self.action_count : int  = 0

        # number of objects and constants of each type
        self.type_counts : dict[str,int] = {}

        # cached spike representations of action effects and conditions
        self.action_add_effect_spikes = {}
        self.action_del_effect_spikes = {}
        self.action_positive_condition_spikes = {
            TimeSpec.AT_START : {},
            TimeSpec.OVER_ALL : {},
            TimeSpec.AT_END : {}
        }
        self.action_negative_condition_spikes = {
            TimeSpec.AT_START : {},
            TimeSpec.OVER_ALL : {},
            TimeSpec.AT_END : {}
        }

        # static predicates
        self.statics = {}
        self.static_offset = 0

        # mutexes
        self.action_mutexes = None
        self.proposition_mutexes = None

    #======================#
    # Setting heads values #
    #======================#

    def ground_problem(self, domain : Domain, problem):

        if self.grounded:
            return
        self.grounded = True

        self.domain = domain

        # determine which predicates are static
        self.check_static_predicates()

        # create tables for mapping labels to ids
        self.prepare_symbol_tables(domain, problem)

        # map labels to ids
        self.ground_object_list(problem)

        # map labels to ids for predicates and functions
        self.ground_symbol_list(self.predicate_table, self.domain.predicates, self.predicate_heads)
        self.proposition_count = self.last_symbol_count
        self.ground_symbol_list(self.function_table, self.domain.functions, self.function_heads)
        self.function_count = self.last_symbol_count
        
        # map labels to ids for operators
        op_formulae = { op.formula.name: op.formula for op in domain.operators.values() }
        self.ground_symbol_list(self.operator_table, op_formulae, self.operator_heads)
        self.action_count = self.last_symbol_count

    def prepare_symbol_tables(self, domain : Domain, problem):
        # create symbol tables for predicates, ordering statics first
        for name, _ in domain.predicates.items():
            if self.statics[name]:
                self.predicate_table.add_symbol(name)
        for name, _ in domain.predicates.items():
            if not self.statics[name]:
                self.predicate_table.add_symbol(name)
        # prepare symbol tables for operatorsand functions
        for name, _ in domain.operators.items():
            self.operator_table.add_symbol(name)
        for name, _ in domain.functions.items():
            self.function_table.add_symbol(name)
        self.type_symbol_tables["object"] = SymbolTable()
        for type in domain.type_tree.keys():
            self.type_symbol_tables[type] = SymbolTable()
        for type in domain.type_tree.keys():
            if type in problem.type_objects_map:
                for obj in problem.type_objects_map[type]:
                    self.update_type_symbol_table(obj, type)
            if type in domain.constants_type_map:
                for obj in domain.constants_type_map[type]:
                    self.update_type_symbol_table(obj, type)

    def update_type_symbol_table(self, obj_name : str, obj_type : str):
        self.type_symbol_tables[obj_type].add_symbol(obj_name)
        if obj_type in self.domain.type_tree:
            self.update_type_symbol_table(obj_name, self.domain.type_tree[obj_type].parent)

    def ground_object_list(self, problem):
        self.type_counts["object"] = len(problem.objects_type_map) + len(self.domain.constants_type_map)
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
            if name in self.statics and self.statics[name]:
                self.static_offset = self.last_symbol_count
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
                return AtomicFormula(name, self.get_parameters_from_id(id, params))

    def get_pne_from_id(self, id : int) -> AtomicFormula:
        for name in self.function_heads:
            if self.function_heads[name][0] <= id and id < self.function_heads[name][1]:
                id = id - self.function_heads[name][0]
                params = self.domain.functions[name].typed_parameters
                return AtomicFormula(name, self.get_parameters_from_id(id, params))

    def get_action_from_id(self, id : int) -> Operator:
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

    # ======== #
    # analysis #
    # ======== #

    def check_static_predicates(self):
        self.statics = {p : True for p in self.domain.predicates.keys()}
        for operator in self.domain.operators.values():
            for p in self.statics.keys():
                if self.effect_affects_predicate(operator.effect, p):
                    self.statics[p] = False
    
    def effect_affects_predicate(self, effect : Effect, predicate : str) -> bool:
        if effect.effect_type == EffectType.CONJUNCTION:
            for e in effect.effects:
                if self.effect_affects_predicate(e, predicate):
                    return True
            return False
        elif effect.effect_type == EffectType.FORALL or \
             effect.effect_type == EffectType.CONDITIONAL or \
             effect.effect_type == EffectType.TIMED:
            return self.effect_affects_predicate(effect.effect, predicate)
        elif effect.effect_type == EffectType.SIMPLE or \
             effect.effect_type == EffectType.NEGATIVE:
            return predicate == effect.formula.name
        return False   

    def compute_action_mutexes(self, actions : np.ndarray):
        """
        Compute mutexes for selected actions through brute force.
        TODO replace this with fast/graphplan implementation.
        param actions: array of type bool indicating which action IDs to check, e.g. only reachable actions.
        """
        self.action_mutexes = np.zeros((self.action_count,self.action_count), dtype=bool)
        for action_id in np.nonzero(actions)[0]:
            action = self.get_action_from_id(action_id)
            for other_id in np.nonzero(actions)[0]:
                if other_id <= action_id: continue
                other = self.get_action_from_id(other_id)
                if self.check_actions_mutex(action, other):
                    self.action_mutexes[action_id, other_id] = True
                    self.action_mutexes[other_id, action_id] = True

    def check_actions_mutex(self, action : Operator, other : Operator) -> bool:
        """
        Check interference between two actions. Actions interfere if they have conflicting effects, 
        of one action affects the other's preconditions.
        """
        # interference between effects
        oth_add_effect, oth_del_effect = self.get_simple_action_effect(other)
        act_add_effect, act_del_effect = self.get_simple_action_effect(action)
        if np.any(np.logical_and(act_add_effect, oth_del_effect)): return True
        if np.any(np.logical_and(act_del_effect, oth_add_effect)): return True

        # interference with action precondition
        act_pos_condition, act_neg_condition = self.get_simple_action_condition(action)
        if np.any(np.logical_and(act_pos_condition, oth_del_effect)): return True
        if np.any(np.logical_and(act_neg_condition, oth_add_effect)): return True

        # interference with other precondition
        oth_pos_condition, oth_neg_condition = self.get_simple_action_condition(other)
        if np.any(np.logical_and(oth_pos_condition, act_del_effect)): return True
        if np.any(np.logical_and(oth_neg_condition, act_add_effect)): return True

        return False


    # ======================================== #
    # get propositional conditions and effects #
    # ======================================== #

    def get_simple_action_condition_from_id(self, id : int, time_spec : TimeSpec = TimeSpec.AT_START) -> tuple[np.ndarray]:
        """
        Returns positive and negative spikes for the action condition, first returning the cached spike if it exists.
        If not, it will create a new spike and cache it.
        return numpy array of propositional action conditions.
        """
        if id in self.action_positive_condition_spikes[time_spec] and id in self.action_negative_condition_spikes[time_spec]:
            return self.action_positive_condition_spikes[time_spec][id], self.action_negative_condition_spikes[time_spec][id]
        else:
            action = self.get_action_from_id(id)
            pos, neg = self.get_simple_action_condition(action, time_spec)
            self.action_positive_condition_spikes[time_spec][id] = pos
            self.action_negative_condition_spikes[time_spec][id] = neg
            return pos, neg

    def get_simple_action_condition(self, action : Operator, time_spec : TimeSpec = TimeSpec.AT_START) -> tuple[np.ndarray]:
        """
        return tuple of numpy arrays, one positive and one negative propositional precondition.
        Only looks at simple and negative conditions.
        """
        if not self.grounded:
            return None

        positive_conditions = np.zeros(self.proposition_count, dtype=bool)
        negative_conditions = np.zeros(self.proposition_count, dtype=bool)
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

    def get_simple_action_effect_from_id(self, id : int, time_spec : TimeSpec = TimeSpec.AT_START) -> tuple[np.ndarray]:
        """
        Returns positive and negative spikes for the action effect, first returning the cached spike if it exists.
        If not, it will create a new spike and cache it.
        return numpy array of propositional action simple effects.
        """
        if (id, time_spec) in self.action_add_effect_spikes and (id, time_spec) in self.action_del_effect_spikes:
            return self.action_add_effect_spikes[(id, time_spec)], self.action_del_effect_spikes[(id, time_spec)]
        else:
            action = self.get_action_from_id(id)
            pos, neg = self.get_simple_action_effect(action, time_spec)
            self.action_add_effect_spikes[(id, time_spec)] = pos
            self.action_del_effect_spikes[(id, time_spec)] = neg
            return pos, neg

    def get_simple_action_effect(self, action : Operator, time_spec : TimeSpec = TimeSpec.AT_START) -> tuple[np.ndarray]:      
        """
        return tuple of numpy arrays, one adding and one deleting propositional effect.
        """
        if not self.grounded:
            return None

        positive_effects = np.zeros(self.proposition_count, dtype=bool)
        negative_effects = np.zeros(self.proposition_count, dtype=bool)
        self.get_simple_effects(action.effect, positive_effects, negative_effects, time_spec)
        return positive_effects, negative_effects  

    def get_simple_til_effect(self, til : TimedInitialLiteral) -> tuple[np.ndarray]:      
        """
        return tuple of numpy arrays, one adding and one deleting propositional effect.
        """
        if not self.grounded:
            return None

        positive_effects = np.zeros(self.proposition_count, dtype=bool)
        negative_effects = np.zeros(self.proposition_count, dtype=bool)
        self.get_simple_effects(til.effect, positive_effects, negative_effects)
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
    
    #======================#
    # state helper methods #
    #======================#

    def check_simple_conditions(self, action_id : int, state : State, time_spec : TimeSpec = TimeSpec.AT_START) -> bool:
        """
        Checks if the action's simple conditions are satisfied in the given state.
        param action_id: the id of the action to check.
        param state: numpy array of boolean values representing the logical part of the state.
        """
        pos, neg = self.get_simple_action_condition_from_id(action_id, time_spec)
        # check positive preconditions
        if np.any(np.logical_xor(pos, np.logical_and(state.logical, pos))):
            return False
        # check negative preconditions
        if np.any(np.logical_and(state.logical, neg)):
            return False
        return True

    def apply_simple_action_effects(self, action_id : int, state : State, time_spec : TimeSpec = TimeSpec.AT_START) -> None:
        """
        Apply the propositional effects of the action to the logical state.
        """
        adds, dels = self.get_simple_action_effect_from_id(action_id, time_spec)
        np.logical_xor(state.logical, np.logical_and(state.logical, dels), out=state.logical)
        np.logical_or(state.logical, adds, out=state.logical)
    
    def apply_simple_til_effects(self, til : TimedInitialLiteral, state : State) -> None:
        """
        Apply the propositional effects of the action to the logical state.
        """
        adds, dels = self.get_simple_til_effect(til)
        np.logical_xor(state.logical, np.logical_and(state.logical, dels), out=state.logical)
        np.logical_or(state.logical, adds, out=state.logical)

    def check_simple_goal(self, state : State, goal : GoalDescriptor) -> bool:
        """
        Checks if the simple goal true in the state.
        param state: numpy array of boolean values representing the logical part of the state.
        """
        positive_conditions = np.zeros(self.proposition_count, dtype=bool)
        negative_conditions = np.zeros(self.proposition_count, dtype=bool)
        self.get_simple_conditions(goal, positive_conditions, negative_conditions)
        for id in np.nonzero(positive_conditions)[0]:
            if not state.logical[id]: return False
        for id in np.nonzero(negative_conditions)[0]:
            if state.logical[id]: return False
        return True