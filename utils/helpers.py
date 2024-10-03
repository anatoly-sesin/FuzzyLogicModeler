import streamlit as st
import json
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
#from ..fuzzy_logic.linguistic_variable import LinguisticVariable
from fuzzy_logic.linguistic_variable import LinguisticVariable
from fuzzy_logic.fuzzy_rule import FuzzyRule

def create_unique_key(base_key, index):
    return f"{base_key}_{index}"

def check_new_params(mf_type, range_min, range_max, params):
    if mf_type == "triangular":
        return range_min <= params[0] <= params[1] <= params[2] <= range_max
    elif mf_type == "trapezoidal":
        return range_min <= params[0] <= params[1] <= params[2] <= params[3] <= range_max
    elif mf_type == "gaussian":
        return True #["mean", "standard_deviation"]
    elif mf_type == "sigmoid":
        return True #["a", "c"]
    else:
        return True #[]

def get_membership_function_params(mf_type):
    if mf_type == "triangular":
        return ["a", "b", "c"]
    elif mf_type == "trapezoidal":
        return ["a", "b", "c", "d"]
    elif mf_type == "gaussian":
        return ["mean", "standard_deviation"]
    elif mf_type == "sigmoid":
        return ["a", "c"]
    else:
        return []

def display_membership_function_inputs(mf_type, key_prefix, initial_values=None):
    params = get_membership_function_params(mf_type)
    values = []
    cols = st.columns(len(params))
    for i, param in enumerate(params):
        default_value = initial_values[i] if initial_values and i < len(initial_values) else 0.0
        with cols[i]:
            value = st.number_input(f"{param}:", value=default_value, key=create_unique_key(f"{key_prefix}_{param}", i))
            values.append(value)
    return values

def get_linguistic_variable_by_name(name):
    for lv in st.session_state.linguistic_variables:
        if lv.name == name:
            return lv
    return None

def export_fuzzy_system():
    export_data = {
        "linguistic_variables": [],
        "fuzzy_rules": []
    }

    for lv in st.session_state.linguistic_variables:
        lv_data = {
            "name": lv.name,
            "range_min": lv.range_min,
            "range_max": lv.range_max,
            "variable_type": lv.variable_type,
            "terms": lv.terms
        }
        export_data["linguistic_variables"].append(lv_data)

    for rule in st.session_state.fuzzy_rules:
        rule_data = {
            "antecedents": rule.antecedents,
            "consequent": rule.consequent,
            "weight": rule.weight,
            "operation": rule.operation
        }
        export_data["fuzzy_rules"].append(rule_data)

    return json.dumps(export_data, indent=2)

def import_fuzzy_system(data):
    if not data['linguistic_variables']:
        return
    st.session_state.linguistic_variables = []
    for lv_data in data['linguistic_variables']:
        st.session_state.linguistic_variables.append(LinguisticVariable(
            lv_data['name'], float(lv_data['range_min']), float(lv_data['range_max']), lv_data['variable_type']
        ))
        variable = st.session_state.linguistic_variables[-1]
        for name, value in lv_data['terms'].items():
            variable.add_term(name, value[0], value[-1])
    
    st.session_state.fuzzy_rules = []
    if data['fuzzy_rules']:
        for rule_data in data['fuzzy_rules']:
            antecedents = [tuple(elem) for elem in rule_data['antecedents']]
            consequent = tuple(rule_data['consequent'])          
            st.session_state.fuzzy_rules.append(FuzzyRule(antecedents, consequent, weight=1, operation=rule_data['operation']))

# with open('/Users/anatolysesin/Downloads/fuzzy_system_config-3.json') as file:
#     data = json.load(file)
#     for rule_data in data['fuzzy_rules']:
#             print(rule_data)
    #import_fuzzy_system(data)
