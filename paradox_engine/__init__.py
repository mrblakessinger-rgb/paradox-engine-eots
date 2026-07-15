"""
Paradox Engine + Eye of the Storm
=================================
Free sample for multi-agent / LLM fleet stability under interference thrash.

MIT License. No commercial storefront coupling.
"""

from .eye import EyeOfTheStorm, StepReport
from .interference_log import InterferenceLog
from .engine import ParadoxEngine
from . import purge_simulation as _purge  # binds ParadoxEngine.stress_test_purge_simulation
from .purge_simulation import stress_test_purge_simulation

__version__ = "0.2.0"
__all__ = [
    "ParadoxEngine",
    "EyeOfTheStorm",
    "StepReport",
    "InterferenceLog",
    "stress_test_purge_simulation",
    "__version__",
]
