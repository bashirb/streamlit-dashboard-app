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


## Q1 - Top 10 Sectors by Position

# title
st.subheader("Top 10 Sectors by Position (USD)")

# load the query from the file
top_10_sectors_data = load_query_from_file('top_10_sectors.sql')

# query the top 10 sectors
top_10_sectors_df = run_query(top_10_sectors_data)

if not top_10_sectors_df.empty:
    # create the chart
    chart = alt.Chart(top_10_sectors_df).mark_bar().encode(
        y=alt.Y(
            'SECTOR_NAME:N', 
            title='Sector Name', 
            sort='-x', 
            axis=alt.Axis(labelLimit=300)  # Increase the space allowed for the sector names
        ),
        x=alt.X(
            'SECTOR_POSITION_USD:Q', 
            title='Sector Position (USD)', 
            scale=alt.Scale(type='log'),
            axis=alt.Axis(grid=False, labels=False)  # Remove gridlines and labels        
        ),
        color=alt.Color(
            'SECTOR_POSITION_USD:Q', 
            scale=alt.Scale(
                range=['#c6dbef', '#08306b'],  # Light to dark blue shades for the gradient
                type='linear'
            ),
            legend=None  # Hide legend
        ),
        tooltip=[
            alt.Tooltip('SECTOR_NAME:N', title='Sector Name'),
            alt.Tooltip('SECTOR_POSITION_USD:Q', title='Position (USD)', format='$,.2f')
        ]
    ).properties(
        title='From highest to lowest',
    ).interactive()

    # Add text labels on the bars
    text = chart.mark_text(
        align='left',
        baseline='middle',
        dx=3  # Adjust the distance of the text from the bars
    ).encode(
        text=alt.Text('SECTOR_POSITION_USD:Q', format='$,.2f')  # Format the text as USD
    )
    final_chart = chart + text

    # Display the chart 
    st.altair_chart(final_chart, use_container_width=True)

else:
    st.write("Refresh page to get the data")


st.divider()


######### Q2 - Top 25% Companies latest data  #########
st.subheader("Top 25% Companies latest data")

# load the data from file
top_25_percent_query = load_query_from_file('top_25_percent_data.sql')

# query the top 25% from snowflake
top_25_data = run_query(top_25_percent_query)

# display the dataframe
st.dataframe(top_25_data, use_container_width=True)

st.divider()
