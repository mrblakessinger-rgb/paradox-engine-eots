"""Interference logging — structured thrash telemetry (no PII)."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass
class InterferenceEvent:
    t: int
    I: float
    felt_I: float
    stability: float
    thrash: float
    storm_active: bool
    alive: bool
    note: str = ""


@dataclass
class InterferenceLog:
    """Append-only log of interference pressure and fleet response."""

    events: list[InterferenceEvent] = field(default_factory=list)
    hard_breaks: int = 0
    soft_breaks: int = 0
    max_I: float = 0.0
    max_thrash: float = 0.0

    def record(self, ev: InterferenceEvent) -> None:
        self.events.append(ev)
        self.max_I = max(self.max_I, float(ev.I))
        self.max_thrash = max(self.max_thrash, float(ev.thrash))
        if not ev.alive:
            self.hard_breaks += 1
        if ev.stability < 0.55 and ev.alive:
            self.soft_breaks += 1

    def summary(self) -> dict[str, Any]:
        if not self.events:
            return {"n": 0}
        stabs = [e.stability for e in self.events]
        thr = [e.thrash for e in self.events]
        late = stabs[-max(1, len(stabs) // 5) :]
        return {
            "n": len(self.events),
            "max_I": self.max_I,
            "max_thrash": self.max_thrash,
            "mean_stability": float(sum(stabs) / len(stabs)),
            "late_stability": float(sum(late) / len(late)),
            "min_stability": float(min(stabs)),
            "mean_thrash": float(sum(thr) / len(thr)),
            "hard_breaks": self.hard_breaks,
            "soft_breaks": self.soft_breaks,
            "storm_frac": float(sum(1 for e in self.events if e.storm_active) / len(self.events)),
            "zero_hard_break": self.hard_breaks == 0,
        }

    def as_list(self) -> list[dict[str, Any]]:
        return [asdict(e) for e in self.events]
