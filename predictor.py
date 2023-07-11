# Importing libraries

import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pandas.api.types import CategoricalDtype
import optuna
import shap
from xgboost import XGBRegressor
from tkinter import *
from tkinter import ttk
import matplotlib.pyplot as plt

st.set_option('deprecation.showPyplotGlobalUse', False)

st.title("House Price Prediction in Ames, Iowa")

st.write("A multi-step process is used to estimate the range of house prices based on your selection. The modeling process is done using the data found on Kaggle.")

st.write("Check out Milestone 1, set up a development environment [link](https://github.com/DavidGomezCamargo/Project/tree/Milestone-1)")

st.write("Check out Milestone 2, SHAP interpretation of the house price prediction model [link](https://github.com/DavidGomezCamargo/Project/blob/f380847a17d3ade040f2b5c2b3618bd046579ad0/Milestone_2.ipynb)")

st.write("Check out Milestone 3, tunning hyperparameters with Optuna [link](https://github.com/DavidGomezCamargo/Project/blob/622f72716ba10fdf73b31ca846d08d59d8af6e51/Milestone_3.ipynb)")

name_list = ['MSSubClass',
 'OverallQual',
 'YearBuilt',
 'YearRemodAdd',
 'BsmtUnfSF',
 'TotalBsmtSF',
 'FstFlrSF',
 'SndFlrSF',
 'GrLivArea',
 'FullBath',
 'HalfBath',
 'TotRmsAbvGrd',
 'Fireplaces',
 'GarageCars',
 'GarageArea',
 'MoSold',
 'YrSold']

name_list_train = ['MSSubClass',
 'OverallQual',
 'YearBuilt',
 'YearRemodAdd',
 'BsmtUnfSF',
 'TotalBsmtSF',
 '1stFlrSF',
 '2ndFlrSF',
 'GrLivArea',
 'FullBath',
 'HalfBath',
 'TotRmsAbvGrd',
 'Fireplaces',
 'GarageCars',
 'GarageArea',
 'MoSold',
 'YrSold']

description_list = [
 'What is the building class?',
 'What is the Overall material and finish quality?',
 'In which year was the Original construction date?',
 'In which year was it remodelled?',
 'What is the Unfinished square feet of basement area?',
 'What is the Total square feet of basement area?',
 'What is the First Floor square feet?',
 'What is the Second floor square feet?',
 'What is the Above grade (ground) living area square feet?',
 'What is the number of full bathrooms?',
'What is the number of Half baths?',
'What is the number of  Total rooms above grade (does not include bathrooms)?',
'What is the number of fireplaces?',
'What is the garage capacity in car sizes?',
'What is the size of garage in square feet?',
'In which month was it sold?',
'In which year was it sold?'
 ]

min_list = [20.0,1.0,1872.0,
 1950.0,
 0.0,
 0.0,
 334.0,
 0.0,
 334.0,
 0.0,
 0.0,
 2.0,
 0.0,
 0.0,
 0.0,
 1.0,
 2006.0]

max_list = [190.0,
 10.0,
 2010.0,
 2010.0,
 2336.0,
 6110.0,
 4692.0,
 2065.0,
 5642.0,
 3.0,
 2.0,
 14.0,
 3.0,
 4.0,
 1418.0,
 12.0,
 2010.0]

count = 0

with st.sidebar:

    for i in range(len(name_list)):
        variable_name = name_list[i]
        globals()[variable_name] = st.slider(description_list[i] ,min_value=int(min_list[i]), max_value =int(max_list[i]),step=1)
    st.write("[Kaggle Link to Data Set](https://www.kaggle.com/competitions/house-prices-advanced-regression-techniques)")

data_df = {
'MSSubClass': [MSSubClass],
 'OverallQual': [OverallQual],
 'YearBuilt': [YearBuilt],
 'YearRemodAdd': [YearRemodAdd],
 'BsmtUnfSF': [BsmtUnfSF],
 'TotalBsmtSF': [TotalBsmtSF],
 '1stFlrSF': [FstFlrSF],
 '2ndFlrSF': [SndFlrSF],
 'GrLivArea':[GrLivArea],
 'FullBath': [FullBath],
 'HalfBath': [HalfBath],
 'TotRmsAbvGrd':[TotRmsAbvGrd],
 'Fireplaces': [Fireplaces],
 'GarageCars': [GarageCars],
 'GarageArea':[GarageArea],
 'MoSold': [MoSold],
 'YrSold' : [YrSold]
}

# Loading the dataset

train_dataset = pd.read_csv('https://raw.githubusercontent.com/DavidGomezCamargo/Project/main/train.csv')
test_dataset = pd.read_csv('https://raw.githubusercontent.com/DavidGomezCamargo/Project/main/test.csv')

# Selecting features - Train Set

train_dataset = train_dataset[["MSSubClass", "OverallQual", "YearBuilt", "YearRemodAdd", "BsmtUnfSF", "TotalBsmtSF", "1stFlrSF", "2ndFlrSF", "GrLivArea", "FullBath", "HalfBath", "TotRmsAbvGrd", "Fireplaces", "GarageCars", "GarageArea", "MoSold", "YrSold", "SalePrice"]]

# X and y - Train Set

X_train = pd.get_dummies(train_dataset.drop('SalePrice', axis=1))
y_train = train_dataset['SalePrice']

# Selecting features - Test Set

test_dataset = test_dataset[["MSSubClass", "OverallQual", "YearBuilt", "YearRemodAdd", "BsmtUnfSF", "TotalBsmtSF", "1stFlrSF", "2ndFlrSF", "GrLivArea", "FullBath", "HalfBath", "TotRmsAbvGrd", "Fireplaces", "GarageCars", "GarageArea", "MoSold", "YrSold"]]
X_test = pd.get_dummies(test_dataset)

xgb_params = {'max_depth': 10,
 'learning_rate': 0.006612267058442724,
 'n_estimators': 3579,
 'min_child_weight': 10,
 'colsample_bytree': 0.22197134134998234,
 'subsample': 0.5445801890654369,
 'reg_alpha': 2.4804244221172453,
 'reg_lambda': 1.2765127778298433}

# Train Model and Create Predictions

xgb = XGBRegressor(**xgb_params)

# XGB minimizes MSE, but we want to minimize RMSLE
# So, we need to log-transform y to train and exp-transform the predictions

xgb.fit(X_train, np.log(y_train))

# SHAP Values to explain individual predictions

data_for_prediction = data_df
data_for_prediction = pd.DataFrame(data_for_prediction)
predictions = np.exp(xgb.predict(data_for_prediction))
st.write('The house price based on your selection is',  '${:,.2f}'.format(round(float(np.asarray(predictions)), 2)))


# Generate prediction
y_sample = np.exp(xgb.predict(data_for_prediction))

# Create object that can calculate Shap values
explainer = shap.TreeExplainer(xgb)

# Calculate Shap values from prediction
shap_values = explainer.shap_values(data_for_prediction)

# Feature effect on particular prediction

plt.title('Feature impact on model output (feature impact in details below)')
st.pyplot(shap.summary_plot(shap_values, data_for_prediction))

# Aggregated effect

# Use test set to get predictions
data_for_prediction = X_test

# Generate predictions
y_sample = np.exp(xgb.predict(data_for_prediction))

# Create object that can calculate Shap values
explainer = shap.TreeExplainer(xgb)

# Calculate Shap values from predictions
shap_values = explainer.shap_values(data_for_prediction)

# Feature impact on overall

plt.title('Feature impact on overall model output (feature impact in details below)')
st.pyplot(shap.summary_plot(shap_values, data_for_prediction))