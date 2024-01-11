import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
from dataset import splitByEra

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

def visualize_all(x, y, coeff, intercept, var, prefix):
    plt.scatter(x, y, color='blue', label='Validation Data')
    plt.plot(x, coeff[0] * x + intercept, color='red', label='Regression Line')
    plt.title('Linear Regression: HPA vs. ' + var)
    plt.xlabel(var)
    plt.ylabel("HPA")
    plt.legend()
    plt.savefig(prefix + var)
    plt.clf()

def visualize_eras(x, y, dataset_years_df, var, prefix):
    eras = [[dataset_years_df['2010-2020'][var], dataset_years_df['2010-2020']["HPA_PC"]],
            [dataset_years_df['2021'][var], dataset_years_df['2021']["HPA_PC"]],
            [dataset_years_df['2022'][var], dataset_years_df['2022']["HPA_PC"]],
            [dataset_years_df['2023'][var], dataset_years_df['2023']["HPA_PC"]]]
    
    plt.scatter(eras[0][0], eras[0][1], color='gold', label='2011-2020')
    print(eras[1][0])
    print(eras[1][1])
    plt.scatter(eras[1][0], eras[1][1], color='green', label='2021')
    plt.scatter(eras[2][0], eras[2][1], color='blue', label='2022')
    plt.scatter(eras[3][0], eras[3][1], color='purple', label='2023')

    colors = ['gold', 'green', 'blue', 'purple']
    years = ['\'10-\'20','\'21','\'22','\'23']
    for i in range(0, 4):
        _, coeff, intercept = linreg(eras[i][0], eras[i][1])
        plt.plot(x, coeff[0] * x + intercept, color=colors[i], label=years[i] + ' Regression Line')
    
    plt.title('Linear Regression: HPA vs. ' + var)
    plt.xlabel(var)
    plt.ylabel("HPA")
    plt.legend()
    plt.savefig(prefix + var)
    plt.clf()


def main():
    dataset_df = pd.read_csv("datasets/new_wm_dataset.csv", parse_dates=['DATE'])
    dataset_years_df = splitByEra(dataset_df)

    predict_hpi = 'HPI'
    predict_hpa = 'HPA_PC'
    variables = ["TENYRT", "TENYRT_PC","MORTGAGE","MORTGAGE_PC","UNEMPLOYMENT","UNEMPLOYMENT_PC","WAGES","WAGES_PC","SUPPLY","SUPPLY_PC"]
    
    path_prefix_all = "linreg_vis_all/"
    path_prefix_eras = "linreg_vis_split/"

    # predict hpa vs. single variables (no percent changes)
    print()
    print("1. HPA VS. SINGLE VARIABLES")
    for i in range(0, len(variables), 2):
        mse, coeff, intercept = linreg(dataset_df[variables[i]], dataset_df[predict_hpa])
        print("HPA vs.", variables[i], ": coeff =", coeff[0], "& intercept =", intercept)
        print("        MSE:", mse)

        visualize_all(dataset_df[variables[i]], dataset_df[predict_hpa], coeff, intercept, variables[i], path_prefix_all)
        visualize_eras(dataset_df[variables[i]], dataset_df[predict_hpa], dataset_years_df, variables[i], path_prefix_eras)

    # predict hpa vs. percent changes of single variables
    print()
    print("2. HPA VS. PERCENT CHANGE OF SINGLE VARIABLES")
    for i in range(1, len(variables), 2):
        mse, coeff, intercept = linreg(dataset_df[variables[i]], dataset_df[predict_hpa])
        print("HPA vs.", variables[i], ": coeff =", coeff[0], "& intercept =", intercept)
        print("        MSE:", mse)

        visualize_all(dataset_df[variables[i]], dataset_df[predict_hpa], coeff, intercept, variables[i], path_prefix_all)
        visualize_eras(dataset_df[variables[i]], dataset_df[predict_hpa], dataset_years_df, variables[i], path_prefix_eras)

    # predict hpa vs. variables AND percent changes (2 dimensional input)
    print()
    print("3. HPA VS. SINGLE VARIABLES + PERCENT CHANGE OF SINGLE VARIABLES")
    for i in range(0, len(variables), 2):
        linreg(dataset_df[variables[i]], dataset_df[predict_hpa])
        mse, coeff, intercept = linreg(dataset_df[[variables[i], variables[i + 1]]], dataset_df[predict_hpa])
        print("HPA vs.", variables[i], ": coeff =", coeff, "& intercept =", intercept)
        print("        MSE:", mse)

if __name__ == '__main__': 
    main()