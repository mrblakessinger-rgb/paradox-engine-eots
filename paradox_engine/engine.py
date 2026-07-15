"""
ParadoxEngine — public façade over the frozen swarm kernel.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any

import numpy as np

from . import _kernel_v1 as K


class ParadoxEngine:
    """
    One-way Paradox + hive swarm health core.

    - Paradox installs instinct/wisdom; swarm never stores Paradox
    - Wisdom Compression: raw scars → compact rules (not trauma dumps)
    - Target band ~0.92 with soft anti-lock ceiling ~0.97
    """

    def __init__(self, seed: int = 42, dna: dict[str, Any] | None = None):
        self.seed = int(seed)
        self.rng = np.random.default_rng(self.seed)
        self.paradox = K.Paradox(dna if dna is not None else K.PROMOTED_DNA)
        self.agents = K.make_swarm(self.rng)
        self.paradox.install_drivers(self.agents)
        self.ambient = 0.0
        self.cycle = 0
        self.target = float(K.TARGET_STABILITY)

    @property
    def stability(self) -> float:
        return float(K.stability(self.agents))

    @property
    def alive(self) -> bool:
        """Hard-break = fleet death. Soft thrash is not a crash."""
        st = self.stability
        # alive if mean coherence not collapsed and agents exist
        if not self.agents:
            return False
        n_dead = sum(1 for a in self.agents if a.coherence < 0.08)
        return st >= 0.20 and n_dead < 0.85 * len(self.agents)

    def wisdom_snapshot(self) -> dict[str, Any]:
        w = self.paradox.wisdom if isinstance(self.paradox.wisdom, dict) else {}
        return dict(w)

    def export_dna(self) -> dict[str, Any]:
        return self.paradox.export_dna()

    def load_dna(self, dna: dict[str, Any]) -> None:
        self.paradox.load_dna(dna)
        self.paradox.install_drivers(self.agents)

    def absorb_scars(self, scars: list[dict], *, meta: dict | None = None) -> None:
        self.paradox.absorb_episode(scars, episode_meta=meta)

    def compress_wisdom(self, **kwargs: Any) -> dict[str, Any]:
        """Wisdom Compression — distill raw scars into compact rules + capped nudges."""
        return self.paradox.compress_scars_to_wisdom(**kwargs)

    def step_raw(self, interference: float) -> float:
        """
        One swarm cycle at *felt* interference (already cooled by Eye if used).
        Returns stability after step.
        """
        I = float(max(0.0, interference))
        for a in self.agents:
            a.step(I, self.ambient, self.rng)
        self.ambient = 0.03 * float(np.mean([a.flux for a in self.agents]))
        self.paradox.hive_pair_churn(self.agents, self.rng)
        self.paradox.install_drivers(self.agents)
        for a in self.agents:
            tcoh = a.instinct.get("target_coherence", self.target)
            a.performance = float(
                np.clip(1.0 - 1.2 * abs(a.coherence - tcoh) - 0.4 * a.pred_error, 0, 1)
            )
        self.cycle += 1
        self.paradox.cycle = self.cycle
        return self.stability

    def clone(self) -> "ParadoxEngine":
        eng = ParadoxEngine(seed=self.seed + 1, dna=self.export_dna())
        return eng
