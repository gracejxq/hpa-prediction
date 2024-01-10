import pandas as pd
import matplotlib.pyplot as plt

start_date = '2000-01-01' # earliest year is 2000
end_date = '2023-12-01'
save_path = "visualizations/hpa_supply.png"

# Load the datasets
hpa_data = pd.read_csv('raw_datasets/hpa.csv', parse_dates=[0], index_col=0)
supply_data = pd.read_csv('raw_datasets/supply.csv', parse_dates=[0], index_col=0)

# Filter the datasets for the date range
hpa_data = hpa_data[(hpa_data.index >= start_date) & (hpa_data.index <= end_date)]
supply_data = supply_data[(supply_data.index >= start_date) & (supply_data.index <= end_date)]

# Merge the datasets on the date column
merged_data = pd.merge(hpa_data, supply_data, left_index=True, right_index=True)

# Create a scatter plot
plt.figure(figsize=(10, 6))
plt.scatter(merged_data.iloc[:, 1], merged_data.iloc[:, 0])

# Adding labels and title
plt.xlabel('Supply (total # of housing units)')
plt.ylabel('HPA (MoM % Change)')
plt.title(f'HPA vs Supply ({start_date} to {end_date})')
plt.savefig(save_path)

# Display the plot
plt.show()