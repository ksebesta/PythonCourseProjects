'''
Title: Homework 3
Author: Kalea Sebesta
Date: 11/3/2017
Due Date: 11/14/2017
Purpose:
Part 1
Resolving Class Imbalance –  Using the Pima Indian Diabetes dataset,
create a balanced dataset (balanced with respect to the number of observations
in each of the diabetes classes). Do it two different ways﻿﻿: By creating synthetic
observations in the minority class via the Synthetic Minority Over-sampling
Technique (SMOTE), and By selecting a subset of the majority class that is equal
in size to the minority class size.

Part 2
Structured Data Cleansing – Using the “HW2_2013Sales_AllQuant.csv” data, Identify
the dimensions of the dataset (number of observations and features). Provide and
evaluate basic descriptive statistics for each feature (Pandas DataFrame describe()
function). Examine each column for missing values. Impute missing values with the
mean, median, or mode, as you deem appropriate (and defend your method selection).
Examine each column for nonsense or impossible values. ‘Fix’ missing values and
defend your method of fixing them. Assess whether any list-wise deletion procedures
are in order. Apply and defend your actions. Assess whether any features need to be
standardized or normalized. Apply and defend your actions.
'''

# -------------------------------------------------------------------------------
# Part 1: Resolving Class Imbalance
# -------------------------------------------------------------------------------
''' Using the Pima Indian Diabetes dataset, create a balanced dataset
(balanced with respect to the number of observations in each of the diabetes classes).
'''
# import packages
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from collections import Counter
from sklearn.datasets import make_classification
from sklearn.utils import resample
from imblearn.under_sampling import RandomUnderSampler
from imblearn.over_sampling import SMOTE
import csv
# -------------------------------------------------------------------------------
# import data set
pima = pd.read_csv('/Volumes/UTSA QRT2/IS 6713 Data Foundations/pima-indians-diabetes.data.txt')
print(pima.shape)

# TAKE OUT ALL CLEANING FOR PART 1
# examine whether there are missing values
col_NaN_count = pima.isnull().sum()
print(col_NaN_count)

# examine our dataframe for impossible values
    # PGC, BP, TRI, Insulin, BMI, cannot have a min=0
    # BP having a max over 100 is suspicious as potential outlier
    # TRI over 50 is suspicious as potential outlier
    # BMI over 42 is suspicious as potential outlier
    # PGC shouldn't be under 40 mg/dl

pima.describe()
pima.hist(color='k')

# calculating how many entries are over 100
pima_BP = pima[pima['BP'] > 100]
len(pima_BP.index)

# calculating how many folds are over 50
pima_TT = pima[pima['Tri.Thick'] > 50]
len(pima_TT.index)

# calculating how many BMI are over 42
pima_BMI = pima[pima['BMI'] > 42]
len(pima_BMI.index)

# calculating how many PGC equal zero
pima_PGC = pima[pima['PGC'] == 0]
len(pima_PGC.index)

# dealing with dirty data
# replacing the impossible values with nan
pima['BP'].replace(0, np.nan, inplace=True)
pima['BMI'].replace(0, np.nan, inplace=True)
pima['Tri.Thick'].replace(0, np.nan, inplace=True)
pima['Insulin'].replace(0, np.nan, inplace=True)
pima['PGC'].replace(0, np.nan, inplace=True)

# replacing values that are too high for the categories with NaN
pima['BP'][pima['BP'] > 100] = np.NAN
pima['BMI'][pima['BMI'] > 42] = np.NAN
pima['Tri.Thick'][pima['Tri.Thick'] > 50] = np.NAN

# replace the missing values with the mean of that category
pima['BP'].fillna(pima['BP'].mean())
pima['BMI'].fillna(pima['BMI'].mean())
pima['Tri.Thick'].fillna(pima['Tri.Thick'].mean())
pima['Insulin'].fillna(pima['Insulin'].mean())
pima['PGC'].fillna(pima['PGC'].mean())

# shows that the new mins for BP, BMI, Tri.Thick, Insulin
pima.describe()

# identify minority and majority class having diabetes = 1
# the results show that the minority category is those without diabetes
pima_Pos_D=(pima['Diabetes'] == 0).sum()
pima_Neg_D=(pima['Diabetes'] == 1).sum()

print('The number of people with Diabetes: %d' % pima_Pos_D)
print('The number of people without Diabetes: %d' % pima_Neg_D)
# -------------------------------------------------------------------------------
#
# a. Creating synthetic observations in the minority class via the Synthetic Minority
# minority class is those without diabetes diabetes==0
# Over-sampling Technique (SMOTE)
y = pima.Diabetes
pima = np.array(pima)
sm = SMOTE(kind='regular')
X_res, y_res = sm.fit_sample(pima, y)

# include visual evidence of task accomplished
# show the class sizes before/after sampling
print('Original dataset shape {}'.format(Counter(y)))
print('New dataset shape {}'.format(Counter(y_res)))

# ------------------------------------------------------------------------------
# b. Create balanced set by selecting a subset of the majority class that is equal in
# size to the minority class size.

pima_us = RandomUnderSampler()
X_resampled, y_resampled = pima_us.fit_sample(pima, y)
# include visual evidence of task accomplished
# show the class sizes before/after random under sampling
print('Original dataset shape {}'.format(Counter(y)))
print('New dataset shape {}'.format(Counter(y_resampled)))

# ------------------------------------------------------------------------------
# outprint csv file of balanced data set
# open and write to a file
fout_sm = sm.fit_sample(pima, y)

# the fout_sm is originally a tuple with two arrays so each array needs to become
# a dataframe
# puts the predictor features into a data frame
df = pd.DataFrame(fout_sm[0][:])

# puts the response variable (diabetes) into a data frame
df2 = pd.DataFrame(fout_sm[1][:])

# put RUS data into data from
df1 = pd.DataFrame(pima_us.fit_sample(pima, y)[0][:])
df3 = pd.DataFrame(pima_us.fit_sample(pima, y)[1][:])

# This prints the csv file for the cleaned and balanced set
# that was produced by the SMOTE method, thus 500 values in each class of diabetes
np.savetxt("sebesta_HW2_pima_balanced-SMOTE.csv", df,
           header='Preg. Freq, PGC, BP, Tri.Thick, Insulin, BMI, DPF, Age, Diabetes',
           delimiter=",")

np.savetxt("sebesta_HW2_pima_balanced-RUS.csv", df1,
           header='Preg. Freq, PGC, BP, Tri.Thick, Insulin, BMI, DPF, Age, Diabetes',
           delimiter=",")

# --------------------------------------------------------------------------------
# Part 2: Structured Data Cleansing
# --------------------------------------------------------------------------------
''' Using the "HW2_2013Sales_AllQuant.csv" data accomplish tasks a-g. Include 
visual evidence that each task was accomplished.
'''
# import data set
sales = pd.read_csv('/Volumes/UTSA QRT2/IS 6713 Data Foundations/Assignments/HW2/HW2_2013Sales_AllQuant.txt')
# --------------------------------------------------------------------------------
# a. Identify the dimensions of the dataset (number of observations and features)
print(sales.shape)

sales.Item_Identifier_Code.hist()
sales.Item_Weight.hist()
sales.Item_Fat_Content_Code.hist()
sales.Item_Visibility.hist()
sales.Item_Type_Code.hist()
sales.Item_MRP.hist()
sales.Outlet_Identifier_Code.hist()
sales.Outlet_Establishment_Year.hist()
sales.Outlet_Size_Code.hist()
sales.Outlet_Location_Type.hist()
sales.Outlet_Type_Code.hist()
sales.Item_Outlet_Sales.hist()

sales.hist()

# -------------------------------------------------------------------------------

# b. Provide and evaluate basic descriptive statistics for each feature
# (Pandas DataFrame describe() function)
sales.describe()

# -------------------------------------------------------------------------------

# c. Examine each column for missing values
# replace the zeros in the outlet_type_code with na
# the outlet_type_code and the outlet_size should be similar as the size is the
# area of a store would be larger for larger stores like a supermarket
sales_col_NaN_count = sales.isnull().sum()
print(sales_col_NaN_count)

# -------------------------------------------------------------------------------

# d. Impute missing values with the mean, median, or mode, as you deem appropriate
# (and defend you method selection)
# item weights seems to have an outlier and thus I will impute by the median value
sales['Item_Weight'] = sales['Item_Weight'].fillna(sales['Item_Weight'].median())

# outlet size code takes on one of three values (1,2,3) and they are similar should
# have some relation to outlet_type code (0,1,2,3). size code will be replaced with
# the mode
sales['Outlet_Size_Code'] = sales['Outlet_Size_Code'].fillna(sales['Outlet_Size_Code'].median())

# the visibility is skewed and thus I will choose the mean to impute by
sales['Item_Visibility'] = sales['Item_Visibility'].fillna(sales['Item_Visibility'].mean())

# the item_outlet_sales
sales['Item_Outlet_Sales'] = sales['Item_Outlet_Sales'].fillna(sales['Item_Outlet_Sales'].median())

# look at descriptive stats after cleaning
sales.describe()
# --------------------------------------------------------------------------------

# e. Examine each column for nonsense or impossible values.
# 'Fix' missing values and defend you method of fixing them
# Item_Weight >12000 most probable of needing fixing, all other values are under 2000,
# it seems that potentially an extra zero was added to these entries. I will replace them
# with nan and then replace the missing values with the median
sal_IW = sales[sales['Item_Weight'] > 12000]
len(sal_IW)
sales['Item_Weight'][sales['Item_Weight'] > 12000] = np.NAN

# The following are slightly skewed but may not be in need of fixing
# Item_Outlet_Sales >8000
sal_IOS = sales[sales['Item_Outlet_Sales'] > 8000]
len(sal_IOS)

# Item_Visibility>0.25
sal_IV = sales[sales['Item_Visibility'] > 0.25]
len(sal_IV)

# --------------------------------------------------------------------------------

# f. Assess whether any list-wise deletion procedures are in order.
# Apply and defend you actions.

# 77 rows of data have na in any column. all 77 na come from the Item Weight column
# 8543 total the 77 rows with missing data is only 0.1% of the data therefore performing
# list-wise deletion on these row is appropreiate
sales_NaN = sales[sales.isnull().any(axis=1)]
print(sales_NaN)

col_NaN_count = sales.isnull().sum()
print(col_NaN_count)

# deleting the rows with the nan values
sales_dropNaN=sales.dropna(inplace=True)
print(sales.shape)
# --------------------------------------------------------------------------------

# g. Assess whether any features need to be standardized or normalized.
# Apply and defend your actions.
# using .skew and .kurt to assess whether to standardize or normalize variables

# sknewness less than -1 or greater than 1 distribution is highly skewed
# [Item_Outlet_Sales, Item_Visibility]
# skewness between -1 an 0-.5 distribution is slightly skewed
# [Outlet_Type_Code, Item_Fat_Content_Code]
# lack of skewness value =0
print(sales.skew())

# kurtosis are values between -2 and 2 are considered acceptable
print(sales.kurt())

# Item_Outlet_Sales and Item_Visibility are highly skewed and need to be looked at
# and scaled, the histograms validate the skewness
sales.Item_Outlet_Sales.hist()
sales.Item_Visibility.hist()

# scale Item_Outlet_Sales and Item_Visibility
sales_scaled = (sales-sales.min())/(sales.max()-sales.min())
sales_scaled.describe()

# --------------------------------------------------------------------------------
# write balanced data set to file
sales_df = pd.DataFrame(sales)

# This prints the csv file for the scaled data set of sales
np.savetxt("sebesta_HW2_sales.csv", sales_df,
           header='Item_Identifier_Code, Item_Weight, Item_Fat_Content_Code, Item_Visibility, '
                  'Item_Type_Code, Item_MRP, Outlet_Identifier_Code, Outlet_Establishment_Year, '
                  'Outlet_Size_Code, Outlet_Location_Type, Outlet_Type_Code, Item_Outlet_Sales',
           delimiter=",")
# --------------------------------------------------------------------------------