import streamlit as st

def render_sidebar():
    st.sidebar.title("Navigation")
    pages = [
        "Linguistic Variables",
        "Membership Functions",
        "Fuzzy Rules",
        "Inference System"
    ]
    selected_page = st.sidebar.radio("Go to", pages)
    return selected_page
