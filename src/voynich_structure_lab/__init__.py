"""Dependency-free tools for structural analysis of tokenized texts."""

from .deletion import deletion_children, reachable_sinks
from .diamonds import DeletionDiamond, deletion_diamonds
from .graph import connected_components, indel_adjacency, one_deletions
from .units import split_units

__all__ = [
    "DeletionDiamond",
    "connected_components",
    "deletion_children",
    "deletion_diamonds",
    "indel_adjacency",
    "one_deletions",
    "reachable_sinks",
    "split_units",
]
__version__ = "0.2.0"
