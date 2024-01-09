# Creates a dataset from HPI, HPA, treasury rates, unemployment rates, wages, and supply. 
# HPA is calculated from HPI raw data. TVT split is 70-15-15. 
# For the dataset generated from wages_monthly data (as opposed to wages_quarterly):
#   train has 2247 examples, val has 481 examples, and test has 483 examples.
# For the dataset generated from wages_quarterly data (as opposed to wages_monthly):
#   train has 4126 examples, val has 884 examples, and test has 885 examples.

import numpy as np
import pandas as pd
from datetime import datetime
from pprint import pprint

# filepaths for raw data
hpi = "raw_datasets/hpi.csv"
ten_yrt = "raw_datasets/10yr_treasury.csv" 
unemployment = "raw_datasets/unemployment.csv" 
wages = "raw_datasets/wages_monthly.csv" 
# wages = "raw_datasets/wages_quarterly.csv"
wages_quarterly = "raw_datasets/wages_quarterly.csv"
supply = "raw_datasets/supply.csv" 

# save path toggle (based on which wage data being used) for final dataset split
toggle = "wm_" if wages == "raw_datasets/wages_monthly.csv" else "wq_"

def splitDataset(dataset, train=0.7, val=0.15, test=0.15):
    if (train + val + test != 1):
        raise Exception("Train, val, test split is invalid -- must sum to 1")
    
    # shuffle data points before splitting to guarantee randomness
    # DO NOT CHANGE RANDOM_STATE VALUE... ensures reproducibility (like a seed value)
    dataset = dataset.sample(frac=1, random_state=1)
    
    total_rows = dataset.shape[0]
    train_end = int(total_rows * train)
    val_end = train_end + int(total_rows * val)
    train = dataset.iloc[:train_end]
    val = dataset.iloc[train_end:val_end]
    test = dataset.iloc[val_end:]

    # print("TRAIN")
    # print(train)
    # print("VAL")
    # print(val)
    # print("TEST")

    print("2. Dataset successfully split into training, validation, and testing sets")
    print("     Training size:  ", train.shape[0], "data points with", train.shape[1], "dimensions")
    print("     Validation size:", val.shape[0], "data points with", val.shape[1], "dimensions")
    print("     Testing size:   ", test.shape[0], "data points with", test.shape[1], "dimensions")
    
    return train, val, test

# Function to construct a dataset with inputs from 10 year treasury rates, unemployment rates,
# wages, and housing supply & outputs the HPA index; daily increments
def constructDataset():
    # convert all csv files to dataframes & parse dates
    hpi_df = pd.read_csv(hpi, parse_dates=['DATE'])
    ten_yrt_df = pd.read_csv(ten_yrt, parse_dates=['DATE'])
    unemployment_df = pd.read_csv(unemployment, parse_dates=['DATE'])
    wages_df = pd.read_csv(wages, parse_dates=['DATE'])
    supply_df = pd.read_csv(supply, parse_dates=['DATE'])

    # create hpa (housing price appreciation index) data from hpi data
    hpa_values = (hpi_df["VAL"].diff() / hpi_df["VAL"].shift(12)) * 100 # 12 for months in a year, hpa is annual
    hpa_df = pd.DataFrame({
        "DATE": hpi_df["DATE"][1:],
        "HPA": hpa_values[1:]
    })
    hpa_df.to_csv("raw_datasets/hpa.csv", index=False)

    print("1. HPA Index data successfully extrapolated from HPI data")

    # let the date be the index for all dataframes
    for df in [hpi_df, hpa_df, ten_yrt_df, unemployment_df, wages_df, supply_df]:
        df.set_index('DATE', inplace=True)
    
    # find latest start year & earliest end year
    latest_start = max([df.index.min() for df in [hpi_df, hpa_df, ten_yrt_df, unemployment_df, wages_df, supply_df]])
    earliest_end = min([df.index.max() for df in [hpi_df, hpa_df, ten_yrt_df, unemployment_df, wages_df, supply_df]])

    # merge into single dataframe
    combined_df = pd.concat([hpi_df, hpa_df, ten_yrt_df, unemployment_df, wages_df, supply_df], axis=1)
    combined_df.ffill(inplace=True)
    combined_df = combined_df[(combined_df.index >= latest_start) & (combined_df.index <= earliest_end)]
    combined_df.columns = ['HPI', 'HPA', 'TENYRT', 'UNEMPLOYMENT', 'WAGES', 'SUPPLY']

    # parse out rows with invalid entries (some tenyrt values are just "." in the csv)
    combined_df = combined_df.apply(pd.to_numeric, errors='coerce')
    combined_df = combined_df.dropna()

    combined_df.reset_index(drop=False, inplace=True) # uncomment to add dates back in to the final datasets
    combined_df.to_csv("datasets/" + toggle + "dataset.csv", index=False)

    # pprint(combined_df)

    print("3. Dataset successfully constructed of size:", combined_df.shape[0], "data points with", combined_df.shape[1], "dimensions")

    return combined_df

def cleanWagesQuarterly():
    wages_df_quarterly = pd.read_csv(wages_quarterly, parse_dates=['DATE'])
    wages_df_quarterly.iloc[:, 1] = wages_df_quarterly.iloc[:, 1] / 40
    wages_df_quarterly.to_csv(wages_quarterly, index=False) # replace old wages_quarterly data

def main():
    # DO NOT UNCOMMENT, already cleaned (divided by 40 hours for hourly wage instead of weekly wage)
    # cleanWagesQuarterly()

    dataset = constructDataset()
    train, val, test = splitDataset(dataset)

    train.to_csv("datasets/" + toggle + "train.csv", index=False)
    val.to_csv("datasets/" + toggle + "val.csv", index=False)
    test.to_csv("datasets/" + toggle + "test.csv", index=False)

    print("4. Dataset split successfully saved as csv files")

if __name__ == '__main__': 
    main()