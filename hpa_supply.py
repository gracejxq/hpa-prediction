import pandas as pd
import matplotlib.pyplot as plt

def supply_change():
    start_date = '2011-11-01' # earliest year is 2011
    end_date = '2023-07-01'
    save_path = "visualizations/hpa_supply_change.png"

    # Load the datasets
    hpa_data = pd.read_csv('datasets/new_wm_dataset.csv', parse_dates=[0], index_col=0)
    supply_data = pd.read_csv('datasets/new_wm_dataset.csv', parse_dates=[0], index_col=0)

    # Filter the datasets for the date range
    hpa_data = hpa_data[(hpa_data.index >= start_date) & (hpa_data.index <= end_date)]
    hpa_data = hpa_data['HPA_PC']
    supply_data = supply_data[(supply_data.index >= start_date) & (supply_data.index <= end_date)]
    supply_data = supply_data['SUPPLY_PC']

    # Merge the datasets on the date column
    merged_data = pd.merge(hpa_data, supply_data, left_index=True, right_index=True)
    merged_data['Year'] = merged_data.index.year

    # Create a scatter plot
    plt.figure(figsize=(10, 6))
    # plt.scatter(merged_data.iloc[:, 1], merged_data.iloc[:, 0])
    cmap = plt.get_cmap('viridis')
    unique_years = sorted(merged_data['Year'].unique())
    color_dict = {year: cmap(i / len(unique_years)) for i, year in enumerate(unique_years)}
    for year in unique_years:
        subset = merged_data[merged_data['Year'] == year]
        plt.scatter(subset.iloc[:, 1], subset.iloc[:, 0], color=color_dict[year], label=year)

    # Adding labels and title
    plt.xlabel('Change in Supply (MoM % Change)')
    plt.ylabel('HPA (MoM % Change)')
    plt.title(f'HPA vs Supply Growth ({start_date} to {end_date})')
    plt.legend(title='Year', loc='upper right', bbox_to_anchor=(1.1, 1))
    plt.savefig(save_path)

    # Display the plot
    plt.show()

def supply():
    start_date = '2011-11-01' # earliest year is 2011
    end_date = '2023-07-01'
    save_path = "visualizations/hpi_supply.png"

    # Load the datasets
    hpa_data = pd.read_csv('datasets/new_wm_dataset.csv', parse_dates=[0], index_col=0)
    supply_data = pd.read_csv('datasets/new_wm_dataset.csv', parse_dates=[0], index_col=0)

    # Filter the datasets for the date range
    hpa_data = hpa_data[(hpa_data.index >= start_date) & (hpa_data.index <= end_date)]
    hpa_data = hpa_data['HPI']
    supply_data = supply_data[(supply_data.index >= start_date) & (supply_data.index <= end_date)]
    supply_data = supply_data['SUPPLY']

    # Merge the datasets on the date column
    merged_data = pd.merge(hpa_data, supply_data, left_index=True, right_index=True)
    merged_data['Year'] = merged_data.index.year

    # Create a scatter plot
    plt.figure(figsize=(10, 6))
    # plt.scatter(merged_data.iloc[:, 1], merged_data.iloc[:, 0])
    cmap = plt.get_cmap('viridis')
    unique_years = sorted(merged_data['Year'].unique())
    color_dict = {year: cmap(i / len(unique_years)) for i, year in enumerate(unique_years)}
    for year in unique_years:
        subset = merged_data[merged_data['Year'] == year]
        plt.scatter(subset.iloc[:, 1], subset.iloc[:, 0], color=color_dict[year], label=year)

    # Adding labels and title
    plt.xlabel('Supply (total # of housing units)')
    plt.ylabel('HPI')
    plt.title(f'HPI vs Supply ({start_date} to {end_date})')
    plt.legend(title='Year', loc='upper right', bbox_to_anchor=(1.1, 1))
    plt.savefig(save_path)

    # Display the plot
    plt.show()

# Toggle between graphing 0th order or 1st order changes
supply()
# supply_change()