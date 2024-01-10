# Creates a dataset from HPI, HPA, treasury rates, mortgage rates, unemployment rates, wages, and supply. 
# HPA is calculated from HPI raw data. TVT split is 70-15-15. 
# For the dataset generated from wages_monthly data (as opposed to wages_quarterly):
#   train has 2247 examples, val has 481 examples, and test has 483 examples.
# For the dataset generated from wages_quarterly data (as opposed to wages_monthly):
#   train has 4126 examples, val has 884 examples, and test has 885 examples.

import numpy as np
import pandas as pd
from varname import nameof
import numbers
from datetime import datetime
from pprint import pprint

# filepaths for raw data
hpi = "raw_datasets/hpi.csv"
ten_yrt = "raw_datasets/ten_yrt.csv" 
mortgage = "raw_datasets/mortgage.csv"
unemployment = "raw_datasets/unemployment.csv" 
wages = "raw_datasets/wages_monthly.csv" 
# wages = "raw_datasets/wages_quarterly.csv" # no need to toggle anymore, only use monthly wages
wages_quarterly = "raw_datasets/wages_quarterly.csv"
supply = "raw_datasets/supply.csv" 

# save path toggle (based on which wage data being used) for final dataset split
toggle = "wm_" if wages == "raw_datasets/wages_monthly.csv" else "wq_"

def splitDataset(dataset, train=0.7, val=0.15, test=0.15):
    if (train + val + test != 1):
        raise Exception("Train, val, test split is invalid -- must sum to 1")
    
    # shuffle data points before splitting to guarantee randomness
    # DO NOT CHANGE RANDOM_STATE VALUE... ensures reproducibility (like a seed value)
    # dataset = dataset.sample(frac=1, random_state=1)
    
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

def replace_invalid_with_nan(val):
    if val == "None":
        return np.nan
    return val

def calculateChangeDFs(raw_df, raw_df_name):
    new_df = raw_df.copy()
    if raw_df_name == "hpi":
        modified_df_name = "hpa.csv"
    else:
        modified_df_name = raw_df_name + "_apc.csv"
    
    # determine the shift size based on the frequency of measurements
    if raw_df_name in {"ten_yrt"}: # daily
        shift_size = 249
    elif raw_df_name in {"mortgage"}: # weekly
        shift_size = 52
    elif raw_df_name in {"hpi", "unemployment", "wages"}: # monthly
        shift_size = 12
    else: # quarterly
        shift_size = 4
    
    # shift and calculate annual percentage change
    new_df['VAL_PREV_YEAR'] = new_df['VAL'].shift(shift_size)
    new_df['VAL_PREV_YEAR'] = new_df['VAL_PREV_YEAR'].apply(replace_invalid_with_nan)
    new_df['PC'] = (new_df['VAL'] - new_df['VAL_PREV_YEAR']) / new_df['VAL_PREV_YEAR'] * 100

    # drop middle 2 columns (intermediaries) & cut first year (no previous years for calculation)
    new_df = new_df.drop(['VAL', 'VAL_PREV_YEAR'], axis=1)
    new_df = new_df[new_df['PC'].notna()]

    new_df.to_csv("raw_datasets/" + modified_df_name)

    return new_df

# Function to construct a dataset with inputs from 10 year treasury rates, mortgage rates, 
# unemployment rates, wages, and housing supply & outputs the HPA index; daily increments
def constructDataset():
    # convert all csv files to dataframes & parse dates
    hpi_df = pd.read_csv(hpi, parse_dates=['DATE'])
    ten_yrt_df = pd.read_csv(ten_yrt, parse_dates=['DATE'])
    mortgage_df = pd.read_csv(mortgage, parse_dates=['DATE'])
    unemployment_df = pd.read_csv(unemployment, parse_dates=['DATE'])
    wages_df = pd.read_csv(wages, parse_dates=['DATE'])
    supply_df = pd.read_csv(supply, parse_dates=['DATE'])

    # let the date be the index for all dataframes
    for df in [hpi_df, ten_yrt_df, mortgage_df, unemployment_df, wages_df, supply_df]:
        df.set_index('DATE', inplace=True)

    # parse out rows with invalid entries (some tenyrt values are just "." in the csv)
    ten_yrt_df = ten_yrt_df.apply(pd.to_numeric, errors='coerce')
    ten_yrt_df = ten_yrt_df.dropna()

    all_raw_datasets = [hpi_df]
    # second param splices out "_df" for naming purposes (same for all calls to calculateChangeDFs)
    all_raw_datasets.append(calculateChangeDFs(hpi_df, nameof(hpi_df)[:-3]))
    all_raw_datasets.append(ten_yrt_df)
    all_raw_datasets.append(calculateChangeDFs(ten_yrt_df, nameof(ten_yrt_df)[:-3]))
    all_raw_datasets.append(mortgage_df)
    all_raw_datasets.append(calculateChangeDFs(mortgage_df, nameof(mortgage_df)[:-3]))
    all_raw_datasets.append(unemployment_df)
    all_raw_datasets.append(calculateChangeDFs(unemployment_df, nameof(unemployment_df)[:-3]))
    all_raw_datasets.append(wages_df)
    all_raw_datasets.append(calculateChangeDFs(wages_df, nameof(wages_df)[:-3]))
    all_raw_datasets.append(supply_df)
    all_raw_datasets.append(calculateChangeDFs(supply_df, nameof(supply_df)[:-3]))

    print("1. Annual percentage change data successfully extrapolated from HPI data & prelim dataset constructed")

    # find latest start year & earliest end year
    latest_start = max([df.index.min() for df in all_raw_datasets])
    earliest_end = min([df.index.max() for df in all_raw_datasets])

    # merge into single dataframe
    combined_df = pd.concat(all_raw_datasets, axis=1)
    combined_df.ffill(inplace=True)
    combined_df = combined_df[(combined_df.index >= latest_start) & (combined_df.index <= earliest_end)]

    # pprint(combined_df)

    combined_df.columns = ['HPI', 'HPA_PC', 'TENYRT', 'TENYRT_PC', 'MORTGAGE', 'MORTGAGE_PC', 'UNEMPLOYMENT', 'UNEMPLOYMENT_PC', 'WAGES', 'WAGES_PC', 'SUPPLY', 'SUPPLY_PC']

    # parse out rows with invalid entries (some tenyrt values are just "." in the csv)
    combined_df = combined_df.apply(pd.to_numeric, errors='coerce')
    combined_df = combined_df.dropna()

    # add dates back in to the final datasets (instead of being the index)
    combined_df.reset_index(drop=False, inplace=True) 

    # pprint(combined_df)

    print("3. Dataset successfully constructed of size:", combined_df.shape[0], "data points with", combined_df.shape[1], "dimensions")

    return combined_df

def cleanWagesQuarterly():
    wages_df_quarterly = pd.read_csv(wages_quarterly, parse_dates=['DATE'])
    wages_df_quarterly.iloc[:, 1] = wages_df_quarterly.iloc[:, 1] / 40
    wages_df_quarterly.to_csv(wages_quarterly, index=False) # replace old wages_quarterly data

def condenseDataset(original):
    condensed_df = original.copy()
    condensed_df = condensed_df.sort_values(by='DATE')
    condensed_df['YEAR_MONTH'] = condensed_df['DATE'].dt.to_period('M')
    condensed_df = condensed_df.drop_duplicates(subset='YEAR_MONTH')
    return condensed_df

def main():
    # DO NOT UNCOMMENT, already cleaned (divided by 40 hours for hourly wage instead of weekly wage)
    # cleanWagesQuarterly()

    complete_dataset = constructDataset() # uses extrapolation
    complete_dataset.to_csv("datasets/" + toggle + "dataset.csv", index=False)
    train, val, test = splitDataset(complete_dataset)

    train.to_csv("datasets/" + toggle + "train.csv", index=False)
    val.to_csv("datasets/" + toggle + "val.csv", index=False)
    test.to_csv("datasets/" + toggle + "test.csv", index=False)

    # condenses dataset to only include one entry from each month
    condensed_dataset = condenseDataset(complete_dataset)
    condensed_dataset = condensed_dataset.drop(['YEAR_MONTH'], axis=1)
    condensed_dataset.to_csv("datasets/new_" + toggle + "dataset.csv", index=False)
    train_new, val_new, test_new = splitDataset(condensed_dataset)

    train_new.to_csv("datasets/new_" + toggle + "train.csv", index=False)
    val_new.to_csv("datasets/new_" + toggle + "val.csv", index=False)
    test_new.to_csv("datasets/new_" + toggle + "test.csv", index=False)

    print("4. Dataset split successfully saved as csv files")

if __name__ == '__main__': 
    main()