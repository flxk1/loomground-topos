# SPDX-FileCopyrightText: 2026 flxk1
# SPDX-License-Identifier: Apache-2.0
"""Loomground Topos: the legal-system topology plane, published as data.

The package exposes the shared plane descriptor (``plane()``), registered under the
entry-point group ``loomground.planes`` as ``topos``. Everything the descriptor
carries is derived at runtime from the repository's own published artifacts
(``grammar/topos.ebnf``, ``spec/SPEC.md``) and from the package data files.
"""

from ._version import __version__
from .plane import (
    binding,
    language_version,
    load_grounded,
    nd_system,
    plane,
    produce,
)

__all__ = [
    "__version__",
    "binding",
    "language_version",
    "load_grounded",
    "nd_system",
    "plane",
    "produce",
]
