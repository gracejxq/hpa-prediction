import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt

# train = "datasets/new_wm_train.csv"
# val = "datasets/new_wm_val.csv"
# test = "datasets/new_wm_test.csv"
complete = "datasets/new_wm_dataset.csv"

# def linreg(x_train, x_val, y_train, y_val):
#     if x_train.ndim == 1:
#         x_train_reshaped = x_train.values.reshape(-1, 1)
#         x_val_reshaped = x_val.values.reshape(-1, 1)
#     else:
#         x_train_reshaped = x_train
#         x_val_reshaped = x_val

#     model = LinearRegression()
#     model.fit(x_train_reshaped, y_train)
#     predictions = model.predict(x_val_reshaped)
#     mse = mean_squared_error(y_val, predictions)

#     return mse, model.coef_, model.intercept_

def linreg(x, y):
    if x.ndim == 1:
        x_reshaped = x.values.reshape(-1, 1)
    else:
        x_reshaped = x

    model = LinearRegression()
    model.fit(x_reshaped, y)
    predictions = model.predict(x_reshaped)
    mse = mean_squared_error(y, predictions)

    return mse, model.coef_, model.intercept_

def main():
    # train_df = pd.read_csv(train, parse_dates=['DATE'])
    # val_df = pd.read_csv(val, parse_dates=['DATE'])
    # test_df = pd.read_csv(test, parse_dates=['DATE'])
    dataset_df = pd.read_csv(complete, parse_dates=['DATE'])

    predict_hpi = 'HPI'
    predict_hpa = 'HPA_PC'
    variables = ["TENYRT", "TENYRT_PC","MORTGAGE","MORTGAGE_PC","UNEMPLOYMENT","UNEMPLOYMENT_PC","WAGES","WAGES_PC","SUPPLY","SUPPLY_PC"]
    
    path_prefix = "linreg_visualizations/"

    # predict hpi vs. single variables (no percent changes)
    print("1. HPI VS. SINGLE VARIABLES")
    for i in range(0, len(variables), 2):
        mse, coeff, intercept = linreg(dataset_df[variables[i]], dataset_df[predict_hpi])
        # mse, coeff, intercept = linreg(train_df[variables[i]], val_df[variables[i]], train_df[predict_hpi], val_df[predict_hpi])
        print("HPI vs.", variables[i], ": coeff =", coeff[0], "& intercept =", intercept)
        print("        MSE:", mse)

    # predict hpa vs. single variables (no percent changes)
    print()
    print("2. HPA VS. SINGLE VARIABLES")
    for i in range(0, len(variables), 2):
        mse, coeff, intercept = linreg(dataset_df[variables[i]], dataset_df[predict_hpa])
        # mse, coeff, intercept = linreg(train_df[variables[i]], val_df[variables[i]], train_df[predict_hpa], val_df[predict_hpa])
        print("HPA vs.", variables[i], ": coeff =", coeff[0], "& intercept =", intercept)
        print("        MSE:", mse)

        val_df= pd.read_csv("datasets/new_wm_dataset.csv", parse_dates=['DATE'])

        print(val_df[variables[i]])
        print(val_df[predict_hpa])
        plt.scatter(val_df[variables[i]], val_df[predict_hpa], color='blue', label='Validation Data')
        plt.plot(val_df[variables[i]], coeff[0] * val_df[variables[i]] + intercept, color='red', label='Regression Line')
        plt.title('Linear Regression: HPA vs. ' + variables[i])
        plt.xlabel(variables[i])
        plt.ylabel("HPA")
        plt.legend()
        plt.savefig(path_prefix + variables[i])
        plt.clf()
    
    # # predict hpa vs. percent changes of single variables
    # print()
    # print("3. HPA VS. PERCENT CHANGE OF SINGLE VARIABLES")
    # for i in range(1, len(variables), 2):
    #     mse, coeff, intercept = linreg(train_df[variables[i]], val_df[variables[i]], train_df[predict_hpa], val_df[predict_hpa])
    #     print("HPA vs.", variables[i], ": coeff =", coeff[0], "& intercept =", intercept)
    #     print("        MSE:", mse)

    # # predict hpa vs. variables AND percent changes (2 dimensional input)
    # print()
    # print("4. HPA VS. PERCENT CHANGE OF SINGLE VARIABLES")
    # for i in range(0, len(variables), 2):
    #     mse, coeff, intercept = linreg(train_df[[variables[i], variables[i + 1]]], val_df[[variables[i], variables[i + 1]]], train_df[predict_hpa], val_df[predict_hpa])
    #     print("HPA vs.", variables[i], ": coeff =", coeff, "& intercept =", intercept)
    #     print("        MSE:", mse)

if __name__ == '__main__': 
    main()