### INF601 - Advanced Programming in Python
### Sokly Hour
### Mini Project 2

import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Create a folder to save charts if it doesn't exist
def make_dir():
    Path('charts').mkdir(exist_ok=True)

# Function to load and clean the job market data from a CSV file
def retrieve_clean_data():
    # Load the data into a pandas DataFrame
    aiJobMarket = pd.read_csv("ai_job_market_insights.csv", index_col=0)
    
    # Ensure that 'Salary_USD' is a string type first
    aiJobMarket['Salary_USD'] = aiJobMarket['Salary_USD'].astype(str)
    
    # Remove commas and convert to float, handling any conversion errors
    aiJobMarket['Salary_USD'] = aiJobMarket['Salary_USD'].str.replace(',', '')
    
    # Convert to numeric, forcing errors to NaN and then filling with 0 if needed
    aiJobMarket['Salary_USD'] = pd.to_numeric(aiJobMarket['Salary_USD'], errors='coerce').fillna(0)
    
    return aiJobMarket

# 1. Function to plot average salary by industry
def plot_average_salary_by_industry(df):
    # Calculate the average salary for each industry
    avg_salary = df.groupby('Industry')['Salary_USD'].mean().sort_values()
    
    # Create a horizontal bar chart
    plt.figure(figsize=(12, 8))
    avg_salary.plot(kind='barh', color='skyblue', edgecolor='black')
    plt.title('Average Salary by Industry', fontsize=18)
    plt.xlabel('Average Salary (USD)', fontsize=16)
    plt.ylabel('Industry', fontsize=16)
    plt.grid(axis='x', linestyle='--', alpha=1)
    plt.tight_layout()
    plt.savefig('charts/average_salary_by_industry.png')
    plt.clf()  # Clear the plot for the next chart

# 2. Function to plot job count by required skills
def plot_job_count_by_skills(df):
    # Count how many times each skill appears
    job_count = df['Required_Skills'].value_counts().sort_values()
    
    # Create a vertical bar chart
    plt.figure(figsize=(12, 6))
    plt.bar(job_count.index, job_count.values, color='skyblue', edgecolor='black')
    plt.title('Job Count by Required Skills', fontsize=16)
    plt.xlabel('Required Skills', fontsize=12)
    plt.ylabel('Number of Jobs', fontsize=12)
    plt.xticks(rotation=45, ha='right')  # Rotate skill names for better readability
    
    # Add numbers on top of each bar
    for i, value in enumerate(job_count.values):
        plt.text(i, value + 0.1, str(value), ha='center', fontsize=10)

    plt.tight_layout()
    plt.savefig('charts/job_count_by_skills.png')
    plt.clf()

# 3. Function to plot job count by industry and AI adoption level
def plot_grouped_job_count_by_industry_ai_adoption(df):
    # Create a table showing job counts by industry and AI adoption level
    job_count_by_industry = pd.crosstab(df['Industry'], df['AI_Adoption_Level'])
    
    # Create a grouped bar chart
    ax = job_count_by_industry.plot(kind='bar', figsize=(12, 6), color=['lightblue', 'salmon', 'lightgreen'])
    
    # Add numbers on top of each bar
    for container in ax.containers:
        for bar in container:
            height = bar.get_height()
            ax.annotate(f'{int(height)}',  # Display the count as an integer
                        xy=(bar.get_x() + bar.get_width() / 2, height),  # Position above the bar
                        ha='center', va='bottom')

    # Calculate and display the total job count for each industry
    total_counts = job_count_by_industry.sum(axis=1)
    for i, total in enumerate(total_counts):
        ax.annotate(f'Total: {total}',
                    xy=(i, total + 1),  # Position slightly above the last bar
                    ha='center', va='bottom', fontsize=10, color='black', weight='bold')

    # Customize the plot
    plt.title('Job Count by Industry and AI Adoption Level', fontsize=16)
    plt.xlabel('Industry', fontsize=12)
    plt.ylabel('Job Count', fontsize=12)
    plt.legend(title='AI Adoption Level', fontsize=10)
    plt.grid(True, axis='y', linestyle='--', alpha=0.7)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    
    # Save the figure
    plt.savefig('charts/grouped_job_count_by_industry_ai_adoption.png')
    plt.clf()

# 4. Function to plot average salary by location
def plot_average_salary_by_location(df):
    # Group data by location and calculate average salary
    avg_salary_by_location = df.groupby('Location')['Salary_USD'].mean().sort_values()
    
    # Create a bar chart
    plt.figure(figsize=(12, 8))
    bars = avg_salary_by_location.plot(kind='bar', color='salmon', edgecolor='black')
    plt.title('Average Salary by Location', fontsize=16)
    plt.xlabel('Location', fontsize=14)
    plt.ylabel('Average Salary (USD)', fontsize=14)
    plt.xticks(rotation=45, ha='right', fontsize=12)
    
    # Add numbers on top of each bar
    for bar in bars.patches:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, height + 1000,
                 ha='center', va='bottom', fontsize=12)

    plt.grid(True, axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig('charts/average_salary_by_location.png')
    plt.clf()

# Function to inspect column names in the dataset
def inspect_columns(df):
    print("Column names in the dataset:", df.columns)

# Main function to execute the script
def main():
    make_dir()  # Create the 'charts' folder
    aiJobMarket = retrieve_clean_data()  # Load and clean the data
    inspect_columns(aiJobMarket)  # Show column names
    # Generate charts
    plot_average_salary_by_industry(aiJobMarket) 
    plot_job_count_by_skills(aiJobMarket)
    plot_grouped_job_count_by_industry_ai_adoption(aiJobMarket)
    plot_average_salary_by_location(aiJobMarket)

if __name__ == "__main__":
    main()
