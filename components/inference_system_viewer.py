import streamlit as st
import numpy as np
from fuzzy_logic.inference_system import InferenceSystem
from utils.helpers import get_linguistic_variable_by_name
from utils.plotting import plot_rule_viewer
# import networkx as nx
import matplotlib.pyplot as plt
import io
import skfuzzy as fuzz
import simpful as smfuzz


def render_inference_system_viewer():
    st.header("Inference System Viewer")
    tabs = st.tabs(["Mamdani Inference", "Sugeno Inference"])

    with tabs[0]:
        if not st.session_state.linguistic_variables or not st.session_state.fuzzy_rules:
            st.warning("Please define linguistic variables and fuzzy rules before using the inference system.")
            return


        # selected_defuzz = st.selectbox("Defuzzification Method for Mamdani Algorithm", ['centroid', 'bisector', 'mom', 'som', 'lom'])
        # Build inference system
        if st.button("Build Inference System", use_container_width=True):
            
            st.session_state.inference_system = InferenceSystem(st.session_state.linguistic_variables, st.session_state.fuzzy_rules)
            st.session_state.inference_system.build_system()
            st.success("Inference system built successfully!")

        selected_defuzz = st.selectbox("Defuzzification Method for Mamdani Algorithm", ['centroid', 'bisector', 'mom', 'som', 'lom'])
        if st.session_state.inference_system is not None:
            # st.session_state.inference_system.defuzzification_method = selected_defuzz
            st.session_state.inference_system = InferenceSystem(st.session_state.linguistic_variables, st.session_state.fuzzy_rules, selected_defuzz)
            st.session_state.inference_system.build_system()
            # st.success("Inference system built successfully!")
            


        if st.session_state.inference_system:
            st.subheader("Test Inference System")

            # Input values
            inputs = {}
            output_name = ''
            for lv in st.session_state.linguistic_variables:
                if lv.name not in [rule.consequent[0] for rule in st.session_state.fuzzy_rules]:
                    inputs[lv.name] = st.slider(f"{lv.name}:", min_value=float(lv.range_min), max_value=float(lv.range_max), value=float(lv.range_min), step=0.1)
                else:
                    output_name = lv.name


            if st.button("Compute Mamdani", use_container_width=True):
                results = st.session_state.inference_system.compute(inputs)
                # st.write("### Results")
                if  len(results.output) == 0:
                    st.error('Error: There are not enough rules in the rule base')
                else:
                # for var_name, value in results.items():
                #     st.write(f"{var_name}: {value:.2f}")
                    st.write(f'### Result Mamdani')
                    st.write(f'#### *{output_name}:* {results.output[output_name]:.2f}')


                    # Plot rule viewer
                    st.write("### Rule Viewer")
                    #print(st.session_state.inference_system.ctrl_simulation.ctrl.graph)
                    # print(st.session_state.linguistic_variables)
                    # for lv in st.session_state.linguistic_variables:
                    #     st.session_state.inference_system
                    #     if lv.name == output_name:
                    #         lv.view(sim=results)
                    #fig, ax = plt.subplots()
                    
                    #st.pyplot()
                    #print((st.session_state.inference_system.consequents[output_name].view(sim=results)))

                    fig = plt.figure(figsize=(10, 7))
                    ax = fig.add_subplot(1, 1, 1)
                    st.session_state.inference_system.consequents[output_name].view(sim=results)
                    #print(type(st.session_state.inference_system.consequents[output_name]))
                    # fig, ax = fuzz.control.visualization.ControlSystemVisualizer(st.session_state.inference_system.consequents[output_name]).graph()
                    # st.pyplot(plt.show())
                    # st.pyplot(fig)
                    buf = io.BytesIO()
                    plt.savefig(buf, format='png')
                    buf.seek(0)

                    # Show graph in Streamlit
                    st.image(buf, use_column_width=True)


                
                
                #st.graphviz_chart(nx.nx_pydot.to_pydot().to_string())
                # rule_viewer_plot = plot_rule_viewer(st.session_state.inference_system, inputs)
                # if rule_viewer_plot:
                #     st.pyplot(rule_viewer_plot)
                # G = st.session_state.inference_system.ctrl_simulation.ctrl.graph
                # # Создаем фигуру для matplotlib
                # fig, ax = plt.subplots()

                # # Визуализируем граф с помощью networkx и matplotlib
                # pos = nx.spring_layout(G)  # Определяем расположение узлов
                # nx.draw(G, pos, with_labels=True, ax=ax, node_color='skyblue', font_size=8, font_weight='light', node_size=700, arrowsize=20)

                # # Отображаем граф в Streamlit
                # st.pyplot(fig)
        else:
            st.info("Please build the inference system first.")         

    with tabs[1]:
        if not st.session_state.linguistic_variables or not st.session_state.fuzzy_rules:
            st.warning("Please define linguistic variables and fuzzy rules before using the inference system.")
            return
        if st.button("Build Inference System", key="sugeno_build", use_container_width=True):
            #st.write("#### ")
            st.session_state.inference_system_for_sugeno = smfuzz.FuzzySystem()

        if st.session_state.inference_system_for_sugeno is not None:
            #system = st.session_state.inference_system_for_sugeno
            mfuncs = {
                'triangular': smfuzz.Triangular_MF,
                'trapezoidal': smfuzz.Trapezoidal_MF,
                'gaussian': smfuzz.Gaussian_MF,
                'sigmoid': smfuzz.Sigmoid_MF
            }
            
            inputs_names = []
            output_terms = []
            for elem in st.session_state.linguistic_variables:
                if elem.variable_type == "input":
                    term = []   
                    for name, params in elem.terms.items():
                        # st.write(mfuncs.get(params[0])(*params[1]))
                        func = mfuncs.get(params[0])(*params[1])
                        term.append(smfuzz.FuzzySet(function=func, term=name))
                    st.session_state.inference_system_for_sugeno.add_linguistic_variable(elem.name, smfuzz.LinguisticVariable(term, universe_of_discourse=[elem.range_min, elem.range_max]))
                    inputs_names.append(elem.name)
                    #st.write(term)
                else:
                    output_terms = {key: None for key in elem.terms}
            
            cols = st.columns(2)
            for term in output_terms:
                with cols[0]:
                    option = st.selectbox(f"Select type for *{term}* and enter value/function: ", ["crisp", "linear"], key=f"select_sugeno_{term}")
                    if option == "linear":
                        st.markdown(f"Inputs variables:  {inputs_names}")
                    else:
                        st.markdown("_")
                with cols[1]:
                    value = st.text_input("", placeholder=f"Enter", key=f"enter_linear_sugeno_{term}")
                    st.markdown("_")
                    output_terms[term] = (option, value)

            # st.session_state.sugeno_params = 
            try:
                if all(value[-1] is not None for value in output_terms.values()):
                    for term, value in output_terms.items():
                        if value[0] == "crisp" and value[1]:
                            st.session_state.inference_system_for_sugeno.set_crisp_output_value(term, float(value[1]))
                        else:
                            st.session_state.inference_system_for_sugeno.set_output_function(term, value[1])
                    st.session_state.inference_system_for_sugeno.add_rules([str(rule) for rule in st.session_state.fuzzy_rules])


                    inputs = {}
                    output_name = ''
                    for lv in st.session_state.linguistic_variables:
                        if lv.name not in [rule.consequent[0] for rule in st.session_state.fuzzy_rules]:
                            inputs[lv.name] = st.slider(f"{lv.name}:", min_value=float(lv.range_min), max_value=float(lv.range_max), value=float(lv.range_min), step=0.1, key=f'sugeno_slider_input_{lv.name}')
                        else:
                            output_name = lv.name

                    if st.button("Compute Sugeno", use_container_width=True):
                        for name in inputs_names:
                            st.session_state.inference_system_for_sugeno.set_variable(name, inputs[name])

                    st.write(f'### Result Sugeno')
                    result = st.session_state.inference_system_for_sugeno.Sugeno_inference([output_name])
                    st.write(f'#### *{output_name}:* {result[output_name]:.2f}')

                else:
                    st.warning("Define the terms of the output variable by constants and/or a linear combination of inputs")
            except SyntaxError:
                st.warning("Define the terms of the output variable by constants and/or a linear combination of inputs")
            except Exception as e:
                st.error("Define the terms of the output variable by numeric constants and/or a correct linear combination of inputs")
                # st.error(e)
        else:
            st.info("Please build the inference system first.") 
                
    
