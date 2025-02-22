# pip install pandas matplotlib fredapi plotly nbformat requests

import pandas as pd
import matplotlib.pyplot as plt
from fredapi import Fred
from datetime import datetime
from dotenv import load_dotenv
import os

# Set pandas parameters
pd.set_option("display.max_colwidth", 1000)

# Load environment variables from .env file
load_dotenv()

FRED_API_KEY = os.getenv("FRED_API_KEY")
if FRED_API_KEY is None:
    raise ValueError("FRED_API_KEY environment variable not set")


# Search for state indicators
fred = Fred(api_key=FRED_API_KEY)
results = fred.search(
    "Homeownership", limit=10, order_by="popularity", sort_order="desc"
)

list_states = [
    "WV",
    "FL",
    "IL",
    "MN",
    "MD",
    "RI",
    "ID",
    "NH",
    "NC",
    "VT",
    "CT",
    "DE",
    "NM",
    "CA",
    "NJ",
    "WI",
    "OR",
    "NE",
    "PA",
    "WA",
    "LA",
    "GA",
    "AL",
    "UT",
    "OH",
    "TX",
    "CO",
    "SC",
    "OK",
    "TN",
    "WY",
    "HI",
    "ND",
    "KY",
    "VI",
    "MP",
    "GU",
    "ME",
    "NY",
    "NV",
    "AK",
    "AS",
    "MI",
    "AR",
    "MS",
    "MO",
    "MT",
    "KS",
    "IN",
    "PR",
    "SD",
    "MA",
    "VA",
    "DC",
    "IA",
    "AZ",
]


def collect_state_data(
    api_key, state_codes, series_suffix, observation_start="2000-01-01"
):
    """
    Retrieve employment data for each US state from FRED API and compile into a single DataFrame.

    Parameters:
    - api_key (str): Your FRED API key.
    - state_codes (list): List of state codes, e.g., ['TX', 'CA', 'NY', ...].
    - observation_start (str): The start date for retrieving data (YYYY-MM-DD).

    Returns:
    - pd.DataFrame: DataFrame with employment data for each state, indexed by date.
    """
    # Initialize FRED client
    fred = Fred(api_key=api_key)

    # Create an empty DataFrame to store all state data
    all_data = pd.DataFrame()

    # Loop over each state code
    for state_code in state_codes:
        series_id = f"{state_code}{series_suffix}"  # Construct the series ID
        try:
            # Retrieve data for the specific state
            data = fred.get_series(series_id, observation_start=observation_start)
            # Add the state's data to the main DataFrame
            all_data[state_code] = data
        except Exception as e:
            print(f"Error retrieving data for {state_code}: {e}")

    return all_data


data = collect_state_data(
    api_key=FRED_API_KEY,
    state_codes=list_states,
    series_suffix="HOWN",
    observation_start="1984-01-01",
)


# Get today's date in YYYYMMDD format
today_date = datetime.today().strftime("%Y%m%d")

# Save the data to a CSV file with today's date appended
data.to_csv(f"../data/raw/homeownership_state_{today_date}.csv", index=True)
