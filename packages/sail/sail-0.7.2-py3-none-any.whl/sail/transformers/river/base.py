from river.compat import River2SKLTransformer
from sklearn.base import OneToOneFeatureMixin
from sklearn.utils.validation import _get_feature_names
from sail.utils.mixin import RiverAttributeMixin


class BaseRiverTransformer(
    OneToOneFeatureMixin, RiverAttributeMixin, River2SKLTransformer
):
    def __init__(self, *args, **Kwargs):
        super(BaseRiverTransformer, self).__init__(*args, **Kwargs)

    def _partial_fit(self, X, y):
        if not hasattr(self, "n_features_in_"):
            feature_names_in = _get_feature_names(X)
            if feature_names_in is not None:
                self.feature_names_in_ = feature_names_in

        return super()._partial_fit(X, y)
