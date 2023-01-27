import numpy as np
import pandas as pd
import math
from joblib import dump, load
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

DEFAULT_PD_DATA = [2, 2, 3, 10, 10, 1, 1, 2]  # The input if no other input data is given.
FEATURES = ['studytime', 'failures', 'absences', 'G1', 'G2', 'freetime', 'goout',
            'traveltime']  # The features which are used to predict the grade.


class GradePredictionController:
    """
    A class to train and predict a students grade based on eight constant features.
    """

    def __init__(self, input_arr=None):
        if input_arr is None:
            input_arr = DEFAULT_PD_DATA
        self.model_storage_link = 'grade_prediction_model.joblib'
        self.training_data = pd.read_csv('data/student-mat.csv')
        self.features = FEATURES
        self.input_arr = input_arr

    def train_model(self):
        trainer = Trainer(parent=self)
        trainer.persist_model()

    def predict(self):
        predicter = Predicter(parent=self)
        return predicter.predict()


class Trainer:
    def __init__(self, parent):
        self.parent = parent  # The instance to the controller.
        self.model = self._train_model()

    def persist_model(self):
        """
        Stores the trained model at the defined model storage link.
        """
        dump(self.model, self.parent.model_storage_link)

    def _train_model(self):
        X, Y = self._get_x_y()
        X_train, X_test, Y_train, Y_test = self._train(X, Y)
        model = LinearRegression()
        model.fit(X_train, Y_train)
        return model

    def _get_x_y(self):
        X = (self.parent.training_data[self.parent.features]).values
        Y = self.parent.training_data['G3']
        return X, Y

    def _train(self, X, Y):
        """
        Parameters
        ----------
        :param X: The features data.
        :param Y: The data to be predicted by the model.
        """
        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.4, random_state=20, shuffle=True)
        return X_train, X_test, Y_train, Y_test


class Predicter:
    def __init__(self, parent):
        self.parent = parent # The instance to the controller.
        self.model = None  # The pre-trained model
        self.load_model()

    def load_model(self):
        """
        Loads the pre-trained model from the storage. If the model does not exist
        it trains and stores a new model.
        """
        try:
            self.model = load(self.parent.model_storage_link)
        except FileNotFoundError as e:
            self.parent.train_model()
            self.load_model()

    def predict(self):
        return math.ceil(self.model.predict(np.array(self.parent.input_arr).reshape((1, -1)))[0])
