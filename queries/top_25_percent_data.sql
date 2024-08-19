-- Calculate daily position value in USD
WITH daily_position AS (
    SELECT 
        p.date,
        p.company_id,
        p.shares,
        pr.close_usd,
        -- daily position is calculated by multiplying shares by the closing price
        p.shares * pr.close_usd AS daily_position_usd
    FROM
        POSITION p
    JOIN 
        PRICE pr
    ON p.company_id = pr.company_id AND p.date = pr.date
),
-- calculates the average position value for each company over the last year.
last_year_avg_position AS (
    SELECT 
        company_id,
        -- calculates the average position value
        avg(daily_position_usd) AS avg_position
    FROM 
        --uses the daily_position CTE as its source
        daily_position dp
    WHERE 
        -- filters dates within the last year
        date >= dateadd(year,-1, current_date())
    GROUP BY
        -- groups the results by company_id to get an average for each company
        company_id
),
-- ranking companies based on last year's avg position
ranked_companies AS (
    SELECT
        company_id,
        avg_position,
        -- assigns a value from 1 to 4 to each company based on avg position, 
        -- with 1 representing the top 25%.
        NTILE(4) OVER (ORDER BY avg_position DESC) AS quartile -- already partitioned by companyies
    FROM
        last_year_avg_position
),
-- Select top 25% of companies by average position
top_25_percent AS (
    SELECT 
        company_id,
        avg_position,
    FROM
        ranked_companies
    WHERE 
        -- Select only the first quartile (top 25%)
        quartile = 1 
),
-- Get the most recent data for each company in the top 25%
latest_data AS (
    SELECT
        dp.company_id,
        dp.shares,
        dp.close_usd,
        dp.date,
        -- Assign a row number to each company's data, ordered by date descending
        ROW_NUMBER() OVER (PARTITION BY dp.company_id ORDER BY dp.date DESC) as rn
    FROM 
        daily_position dp
    JOIN
        -- Select only the companies in the top 25%
        top_25_percent t ON dp.company_id = t.company_id
        
)
-- Final query to get detailed information for the top 25% of companies
SELECT
    c.TICKER,
    c.sector_name,
    ld.shares,
    ld.close_usd AS last_close_price_usd,
    t.avg_position AS average_position_last_year
FROM 
    top_25_percent t
JOIN 
    -- Join with company table to get ticker and sector information
    CODE_CHALLENGE_ZHEWNTMM.SOURCE.COMPANY c ON  t.company_id = c.id
JOIN 
    -- Join with latest_data to get the most recent position information
    latest_data ld ON t.company_id = ld.company_id
WHERE 
    -- Select only the most recent data point for each company
    ld.rn = 1
ORDER BY 
    -- Sort the results by average position, descending
    t.avg_position DESC;
