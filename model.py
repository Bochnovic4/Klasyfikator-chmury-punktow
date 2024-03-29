from sklearn.model_selection import StratifiedShuffleSplit
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

import joblib

from settings import N_JOBS, COLUMNS


class CloudPointClassifier:
    def __init__(self):
        self.model = None

    def classify(self, points):
        df = pd.DataFrame(points, columns=COLUMNS)
        predictions = self.model.predict(df)
        return predictions

    def train_model(self, features, labels):
        features = pd.DataFrame(features, columns=COLUMNS)
        features = features.apply(pd.to_numeric, errors='coerce')
        labels = pd.Series(labels)

        splitter = StratifiedShuffleSplit(n_splits=1, test_size=0.2, random_state=42)
        for train_index, test_index in splitter.split(features, labels):
            X_train, X_test = features.iloc[train_index], features.iloc[test_index]
            y_train, y_test = labels.iloc[train_index], labels.iloc[test_index]

        self.model = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=N_JOBS)
        self.model.fit(X_train, y_train)

    def save(self, filename):
        joblib.dump(self.model, filename)

    def load(self, filename):
        self.model = joblib.load(filename)

