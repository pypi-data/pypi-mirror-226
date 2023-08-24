from .base import SAILTransformer
import numpy as np


class Polar2CartTransformer(SAILTransformer):
    def __init__(self, n, features=None, suffix_x="x", suffix_y="y") -> None:
        self.n = n
        self.features = features
        self.suffix_x = suffix_x
        self.suffix_y = suffix_y

    def fit(self, X: list, y=None):
        return self

    def transform(self, X, y=None):
        features = self.features if self.features else X.columns
        for feature in features:
            name_x = feature + "_" + self.suffix_x
            X[name_x] = np.cos(2 * np.pi * X[feature] / self.n)
            name_y = feature + "_" + self.suffix_y
            X[name_y] = np.sin(2 * np.pi * X[feature] / self.n)

        return X

    def fit_transform(self, X, y=None):
        return self.transform(X)
