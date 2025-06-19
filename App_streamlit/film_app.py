import streamlit as st

# Navigation
   
page_1 = st.Page("page1.py", title="Présentation générale", icon="🎬")     # Film clapperboard
page_2 = st.Page("page2.py", title=" Statistiques des tags", icon="📊")  # Bar chart
page_3 = st.Page("page3.py", title="Catalogue de films", icon="🔎") # Magnifying glass

pg = st.navigation([ page_1, page_2, page_3])
pg.run()