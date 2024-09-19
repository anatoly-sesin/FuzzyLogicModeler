import streamlit as st
from fuzzy_logic.fuzzy_rule import FuzzyRule
from utils.helpers import create_unique_key, get_linguistic_variable_by_name

def render_rule_editor():
    st.header("Fuzzy Rule Editor")

    if not st.session_state.linguistic_variables:
        st.warning("No linguistic variables defined. Please add linguistic variables first.")
        return

    # Add new rule
    st.subheader("Add New Rule")
    antecedents = []
    consequent = None

    # Antecedents
    input_variables = [lv for lv in st.session_state.linguistic_variables if lv.variable_type == "input"]
    num_antecedents = st.number_input("Number of Antecedents:", min_value=1, max_value=len(input_variables), value=1)
    
    for i in range(num_antecedents):
        col1, col2 = st.columns(2)
        with col1:
            ant_var = st.selectbox(f"Antecedent {i+1} Variable:", [lv.name for lv in input_variables], key=create_unique_key("ant_var", i))
        with col2:
            ant_term = st.selectbox(f"Antecedent {i+1} Term:", get_linguistic_variable_by_name(ant_var).get_terms().keys(), key=create_unique_key("ant_term", i))
        antecedents.append((ant_var, ant_term))

    # Add operation selection (AND/OR)
    operation = st.radio("Select Operation:", ["AND", "OR"])

    # Consequent
    output_variables = [lv for lv in st.session_state.linguistic_variables if lv.variable_type == "output"]
    if output_variables:
        col1, col2 = st.columns(2)
        with col1:
            cons_var = st.selectbox("Consequent Variable:", [lv.name for lv in output_variables], key="cons_var")
        with col2:
            cons_term = st.selectbox("Consequent Term:", get_linguistic_variable_by_name(cons_var).get_terms().keys(), key="cons_term")
        consequent = (cons_var, cons_term)

        # Rule weight
        rule_weight = st.slider("Rule Weight:", min_value=0.0, max_value=1.0, value=1.0, step=0.1)

        if st.button("Add Rule"):
            new_rule = FuzzyRule(antecedents, consequent, rule_weight, operation)
            st.session_state.fuzzy_rules.append(new_rule)
            st.success("Rule added successfully!")
    else:
        st.warning("No output variables defined. Please add at least one output variable.")

    # Display existing rules
    st.subheader("Existing Rules")
    for i, rule in enumerate(st.session_state.fuzzy_rules):
        st.write(f"{i+1}. {rule}")
        col1, col2 = st.columns(2)
        with col1:
            if st.button(f"Edit Rule {i+1}", key=create_unique_key("edit_rule", i)):
                st.session_state[f"editing_rule_{i}"] = True
        with col2:
            if st.button(f"Remove Rule {i+1}", key=create_unique_key("remove_rule", i)):
                st.session_state.fuzzy_rules.pop(i)
                st.success(f"Rule {i+1} removed successfully!")
                st.rerun()

        if st.session_state.get(f"editing_rule_{i}", False):
            edit_rule(rule, i)

def edit_rule(rule, rule_index):
    st.write("### Edit Rule")
    antecedents = []
    
    # Edit antecedents
    for i, (var, term) in enumerate(rule.antecedents):
        col1, col2 = st.columns(2)
        with col1:
            ant_var = st.selectbox(f"Antecedent {i+1} Variable:", [lv.name for lv in st.session_state.linguistic_variables if lv.variable_type == "input"], index=[lv.name for lv in st.session_state.linguistic_variables if lv.variable_type == "input"].index(var), key=create_unique_key(f"edit_ant_var_{rule_index}", i))
        with col2:
            ant_term = st.selectbox(f"Antecedent {i+1} Term:", get_linguistic_variable_by_name(ant_var).get_terms().keys(), index=list(get_linguistic_variable_by_name(ant_var).get_terms().keys()).index(term), key=create_unique_key(f"edit_ant_term_{rule_index}", i))
        antecedents.append((ant_var, ant_term))

    # Edit operation
    operation = st.radio("Select Operation:", ["AND", "OR"], index=0 if rule.operation == "AND" else 1, key=f"edit_operation_{rule_index}")

    # Edit consequent
    col1, col2 = st.columns(2)
    with col1:
        cons_var = st.selectbox("Consequent Variable:", [lv.name for lv in st.session_state.linguistic_variables if lv.variable_type == "output"], index=[lv.name for lv in st.session_state.linguistic_variables if lv.variable_type == "output"].index(rule.consequent[0]), key=f"edit_cons_var_{rule_index}")
    with col2:
        cons_term = st.selectbox("Consequent Term:", get_linguistic_variable_by_name(cons_var).get_terms().keys(), index=list(get_linguistic_variable_by_name(cons_var).get_terms().keys()).index(rule.consequent[1]), key=f"edit_cons_term_{rule_index}")
    consequent = (cons_var, cons_term)

    # Edit rule weight
    rule_weight = st.slider("Rule Weight:", min_value=0.0, max_value=1.0, value=rule.weight, step=0.1, key=f"edit_weight_{rule_index}")

    if st.button("Save Changes", key=f"save_rule_{rule_index}"):
        st.session_state.fuzzy_rules[rule_index] = FuzzyRule(antecedents, consequent, rule_weight, operation)
        st.success("Rule updated successfully!")
        st.session_state[f"editing_rule_{rule_index}"] = False
        st.rerun()

    if st.button("Cancel", key=f"cancel_edit_{rule_index}"):
        st.session_state[f"editing_rule_{rule_index}"] = False
        st.rerun()
