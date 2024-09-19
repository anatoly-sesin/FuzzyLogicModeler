import streamlit as st
from utils.helpers import create_unique_key, display_membership_function_inputs, get_linguistic_variable_by_name
from utils.plotting import plot_membership_functions

def render_membership_function_editor():
    st.header("Membership Function Editor")

    if not st.session_state.linguistic_variables:
        st.warning("No linguistic variables defined. Please add linguistic variables first.")
        return

    selected_lv_name = st.selectbox("Select Linguistic Variable:", [lv.name for lv in st.session_state.linguistic_variables])
    selected_lv = get_linguistic_variable_by_name(selected_lv_name)

    if selected_lv:
        st.subheader(f"Editing Membership Functions for {selected_lv.name}")
        st.write(f"Range: [{selected_lv.range_min}, {selected_lv.range_max}]")

        # Edit existing terms
        for term_name, (term_type, term_params) in selected_lv.get_terms().items():
            st.write(f"### {term_name}")
            new_term_type = st.selectbox("Membership Function Type:", ["triangular", "trapezoidal", "gaussian", "sigmoid"], index=["triangular", "trapezoidal", "gaussian", "sigmoid"].index(term_type), key=create_unique_key(f"{term_name}_type", 0))
            new_term_params = display_membership_function_inputs(new_term_type, create_unique_key(f"{term_name}_params", 0), initial_values=term_params)

            # Display active values of the function parameters
            st.write("Current parameter values:")
            for i, param in enumerate(new_term_params):
                st.text(f"Parameter {i+1}: {param:.2f}")

            if st.button(f"Update {term_name}", key=create_unique_key(f"update_{term_name}", 0)):
                selected_lv.terms[term_name] = (new_term_type, new_term_params)
                st.success(f"Updated term '{term_name}' in {selected_lv.name}")

        # Plot updated membership functions
        st.pyplot(plot_membership_functions(selected_lv))
    else:
        st.error("Selected linguistic variable not found.")
