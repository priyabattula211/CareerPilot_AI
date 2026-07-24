import streamlit as st

def kpi_card(title, value, delta=None):
    """Renders a custom KPI metric card using HTML/CSS."""
    delta_html = ""
    if delta:
        color = "#34D399" if delta.startswith("+") else "#F87171"
        arrow = "↑" if delta.startswith("+") else "↓"
        delta_html = f'<span style="color: {color}; font-size: 0.875rem; font-weight: 500;">{arrow} {delta}</span>'
        
    st.markdown(f"""
        <div class="metric-card">
            <h3>{title}</h3>
            <div style="display: flex; align-items: baseline; gap: 0.5rem;">
                <h2>{value}</h2>
                {delta_html}
            </div>
        </div>
    """, unsafe_allow_html=True)

def skill_badge(skill, status="neutral"):
    """
    Renders a skill badge. 
    status can be: 'neutral', 'matched', 'missing'
    """
    return f'<span class="skill-badge {status}">{skill}</span>'
