import numpy as np
import random
import torch

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

def splitDataset(x, y):
    x_train = 
    x_val = 
    x_test = 
    y_train = 
    y_val = 
    y_test = 
    return 
    print("Dataset split into training, validation, and testing sets")

def hpaCalculator(year1, year2):
    return (year2 - year1) / year1 * 100

# Function to construct a dataset with inputs from 10 year treasury rates, unemployment rates,
# wages, and housing supply & outputs the HPA index; daily increments
def constructDataset():
    input = 
    output = 
    splitDataset(input, output)
    print("Created HPA index dataset from dataset.py")