import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split


class CloudPointClassifier:
    def __init__(self):
        self.model = RandomForestClassifier()

    def classify_las(self, df):
        predictions = self.model.predict(df.drop(columns=['label']))
        return predictions

    def train_model(self, features, labels):
        features = features.apply(pd.to_numeric, errors='coerce')
        X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.2, random_state=42)
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.model.fit(X_train, y_train)
        return self.model
