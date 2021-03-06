# -*- coding: utf-8 -*-
"""California Housing regression.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1RowZwE0L12d9R4tifwkAwZs5wXQJGCQj

# Regression Analysis

## Importing the libraries
"""

from google.colab import drive
drive.mount('/content/drive')

# Commented out IPython magic to ensure Python compatibility.
import pandas as pd
import numpy as np
import matplotlib
# %matplotlib inline
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pandas.plotting import scatter_matrix
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor

from sklearn import metrics

"""## Importing the Dataset and visualizing the data"""

data_ =pd.read_csv('/content/drive/My Drive/data/housing.csv')
data_.head()

data_.info()

data_.describe()

data_.shape

len(data_)

data_.isnull().sum()

"""### Missing Values
- Drop rows with missing values
- Fill with constant
- Fill with mean, median, mode
- Fill with random sample
- Impute value from predictive model
"""

#data_.dropna() for dropping
#data_['total_bedrooms'].fillna(300, inplace=True)  #fill up with constant value
#data_['total_bedrooms'].fillna(data_['total_bedrooms'].sample().iloc[0], inplace=True)

data_['total_bedrooms'].fillna(data_['total_bedrooms'].median(), inplace=True)

data_.isnull().sum()

data_["ocean_proximity"].value_counts()

data_.hist(bins=50, figsize=(20,15))
plt.show();

pd.plotting.scatter_matrix(data_, figsize=(20,20))
plt.show()

data_.plot(kind="scatter", x="median_income", y="median_house_value",
             alpha=0.1,color = 'blue')
plt.show()

"""This plot reveals a few things. First, the correlation is indeed very strong; you can clearly see the upward trend and the points are not too dispersed."""

# since there are latitude and longitudes, its good idea to have a scatter plot
#set alpha =0.1 to clearly see dense points
data_.plot(kind="scatter",x="longitude",y="latitude",alpha=0.1)

#advanced scatter plot using median value of house
data_.plot(kind="scatter",x="longitude",y="latitude",alpha=0.4,
         s=data_["population"]/100,label="population",
         c="median_house_value",cmap=plt.get_cmap("jet"),
         colorbar=True)
plt.legend()

"""Now we can say that the house price is a bit related to the location (e.g close to ocean) and to the density of the population."""

# Calculate pearson's r coefficient
corr_matrix=data_.corr()
corr_matrix

corr_matrix["median_house_value"].sort_values(ascending=False)

#Adding more feature

data_["rooms_per_household"]=data_["total_rooms"]/data_["households"]
data_["bedrooms_per_room"]=data_["total_bedrooms"]/data_["total_rooms"]
data_["population_per_household"]=data_["population"]/data_["households"]

data_.head()

corr_matrix=data_.corr()
corr_matrix["median_house_value"].sort_values(ascending=False)

"""Not bad haha ! The number of rooms per household is now more informative than the total number of rooms in a district"""

#heatmap using seaborn
#set the context for plotting 
sns.set(context="paper",font="monospace")
data_corr_matrix = data_.corr()
#set the matplotlib figure
fig, axe = plt.subplots(figsize=(12,8))
#Generate color palettes 
cmap = sns.diverging_palette(220,10,center = "light", as_cmap=True)
#draw the heatmap
sns.heatmap(data_corr_matrix,vmax=1,square =True, cmap=cmap,annot=True );

labelEncoder = LabelEncoder()
print(data_["ocean_proximity"].value_counts())
data_["ocean_proximity"] = labelEncoder.fit_transform(data_["ocean_proximity"])
data_["ocean_proximity"].value_counts()
data_.head()

"""**Dependent and independent features**"""

X= data_.drop(['median_house_value'],axis=1)
y= data_['median_house_value']

X.head()

y.head()

#y=y.values.reshape(-1,1)

"""## Train test split"""

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.20, random_state = 42)

SC= StandardScaler()
X_train = SC.fit_transform(X_train)
X_test = SC.transform(X_test)

print(X_train[0:5,:])
print(X_test[0:5,:])

"""##XGBoost Regression"""

import xgboost as xgb
from sklearn.model_selection import cross_val_score, KFold

xgbr = xgb.XGBRegressor(verbosity=0)
xgbr.fit(X_train, y_train)

score = xgbr.score(X_train, y_train)  
print("Training score: ", score)

score = xgbr.score(X_test, y_test)  
print("Testing score: ", score)

scores = cross_val_score(xgbr, X_train, y_train,cv=10)
print("Mean cross-validation score: %.2f" % scores.mean())

kfold = KFold(n_splits=10, shuffle=True)
kf_cv_scores = cross_val_score(xgbr, X_train, y_train, cv=kfold )
print("K-fold CV average score: %.2f" % kf_cv_scores.mean())

"""##Random Forest Regression"""

from sklearn.ensemble import RandomForestRegressor
regressor = RandomForestRegressor(n_estimators = 100, random_state = 42)
regressor.fit(X_train, y_train)

"""**Coefficient of determination, $R^2$**<br/>
The proportion of the variance in the dependent variable that is predictable from the independent variable(s).

<p style="text-align: center;">
$R^2 = 1 - \frac{MSE}{\sigma^2} $
</p>

The method `score` will calculate $R^2$ for us.

**Testing Accuracy**
"""

regressor.score(X_test,y_test) #providing R^2 value

"""**Training Accuracy**"""

regressor.score(X_train,y_train)

"""**Parameter of the model**"""

regressor.get_params()

"""n_estimators = number of trees in the forest

max_features = max number of features considered for splitting a node

max_depth = max number of levels in each decision tree

min_samples_split = min number of data points placed in a node before the node is split

min_samples_leaf = min number of data points allowed in a leaf node

bootstrap = method for sampling data points (with or without replacement)

## Hyperparameter Tuning with RandomsearchCV
"""

from pprint import pprint
from sklearn.model_selection import RandomizedSearchCV
# Number of trees in random forest
n_estimators = [int(x) for x in np.linspace(start = 100, stop = 2000, num = 10)]
# Number of features to consider at every split
max_features = ['auto', 'sqrt']
# Maximum number of levels in tree
max_depth = [int(x) for x in np.linspace(10, 110, num = 11)]
max_depth.append(None)
# Minimum number of samples required to split a node
min_samples_split = [2, 5, 10]
# Minimum number of samples required at each leaf node
min_samples_leaf = [1, 2, 4]
# Method of selecting samples for training each tree
bootstrap = [True, False]
# Create the random grid
random_grid = {'n_estimators': n_estimators,
               'max_features': max_features,
               'max_depth': max_depth,
               'min_samples_split': min_samples_split,
               'min_samples_leaf': min_samples_leaf,
               'bootstrap': bootstrap}
pprint(random_grid)

# Using the random grid to search for best hyperparameters
# First creating the base model to tune
rf = RandomForestRegressor()
# Random search of parameters, using 10 fold cross validation, 
# search across 100 different combinations, and use all available cores
rf_random = RandomizedSearchCV(estimator = rf, param_distributions = random_grid, n_iter = 500, cv = 10, verbose=2, random_state=42, n_jobs = -1)
# Fit the random search model
rf_random.fit(X_train, y_train)

rf_random.best_params_

best_rand=rf_random.best_estimator_

best_rand.score(X_test,y_test)

best_rand.score(X_train,y_train)

"""## Hyperparameter Tuning with GridsearchCV"""

from sklearn.model_selection import GridSearchCV

# Creating the parameter grid based on the results of random search 
param_grid = {
    'bootstrap': [True],
    'max_depth': [None, 80, 90, 100, 110],
    'min_samples_leaf': [1, 2, 3, 4, 5],
    'min_samples_split': [2, 4, 6, 8, 10, 12],
    'n_estimators': [10, 50, 100, 200, 300, 1000]
}
# Creating a based model
rf = RandomForestRegressor()
# Instantiate the grid search model
grid_search = GridSearchCV(estimator = rf, param_grid = param_grid, 
                          cv = 5, n_jobs = -1, verbose = 2)

# Fit the grid search to the data
grid_search.fit(X_train, y_train)

grid_search.best_params_

best_grid = grid_search.best_estimator_
best_grid.score(X_test,y_test)

best_grid.score(X_train,y_train)

"""## Decision Tree Model

**Fitting the Model**
"""

from sklearn.tree import DecisionTreeRegressor
regressor_dt = DecisionTreeRegressor(random_state = 42)
regressor_dt.fit(X_train, y_train)

"""**Test Accuracy**"""

regressor_dt.score(X_test,y_test)

"""**Training Accuracy**"""

regressor_dt.score(X_train,y_train)

"""**Parameter of the Model**"""

regressor_dt.get_params

"""##Multiple linear Regression"""

from sklearn.linear_model import LinearRegression
lin_regressor = LinearRegression()
lin_regressor.fit(X_train, y_train)

"""**Testing Accuracy**"""

lin_regressor.score(X_test,y_test)

"""**Training Accuracy**"""

lin_regressor.score(X_train,y_train)

"""we can use regularization method such as lasso regression or ridge regression to reduce the overfitting"""