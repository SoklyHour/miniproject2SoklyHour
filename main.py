import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Ensure the 'charts' directory exists
def make_dir():
    try:
        Path('charts').mkdir()
    except FileExistsError:
        pass

# Load and clean data
def retrieve_clean_data():
    aiJobMarket = pd.read_csv("miniproject2SoklyHour/ai_job_market_insights.csv", index_col=0)

    # Convert the 'Salary_USD' column to string, so we can manipulate the data as text
    aiJobMarket['Salary_USD'] = aiJobMarket['Salary_USD'].astype(str)

    # Remove commas from the salary values (ex:"100,000" becomes "100000")
    aiJobMarket['Salary_USD'] = aiJobMarket['Salary_USD'].str.replace(',', '')

    # Convert the cleaned-up salary values back to numeric (numbers)
    # errors='coerce' means if there are any values that can't be converted, they will be replaced with NaN (Not a Number) instead of causing an error
    aiJobMarket['Salary_USD'] = pd.to_numeric(aiJobMarket['Salary_USD'], errors='coerce')

    return aiJobMarket
