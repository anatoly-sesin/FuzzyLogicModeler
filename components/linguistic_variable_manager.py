import streamlit as st
from fuzzy_logic.linguistic_variable import LinguisticVariable
from utils.helpers import create_unique_key, display_membership_function_inputs, get_linguistic_variable_by_name
from utils.plotting import plot_membership_functions

def render_linguistic_variable_manager():
    st.header("Linguistic Variable Manager")

    # Add new linguistic variable
    st.subheader("Add New Linguistic Variable")
    new_var_name = st.text_input("Variable Name:")
    new_var_type = st.selectbox("Variable Type:", ["input", "output"])
    new_var_range_min = st.number_input("Range Minimum:", value=0.0)
    new_var_range_max = st.number_input("Range Maximum:", value=100.0)

    if st.button("Add Linguistic Variable"):
        if new_var_name and new_var_range_min < new_var_range_max:
            new_var = LinguisticVariable(new_var_name, new_var_range_min, new_var_range_max, new_var_type)
            st.session_state.linguistic_variables.append(new_var)
            st.success(f"Added linguistic variable: {new_var_name} ({new_var_type})")
        else:
            st.error("Invalid input. Please check the variable name and range.")

    # Manage existing linguistic variables
    st.subheader("Manage Linguistic Variables")
    for i, lv in enumerate(st.session_state.linguistic_variables):
        st.write(f"### {lv.name} ({lv.variable_type})")
        st.write(f"Range: [{lv.range_min}, {lv.range_max}]")

        # Add new term
        new_term_name = st.text_input("New Term Name:", key=create_unique_key("new_term_name", i))
        new_term_type = st.selectbox("Membership Function Type:", ["triangular", "trapezoidal", "gaussian", "sigmoid"], key=create_unique_key("new_term_type", i))
        new_term_params = display_membership_function_inputs(new_term_type, create_unique_key("new_term_params", i))

        if st.button("Add Term", key=create_unique_key("add_term_button", i)):
            lv.add_term(new_term_name, new_term_type, new_term_params)
            st.success(f"Added term '{new_term_name}' to {lv.name}")

        # Display existing terms
        st.write("#### Existing Terms")
        terms_to_remove = []
        for term_name, (term_type, term_params) in list(lv.get_terms().items()):
            st.write(f"- {term_name} ({term_type}): {term_params}")
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button(f"Edit {term_name}", key=create_unique_key(f"edit_{term_name}", i)):
                    st.session_state[f"editing_{term_name}"] = True
            with col2:
                if st.button(f"Remove {term_name}", key=create_unique_key(f"remove_{term_name}", i)):
                    terms_to_remove.append(term_name)
            
            if st.session_state.get(f"editing_{term_name}", False):
                new_term_name = st.text_input("Term Name:", value=term_name, key=create_unique_key(f"edit_name_{term_name}", i))
                new_term_type = st.selectbox("Membership Function Type:", ["triangular", "trapezoidal", "gaussian", "sigmoid"], index=["triangular", "trapezoidal", "gaussian", "sigmoid"].index(term_type), key=create_unique_key(f"edit_type_{term_name}", i))
                new_term_params = display_membership_function_inputs(new_term_type, create_unique_key(f"edit_params_{term_name}", i), initial_values=term_params)
                
                if st.button("Save Changes", key=create_unique_key(f"save_edit_{term_name}", i)):
                    lv.remove_term(term_name)
                    lv.add_term(new_term_name, new_term_type, new_term_params)
                    st.success(f"Updated term '{term_name}' in {lv.name}")
                    st.session_state[f"editing_{term_name}"] = False
                    st.rerun()

        # Remove terms after iteration
        for term_name in terms_to_remove:
            lv.remove_term(term_name)
            st.success(f"Removed term '{term_name}' from {lv.name}")

        # Plot membership functions
        st.pyplot(plot_membership_functions(lv))

        if st.button(f"Remove {lv.name}", key=create_unique_key(f"remove_{lv.name}", i)):
            st.session_state.linguistic_variables.remove(lv)
            st.success(f"Removed linguistic variable: {lv.name}")

    st.write("---")
