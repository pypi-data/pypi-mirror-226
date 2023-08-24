from sklearn.base import ClassNamePrefixFeaturesOutMixin
from .base import SAILTransformer


class ColumnNamePrefixTransformer(ClassNamePrefixFeaturesOutMixin, SAILTransformer):
    def __init__(self, prefix="") -> None:
        self.prefix = prefix

    def fit(self, X: list, y=None):
        return self

    def transform(self, X, y=None):
        X = X.copy()

        for feature in X.columns:
            X[self.prefix + "_" + feature] = X[feature]

        return X

    def fit_transform(self, X, y=None):
        return self.transform(X)
