-- Define the starting date as the earliest date in the position table
WITH starting_date AS (
    SELECT MIN(p.date) AS min_date
    FROM position p
    JOIN price pr ON p.date = pr.date
),
-- Generate a continuous date range from the starting date to the current date
date_range AS (
    -- Start with the minimum date
    SELECT sd.min_date as dt
    FROM starting_date sd
    UNION ALL
    -- Recursively add one day until reaching the current date
    SELECT DATEADD('day',1,dt) as dt
    FROM date_range
    WHERE dt < current_date()
),
-- Fill in missing data for all dates and companies
filled_data AS (
    SELECT 
        dr.dt AS date,
        c.ID AS COMPANY_ID,
        c.SECTOR_NAME,
        p.shares,
        -- Use a window function to fill forward the last known number of shares
        -- IGNORE NULLS ensures we only consider non-null values
        -- ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW creates a window
        -- from the start of the partition up to the current row
        LAST_VALUE(p.SHARES IGNORE NULLS) OVER (
            PARTITION BY c.ID ORDER BY dr.dt
            ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
        ) AS filled_shares,
        pr.close_usd,
        -- Similar window function to fill forward the last known price
        LAST_VALUE(pr.CLOSE_USD IGNORE NULLS) OVER (
            PARTITION BY c.ID ORDER BY dr.dt
            ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
        ) AS filled_price_usd
    FROM date_range dr
    -- CROSS JOIN creates a row for every combination of date and company
    CROSS JOIN company c
    -- LEFT JOINs ensure we keep all dates and companies, even if there's no matching data
    LEFT JOIN position p ON dr.dt = p.DATE AND c.ID = p.COMPANY_ID
    LEFT JOIN price pr ON dr.dt = pr.DATE AND c.ID = pr.COMPANY_ID
),
-- Calculate the position value for each company
company_position AS (
    SELECT
        date,
        COMPANY_ID,
        SECTOR_NAME,
        filled_shares,
        filled_price_usd,
        -- COALESCE returns the first non-null value, defaulting to 0 if both are null
        COALESCE(filled_shares * filled_price_usd, 0) AS position_usd
    FROM filled_data
    -- Filter out rows where we don't have both shares and price data
    WHERE filled_shares IS NOT NULL AND filled_price_usd IS NOT NULL
),
-- Aggregate positions by sector
sector_position AS (
    SELECT 
        date,
        SECTOR_NAME,
        -- Aggregate the position values for each sector
        SUM(position_usd) AS sector_position_usd
    FROM company_position
    GROUP BY date, SECTOR_NAME
),
-- Find the most recent date in the data
latest_date AS (
    -- gets the most recent date
    SELECT MAX(date) AS max_date
    FROM sector_position
),
-- Select the top 10 sectors by position value on the most recent date
top_10_sectors AS (
    SELECT 
        sp.SECTOR_NAME,
        sp.sector_position_usd
    FROM sector_position sp
    -- Join with latest_date to get only the most recent data
    JOIN latest_date ld ON sp.date = ld.max_date
    ORDER BY sp.sector_position_usd DESC
    -- LIMIT clause restricts the output to the top 10 sectors
    LIMIT 10
)
-- Final output: top 10 sectors by position value, in descending order
SELECT 
    SECTOR_NAME,
    sector_position_usd
FROM top_10_sectors
ORDER BY sector_position_usd DESC;