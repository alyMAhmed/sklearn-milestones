from __future__ import annotations
from dataclasses import dataclass, field

@dataclass(slots=True)
class InputTags:
    one_d_array: bool = False
    two_d_array: bool = True
    three_d_array: bool = False
    sparse: bool = False
    categorical: bool = False
    string: bool = False
    dict: bool = False
    positive_only: bool = False
    allow_nan: bool = False
    pairwise: bool = False

@dataclass(slots=True)
class TargetTags:
    required: bool
    one_d_labels: bool = False
    two_d_labels: bool = False
    positive_only: bool = False
    multi_output: bool = False
    single_output: bool = True

@dataclass(slots=True)
class TransformerTags:
    preserves_dtype: list[str] = field(default_factory=lambda: ["float64"])

@dataclass(slots=True)
class ClassifierTags:
    poor_score: bool = False
    multi_class: bool = True
    multi_label: bool = False

@dataclass(slots=True)
class RegressorTags:
    poor_score: bool = False

@dataclass(slots=True)
class Tags:
    estimator_type: str | None
    target_tags: TargetTags
    transformer_tags: TransformerTags | None = None
    classifier_tags: ClassifierTags | None = None
    regressor_tags: RegressorTags | None = None
    array_api_support: bool = False
    no_validation: bool = False
    non_deterministic: bool = False
    requires_fit: bool = True
    _skip_test: bool = False
    input_tags: InputTags = field(default_factory=InputTags)

def default_tags(estimator) -> Tags:
    est_is_classifier = getattr(estimator, "_estimator_type", None) == "classifier"
    est_is_regressor = getattr(estimator, "_estimator_type", None) == "regressor"
    target_required = est_is_classifier or est_is_regressor
    return Tags(
        estimator_type=getattr(estimator, "_estimator_type", None),
        target_tags=TargetTags(required=target_required),
        transformer_tags=(
            TransformerTags()
            if hasattr(estimator, "transform") or hasattr(estimator, "fit_transform")
            else None
        ),
        classifier_tags=ClassifierTags() if est_is_classifier else None,
        regressor_tags=RegressorTags() if est_is_regressor else None,
    )

import numpy as np

_DEFAULT_TAGS = {
    "array_api_support": False,
    "non_deterministic": False,
    "requires_positive_X": False,
    "requires_positive_y": False,
    "X_types": ["2darray"],
    "poor_score": False,
    "no_validation": False,
    "multioutput": False,
    "allow_nan": False,
    "stateless": False,
    "multilabel": False,
    "_skip_test": False,
    "_xfail_checks": False,
    "multioutput_only": False,
    "binary_only": False,
    "requires_fit": True,
    "preserves_dtype": [np.float64],
    "requires_y": False,
    "pairwise": False,
}


def _safe_tags(estimator, key=None):
    """Safely get estimator tags.

    :class:`~sklearn.BaseEstimator` provides the estimator tags machinery.
    However, if an estimator does not inherit from this base class, we should
    fall-back to the default tags.

    For scikit-learn built-in estimators, we should still rely on
    `self._get_tags()`. `_safe_tags(est)` should be used when we are not sure
    where `est` comes from: typically `_safe_tags(self.base_estimator)` where
    `self` is a meta-estimator, or in the common checks.

    Parameters
    ----------
    estimator : estimator object
        The estimator from which to get the tag.

    key : str, default=None
        Tag name to get. By default (`None`), all tags are returned.

    Returns
    -------
    tags : dict or tag value
        The estimator tags. A single value is returned if `key` is not None.
    """
    if hasattr(estimator, "_get_tags"):
        tags_provider = "_get_tags()"
        tags = estimator._get_tags()
    elif hasattr(estimator, "_more_tags"):
        tags_provider = "_more_tags()"
        tags = {**_DEFAULT_TAGS, **estimator._more_tags()}
    else:
        tags_provider = "_DEFAULT_TAGS"
        tags = _DEFAULT_TAGS

    if key is not None:
        if key not in tags:
            raise ValueError(
                f"The key {key} is not defined in {tags_provider} for the "
                f"class {estimator.__class__.__name__}."
            )
        return tags[key]
    return tags
