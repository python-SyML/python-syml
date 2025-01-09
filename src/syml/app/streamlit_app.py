import streamlit as st

homepage = st.Page("homepage.py", title="Homepage", icon="🏠")

data_discovery_page = st.Page("data_exploration/discovery_dashboard.py", title="Data Discovery Dashboard", icon="🔭")

quality_improvement_page = st.Page("data_exploration/quality_improvement.py", title="Quality Improvement Assistant", icon="🧑🏼‍🔬")


nav_tree = {"Homepage": [homepage], "Data Mining": [data_discovery_page, quality_improvement_page]}

pg = st.navigation(nav_tree)
st.set_page_config(page_title="Data manager", page_icon=":material/edit:", layout="wide")
pg.run()
