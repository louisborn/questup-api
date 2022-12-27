import numpy as np
import pandas as pd
# from sklearn import *
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
# from sklearn.metrics import *
from joblib import dump, load


class GradePredictionController:
    """

    """
    def __init__(self, prediction_data=None):
        if prediction_data is None:
            prediction_data = [2, 0, 3, 10, 10]
        self.storage = 'grade_prediction_model.joblib'
        self.data = pd.read_csv('questup-api/data/student-mat.csv')
        self.features = ['studytime', 'failures', 'absences', 'G1', 'G2']
        self.prediction_data = prediction_data

    def train_model(self):
        trainer = Trainer(student_data=self.data, selected_features=self.features)
        trainer.persist_model()
        return 'Okay'

    def predict(self):
        predicter = Predicter(self.storage, self.prediction_data)
        return predicter.predict()


class Trainer:
    def __init__(self, storage, student_data, selected_features):
        self.storage = storage
        self.student_data = student_data
        self.selected_features = selected_features
        self.model = self._train_model()

    def persist_model(self):
        dump(self.model, self.storage)

    def _train_model(self):
        X, Y = self._get_x_y()
        X_train, X_test, Y_train, Y_test = self._train(X, Y)
        model = LinearRegression()
        model.fit(X_train, Y_train)
        return model

    def _get_x_y(self):
        X = (self.student_data[self.selected_features]).values
        Y = self.student_data['G3']
        return X, Y

    def _train(self, X, Y):
        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.4, random_state=20, shuffle=True)
        return X_train, X_test, Y_train, Y_test


class Predicter:
    def __init__(self, storage, prediction_data):
        self.storage = storage
        self.prediction_data = prediction_data
        self.model = self.load_model()

    def load_model(self):
        return load(self.storage)

    def predict(self):
        return self.model.predict(np.array(self.prediction_data).reshape((1, -1)))[0]

# student_data['G4'] = model.predict(np.array(input_to_guess).reshape((1, -1)))[0]
# print(model.predict(np.array(input_to_guess).reshape((1, -1)))[0])

# it would also be possible to make a prediction for a particular row in the dataset
# print(model.predict((student_data.iloc[44-2][best_features]).values.reshape(1,-1)), "guessed_row")
