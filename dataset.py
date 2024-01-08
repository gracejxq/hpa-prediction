import numpy as np
import random
import torch

# filepaths for raw data
hpi = "datasets/hpi.csv"
ten_yrt = "datasets/10yr_treasury.csv"
wages = "datasets/wages_monthly.csv"
unemployment = "datasets/unemployment.csv"
supply = "datasets/supply_monthly.csv"
# supply = "datasets/supply_quarterly.csv"

# save path for final dataset
save_path = "datasets/dataset"
toggle = "_supply_monthly.csv" if supply == "datasets/supply_monthly.csv" else "_supply_quarterly.csv"
save_path += toggle

def splitDataset(x, y):
    x_train = 
    x_val = 
    x_test = 
    y_train = 
    y_val = 
    y_test = 
    return 
    print("Dataset split into training, validation, and testing sets")

# Function to construct a dataset with inputs from 10 year treasury rates, wages, unemployment
# rates, and housing supply & outputs the HPA index; daily increments
def constructDataset():
    input = 
    output = 
    splitDataset(input, output)
    print("Created HPA index dataset from dataset.py")