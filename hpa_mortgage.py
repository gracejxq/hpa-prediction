import pandas as pd
import matplotlib.pyplot as plt

start_date = '2011-11-01' # earliest year is 2011
end_date = '2023-07-01'
save_path = "visualizations/hpa_mortgage.png"

# Load the datasets
hpa_data = pd.read_csv('datasets/new_wm_dataset.csv', parse_dates=[0], index_col=0)
mortgage_data = pd.read_csv('datasets/new_wm_dataset.csv', parse_dates=[0], index_col=0)

# Filter the datasets for the date range
hpa_data = hpa_data[(hpa_data.index >= start_date) & (hpa_data.index <= end_date)]
hpa_data = hpa_data['HPA_PC']
mortgage_data = mortgage_data[(mortgage_data.index >= start_date) & (mortgage_data.index <= end_date)]
mortgage_data = mortgage_data['MORTGAGE']

# Merge the datasets on the date column
merged_data = pd.merge(hpa_data, mortgage_data, left_index=True, right_index=True)

# Create a scatter plot
plt.figure(figsize=(10, 6))
plt.scatter(merged_data.iloc[:, 1], merged_data.iloc[:, 0])

# Adding labels and title
plt.xlabel('30yr Mortgage Rates (%)')
plt.ylabel('HPA (MoM % Change)')
plt.title(f'HPA vs 30yr Mortgage Rates ({start_date} to {end_date})')
plt.savefig(save_path)

# Display the plot
plt.show()