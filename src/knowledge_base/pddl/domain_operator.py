from typing import List
from domain_formula import DomainFormula
from domain_assignment import DomainAssignment
from domain_inequality import DomainInequality
from probabilistic_effect import ProbabilisticEffect


class DomainOperator:
    """ 
    A class used to represent an operator in the domain.
    """

    def __init__(self,
            # header
            formula  : DomainFormula,
            duration : DomainInequality,

            # simple conditions
            at_start_simple_condition  : List[DomainFormula] = [],
            over_all_simple_condition  : List[DomainFormula] = [],
            at_end_simple_condition  : List[DomainFormula] = [],
            at_start_neg_condition  : List[DomainFormula] = [],
            over_all_neg_condition  : List[DomainFormula] = [],
            at_end_neg_condition  : List[DomainFormula] = [],

            # numeric conditions
            at_start_comparison : List[DomainInequality] = [],
            at_end_comparison : List[DomainInequality] = [],
            over_all_comparison : List[DomainInequality] = [],

            # simple effects
            at_start_add_effects : List[DomainFormula] = [],
            at_start_del_effects : List[DomainFormula] = [],
            at_end_add_effects : List[DomainFormula] = [],
            at_end_del_effects : List[DomainFormula] = [],

            # numeric effects
            at_start_assign_effects : List[DomainAssignment] = [],
            at_end_assign_effects : List[DomainAssignment] = [],
            continuous_numeric_effects : List[DomainAssignment] = [],

            # probabilistic effects
            probabilistic_effects : List[ProbabilisticEffect] = []
            ) -> None:
        
        # TODO assert duration includes "?duration" special type.
        self.formula = formula
        self.duration = duration
        self.at_start_simple_condition = at_start_simple_condition
        self.over_all_simple_condition = over_all_simple_condition
        self.at_end_simple_condition = at_end_simple_condition
        self.at_start_neg_condition = at_start_neg_condition
        self.over_all_neg_condition = over_all_neg_condition
        self.at_end_neg_condition = at_end_neg_condition
        self.at_start_comparison = at_start_comparison
        self.at_end_comparison = at_end_comparison
        self.over_all_comparison = over_all_comparison
        self.at_start_add_effects = at_start_add_effects
        self.at_start_del_effects = at_start_del_effects
        self.at_end_add_effects = at_end_add_effects
        self.at_end_del_effects = at_end_del_effects
        self.at_start_assign_effects = at_start_assign_effects
        self.at_end_assign_effects = at_end_assign_effects
        self.continuous_numeric_effects = continuous_numeric_effects
        self.probabilistic_effects = probabilistic_effects

    def __str__(self) -> str:
        # TODO checking for empty parameters and conditions
        return "(durative-action " + self.formula.name + "\n" \
                + "  :parameters (" + str(self.formula).partition()[1] + ")\n" \
                + "  :duration " + str(self.duration) + "\n" \
                + "  :condition (and\n" \
                + "    " + "\n".join(["(at start " + c + ")" for c in self.at_start_simple_condition]) + "\n" \
                + "    " + "\n".join(["(at start (not " + c + "))" for c in self.at_start_neg_condition]) + "\n" \
                + "    " + "\n".join(["(over all " + c + ")" for c in self.over_all_simple_condition]) + "\n" \
                + "    " + "\n".join(["(over all (not " + c + "))" for c in self.over_all_neg_condition]) + "\n" \
                + "    " + "\n".join(["(at end " + c + ")" for c in self.at_end_simple_condition]) + "\n" \
                + "    " + "\n".join(["(at end (not " + c + "))" for c in self.at_end_neg_condition]) + "\n" \
                + "    " + "\n".join(["(at start " + c + ")" for c in self.at_start_comparison]) + "\n" \
                + "    " + "\n".join(["(over all " + c + ")" for c in self.over_all_comparison]) + "\n" \
                + "    " + "\n".join(["(at end " + c + ")" for c in self.at_end_comparison]) + "\n" \
                + "  )\n" \
                + "  :effect (and\n" \
                + "    " + "\n".join(["(at start " + e + ")" for e in self.at_start_add_effects]) + "\n" \
                + "    " + "\n".join(["(at start (not " + e + "))" for e in self.at_start_del_effects]) + "\n" \
                + "    " + "\n".join(["(at end " + e + ")" for e in self.at_end_add_effects]) + "\n" \
                + "    " + "\n".join(["(at end (not " + e + "))" for e in self.at_end_del_effects]) + "\n" \
                + "    " + "\n".join(["(at start " + e + ")" for e in self.at_start_assign_effects]) + "\n" \
                + "    " + "\n".join(["(at end " + e + ")" for e in self.at_end_assign_effects]) + "\n" \
                + "    " + "\n".join([e for e in self.continuous_numeric_effects]) + "\n" \
                + "  )\n" \
                + ")"
    

