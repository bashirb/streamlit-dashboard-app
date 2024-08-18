import os
import streamlit as st
import snowflake.connector
import pandas as pd
from dotenv import load_dotenv
import altair as alt


# page layout setup
st.set_page_config(
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded")

st.write("## Financial Market Analysis Dashboard")
st.divider()

