import streamlit as st
from components.sidebar import render_sidebar
from components.linguistic_variable_manager import render_linguistic_variable_manager
from components.membership_function_editor import render_membership_function_editor
from components.rule_editor import render_rule_editor
from components.inference_system_viewer import render_inference_system_viewer
from fuzzy_logic.linguistic_variable import LinguisticVariable
from utils.helpers import export_fuzzy_system

st.set_page_config(page_title="Fuzzy Logic Toolbox", layout="wide")

def initialize_variables():
    if 'linguistic_variables' not in st.session_state:
        st.session_state.linguistic_variables = [
            LinguisticVariable("soil moisture", 0, 50, "input"),
            LinguisticVariable("relative humidity", 0, 100, "input"),
            LinguisticVariable("air temperature", 0, 40, "input"),
            LinguisticVariable("water pump pressure", 0, 100, "output")
        ]
        
        # Add terms to each linguistic variable
        soil_moisture = st.session_state.linguistic_variables[0]
        soil_moisture.add_term("saturated", "trapezoidal", [30, 40, 50, 50])
        soil_moisture.add_term("optimal", "triangular", [15, 25, 35])
        soil_moisture.add_term("insufficient", "trapezoidal", [0, 0, 10, 20])

        relative_humidity = st.session_state.linguistic_variables[1]
        relative_humidity.add_term("low", "trapezoidal", [0, 0, 20, 40])
        relative_humidity.add_term("medium", "triangular", [30, 50, 70])
        relative_humidity.add_term("normal", "triangular", [60, 75, 90])
        relative_humidity.add_term("high", "trapezoidal", [80, 90, 100, 100])

        air_temperature = st.session_state.linguistic_variables[2]
        air_temperature.add_term("low", "trapezoidal", [0, 0, 10, 15])
        air_temperature.add_term("medium", "triangular", [10, 20, 30])
        air_temperature.add_term("normal", "triangular", [25, 30, 35])
        air_temperature.add_term("high", "trapezoidal", [30, 35, 40, 40])

        water_pump_pressure = st.session_state.linguistic_variables[3]
        water_pump_pressure.add_term("very weak", "trapezoidal", [0, 0, 10, 20])
        water_pump_pressure.add_term("weak", "triangular", [10, 25, 40])
        water_pump_pressure.add_term("medium", "triangular", [30, 50, 70])
        water_pump_pressure.add_term("high", "triangular", [60, 75, 90])
        water_pump_pressure.add_term("maximum", "trapezoidal", [80, 90, 100, 100])
    
    if 'fuzzy_rules' not in st.session_state:
        st.session_state.fuzzy_rules = []
    
    if 'inference_system' not in st.session_state:
        st.session_state.inference_system = None

def main():
    st.title("Fuzzy Logic Toolbox")

    initialize_variables()

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
    if st.sidebar.button("Export Fuzzy System"):
        export_data = export_fuzzy_system()
        st.sidebar.download_button(
            label="Download Fuzzy System Configuration",
            data=export_data,
            file_name="fuzzy_system_config.json",
            mime="application/json"
        )

if __name__ == "__main__":
    main()
