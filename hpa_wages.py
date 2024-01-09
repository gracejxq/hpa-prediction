import pandas as pd
import matplotlib.pyplot as plt

def wages_change():
    start_date = '2010-11-01' # earliest year is 2010
    end_date = '2023-12-01'
    save_path = "visualizations/hpa_wages_change.png"

    # Load the datasets
    hpa_data = pd.read_csv('raw_datasets/hpa.csv', parse_dates=[0], index_col=0)
    wage_data = pd.read_csv('raw_datasets/wages_monthly.csv', parse_dates=[0], index_col=0)

    # Filter the datasets for the date range
    hpa_data = hpa_data[(hpa_data.index >= start_date) & (hpa_data.index <= end_date)]
    wage_data = wage_data[(wage_data.index >= start_date) & (wage_data.index <= end_date)]

    # Merge the datasets on the date column
    merged_data = pd.merge(hpa_data, wage_data, left_index=True, right_index=True)

    # Create a scatter plot
    plt.figure(figsize=(10, 6))
    plt.scatter(merged_data.iloc[:, 1], merged_data.iloc[:, 0])

    # Adding labels and title
    plt.xlabel('Wages (real avg earnings/hr)')
    plt.ylabel('HPA (MoM % Change)')
    plt.title(f'HPA vs Wages ({start_date} to {end_date})')
    plt.savefig(save_path)

    # Display the plot
    plt.show()

def wages():
    start_date = '2010-01-01' # earliest year is 2010
    end_date = '2023-12-01'
    save_path = "visualizations/hpa_wages.png"

    # Load the datasets
    hpa_data = pd.read_csv('raw_datasets/hpai.csv', parse_dates=[0], index_col=0)
    wage_data = pd.read_csv('raw_datasets/wages_monthly.csv', parse_dates=[0], index_col=0)

    # Filter the datasets for the date range
    hpa_data = hpa_data[(hpa_data.index >= start_date) & (hpa_data.index <= end_date)]
    wage_data = wage_data[(wage_data.index >= start_date) & (wage_data.index <= end_date)].diff() / wage_data[(wage_data.index >= start_date) & (wage_data.index <= end_date)].shift(1) * 100

    # Merge the datasets on the date column
    merged_data = pd.merge(hpa_data, wage_data, left_index=True, right_index=True)

    # Create a scatter plot
    plt.figure(figsize=(10, 6))
    plt.scatter(merged_data.iloc[:, 1], merged_data.iloc[:, 0])

    # Adding labels and title
    plt.xlabel('Change in Wages (MoM % Change)')
    plt.ylabel('HPA (MoM % Change)')
    plt.title(f'HPA vs Change in Wages ({start_date} to {end_date})')
    plt.savefig(save_path)

    # Display the plot
    plt.show()

wages()