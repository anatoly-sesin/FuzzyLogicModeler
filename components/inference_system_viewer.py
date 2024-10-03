import streamlit as st
import numpy as np
from fuzzy_logic.inference_system import InferenceSystem
from utils.helpers import get_linguistic_variable_by_name
from utils.plotting import plot_rule_viewer
import networkx as nx
import matplotlib.pyplot as plt
import io
import skfuzzy as fuzz

def render_inference_system_viewer():
    st.header("Inference System Viewer")

    if not st.session_state.linguistic_variables or not st.session_state.fuzzy_rules:
        st.warning("Please define linguistic variables and fuzzy rules before using the inference system.")
        return

    # Build inference system
    if st.button("Build Inference System", use_container_width=True):
        st.session_state.inference_system = InferenceSystem(st.session_state.linguistic_variables, st.session_state.fuzzy_rules)
        st.session_state.inference_system.build_system()
        st.success("Inference system built successfully!")

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
                st.write(f'### Result')
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

                # Отображаем граф в Streamlit
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
