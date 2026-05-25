import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Student Performance Analyzer",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inject custom CSS for Roboto font
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap');

html, body, p, div, h1, h2, h3, h4, h5, h6, li, a, span, label, button {
    font-family: 'Roboto', sans-serif;
}

/* Ensure Material Icons still use their correct font */
.material-symbols-rounded, .stIcon, [data-testid="stIconMaterial"] {
    font-family: 'Material Symbols Rounded' !important;
}
</style>
""", unsafe_allow_html=True)

# Initialize session state for data
if "df" not in st.session_state:
    st.session_state.df = None

# Navigation Setup
dashboard = st.Page("pages/1_Dashboard.py", title="Dashboard", icon=":material/dashboard:", default=True)
profiles = st.Page("pages/2_Student_Profiles.py", title="Student Profiles", icon=":material/person:")
ml = st.Page("pages/3_Machine_Learning.py", title="Machine Learning", icon=":material/psychology:")
reports = st.Page("pages/4_Reports.py", title="Reports", icon=":material/description:")

pg = st.navigation(
    {
        "Analytics": [dashboard, profiles],
        "Advanced": [ml, reports]
    }
)

pg.run()
