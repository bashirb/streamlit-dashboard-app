# Financial Market Analysis Dashboard with Streamlit

This repository contains a Streamlit-based web application that provides a financial market analysis dashboard. The dashboard retrieves data from a Snowflake database and visualizes it using Altair charts. The project is structured to load SQL queries from files, execute them against a Snowflake database, and display the results interactively.

![app_gif](https://github.com/user-attachments/assets/02a8dedc-af6a-4ad3-ac57-be69add2344b)

## Features

- **Top 10 Sectors by Position (USD):** Visualizes the top 10 sectors based on their financial positions.
- **Top 25% Companies Latest Data:** Displays the latest data for the top 25% of companies.
- **Daily Close Price Timeseries:** Provides a timeseries chart of the daily closing price for a selected company.

## Project structure

- **`app.py`:** The main application file containing the Streamlit app code.
- **`queries/`:** Directory containing SQL query files used by the app.
- **`.env`:** Environment file for storing credentials (not included in the repo, needs to be created by the user).

## Installation

To run this project locally, follow these steps:

1.  **Ensure You Have Python 3 or Above**

    Make sure you have Python 3.9 or above installed on your system. You can check your Python version by running:

    ```bash
    python --version

    ```

2.  **Clone the Repository**

    First, clone the repository to your local machine and navigate into the project directory:

    ```bash
    git clone https://github.com/bashirb/streamlit-dashboard-app.git
    cd streamlit-dashboard-app

    ```

3.  **Create and Activate a Virtual Environment (Optional but Recommended)**

    It's recommended to create a virtual environment to manage the project's dependencies in isolation:

        python3 -m venv venv
        source venv/bin/activate # On Windows, use `venv\Scripts\activate`

4.  **Install Required Packages**

    Install the necessary Python packages specified in the requirements.txt file:

        pip install -r requirements.txt

    This command will install all the libraries required for the project, such as Streamlit, Snowflake connector, Pandas, and Altair.

5.  **Set Up Snowflake Credentials**

    The app connects to a Snowflake database using credentials that need to be set in an .env file. Create a .env file in the root directory of the project and add your Snowflake username and password:

        user_name=your_username
        password=your_password

    Replace your_username and your_password with your actual Snowflake credentials. The app will read these values when it runs, ensuring secure access to the database.

    **Important Note:**

    The credentials provided are specifically relevant to the following Snowflake database configuration:

        Account: ui76830.west-europe.azure
        Database: CODE_CHALLENGE_ZHEWNTMM
        Schema: SOURCE
        Warehouse: GUEST_CODE_CHALLENGE_ZHEWNTMM
        Role: GUEST_CODE_CHALLENGE_ZHEWNTMM

6.  **Run the Application**

    Start the Streamlit application using the following command:

        streamlit run app.py

    After running this command, the app will be accessible at http://localhost:8501 by default. Open this URL in your web browser to interact with the dashboard.

## Usage

Once the app is running, you can explore various sections of the dashboard:

- Top 10 Sectors by Position (USD): View the top 10 sectors based on financial positions.
- Top 25% Companies Latest Data: Examine the latest data for the top 25% of companies.
- Daily Close Price Timeseries: Select a company from the dropdown to view its daily closing price over time.

## Project files

- app.py: The main script that runs the Streamlit dashboard.
- top_10_sectors.sql: SQL query file to retrieve data for the "Top 10 Sectors by Position (USD)" section.
- top_25_percent_data.sql: SQL query file to retrieve data for the -"Top 25% Companies Latest Data" section.
- companies_names.sql: SQL query file to get the list of companies for the "Daily Close Price Timeseries" section.
