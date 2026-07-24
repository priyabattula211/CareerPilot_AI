import streamlit as st
import time

def load_css():
    """Loads the custom CSS file."""
    try:
        with open("assets/style.css") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning("Custom CSS not found.")

def simulate_loading(message="Analyzing data..."):
    """Simulates a loading process with a spinner."""
    with st.spinner(message):
        time.sleep(1.5)

def page_header(title, description, icon=None):
    """Renders a standard page header."""
    load_css()
    icon_str = f"{icon} " if icon else ""
    st.title(f"{icon_str}{title}")
    st.markdown(f"*{description}*")
    st.markdown("<hr>", unsafe_allow_html=True)
