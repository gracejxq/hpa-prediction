# Creates a dataset from HPI, HPAI, treasury rates, unemployment rates, wages, and supply. 
# HPAI is calculated from HPI raw data. TVT split is 70-15-15. 
# For the dataset generated from wages_monthly data (as opposed to wages_quarterly):
#   train has 2248 examples, val has 482 examples, and test has 484 examples.
# For the dataset generated from wages_quarterly data (as opposed to wages_monthly):
#   dataset has yet to be generated. REMINDER: must divide values by 40 bc wages are weekly

import numpy as np
import pandas as pd
from datetime import datetime
from pprint import pprint

# filepaths for raw data
hpi = "datasets/hpi.csv"
ten_yrt = "datasets/10yr_treasury.csv" 
unemployment = "datasets/unemployment.csv" 
wages = "datasets/wages_monthly.csv" 
# wages = "datasets/wages_quarterly.csv"
supply = "datasets/supply.csv" 

# save path toggle (based on which wage data being used) for final dataset split
toggle = "_wm" if wages == "datasets/wages_monthly.csv" else "_wq"

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

    print("Dataset successfully split into training, validation, and testing sets")
    print(test)
    
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

    # create hpai (housing price appreciation index) data from hpi data
    hpai_values = (hpi_df["VAL"].diff() / hpi_df["VAL"].shift(1)) * 100
    hpai_df = pd.DataFrame({
        "DATE": hpi_df["DATE"][1:],
        "HPAI": hpai_values[1:]
    })
    hpai_df.to_csv("datasets/hpai.csv", index=False)

    print("HPA Index data successfully extrapolated from HPI data")

    # let the date be the index for all dataframes
    for df in [hpi_df, hpai_df, ten_yrt_df, unemployment_df, wages_df, supply_df]:
        df.set_index('DATE', inplace=True)
    
    # find latest start year & earliest end year
    latest_start = max([df.index.min() for df in [hpi_df, hpai_df, ten_yrt_df, unemployment_df, wages_df, supply_df]])
    earliest_end = min([df.index.max() for df in [hpi_df, hpai_df, ten_yrt_df, unemployment_df, wages_df, supply_df]])

    # merge into single dataframe
    combined_df = pd.concat([hpi_df, hpai_df, ten_yrt_df, unemployment_df, wages_df, supply_df], axis=1)
    combined_df.ffill(inplace=True)
    combined_df = combined_df[(combined_df.index >= latest_start) & (combined_df.index <= earliest_end)]
    combined_df.columns = ['HPI', 'HPAI', 'TENYRT', 'UNEMPLOYMENT', 'WAGES', 'SUPPLY']

    # parse out rows with invalid entries (some tenyrt values are just "." in the csv)
    combined_df = combined_df.apply(pd.to_numeric, errors='coerce')
    combined_df = combined_df.dropna()

    # combined_df has shape: [3211 rows x 6 columns]
    # pprint(combined_df)
    # pprint(combined_df.shape)

    print("Dataset successfully constructed")

    return combined_df

def main():
    dataset = constructDataset()
    train, val, test = splitDataset(dataset)

    train.to_csv("datasets/train" + toggle + ".csv", index=False)
    val.to_csv("datasets/val" + toggle + ".csv", index=False)
    test.to_csv("datasets/test" + toggle + ".csv", index=False)

    print("Dataset split successfully saved as csv")

if __name__ == '__main__': 
    main()