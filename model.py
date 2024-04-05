import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import QuantileTransformer
import joblib

from settings import N_JOBS, COLUMNS


class CloudPointClassifier:
    def __init__(self):
        self.model = None
        self.transformer = None

    def classify(self, points):
        df = pd.DataFrame(points, columns=COLUMNS)
        df = df.apply(pd.to_numeric, errors='coerce')
        df = self.transformer.transform(df)
        predictions = self.model.predict(df)
        return predictions

    def train_model(self, features, labels):
        features = pd.DataFrame(features, columns=COLUMNS)
        features = features.apply(pd.to_numeric, errors='coerce')
        
        self.transformer = QuantileTransformer(output_distribution='uniform', random_state=42)
        features = self.transformer.fit_transform(features)

        X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.2, random_state=42)

        self.model = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=N_JOBS)
        self.model.fit(X_train, y_train)

    def save(self, filename):
        joblib.dump((self.model, self.transformer), filename)

    def load(self, filename):
        self.model, self.transformer = joblib.load(filename)
