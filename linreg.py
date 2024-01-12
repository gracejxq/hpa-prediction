import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score
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
    r2 = r2_score(y, predictions)
    mse = mean_squared_error(y, predictions)

    return r2, mse, model.coef_, model.intercept_

def visualize_all(x, y, coeff, intercept, var, prefix):
    var_to_xlabel = {'MORTGAGE': "Mortgage Rates",
                     'MORTGAGE_PC': "Annual Percent Change of Mortgage Rates",
                     'SUPPLY': "Housing Supply",
                     'SUPPLY_PC': "Annual Percent Change of Housing Supply",
                     'TENYRT': "10-Year Treasury Rates",
                     'TENYRT_PC': "Annual Percent Change of 10-Year Treasury Rates",
                     'UNEMPLOYMENT': "Unemployment",
                     'UNEMPLOYMENT_PC': "Annual Percent Change of Unemployment",
                     'WAGES': "Wages",
                     'WAGES_PC': "Annual Percent Change of Wages"}
    label = var_to_xlabel[var]

    plt.scatter(x, y, color='black', label='2011-2023 Data')
    plt.plot(x, coeff[0] * x + intercept, color='red', label='Regression Line')
    plt.title('HPA vs. ' + label)
    plt.xlabel(label)
    plt.ylabel("HPA (%)")
    plt.legend()
    plt.savefig(prefix + var)
    plt.clf()

def visualize_eras(x, y, dataset_years_df, var, prefix):
    eras = [[dataset_years_df['Era 1'][var], dataset_years_df['Era 1']["HPA_PC"]],
            [dataset_years_df['Era 2'][var], dataset_years_df['Era 2']["HPA_PC"]],
            [dataset_years_df['Era 3'][var], dataset_years_df['Era 3']["HPA_PC"]],
            [dataset_years_df['Era 4'][var], dataset_years_df['Era 4']["HPA_PC"]],
            [dataset_years_df['Era 5'][var], dataset_years_df['Era 5']["HPA_PC"]]]
    
    plt.scatter(eras[0][0], eras[0][1], color='gold', label='01/2011 - 12/2013')
    plt.scatter(eras[1][0], eras[1][1], color='yellowgreen', label='01/2014 - 03/2020')
    plt.scatter(eras[2][0], eras[2][1], color='green', label='04/2020 - 06/2021')
    plt.scatter(eras[3][0], eras[3][1], color='blue', label='07/2021 - 06/2022')
    plt.scatter(eras[4][0], eras[4][1], color='purple', label='07/2022 - 06/2023')

    colors = ['gold', 'yellowgreen', 'green', 'blue', 'purple']
    years = ['01/2011 - 12/2013', '01/2014 - 03/2020', '04/2020 - 06/2021', '07/2021 - 06/2022', '07/2022 - 06/2023']
    for i in range(0, 5):
        _, _, coeff, intercept = linreg(eras[i][0], eras[i][1])
        plt.plot(x, coeff[0] * x + intercept, color=colors[i], label=years[i] + ' RL')
    

    var_to_xlabel = {'MORTGAGE': "Mortgage Rates",
                     'MORTGAGE_PC': "Annual Percent Change of Mortgage Rates",
                     'SUPPLY': "Housing Supply",
                     'SUPPLY_PC': "Annual Percent Change of Housing Supply",
                     'TENYRT': "10-Year Treasury Rates",
                     'TENYRT_PC': "Annual Percent Change of 10-Year Treasury Rates",
                     'UNEMPLOYMENT': "Unemployment",
                     'UNEMPLOYMENT_PC': "Annual Percent Change of Unemployment",
                     'WAGES': "Wages",
                     'WAGES_PC': "Annual Percent Change of Wages"}
    label = var_to_xlabel[var]

    plt.title('HPA vs. ' + label)
    plt.xlabel(label)
    plt.ylabel("HPA (%)")
    plt.ylim(-5, 22)
    plt.legend(loc='upper right')
    plt.savefig(prefix + var)
    plt.clf()

def main():
    dataset_df = pd.read_csv("datasets/new_wm_dataset.csv", parse_dates=['DATE'])
    dataset_years_df = splitByEra(dataset_df)

    predict_hpa = 'HPA_PC'
    variables = ["TENYRT", "TENYRT_PC","MORTGAGE","MORTGAGE_PC","UNEMPLOYMENT","UNEMPLOYMENT_PC","WAGES","WAGES_PC","SUPPLY","SUPPLY_PC"]
    
    path_prefix_all = "linreg_vis_all/"
    path_prefix_eras = "linreg_vis_era/"

    # predict hpa vs. single variables (no percent changes)
    print()
    print("1. HPA VS. SINGLE VARIABLES")
    for i in range(0, len(variables), 2):
        r2, mse, coeff, intercept = linreg(dataset_df[variables[i]], dataset_df[predict_hpa])
        print("HPA vs.", variables[i], ": coeff =", coeff[0], "& intercept =", intercept)
        print("        MSE:", mse)
        print("         R2:", r2)

        visualize_all(dataset_df[variables[i]], dataset_df[predict_hpa], coeff, intercept, variables[i], path_prefix_all)
        visualize_eras(dataset_df[variables[i]], dataset_df[predict_hpa], dataset_years_df, variables[i], path_prefix_eras)

    # predict hpa vs. percent changes of single variables
    print()
    print("2. HPA VS. PERCENT CHANGE OF SINGLE VARIABLES")
    for i in range(1, len(variables), 2):
        r2, mse, coeff, intercept = linreg(dataset_df[variables[i]], dataset_df[predict_hpa])
        print("HPA vs.", variables[i], ": coeff =", coeff[0], "& intercept =", intercept)
        print("        MSE:", mse)
        print("         R2:", r2)

        visualize_all(dataset_df[variables[i]], dataset_df[predict_hpa], coeff, intercept, variables[i], path_prefix_all)
        visualize_eras(dataset_df[variables[i]], dataset_df[predict_hpa], dataset_years_df, variables[i], path_prefix_eras)

    # predict hpa vs. variables AND percent changes (2 dimensional input)
    print()
    print("3. HPA VS. SINGLE VARIABLES + PERCENT CHANGE OF SINGLE VARIABLES")
    for i in range(0, len(variables), 2):
        linreg(dataset_df[variables[i]], dataset_df[predict_hpa])
        r2, mse, coeff, intercept = linreg(dataset_df[[variables[i], variables[i + 1]]], dataset_df[predict_hpa])
        print("HPA vs.", variables[i], ": coeff =", coeff, "& intercept =", intercept)
        print("        MSE:", mse)
        print("         R2:", r2)

if __name__ == '__main__': 
    main()