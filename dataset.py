import numpy as np
import pandas as pd
from datetime import datetime
# import random
# import torch

# filepaths for raw data
hpi = "datasets/hpi.csv"
ten_yrt = "datasets/10yr_treasury.csv" # henry
unemployment = "datasets/unemployment.csv" # grace
wages = "datasets/wages_monthly.csv" # chris
# wages = "datasets/wages_quarterly.csv"
supply = "datasets/supply.csv" # daniel

# rates of data collection for input types
daily = {ten_yrt}
if wages == "datasets/wages_monthly.csv":
    monthly = {unemployment, wages}
    quarterly = {supply}
else:
    monthly = {unemployment}
    quarterly = {wages, supply}

# save path for final dataset
toggle = "_supply_monthly.csv" if wages == "datasets/wages_monthly.csv" else "_wages_quarterly.csv"
save_path = "datasets/dataset" + toggle

# def splitDataset(x, y):
#     x_train = 
#     x_val = 
#     x_test = 
#     y_train = 
#     y_val = 
#     y_test = 
#     return 
#     print("Dataset split into training, validation, and testing sets")

def hpaCalculator(year1, year2):
    return (year2 - year1) / year1 * 100

def wage_date_parser(date_str):
    return datetime.strptime(date_str, '%b \'%y')

# Function to construct a dataset with inputs from 10 year treasury rates, unemployment rates,
# wages, and housing supply & outputs the HPA index; daily increments
def constructDataset():
    # convert all csv files to dataframes & parse dates
    hpi_df = pd.read_csv(hpi, parse_dates=['DATE'])
    ten_yrt_df = pd.read_csv(ten_yrt, parse_dates=['DATE'])
    unemployment_df = pd.read_csv(unemployment, parse_dates=['DATE'])
    # special date parse function for nonstandard dates in wages
    wages_df = pd.read_csv(wages, parse_dates=['DATE'])
    #wages_df = pd.read_csv(wages, parse_dates=['DATE'], date_parser=wage_date_parser)
    supply_df = pd.read_csv(supply, parse_dates=['DATE'])

    hpi_df.set_index('DATE', inplace=True)
    ten_yrt_df.set_index('DATE', inplace=True)
    unemployment_df.set_index('DATE', inplace=True)
    wages_df.set_index('DATE', inplace=True)
    supply_df.set_index('DATE', inplace=True)

    # find latest start year & earliest end year
    latest_start = max([df.index.min() for df in [hpi_df, ten_yrt_df, unemployment_df, wages_df, supply_df]])
    earliest_end = min([df.index.max() for df in [hpi_df, ten_yrt_df, unemployment_df, wages_df, supply_df]])

    print(latest_start)
    print(earliest_end)

    # filter each dataframe to start from  latest start year
    hpi_df = hpi_df[hpi_df.index.year >= latest_start.year]
    ten_yrt_df = ten_yrt_df[ten_yrt_df.index.year >= latest_start.year]
    unemployment_df = unemployment_df[unemployment_df.index.year >= latest_start.year]
    wages_df = wages_df[wages_df.index.year >= latest_start.year]
    supply_df = supply_df[supply_df.index.year >= latest_start.year]

    combined_df = pd.concat([hpi_df, ten_yrt_df, unemployment_df, wages_df, supply_df], axis=1)
    combined_df.fillna(method='ffill', inplace=True)

    print(combined_df)

    #combined_df.to_csv(save_path)
    #splitDataset(input, output)
    print("Created HPA index dataset from dataset.py")

def main():
    constructDataset()

if __name__ == '__main__': 
    main()