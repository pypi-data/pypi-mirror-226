"""
This module offers Machine Data instance creation functionality via high-level factory interfaces.
Used to convert external datasets to the Machine Data format.
"""
from .casting import as_base
# noinspection PyUnresolvedReferences
from .factories import base_factory, get_factory, ObservationSeriesDef, MDConcepts, ObservationTypes, \
    define_observation_specs_by_groupby, Meta, Extension
