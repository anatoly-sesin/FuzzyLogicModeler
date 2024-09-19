import matplotlib.pyplot as plt
import numpy as np
import streamlit as st
from fuzzy_logic.membership_function import MembershipFunction

def plot_membership_functions(linguistic_variable):
    fig, ax = plt.subplots(figsize=(12, 6))
    x = np.linspace(linguistic_variable.range_min, linguistic_variable.range_max, 1000)

    colors = ['#FF0000', '#00FF00', '#0000FF', '#FFFF00', '#FF00FF']  # Red, Green, Blue, Yellow, Magenta

    for (term_name, (mf_type, mf_params)), color in zip(linguistic_variable.get_terms().items(), colors):
        mf_function = MembershipFunction.get_function(mf_type)
        y = mf_function(x, mf_params)
        ax.plot(x, y, label=term_name, color=color)
        
        # Find the peak of the membership function
        peak_x = x[np.argmax(y)]
        peak_y = np.max(y)
        
        # Add label to the peak
        ax.annotate(term_name, (peak_x, peak_y), xytext=(0, 5), 
                    textcoords='offset points', ha='center', va='bottom',
                    bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.5),
                    arrowprops=dict(arrowstyle = '->', connectionstyle='arc3,rad=0'))

    ax.set_title(f"Membership Functions for {linguistic_variable.name}")
    ax.set_xlabel(linguistic_variable.name)
    ax.set_ylabel("Membership Degree")
    ax.set_xlim(linguistic_variable.range_min, linguistic_variable.range_max)
    ax.set_ylim(0, 1.1)
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    ax.grid(True)

    # Add x-axis tick labels
    num_ticks = 5
    tick_positions = np.linspace(linguistic_variable.range_min, linguistic_variable.range_max, num_ticks)
    ax.set_xticks(tick_positions)
    ax.set_xticklabels([f"{x:.1f}" for x in tick_positions])

    plt.tight_layout()
    return fig

def plot_rule_viewer(inference_system, inputs):
    if not inference_system.ctrl_simulation:
        return None

    fig, axs = plt.subplots(len(inference_system.rules), len(inputs) + 1, figsize=(12, 3 * len(inference_system.rules)))
    
    if len(inference_system.rules) == 1:
        axs = np.array([axs])
    
    for i, rule in enumerate(inference_system.rules):
        for j, (var_name, value) in enumerate(inputs.items()):
            ax = axs[i, j]
            print(inference_system.ctrl_simulation.ctrl)
            var = inference_system.ctrl_simulation.ctrl.inputs[var_name]
            ax.plot(var.universe, var[rule.antecedents[0][1]].mf)
            ax.fill_between(var.universe, 0, var[rule.antecedents[0][1]].mf)
            ax.set_ylim(0, 1.1)
            ax.set_title(f"{var_name}: {value:.2f}")
            ax.axvline(value, color='r', linestyle='--')

        ax = axs[i, -1]
        var = inference_system.ctrl_simulation.ctrl.outputs[rule.consequent[0]]
        ax.plot(var.universe, var[rule.consequent[1]].mf)
        ax.fill_between(var.universe, 0, var[rule.consequent[1]].mf)
        ax.set_ylim(0, 1.1)
        ax.set_title(f"{rule.consequent[0]}")

    plt.tight_layout()
    return fig
