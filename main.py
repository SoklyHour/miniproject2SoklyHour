### INF601 - Advanced Programming in Python
### Sokly Hour
### Mini Project 2

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

# Create a 'charts' folder if it doesn't exist
def make_dir():
    Path('charts').mkdir(exist_ok=True)

# Function to load and clean the data from a CSV file
def retrieve_clean_data():
    aiJobMarket = pd.read_csv("ai_job_market_insights.csv", index_col=0)
    aiJobMarket['Salary_USD'] = aiJobMarket['Salary_USD'].str.replace(',', '').astype(float)
    return aiJobMarket

# Function to load and clean the data from a CSV file
def retrieve_clean_data():
    # Read the CSV file into a pandas dataframe (a table-like structure)
    aiJobMarket = pd.read_csv("ai_job_market_insights.csv", index_col=0)  # 'index_col=0' means the first column is used as the row index

    # Convert the 'Salary_USD' column to strings to prepare for cleaning
    aiJobMarket['Salary_USD'] = aiJobMarket['Salary_USD'].astype(str)

    # Remove commas from the salary values (e.g., "100,000" becomes "100000")
    aiJobMarket['Salary_USD'] = aiJobMarket['Salary_USD'].str.replace(',', '')

    # Convert the salary column back to numbers (so we can do calculations)
    # 'errors="coerce"' will turn invalid entries (like text) into NaN (Not a Number)
    aiJobMarket['Salary_USD'] = pd.to_numeric(aiJobMarket['Salary_USD'], errors='coerce')

    # Return the cleaned data for further analysis
    return aiJobMarket

# 1. Function to plot the average salary for each industry
def plot_average_salary_by_industry(df):
    # Group the data by 'Industry' and calculate the average salary for each one
    avg_salary = df.groupby('Industry')['Salary_USD'].mean().sort_values()
    
    # Create a horizontal bar chart to visualize the data
    plt.figure(figsize=(12, 8))  # Set the size of the chart
    avg_salary.plot(kind='barh', color='skyblue', edgecolor='black')  # 'barh' creates a horizontal bar chart
    
    # Set the title and labels with larger font sizes for readability
    plt.title('Average Salary by Industry', fontsize=18)
    plt.xlabel('Average Salary (USD)', fontsize=16)
    plt.ylabel('Industry', fontsize=16)
    
    # Add grid lines to make it easier to read
    plt.grid(axis='x', linestyle='--', alpha=1)
    
    # Adjust the layout to ensure everything fits
    plt.tight_layout()
    
    # Save the chart as a PNG file in the 'charts' folder
    plt.savefig('charts/average_salary_by_industry.png')
    
    # Clear the plot to free up memory (prepares for the next chart)
    plt.clf()

# 2. Function to plot the count of jobs for each required skill
def plot_job_count_by_skills(df):
    # Count how many times each skill appears and sort the result
    job_count = df['Required_Skills'].value_counts().sort_values()

    # Create a vertical bar chart
    plt.figure(figsize=(12, 6))  # Set the chart size
    plt.bar(job_count.index, job_count.values, color='skyblue', edgecolor='black')  # 'bar' creates a vertical bar chart

    # Set the title and axis labels
    plt.title('Job Count by Required Skills', fontsize=16, fontweight='bold')
    plt.xlabel('Required Skills', fontsize=12)
    plt.ylabel('Number of Jobs', fontsize=12)

    # Rotate the x-axis labels (the skill names) so they fit better
    plt.xticks(rotation=45, ha='right')

    # Add numbers on top of each bar to show the exact count
    for i, value in enumerate(job_count.values):
        plt.text(i, value + 0.1, str(value), ha='center', fontsize=10)

    # Save the chart as a PNG file
    plt.tight_layout()
    plt.savefig('charts/job_count_by_skills_simple.png')
    plt.clf()
# 3. Function to plot the number of jobs by industry and AI adoption level (Grouped bar chart)
def plot_grouped_job_count_by_industry_ai_adoption(df):
    # Create a table showing the number of jobs by industry and AI adoption level
    job_count_by_industry = pd.crosstab(df['Industry'], df['AI_Adoption_Level'])

    # Create a grouped bar chart
    ax = job_count_by_industry.plot(kind='bar', figsize=(12, 6), color=['lightblue', 'salmon', 'lightgreen'], width=0.8)

    # Set the title and axis labels
    plt.title('Job Count by Industry and AI Adoption Level (Grouped)', fontsize=16, fontweight='bold')
    plt.xlabel('Industry', fontsize=12)
    plt.ylabel('Job Count', fontsize=12)

    # Add a legend (key) explaining the colors
    plt.legend(title='AI Adoption Level', fontsize=10)

    # Add grid lines for better readability
    plt.grid(True, axis='y', linestyle='--', alpha=0.7)

    # Rotate the x-axis labels slightly so they fit better
    plt.xticks(rotation=45, ha='right')

    # Add numbers on top of each bar
    for container in ax.containers:
        for bar in container:
            height = bar.get_height()
            ax.annotate(f'{int(height)}', 
                        xy=(bar.get_x() + bar.get_width() / 2, height), 
                        ha='center', va='bottom', fontsize=10)

    # Save the chart
    plt.tight_layout()
    plt.savefig('charts/grouped_job_count_by_industry_ai_adoption.png')
    plt.clf()

# 4. Function to plot the average salary for each location
def plot_average_salary_by_location(df):
    # Ensure 'Salary_USD' is numeric in case there are any issues
    df['Salary_USD'] = pd.to_numeric(df['Salary_USD'].astype(str).str.replace(',', ''), errors='coerce')
    
    # Group the data by 'Location' and calculate the average salary
    avg_salary_by_location = df.groupby('Location')['Salary_USD'].mean().sort_values()
    
    # Create a bar chart
    plt.figure(figsize=(12, 8))
    bars = avg_salary_by_location.plot(kind='bar', color='salmon', edgecolor='black', alpha=0.8)

    # Set the title and labels
    plt.title('Average Salary by Location', fontsize=16, fontweight='bold', color='darkred')
    plt.xlabel('Location', fontsize=14)
    plt.ylabel('Average Salary (USD)', fontsize=14)
    
    # Rotate the x-axis labels for readability
    plt.xticks(rotation=45, ha='right', fontsize=12)
    
    # Add numbers on top of each bar to show the exact value
    for bar in bars.patches:
        # Get the height (value) of each bar
        height = bar.get_height()
        
        # Place the number slightly above the bar
        plt.text(bar.get_x() + bar.get_width() / 2,  # Horizontal position: center of the bar
                height + 1000,                      # Vertical position: just above the bar
                f'{height:,.0f}',                   # Format the number without decimal places
                ha='center', va='bottom', fontsize=12)  # Align center horizontally, bottom vertically
        
    # Add grid lines for easier reading
    plt.grid(True, axis='y', linestyle='--', alpha=0.7)

    # Save the chart
    plt.tight_layout()
    plt.savefig('charts/average_salary_by_location.png')
    plt.clf()

# Helper function to inspect column names in the dataset
def inspect_columns(df):
    print("Column names in the dataset:", df.columns)

# The main function that ties everything together
def main():
    make_dir()  # Create the 'charts' folder
    aiJobMarket = retrieve_clean_data()  # Load and clean the data
    
    # Show the column names in the dataset
    inspect_columns(aiJobMarket)

    # Generate the charts
    plot_average_salary_by_industry(aiJobMarket)  # Average Salary by Industry
    plot_job_count_by_skills(aiJobMarket)  # Job Count by Required Skills
    plot_grouped_job_count_by_industry_ai_adoption(aiJobMarket)  # Grouped Job Count by Industry and AI Adoption
    plot_average_salary_by_location(aiJobMarket)  # Average Salary by Location

# Run the program
if __name__ == "__main__":
    main(), 