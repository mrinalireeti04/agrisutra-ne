import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
import os

st.set_page_config(page_title="AgriSutra NE | Dashboard", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.stApp { background-color: #0f1117; color: #e0e0e0; }
.app-header { text-align: center; padding: 1.5rem 0 0.5rem 0; border-bottom: 1px solid #1e2a1e; margin-bottom: 1.5rem; }
.app-header h1 { color: #69f0ae; font-size: 2.2rem; font-weight: 700; margin: 0; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="app-header">
    <h1>📊 Farmer History Dashboard</h1>
    <p style="color: #78909c;">Past Recommendations & Analytics</p>
</div>
""", unsafe_allow_html=True)

DB_PATH = "history.db"

if not os.path.exists(DB_PATH):
    st.info("No historical data found. Generate some recommendations first!")
    st.stop()

@st.cache_data(ttl=60)
def load_data():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM recommendations ORDER BY date DESC", conn)
    conn.close()
    return df

df = load_data()

if df.empty:
    st.info("No records in the database.")
    st.stop()

st.markdown("### 📋 Recent Recommendations")
st.dataframe(df, use_container_width=True)

st.markdown("<br>### 📈 Analytics", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    fig_crops = px.pie(df, names='crop', title="Recommendations by Crop", hole=0.4,
                       color_discrete_sequence=['#69f0ae', '#81d4fa', '#ffcc80'])
    fig_crops.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='#e0e0e0')
    st.plotly_chart(fig_crops, use_container_width=True)

with col2:
    fig_fert = px.bar(df, x='date', y=['urea', 'ssp', 'mop'], title="Fertilizer Usage Over Time (kg)",
                      barmode='group', color_discrete_map={'urea': '#69f0ae', 'ssp': '#81d4fa', 'mop': '#ffcc80'})
    fig_fert.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='#e0e0e0')
    st.plotly_chart(fig_fert, use_container_width=True)
