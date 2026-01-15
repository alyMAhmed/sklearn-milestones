"""Stub module for instance_generator - added as environment patch."""

def _get_check_estimator_ids(obj):
    """Stub function."""
    return getattr(obj, "__class__", type(obj)).__name__

def _tested_estimators(*args, **kwargs):
    """Stub function that returns empty list."""
    return []

def _construct_instances(*args, **kwargs):
    """Stub generator function that yields nothing."""
    return iter([])
