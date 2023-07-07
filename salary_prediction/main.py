import os
import requests

import pandas as pd
import itertools
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_percentage_error as mape

# download data if it is unavailable
if 'data.csv' not in os.listdir('.'):
    url = "https://www.dropbox.com/s/3cml50uv7zm46ly/data.csv?dl=1"
    r = requests.get(url, allow_redirects=True)
    open('./data.csv', 'wb').write(r.content)

# read data
data = pd.read_csv('./data.csv')

# write your code here
y = data["salary"]
filtered_columns = data.columns[[x > 0.2 and x != 1 for x in data.corr()["salary"]]]
mapes = []
metrics = []

for i in range(len(filtered_columns)):
    columns = itertools.combinations(filtered_columns, r=i + 1)
    for c in columns:
        X = data.drop(['salary'] + list(c), axis=1)
        
        train_X, test_X, train_y, test_y = train_test_split(X, y, test_size=0.3, random_state=100)
        train_X = np.array(train_X)
        test_X = np.array(test_X)
        train_y = np.array(train_y)
        test_y = np.array(test_y)
        
        model = LinearRegression()
        model.fit(train_X, train_y)
        
        y_pred = model.predict(test_X)
        mapes.append(mape(test_y, y_pred))
        metrics.append(list(c))

best_metrics = metrics[mapes.index(min(mapes))] + ["salary"]
X = data.drop(best_metrics, axis=1)

train_X, test_X, train_y, test_y = train_test_split(X, y, test_size=0.3, random_state=100)
train_X = np.array(train_X)
test_X = np.array(test_X)
train_y = np.array(train_y)
test_y = np.array(test_y)

model = LinearRegression()
model.fit(train_X, train_y)

pred_y = model.predict(test_X)

pred_y_1 = np.copy(pred_y)
pred_y_1[pred_y_1 < 0] = 0
mape_1 = mape(test_y, pred_y_1)

pred_y_2 = np.copy(pred_y)
pred_y_2[pred_y_2 < 0] = np.median(train_y)
mape_2 = mape(test_y, pred_y_2)

print("%.5f" % min(mape_1, mape_2))
