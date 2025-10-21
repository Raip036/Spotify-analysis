import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine
from datetime import datetime
import time

# Database connection setup

engine = create_engine('postgresql://postgres:Ben10boy!@localhost:5432/spotify_dashboard')

# Streamlit page configuration
st.set_page_config(page_title="Spotify Listening Dashboard", layout="wide")
st.title("🎵 Spotify Listening Dashboard")

if 'last_refresh' not in st.session_state:
    st.session_state['last_refresh'] = datetime.now()

if st.button("🔄 Manual Refresh Now"):
    st.session_state['last_refresh'] = datetime.now()

st.caption(f"Last refreshed: {st.session_state['last_refresh'].strftime('%Y-%m-%d %H:%M:%S')}")
           
# Load data 

@st.cache_data(ttl=60)
def load_data():
    query = "SELECT * FROM pratik_history ORDER BY total_ms_played DESC LIMIT 100;"
    df = pd.read_sql(query, engine)
    return df

df = load_data()

# Display data
st.subheader("Top 20 Songs by Total Play Time")
st.dataframe(df)

st.subheader("Total Play Time by Song")
fig = px.bar(df, x='song_key', y='total_minutes_played', color='play_count', title="Total Play Time per Song")
st.plotly_chart(fig, use_container_width=True)

