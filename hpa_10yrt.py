import pandas as pd
import matplotlib.pyplot as plt

start_date = '2011-11-01' # earliest year is 2011
end_date = '2023-07-01'
save_path = "visualizations/hpa_10yrt.png"

# Load the datasets
hpa_data = pd.read_csv('datasets/new_wm_dataset.csv', parse_dates=[0], index_col=0)
treasury_data = pd.read_csv('datasets/new_wm_dataset.csv', parse_dates=[0], index_col=0)

# Filter the datasets for the date range
hpa_data = hpa_data[(hpa_data.index >= start_date) & (hpa_data.index <= end_date)]
hpa_data = hpa_data['HPA_PC']
treasury_data = treasury_data[(treasury_data.index >= start_date) & (treasury_data.index <= end_date)]
treasury_data = treasury_data['TENYRT']

# Merge the datasets on the date column
merged_data = pd.merge(hpa_data, treasury_data, left_index=True, right_index=True)
sorted_merged_data = merged_data.sort_values(by='TENYRT', ascending=True)

# Create a scatter plot
plt.figure(figsize=(10, 6))
plt.scatter(sorted_merged_data.iloc[:, 1], sorted_merged_data.iloc[:, 0])

# Adding labels and title
plt.xlabel('10yr Treasury Yield (%)')
plt.xticks([0, 1, 2, 3, 4, 5])
plt.ylabel('HPA (MoM % Change)')
plt.title(f'HPA vs 10yr Treasury Yield ({start_date} to {end_date})')
plt.savefig(save_path)

# Display the plot
plt.show()