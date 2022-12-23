import numpy as np
import pandas as pd
from sklearn import *
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import *


student_data=pd.read_csv('input/student-mat.csv')

# predict value for new row is not working yet
#student_data.insert(33, column="G4", value=None)

print(student_data.head())

best_features = ['studytime', 'failures', 'absences', 'G1', 'G2']

X = student_data[best_features]
X = X.values
Y = student_data['G3']
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.4, random_state=20, shuffle=True)

# linear Regression is used as machine learning technique
model = LinearRegression()
model.fit(X_train, Y_train)
pred = model.predict(X_test)

print(f'MSE: {metrics.mean_squared_error(Y_test,pred)}')
print(f'Accuracy: {round(r2_score(Y_test , pred),3)*100}%')

best_features=['studytime', 'failures', 'absences', 'G1', 'G2']

# here we have a list of values of the features that we use to make prediction and can use it as single input
input_to_guess = [2, 0, 6, 5, 6]
predicted_grade = model.predict(np.array(input_to_guess).reshape((1, -1)))[0]
print(predicted_grade, "guessed")

student_data['G4'] = model.predict(np.array(input_to_guess).reshape((1, -1)))[0]
print(model.predict(np.array(input_to_guess).reshape((1, -1)))[0])

# it would also be possible to make a prediction for a particular row in the dataset
#print(model.predict((student_data.iloc[44-2][best_features]).values.reshape(1,-1)), "guessed_row")

