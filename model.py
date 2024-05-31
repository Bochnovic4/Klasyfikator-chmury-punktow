import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import joblib
import numpy as np

from settings import N_JOBS, COLUMNS, MAX_DEPTH


class CloudPointClassifier:
    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=N_JOBS, max_depth=MAX_DEPTH)
        self.is_enabled = False

    def classify(self, las_file_manager):
        (z,
         intensity,
         number_of_returns,
         return_number,
         cylinder_density,
         normal_vectors_x,
         normal_vectors_y,
         normal_vectors_z,
         min_height,
         max_height,
         mean_height) = las_file_manager.get_model_values()

        features = np.vstack((z,
                              intensity,
                              number_of_returns,
                              return_number,
                              cylinder_density,
                              normal_vectors_x,
                              normal_vectors_y,
                              normal_vectors_z,
                              min_height,
                              max_height,
                              mean_height)).T
        features = pd.DataFrame(features, columns=COLUMNS)
        las_file_manager.classes = self.model.predict(features)

    def train_model(self, las_file_manager):
        (z,
         intensity,
         number_of_returns,
         return_number,
         cylinder_density,
         normal_vectors_x,
         normal_vectors_y,
         normal_vectors_z,
         min_height,
         max_height,
         mean_height) = las_file_manager.get_model_values(ground_classes=[2])
        features = np.vstack((z,
                              intensity,
                              number_of_returns,
                              return_number,
                              cylinder_density,
                              normal_vectors_x,
                              normal_vectors_y,
                              normal_vectors_z,
                              min_height,
                              max_height,
                              mean_height)).T
        features = pd.DataFrame(features, columns=COLUMNS)
        features = features.apply(pd.to_numeric, errors='coerce')
        x_train, x_test, y_train, y_test = train_test_split(features, las_file_manager.classes, test_size=0.2,
                                                            random_state=42)
        self.model.fit(x_train, y_train)
        self.is_enabled = True

    def save(self, filename):
        joblib.dump(self.model, filename)

    def load(self, filename):
        self.model = joblib.load(filename)
        self.is_enabled = True
