import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px

st.set_page_config(page_title='India Analytics Dashboard', page_icon="Gemini_Generated_Image_sq653msq653msq65.png", layout="wide")

# --------------------------------------- Plot Map ---------------------------------------
def plotfig(data, pri, sec):
    # MAP
    fig1 = px.scatter_mapbox(
        data,
        lat='Latitude',
        lon='Longitude',
        hover_name='District',
        size=pri,
        color=sec,
        hover_data=['State', 'Population'],
        color_continuous_scale='Turbo',
        mapbox_style="carto-positron",
        center=dict(lat=22.5, lon=78.9),
        zoom=4,
        size_max=20,
        height=600
    )
    st.plotly_chart(fig1, use_container_width=True)

    # BAR CHART
    fig2 = px.bar(
        data,
        x='State',
        y=[pri, sec],
        log_y=True,
        barmode='group'
    )
    st.plotly_chart(fig2, use_container_width=True)

    # HISTOGRAM
    fig3 = px.histogram(data, x=pri, y=sec, color='State', barmode='overlay')
    st.plotly_chart(fig3, use_container_width=True)

# --------------------------------------- Load Data ---------------------------------------
df = pd.read_csv(r'India.csv')

states = ['Overall India'] + list(df['State'].unique())

values = sorted(df.select_dtypes(include=np.number).columns)

# ------------------------------------ Side Bar Data Input ------------------------------------

st.title("India Data Reviews")

select_state = st.sidebar.selectbox("Select State", options=states)
select_pri = st.sidebar.selectbox("Primary element", options=values)
select_sec = st.sidebar.selectbox("Secondary element", options=values)
top5_states = st.sidebar.checkbox("Show Top 5 States")

btn = st.sidebar.button(label="Analyze")

if btn:
    if select_pri == select_sec:
        st.warning("Primary and Secondary elements must be different")

    else:
        # Plot for India
        if top5_states:
            st.subheader("Top 10 States Analysis")

            top10_states = df.groupby(['State', 'District'])[['Latitude', 'Longitude', select_pri, select_sec]].sum().sort_values(by=[select_pri, select_sec], ascending=False).head(10)
            top10_states = top10_states.reset_index()
            st.dataframe(top10_states)

            plotfig(top10_states, select_pri, select_sec)

        else:
            data = df if select_state == 'Overall India' else df[df['State'] == select_state]

            st.write(f"**{select_pri}** → Bubble Size")
            st.write(f"**{select_sec}** → Color")

            plotfig(data, select_pri, select_sec)







