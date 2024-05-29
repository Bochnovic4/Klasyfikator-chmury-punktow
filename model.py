import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import balanced_accuracy_score, classification_report
import joblib
import numpy as np
from las_file_manager import LasFileManager
import matplotlib.pyplot as plt
from settings import N_JOBS, COLUMNS, MAX_DEPTH, N_ESTIMATORS


class CloudPointClassifier:
    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=N_ESTIMATORS, random_state=42, n_jobs=N_JOBS, max_depth=MAX_DEPTH)
        self.is_enabled = False

    def classify(self, las_file_manager):
        values_dict = las_file_manager.get_model_values()

        features = pd.DataFrame(values_dict)
        features = features.apply(pd.to_numeric, errors='coerce')

        y_pred = self.model.predict(features)
        y_test = las_file_manager.classes

        acuracy = balanced_accuracy_score(y_test, y_pred)
        print(f'Balanced accuracy: {acuracy:.2f}')
        print(classification_report(y_test, y_pred))
        las_file_manager.classes = self.model.predict(features)

    def train_model(self, las_file_manager):
        values_dict = las_file_manager.get_model_values(ground_classes=[2])

        features = pd.DataFrame(values_dict)
        features = features.apply(pd.to_numeric, errors='coerce')

        x_train, x_test, y_train, y_test = train_test_split(features, las_file_manager.classes, test_size=0.20,
                                                            random_state=42)

        self.model.fit(x_train, y_train)
        self.is_enabled = True

    def save(self, filename):
        joblib.dump(self.model, filename)

    def load(self, filename):
        self.model = joblib.load(filename)
        self.is_enabled = True
