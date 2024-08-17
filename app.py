






## adding the packages to the requirements.txt file
## pip freeze > requirements.txt








import os
import streamlit as st
import snowflake.connector
import pandas as pd
from dotenv import load_dotenv
import altair as alt



# Load environment variables from .env file
load_dotenv()

#Snowflake connection
def _get_snowflake_connection():
    credentials = {
        "user": "guest_ZheWNtmM", 
        "password": "ie6uVad2#", 
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

# page layout setup
st.set_page_config(
    page_title="Financial Market Analysis Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded")


# top 25%
query_top_25_percent_data = """
-- daily poisition in usd 
WITH daily_position AS (
    SELECT 
        p.date,
        p.company_id,
        p.shares,
        pr.close_usd,
        p.shares * pr.close_usd AS daily_position_usd
    FROM
        POSITION p
    JOIN 
        PRICE pr
    ON p.company_id = pr.company_id AND p.date = pr.date
),
-- last year's average position for each company
last_year_avg_position AS (
    SELECT 
        company_id,
        avg(daily_position_usd) AS avg_position
    FROM 
        daily_position dp
    WHERE 
        date >= dateadd(year,-1, current_date())
    GROUP BY
        company_id
),
-- ranking companies based on last year's avg position
ranked_companies AS (
    SELECT
        company_id,
        avg_position,
        NTILE(4) OVER (ORDER BY avg_position DESC) AS quartile -- already partitioned by companyies
    FROM
        last_year_avg_position
),
top_25_percent AS (
    SELECT 
        company_id,
        avg_position,
    FROM
        ranked_companies
    WHERE 
        quartile = 1
),
latest_data AS (
    SELECT
        dp.company_id,
        dp.shares,
        dp.close_usd,
        dp.date,
        ROW_NUMBER() OVER (PARTITION BY dp.company_id ORDER BY dp.date DESC) as rn
    FROM 
        daily_position dp
    JOIN
        top_25_percent t ON dp.company_id = t.company_id
        
)
-- top 25 data% 
SELECT
    c.TICKER,
    c.sector_name,
    ld.shares,
    ld.close_usd AS last_close_price_usd,
    t.avg_position AS last_position_last_year
FROM 
    top_25_percent t
JOIN 
    CODE_CHALLENGE_ZHEWNTMM.SOURCE.COMPANY c ON  t.company_id = c.id
JOIN 
    latest_data ld ON t.company_id = ld.company_id
WHERE 
    ld.rn = 1
ORDER BY 
    t.avg_position DESC;
"""

query_company = """
SELECT DISTINCT ticker
FROM company;
"""

## Q2 - Top 25% Companies latest data
st.subheader("Top 25% Companies latest data")
top_25_data = run_query(query_top_25_percent_data)
st.dataframe(top_25_data, use_container_width=True)


## Q3 - Daily close price timeseries

# getting companies names
df_company = run_query(query_company)
companies_tickers = df_company['TICKER'].tolist()

# title
st.subheader("Daily close price timeseries for the selected company")

# select box for the companies
selected_company = st.selectbox("Select a company", companies_tickers)

# get selected company daily closing price
query_company_daily_close_price = f"""
SELECT p.date,c.ticker, p.close_usd
FROM 
    price p
JOIN
    company c ON p.company_id = c.id
WHERE 
    c.ticker = '{selected_company}'
ORDER BY 
    date ASC
"""

# Fetch the data for the selected company
df_company_data = run_query(query_company_daily_close_price)

# Check if there is data available for the selected company
if not df_company_data.empty:
    # Line chart for the selected company
    line_chart = alt.Chart(df_company_data).mark_line().encode(
        x='DATE:T',
        y='CLOSE_USD:Q',
        tooltip=['DATE:T', 'CLOSE_USD:Q']
    ).properties(
        title=f"Daily Close Price for {selected_company}"
    )
    st.altair_chart(line_chart, use_container_width=True)
else:
    st.warning("No data available for the selected company.")
