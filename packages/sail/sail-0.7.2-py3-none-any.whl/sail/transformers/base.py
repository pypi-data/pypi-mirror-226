from abc import ABCMeta, abstractmethod

from sklearn.base import BaseEstimator, TransformerMixin


class SAILTransformer(TransformerMixin, BaseEstimator, ABCMeta):
    @abstractmethod
    def fit():
        raise NotImplementedError

    @abstractmethod
    def partial_fit():
        raise NotImplementedError

    @abstractmethod
    def transform():
        raise NotImplementedError

    @abstractmethod
    def fit_transform():
        raise NotImplementedError
