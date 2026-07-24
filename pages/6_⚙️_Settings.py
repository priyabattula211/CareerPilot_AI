import streamlit as st
import os
from components.ui import page_header
from database.service import save_setting, get_setting, clear_history

st.set_page_config(page_title="Settings | CareerPilot AI", layout="wide")
page_header("Settings", "Configure application preferences and data", "⚙️")

st.subheader("1. AI Configuration")

default_model = get_setting("GEMINI_MODEL", "gemini-2.5-flash")

st.markdown("**Model Selection**")
st.markdown("Choose which Gemini model you'd like to use for analysis.")
model_options = ["gemini-2.5-flash", "gemini-pro", "gemini-1.5-flash"]
current_index = model_options.index(default_model) if default_model in model_options else 0
model_choice = st.selectbox("Preferred Gemini Model:", model_options, index=current_index)

if st.button("Save AI Settings", type="primary"):
    save_setting("GEMINI_MODEL", model_choice)
    st.success("AI Settings saved successfully!")

st.markdown("<hr>", unsafe_allow_html=True)

st.subheader("2. Data Management")

col1, col2 = st.columns(2)

with col1:
    st.markdown("**Export Analysis History**")
    st.markdown("Download all your past resume and GitHub analysis scores as a CSV file.")
    if st.button("Generate Export"):
        from database.service import get_recent_analyses
        df = get_recent_analyses(limit=100)
        if not df.empty:
            csv = df.to_csv(index=False)
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name="careerpilot_history.csv",
                mime="text/csv"
            )
        else:
            st.warning("No history found to export.")

with col2:
    st.markdown("**Clear Data**")
    st.markdown("Wipe all historical analysis records from your local database.")
    if st.button("Clear History", type="secondary"):
        clear_history()
        st.success("History cleared successfully!")
        
st.markdown("<hr>", unsafe_allow_html=True)
st.caption("CareerPilot AI v1.0 | Local Environment")
