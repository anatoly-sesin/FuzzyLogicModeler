import streamlit as st
import json

def create_unique_key(base_key, index):
    return f"{base_key}_{index}"

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
    for i, param in enumerate(params):
        default_value = initial_values[i] if initial_values and i < len(initial_values) else 0.0
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
            "weight": rule.weight
        }
        export_data["fuzzy_rules"].append(rule_data)

    return json.dumps(export_data, indent=2)
