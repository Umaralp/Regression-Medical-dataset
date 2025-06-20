# -*- coding: utf-8 -*-
"""Regression-ML-python.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1LVEkQ4FYCf48orkB7Wd5WIfF7KOQJNuL

# Regression with Scikit Learn - Machine Learning with Python
Project Outline
- A typical problem statement for machine learning
- Downloading and exploring a dataset for machine learning
- Linear regression with one variable using Scikit-learn
- Linear regression with multiple variables
- Using categorical features for machine learning
- Other models and techniques for regression using Scikit-learn
- Applying linear regression to other datasets
"""

from google.colab import files

# Upload CSV file
uploaded = files.upload()
# a CSV file containing verified historical data, consisting of the aforementioned information and the actual medical charges incurred by over 1300 customers.

import pandas as pd
import numpy as np

medical_df = pd.read_csv('medical-charges.csv')

medical_df # to show the table

"""The dataset contains 1338 rows and 7 columns. Each row of the dataset contains information about one customer.

Our objective is to find a way to estimate the value in the "charges" column using the values in the other columns. If we can do so for the historical data, then we should able to estimate charges for new customers too, simply by asking for information like their age, sex, BMI, no. of children, smoking habits and region.

Let's check the data type for each column.
"""

medical_df.info() # to check the data type for each column

medical_df.describe() # to view some statistics for the numerical columns

"""# Exploratory Analysis and Visualization"""

import plotly.express as px
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns

medical_df.age.describe()

# age
fig = px.histogram(medical_df,
                   x = 'age',
                   marginal='box',
                   nbins=47,
                   title='Age Distribution')
fig.update_layout(bargap=0.05)
fig.show()

#BMI
fig = px.histogram(medical_df,
                   x = 'bmi',
                   marginal='box',
                   title='BMI Distribution')
fig.update_layout(bargap=0.05)
fig.show()

#charges
sns.histplot(medical_df, x='charges',hue='smoker')

#charges
fig = px.histogram(medical_df,
            x='charges',
             title = 'Annual charges',
             color='smoker')
fig.update_layout(bargap=0.05)
fig.show()

# smoking
px.histogram(medical_df, x='smoker',color='sex')

# Age and Charges
px.scatter(medical_df,
           x ='age',
           y = 'charges',
           color='smoker',
           title = 'Age VS charges')

#BMI and Charges
px.scatter(medical_df,
           x = 'bmi',
           y ='charges',
           color = 'smoker',
           title = 'BMI VS charges')

"""### Correlation
As you can tell from the analysis, the values in some columns are more closely related to the values in "charges" compared to other columns. E.g. "age" and "charges" seem to grow together, whereas "bmi" and "charges" don't.

Here's how correlation coefficients can be interpreted ( [source](https://statisticsbyjim.com/basics/correlations/)):

Strength: The greater the absolute value of the correlation coefficient, the stronger the relationship.

The extreme values of -1 and 1 indicate a perfectly linear relationship where a change in one variable is accompanied by a perfectly consistent change in the other. For these relationships, all of the data points fall on a line. In practice, you won’t see either type of perfect relationship.

A coefficient of zero represents no linear relationship. As one variable increases, there is no tendency in the other variable to either increase or decrease.

When the value is in-between 0 and +1/-1, there is a relationship, but the points don’t all fall on a line. As r approaches -1 or 1, the strength of the relationship increases and the data points tend to fall closer to a line.

Direction: The sign of the correlation coefficient represents the direction of the relationship.

Positive coefficients indicate that when the value of one variable increases, the value of the other variable also tends to increase. Positive relationships produce an upward slope on a scatterplot.

Negative coefficients represent cases when the value of one variable increases, the value of the other variable tends to decrease. Negative relationships produce a downward slope.
Here's the same relationship expressed visually:

<img src="https://d138zd1ktt9iqe.cloudfront.net/media/seo_landing_files/diksha-q-how-to-calculate-correlation-coefficient-01-1609233340.png" alt="Correlation Coefficient" width="300"/>

"""

# correlation b/w age and charges
medical_df.charges.corr(medical_df.age)

# correlation b/w BMI and charges
medical_df.charges.corr(medical_df.bmi)

# # correlation b/w smoking and charges (it's high)
smoker_val = {'no':0,'yes':1}
smoker_num = medical_df.smoker.map(smoker_val)
medical_df.charges.corr(smoker_num)

"""# Linear Regression using a Single Feature
We now know that the "smoker" and "age" columns have the strongest correlation with "charges". Let's try to find a way of estimating the value of "charges" using the value of "age" for non-smokers. First, let's create a data frame containing just the data for non-smokers.
"""

non_smoker_df = medical_df[medical_df.smoker == 'no']
non_smoker_df

# visualize the relationship between "age" and "charges"
sns.scatterplot(data=non_smoker_df, x='age',y='charges',s=10)

# The estimate_charges function is our very first model.
def estimate_charges(age, w, b):
  return w * age + b

# Let's guess the values for and use them to estimate the value for charges.

w = 50
b = 100
ages = non_smoker_df.age
estimated_charges = estimate_charges(ages, w, b)

# We can plot the estimated charges using a line graph.

plt.plot(ages,estimated_charges, 'r-o')

#As expected, the points lie on a straight line. We can overlay this line on the actual data, so see how well our model fits the data.
target = non_smoker_df.charges
plt.scatter(ages,target,s=6)

target = non_smoker_df.charges
plt.plot(ages,estimated_charges, 'r-o',alpha=0.7)
plt.scatter(ages,target,s=6)
plt.xlabel('Age');
plt.ylabel("charges");

"""Clearly, the our estimates are quite poor and the line does not "fit" the data. However, we can try different values of
 and
 to move the line around. Let's define a helper function try_parameters which takes w and b as inputs and creates the above plot.
"""

def try_parameters(w, b):
  ages = non_smoker_df.age
  target = non_smoker_df.charges

  estimated_charges = estimate_charges(ages, w, b)

  plt.plot(ages,estimated_charges, 'r-o',alpha=0.7)
  plt.scatter(ages,target,s=6)
  plt.xlabel('Age');
  plt.ylabel("charges");

try_parameters(100, 500)

try_parameters(40, 6000)

"""## Loss/Cost Function
We can compare our model's predictions with the actual targets using the following method:

Calculate the difference between the targets and predictions (the differenced is called the "residual")
Square all elements of the difference matrix to remove negative values.
Calculate the average of the elements in the resulting matrix.
Take the square root of the result
The result is a single number, known as the root mean squared error (RMSE). The above description can be stated mathematically as follows:
###  root mean squared error (RMSE):
![](https://camo.githubusercontent.com/adfca29d2d112f78f2befc9ae0b4c2748eb5f1ef4db425cd224c798ee3a29dea/68747470733a2f2f692e696d6775722e636f6d2f5743616e506b412e706e67)

Geometrically, the residuals can be visualized as follows:

![](https://camo.githubusercontent.com/372a7d3c0b259b6cbc0cefbac29f9b2652597805504c3a438d0239bbc296b603/68747470733a2f2f692e696d6775722e636f6d2f6c6c334e4c38302e706e67)
"""

# Let's define a function to compute the RMSE
def rmse(targets, predictions):
  return np.sqrt(np.mean(np.square(targets - predictions)))

w = 50
b = 100
try_parameters(w, b)

# Let's compute the RMSE for our model with a sample set of weights
targets = non_smoker_df['charges']
predicted = estimate_charges(non_smoker_df.age, w, b)

rmse(targets, predicted) # rmse= 8461.949562575493

"""Here's how we can interpret the above number: On average, each element in the prediction differs from the actual target by $8461.

The result is called the loss because it indicates how bad the model is at predicting the target variables. It represents information loss in the model: the lower the loss, the better the model.
"""

# modify the try_parameters functions to also display the loss.

def try_parameters(w, b):
    ages = non_smoker_df.age
    target = non_smoker_df.charges
    predictions = estimate_charges(ages, w, b)

    plt.plot(ages, predictions, 'r', alpha=0.9);
    plt.scatter(ages, target, s=8,alpha=0.8);
    plt.xlabel('Age');
    plt.ylabel('Charges')
    plt.legend(['Prediction', 'Actual']);

    loss = rmse(targets, predictions)
    print("RMSE LOSS:" ,loss)

try_parameters(50, 100)

#  Try different values of 'w' and 'b' to minimize the RMSE loss.
try_parameters(50, 4000)



"""# Linear Regression using Scikit-learn
In practice, you'll never need to implement either of the above methods yourself. You can use a library like scikit-learn to do this for you.
"""

from sklearn.linear_model import LinearRegression

"""Let's use the LinearRegression class from scikit-learn to find the best fit line for "age" vs. "charges" using the ordinary least squares optimization technique.

First, we create a new model object.
"""

model = LinearRegression()
model

"""Next, we can use the fit method of the model to find the best fit line for the inputs and targets.

Not that the input X must be a 2-d array, so we'll need to pass a dataframe, instead of a single column.
"""

#note: the input and the target should be of the same value!
inputs = non_smoker_df[['age']]
targets = non_smoker_df.charges
print('Inputs.Shape:',inputs.shape)
print('Targets.Shape:',targets.shape)

# Let's fit the model to the data.
model.fit(inputs, targets)

# We can now make predictions using the model. Let's try predicting the charges for the ages 23, 37 and 61
model.predict(np.array([[23],
                       [50],
                       [60]]))

# Compare them with the scatter plot above.

# Let compute the predictions for the entire set of inputs

inputs

predictions = model.predict(inputs)

predictions

# Let's compute the RMSE loss to evaluate the model.
rmse(targets, predictions) # rmse= 4662.505766636395

"""Seems like our prediction is off by $4000 on average, which is not too bad considering the fact that there are several outliers.

The parameters of the model are stored in the coef_ and intercept_ properties.
"""

model.intercept_

model.coef_

# we now got the 'w' and 'b' values
#RMSE LOSS: 4662.505766636395
try_parameters(model.coef_, model.intercept_)

"""# Linear Regression using Multiple Features
So far, we've used on the "age" feature to estimate "charges". Adding another feature like "bmi" is fairly straightforward. We simply assume the following relationship:

[charges = w1 x age + w2 x bmi + b]

We need to change just one line of code to include the BMI.
"""

# create inputs and targets
# Multiple inputs and single target
inputs, targets = non_smoker_df[['age','bmi','children']], non_smoker_df['charges']

# create and train model
model = LinearRegression().fit(inputs, targets)

# Generate predictions
predictions = model.predict(inputs)

# compute the loss
loss = rmse(targets, predictions)
print('Loss: ',loss)

"""Loss:  4608.470405038246
As you can see, adding the BMI doesn't seem to reduce the loss by much, as the BMI has a very weak correlation with charges, especially for non smokers.
"""

non_smoker_df.charges.corr(non_smoker_df.bmi)

px.scatter(non_smoker_df, x='bmi',y='charges')

model.coef_, model.intercept_

"""Let's go one step further, and add the final numeric column: "children", which seems to have some correlation with "charges".

### charges = w1 x age + w2 x bmi + w3 x children + b
"""

non_smoker_df.charges.corr(non_smoker_df.children)

px.strip(non_smoker_df, x="children", y ='charges')

# create inputs and targets
inputs, targets = non_smoker_df[['age','bmi','children']], non_smoker_df['charges']

# create and train model
model = LinearRegression().fit(inputs, targets)

# Generate predictions
predictions = model.predict(inputs)

# compute the loss
loss = rmse(targets, predictions)
print('Loss: ',loss)

"""Once again, we don't see a big reduction in the loss, even though it's greater than in the case of BMI."""

inputs, targets = medical_df[['age','bmi','children']], medical_df['charges']

model = LinearRegression().fit(inputs, targets)

predictions = model.predict(inputs)

loss = rmse(targets, predictions)
print('Loss:', loss)

"""# Using Categorical Features for Machine Learning
So far we've been using only numeric columns, since we can only perform computations with numbers. If we could use categorical columns like "smoker", we can train a single model for the entire dataset.

To use the categorical columns, we simply need to convert them to numbers. There are three common techniques for doing this:

If a categorical column has just two categories (it's called a binary category), then we can replace their values with 0 and 1.
If a categorical column has more than 2 categories, we can perform one-hot encoding i.e. create a new column for each category with 1s and 0s.
If the categories have a natural order (e.g. cold, neutral, warm, hot), then they can be converted to numbers (e.g. 1, 2, 3, 4) preserving the order. These are called ordinals
# Binary Categories
The "smoker" category has just two values "yes" and "no". Let's create a new column "smoker_code" containing 0 for "no" and 1 for "yes".
"""

sns.barplot(data=medical_df, x='smoker',y ='charges')

smoker_codes = {'no':0, 'yes': 1}
medical_df['smoker_code'] = medical_df.smoker.map(smoker_codes)

medical_df

medical_df.charges.corr(medical_df.smoker_code)

"""now use the smoker_df column for linear regression.

### charges = w1 x age + w2 x bmi + w3 x children + w4 x smoker + b
"""

# create inputs and targets
inputs, targets = medical_df[['age','bmi','children','smoker_code']], medical_df['charges']

# create and train model
model = LinearRegression().fit(inputs, targets)

# Generate predictions
predictions = model.predict(inputs)

# compute the loss
loss = rmse(targets, predictions)
print('Loss: ',loss)

"""The loss reduces from 11355 to 6056, almost by 50%! This is an important lesson: never ignore categorical data.

Let's try adding the "sex" column as well.


### charges = w1 x age + w2 x bmi + w3 x children +  w4 x smoker + w5 x sex + b
"""

sns.barplot(data= medical_df, x = 'sex',y ='charges')

sex_code = {'female': 0 , 'male': 1 }

medical_df['sex_code'] = medical_df.sex.map(sex_code)

medical_df.charges.corr(medical_df.sex_code)

# create inputs and targets
inputs, targets = medical_df[['age','bmi','children','sex_code','smoker_code']], medical_df['charges']

# create and train model
model = LinearRegression().fit(inputs, targets)

# Generate predictions
predictions = model.predict(inputs)

# compute the loss
loss = rmse(targets, predictions)
print('Loss: ',loss)

"""# One-hot Encoding
The "region" column contains 4 values, so we'll need to use hot encoding and create a new column for each region.

![](https://camo.githubusercontent.com/769485369ecb3ad366891d8a47e55b53175eee0e37ab233ddb43ee371ae1e478/68747470733a2f2f692e696d6775722e636f6d2f6e384775694f4f2e706e67)

"""

sns.barplot(data = medical_df, x = 'region', y = 'charges');

from sklearn import preprocessing
encode = preprocessing.OneHotEncoder()
encode.fit(medical_df[['region']])
encode.categories_

one_hot = encode.transform(medical_df[['region']]).toarray()
one_hot

medical_df[['northeast','northwest','southeast','southwest']] = one_hot

medical_df

"""Let's include the region columns into our linear regression model.

### charges = w1 x age + w2 x bmi + w3 x children +  w4 x smoker + w5 x sex + w6 x region + b
"""

# create inputs and targets
inputs, targets = medical_df[['age','bmi','children','sex_code','smoker_code','northeast','northwest','southeast','southwest']], medical_df['charges']

# create and train model
model = LinearRegression().fit(inputs, targets)

# Generate predictions
predictions = model.predict(inputs)

# compute the loss
loss = rmse(targets, predictions)
print('Loss: ',loss)

from sklearn.ensemble import RandomForestRegressor

inputs, targets = medical_df[['age','bmi','children','sex_code','smoker_code','northeast','northwest','southeast','southwest']], medical_df['charges']

# create and train model
model_rf = RandomForestRegressor().fit(inputs, targets)

# Generate predictions
predictions = model_rf.predict(inputs)

# compute the loss
loss = rmse(targets, predictions)
print('Loss: ',loss)

model_rf.predict([[19,24,0,0,0,0,0,0,1]])