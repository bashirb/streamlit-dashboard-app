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

# Load environment variables from .env file
load_dotenv()


# Function toload SQL query from a file
def load_query_from_file(file_path):
    with open(file_path, 'r') as file:
        query = file.read()
    return query


#Snowflake connection
def _get_snowflake_connection():
    credentials = {
        "user": os.getenv('user_name'),
        "password": os.getenv('password'),
        "account": "ui76830.west-europe.azure", 
        "database": "CODE_CHALLENGE_ZHEWNTMM", 
        "schema": "SOURCE",
        "warehouse": "GUEST_CODE_CHALLENGE_ZHEWNTMM",
        "role": "GUEST_CODE_CHALLENGE_ZHEWNTMM",
    }
    return snowflake.connector.connect(**credentials)

# Execute a SQL query on a Snowflake database and return the results as a pandas DataFrame.
def run_query(query):
    conn = _get_snowflake_connection()
    df = pd.read_sql(query, conn)
    conn.close()
    return df


