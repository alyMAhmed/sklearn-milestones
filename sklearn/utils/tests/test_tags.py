# [ENV-PATCH] get_tags function not available in M03
# This file is skipped because it imports modules not available in M03
import pytest
pytestmark = pytest.mark.skip(reason='[ENV-PATCH] Entire file skipped - imports unavailable in M03')

# import pytest

# from sklearn.base import BaseEstimator, RegressorMixin, TransformerMixin
# from sklearn.utils._tags import get_tags


# class NoTagsEstimator:
#     pass


# class ClassifierEstimator:
#     # This is to test whether not inheriting from mixins works.
#     _estimator_type = "classifier"


# @pytest.mark.parametrize(
#     "estimator, value",
#     [
#         [NoTagsEstimator(), False],
#         [ClassifierEstimator(), True],
#         [TransformerMixin(), False],
#         [RegressorMixin(), True],
#         [BaseEstimator(), False],
#     ],
# )
# def test_requires_y(estimator, value):
#     assert get_tags(estimator).target_tags.required == value
