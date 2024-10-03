import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
from simpful import *
import streamlit as st

class InferenceSystem:
    def __init__(self, linguistic_variables, rules, defuzzification_method='centroid'):
        self.linguistic_variables = linguistic_variables
        self.rules = rules
        self.defuzzification_method = defuzzification_method
        self.ctrl_system = None
        self.ctrl_simulation = None


        self.consequents = None

    def build_system(self):
        antecedents = {}
        consequents = {}
        # print(st.session_state.linguistic_variables)
        for lv in self.linguistic_variables:
            if lv.name in [rule.consequent[0] for rule in self.rules]:
                consequents[lv.name] = ctrl.Consequent(np.arange(lv.range_min, lv.range_max, 0.1), lv.name)
            else:
                antecedents[lv.name] = ctrl.Antecedent(np.arange(lv.range_min, lv.range_max, 0.1), lv.name)

            for term_name, (mf_type, mf_params) in lv.get_terms().items():
                if mf_type == 'triangular':
                    mf_function = fuzz.trimf
                    mf_function_sugeno = Triangular_MF
                elif mf_type == 'trapezoidal':
                    mf_function = fuzz.trapmf
                    mf_function_sugeno = Trapezoidal_MF
                elif mf_type == 'gaussian':
                    mf_function = lambda x, params: fuzz.gaussmf(x, params[0], params[1])
                    mf_function_sugeno = Gaussian_MF
                elif mf_type == 'sigmoid':
                    mf_function = lambda x, params: fuzz.sigmf(x, params[0], params[1])
                    mf_function_sugeno = Sigmoid_MF
                else:
                    raise ValueError(f"Unsupported membership function type: {mf_type}")

                if lv.name in antecedents:
                    antecedents[lv.name][term_name] = mf_function(antecedents[lv.name].universe, mf_params)
                else:
                    consequents[lv.name][term_name] = mf_function(consequents[lv.name].universe, mf_params)

        ctrl_rules = []
        for rule in self.rules:
            antecedent_terms = [antecedents[var][term] for var, term in rule.antecedents]
            consequent_term = consequents[rule.consequent[0]][rule.consequent[1]]
            
            if rule.operation == "AND":
                antecedent = antecedent_terms[0]
                for term in antecedent_terms[1:]:
                    antecedent = antecedent & term
            elif rule.operation == "OR":
                antecedent = antecedent_terms[0]
                for term in antecedent_terms[1:]:
                    antecedent = antecedent | term
            else:
                raise ValueError(f"Unsupported operation: {rule.operation}")
            
            ctrl_rules.append(ctrl.Rule(antecedent, consequent_term))


            # Note: Rule weight is not applied due to limitations in the skfuzzy API
        self.consequents = consequents
        self.ctrl_system = ctrl.ControlSystem(ctrl_rules)
        self.ctrl_simulation = ctrl.ControlSystemSimulation(self.ctrl_system)

    def compute(self, inputs):
        if not self.ctrl_simulation:
            raise ValueError("Inference system not built. Call build_system() first.")

        for var_name, value in inputs.items():
            self.ctrl_simulation.input[var_name] = value

        self.ctrl_simulation.compute()

        # Apply rule weights manually
        # weighted_outputs = {}
        # for var_name in self.ctrl_simulation.output:
        #     total_weight = sum(rule.weight for rule in self.rules if rule.consequent[0] == var_name)
        #     weighted_sum = sum(rule.weight * self.ctrl_simulation.output[var_name] for rule in self.rules if rule.consequent[0] == var_name)
        #     weighted_outputs[var_name] = weighted_sum / total_weight if total_weight > 0 else self.ctrl_simulation.output[var_name]

        return self.ctrl_simulation
