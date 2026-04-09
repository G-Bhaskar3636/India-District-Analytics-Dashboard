import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

df = pd.read_csv(r'India.csv')

states = ['Overall India'] + list(df['State'].unique())

values = sorted(df.select_dtypes(include=np.number).columns)

# ------------------------------------ Side Bar Data Input ------------------------------------

st.title("India Data Reviews")

select_state = st.sidebar.selectbox("Select State", options=states)
select_pri = st.sidebar.selectbox("Primary element", options=values)
select_sec = st.sidebar.selectbox("Secondary element", options=values)

btn = st.sidebar.button(label="Analyze")

if btn:
    if select_pri == select_sec:
        st.warning("Primary and Secondary elements must be different")

    else:
        # Plot for India

        data = df if select_state == 'Overall India' else df[df['State'] == select_state]

        st.write(f"{select_pri} represents thr Primary Size")
        st.write(f"{select_sec} represents thr Secondary Color")
        fig = px.scatter_mapbox(
            data,
            lat='Latitude',
            lon='Longitude',
            hover_name='District',
            size=select_pri,
            color=select_sec,
            hover_data=['State', 'District code', 'Population'],
            mapbox_style="carto-positron",
            zoom=4,
            size_max=35,
            width = 15000,
            height = 600,
        )

        st.plotly_chart(fig)
