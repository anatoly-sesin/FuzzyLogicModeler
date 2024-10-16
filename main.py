import streamlit as st
from components.sidebar import render_sidebar
from components.linguistic_variable_manager import render_linguistic_variable_manager
from components.membership_function_editor import render_membership_function_editor
from components.rule_editor import render_rule_editor
from components.inference_system_viewer import render_inference_system_viewer
from fuzzy_logic.linguistic_variable import LinguisticVariable
from utils.helpers import export_fuzzy_system, import_fuzzy_system
import json

st.set_page_config(page_title="Fuzzy Logic Toolbox", layout="wide")

def initialize_variables():
    if 'linguistic_variables' not in st.session_state:
        st.session_state.linguistic_variables = []
        
    
    if 'fuzzy_rules' not in st.session_state:
        st.session_state.fuzzy_rules = []
    
    if 'inference_system' not in st.session_state:
        st.session_state.inference_system = None
        st.session_state.inference_system_for_sugeno = None

def main():
    st.title("Fuzzy Logic Toolbox")

    initialize_variables()
    st.session_state.uploaded_file = None

    # Render sidebar
    selected_page = render_sidebar()

    # Render selected page
    if selected_page == "Linguistic Variables":
        render_linguistic_variable_manager()
    elif selected_page == "Membership Functions":
        render_membership_function_editor()
    elif selected_page == "Fuzzy Rules":
        render_rule_editor()
    elif selected_page == "Inference System":
        render_inference_system_viewer()

    # Add export button
    st.sidebar.write("---")
    if st.sidebar.button("Export Fuzzy System", use_container_width=True):
        export_data = export_fuzzy_system()
        st.sidebar.download_button(
            label="Download Fuzzy System Configuration",
            data=export_data,
            file_name="fuzzy_system_config.json",
            mime="application/json"
        )

    uploaded_file = st.sidebar.file_uploader("Upload File To Import Fuzzy System", accept_multiple_files=False)
    if uploaded_file is not None:
        st.session_state.uploaded_file = uploaded_file

    if st.sidebar.button("Import Fuzzy System", use_container_width=True):
        if st.session_state.uploaded_file is not None:
            st.sidebar.write("Loaded file:")
            st.sidebar.write(st.session_state.uploaded_file.name)
            import_fuzzy_system(json.load(uploaded_file))
            st.rerun()
            #st.sidebar.success('Success import')
            
        else:
            st.sidebar.error('No file')

if __name__ == "__main__":
    main()
