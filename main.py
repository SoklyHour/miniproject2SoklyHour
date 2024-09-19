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
    aiJobMarket = pd.read_csv("ai_job_market_insights.csv", index_col=0)

    # Convert the 'Salary_USD' column to string, so we can manipulate the data as text
    aiJobMarket['Salary_USD'] = aiJobMarket['Salary_USD'].astype(str)

    # Remove commas from the salary values (ex:"100,000" becomes "100000")
    aiJobMarket['Salary_USD'] = aiJobMarket['Salary_USD'].str.replace(',', '')

    # Convert the cleaned-up salary values back to numeric (numbers)
    # errors='coerce' means if there are any values that can't be converted, they will be replaced with NaN (Not a Number) instead of causing an error
    aiJobMarket['Salary_USD'] = pd.to_numeric(aiJobMarket['Salary_USD'], errors='coerce')

    return aiJobMarket

# 1. Average Salary by Industry
def plot_average_salary_by_industry(df):
    # Calculate average salary by industry
    avg_salary = df.groupby('Industry')['Salary_USD'].mean().sort_values()
    
    # Create a figure with a larger size for better readability
    plt.figure(figsize=(12, 8))
    
    # Plot the average salary using kind='barh'(horizontal bar chart)
    avg_salary.plot(kind='barh', color='skyblue', edgecolor='black')
    
    # Add a title and axis labels with a larger font size for better readability
    plt.title('Average Salary by Industry', fontsize=18)
    plt.xlabel('Average Salary (USD)', fontsize=16)
    plt.ylabel('Industry', fontsize=16)
    
    # Add grid lines for easier reading of values
    plt.grid(axis='x', linestyle='--', alpha=1)
    
    # Ensure that the layout is adjusted to fit the plot elements
    plt.tight_layout()
    
    # Save the plot to a file
    plt.savefig('charts/average_salary_by_industry.png')
    
    # Clear the figure to free up memory
    plt.clf()



# Helper function to inspect column names
def inspect_columns(df):
    print("Column names in the dataset:", df.columns)

def main():
    make_dir()
    aiJobMarket = retrieve_clean_data()
    
    # Inspect the column names
    inspect_columns(aiJobMarket)

    # Proceed with the rest of the plots
    plot_average_salary_by_industry(aiJobMarket)  # Q1: Salary by Industry

if __name__ == "__main__":
    main()
