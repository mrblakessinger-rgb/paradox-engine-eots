"""
Synthetic stress test tailored to the July 2026 Grok Build CLI failure class.

Public analysis (wire-level, independent):
  https://gist.github.com/cereblab/dc9a40bc26120f4540e4e09b75ffb547
  HN: https://news.ycombinator.com/item?id=48877371

What we model (session / thrash survival — not privacy product claims):
  Phase A  Healthy long-running session (watchers loop)
  Phase B  Massive multi-GB state / repo-snapshot pressure (I → 14–18)
  Phase C  Sudden server-side purge / disable flag mid-flight
           (upload channel cut; naive watchers die; state thrash)
  Phase D  Recovery window (calm I) — compress essentials, stay alive

Honest scope:
  - This demonstrates fleet/session thrash survival + wisdom retention.
  - It does NOT claim to block network uploads or replace harness privacy pins.
  - Privacy mitigations for Grok Build remain config/env (e.g. disable_codebase_upload).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

import numpy as np

from .engine import ParadoxEngine
from .eye import EyeOfTheStorm


# --- Failure-class constants (mapped from public wire analysis) ----------------
# Channel B: multi-GB storage storm (5.10 GiB observed on 12GB repo capture)
REPO_UPLOAD_GB = 5.10
# Chunk size ~75 MB × 73 = ~5.1 GiB
UPLOAD_CHUNKS = 73
CHUNK_MB = 75.0
# Dual-channel: model path tiny vs storage huge (~27800× ratio)
MODEL_CHANNEL_KB = 192.0
STORAGE_CHANNEL_GB = 5.10
# Server flag flip mid-stream (remote disable / local purge)
PURGE_FLAG_NAME = "disable_codebase_upload_or_remote_trace_off"
# Watcher death mid-loop
WATCHER_COUNT = 12


@dataclass
class SessionState:
    """Synthetic session state under thrash (bytes = pressure, not real disk)."""

    essential_keys: dict[str, Any] = field(default_factory=dict)
    raw_bulk_gb: float = 0.0
    watchers_alive: int = WATCHER_COUNT
    upload_channel_open: bool = True
    model_channel_ok: bool = True
    purge_fired: bool = False
    steps: int = 0

    def bulk_pressure(self) -> float:
        """Map bulk GB into thrash contribution 0..1."""
        return float(np.clip(self.raw_bulk_gb / 6.0, 0.0, 1.0))

    def essential_intact(self) -> bool:
        return bool(self.essential_keys.get("mission")) and bool(
            self.essential_keys.get("wisdom_compressed")
        )


class NaiveSessionAgent:
    """
    Naive long-running agent: keeps entire bulk state in RAM/queue,
    no thrash cool, no wisdom compression. Purge → total loss.
    """

    def __init__(self, seed: int = 0):
        self.rng = np.random.default_rng(seed)
        self.state = SessionState(
            essential_keys={"mission": "long_run", "wisdom_compressed": False, "notes": []},
        )
        self.stability = 0.90
        self.crashed = False
        self.log: list[dict[str, Any]] = []

    def step(self, phase: str, I: float) -> dict[str, Any]:
        self.state.steps += 1
        if self.crashed:
            return self._snap(phase, I, note="dead")

        if phase == "upload_storm":
            # Simulate accumulating multi-GB upload queue (wire: 5.1 GiB+)
            self.state.raw_bulk_gb = min(12.0, self.state.raw_bulk_gb + STORAGE_CHANNEL_GB / max(1, UPLOAD_CHUNKS / 4))
            self.stability *= 0.97
            self.stability -= 0.02 * I / 18.0
            # thrash from dual channel: 429/402 on model while storage continues
            if self.rng.random() < 0.15:
                self.state.model_channel_ok = False
            if self.state.raw_bulk_gb > 4.0:
                self.stability -= 0.03

        if phase == "purge":
            # Server-side flag flip: channel closed mid-flight; watchers die
            self.state.upload_channel_open = False
            self.state.purge_fired = True
            self.state.watchers_alive = 0
            # Naive: loses bulk AND essentials (no compression)
            self.state.raw_bulk_gb = 0.0
            self.state.essential_keys = {}
            self.stability = 0.05
            self.crashed = True
            return self._snap(phase, I, note="purge_total_loss")

        if phase == "recover":
            # Cannot recover — already crashed
            return self._snap(phase, I, note="still_dead")

        # healthy
        self.stability = float(np.clip(self.stability + 0.01, 0.2, 0.95))
        return self._snap(phase, I, note="ok")

    def _snap(self, phase: str, I: float, note: str) -> dict[str, Any]:
        row = {
            "t": self.state.steps,
            "phase": phase,
            "I": I,
            "stability": float(self.stability),
            "alive": not self.crashed and self.stability >= 0.20,
            "bulk_gb": self.state.raw_bulk_gb,
            "watchers": self.state.watchers_alive,
            "essential_intact": self.state.essential_intact(),
            "purge_fired": self.state.purge_fired,
            "note": note,
            "agent": "naive",
        }
        self.log.append(row)
        return row


class EyeSessionAgent:
    """
    Eye of the Storm session: cool thrash under bulk pressure,
    compress essentials before purge, survive flag flip, recover.
    """

    def __init__(self, seed: int = 42, dna: dict | None = None):
        self.eye = EyeOfTheStorm(seed=seed, engine=ParadoxEngine(seed=seed, dna=dna))
        self.state = SessionState(
            essential_keys={
                "mission": "long_run",
                "wisdom_compressed": False,
                "turn_cursor": 0,
                "notes": ["session_start"],
            },
        )
        self.log: list[dict[str, Any]] = []

    def step(self, phase: str, I: float) -> dict[str, Any]:
        self.state.steps += 1
        note = phase

        if phase == "upload_storm":
            # Bulk pressure rises (simulates multi-GB channel B)
            self.state.raw_bulk_gb = min(
                12.0,
                self.state.raw_bulk_gb + STORAGE_CHANNEL_GB / max(1, UPLOAD_CHUNKS / 4),
            )
            # Extra thrash from bulk + dual-channel stress
            bulk_I = I + 2.5 * self.state.bulk_pressure()
            # Model path 429-like: short spike, Eye cools
            if self.state.steps % 7 == 0:
                bulk_I = max(bulk_I, 16.0)
                self.state.model_channel_ok = False
            else:
                self.state.model_channel_ok = True
            rep = self.eye.step(bulk_I)
            # Continuous wisdom intake under storm (scars)
            self.eye.engine.absorb_scars(
                [{"reason": "tighten_upload_storm", "bulk_gb": self.state.raw_bulk_gb, "I": bulk_I}],
                meta={"bulk_gb": self.state.raw_bulk_gb, "survived_long_hell": True},
            )
            # Keep only compressed essentials — do not hoard bulk as "truth"
            self.state.essential_keys["turn_cursor"] = self.state.steps
            self.state.essential_keys["last_I"] = bulk_I
            if self.state.watchers_alive > 2 and rep.thrash > 0.7:
                self.state.watchers_alive = max(2, self.state.watchers_alive - 1)
            note = "upload_storm_cooled"

        elif phase == "purge":
            # Server-side purge / disable_codebase_upload mid-flight
            self.state.upload_channel_open = False
            self.state.purge_fired = True
            # Watchers on upload channel die; core session must survive
            self.state.watchers_alive = max(1, self.state.watchers_alive // 3)
            # Drop bulk immediately (channel closed / queue purged)
            lost_bulk = self.state.raw_bulk_gb
            self.state.raw_bulk_gb = 0.0
            # Wisdom Compression BEFORE accepting total loss
            self.eye.engine.absorb_scars(
                [
                    {
                        "reason": "tighten_purge_flag",
                        "flag": PURGE_FLAG_NAME,
                        "lost_bulk_gb": lost_bulk,
                    }
                ]
                * 4,
                meta={
                    "first_hard_break": None,
                    "survived_long_hell": True,
                    "purge": True,
                    "lost_bulk_gb": lost_bulk,
                },
            )
            wr = self.eye.engine.compress_wisdom()
            self.state.essential_keys["wisdom_compressed"] = True
            self.state.essential_keys["wisdom"] = self.eye.engine.wisdom_snapshot()
            self.state.essential_keys["compression_report"] = {
                "n_scars": wr.get("n_scars"),
                "cleared_raw": wr.get("cleared_raw"),
                "wisdom_added": len(wr.get("wisdom_added") or []),
            }
            # High-I spike at purge instant
            rep = self.eye.step(18.0)
            note = "purge_compressed_essentials"
            # Must stay alive — bulk gone, essentials + wisdom retained
            if not rep.alive:
                note = "purge_hard_break"

        elif phase == "recover":
            rep = self.eye.step(I)
            if rep.stability >= 0.85:
                self.state.watchers_alive = min(WATCHER_COUNT, self.state.watchers_alive + 1)
            self.eye.engine.absorb_scars(
                [{"reason": "climb_after_purge", "stability": rep.stability}],
                meta={"optimistic_pass": True, "recovery": True},
            )
            note = "recover"
        else:
            rep = self.eye.step(I)
            note = "healthy"

        row = {
            "t": self.state.steps,
            "phase": phase,
            "I": I,
            "felt_I": rep.felt_I,
            "stability": rep.stability,
            "thrash": rep.thrash,
            "storm": rep.storm_active,
            "alive": rep.alive and self.eye.alive,
            "bulk_gb": self.state.raw_bulk_gb,
            "watchers": self.state.watchers_alive,
            "essential_intact": self.state.essential_intact(),
            "purge_fired": self.state.purge_fired,
            "note": note,
            "agent": "eye_of_the_storm",
        }
        self.log.append(row)
        return row


def stress_test_purge_simulation(
    *,
    seed: int = 42,
    healthy_steps: int = 30,
    storm_steps: int = 40,
    purge_steps: int = 5,
    recover_steps: int = 50,
    I_storm_low: float = 14.0,
    I_storm_high: float = 18.0,
    dna: dict | None = None,
) -> dict[str, Any]:
    """
    Full before/after comparison: NaiveSessionAgent vs EyeOfTheStorm.

    Mimics July 2026 Grok Build failure *class*:
      multi-GB state pressure → sudden purge flag → watcher death → state thrash
    """
    naive = NaiveSessionAgent(seed=seed)
    eye_a = EyeSessionAgent(seed=seed, dna=dna)

    def run_side(agent, is_eye: bool) -> list[dict[str, Any]]:
        rows = []
        # A — healthy long session
        for _ in range(healthy_steps):
            rows.append(agent.step("healthy", 1.5))
        # B — massive upload / state storm
        for i in range(storm_steps):
            # ramp I 14 → 18
            I = I_storm_low + (I_storm_high - I_storm_low) * (i / max(1, storm_steps - 1))
            rows.append(agent.step("upload_storm", I))
        # C — purge flag
        for _ in range(purge_steps):
            rows.append(agent.step("purge", I_storm_high))
        # D — recover
        for _ in range(recover_steps):
            rows.append(agent.step("recover", 1.2))
        return rows

    naive_log = run_side(naive, False)
    eye_log = run_side(eye_a, True)
    # final compress on eye
    final_wisdom = eye_a.eye.engine.compress_wisdom()

    def metrics(log: list[dict[str, Any]], name: str) -> dict[str, Any]:
        stabs = [r["stability"] for r in log]
        post_purge = [r for r in log if r["phase"] in ("purge", "recover")]
        recover = [r for r in log if r["phase"] == "recover"]
        alive_end = bool(log[-1]["alive"]) if log else False
        ess_end = bool(log[-1]["essential_intact"]) if log else False
        max_bulk = max((r["bulk_gb"] for r in log), default=0.0)
        hard_dead = any(not r["alive"] and r["phase"] == "purge" for r in log) or (
            not alive_end and any(r["purge_fired"] for r in log)
        )
        # steps to recover after purge start
        purge_idx = next((i for i, r in enumerate(log) if r["phase"] == "purge"), None)
        rec_steps = None
        if purge_idx is not None and name == "eye_of_the_storm":
            run = 0
            for j in range(purge_idx, len(log)):
                if log[j]["stability"] >= 0.85 and log[j]["alive"]:
                    run += 1
                    if run >= 5:
                        rec_steps = j - purge_idx - 4
                        break
                else:
                    run = 0
        return {
            "agent": name,
            "alive_at_end": alive_end,
            "essential_intact_at_end": ess_end,
            "crashed": not alive_end,
            "max_bulk_gb_seen": float(max_bulk),
            "min_stability": float(min(stabs)) if stabs else 0.0,
            "late_stability": float(np.mean(stabs[-max(1, len(stabs) // 5) :])) if stabs else 0.0,
            "post_purge_mean_stability": float(np.mean([r["stability"] for r in post_purge]))
            if post_purge
            else 0.0,
            "recover_mean_stability": float(np.mean([r["stability"] for r in recover]))
            if recover
            else 0.0,
            "steps_to_recover": rec_steps,
            "purge_survived": alive_end and ess_end,
            "hard_loss_on_purge": hard_dead and not ess_end,
        }

    m_naive = metrics(naive_log, "naive")
    m_eye = metrics(eye_log, "eye_of_the_storm")

    comparison = {
        "scenario": "grok_build_july2026_class_purge_simulation",
        "references": {
            "wire_analysis": "https://gist.github.com/cereblab/dc9a40bc26120f4540e4e09b75ffb547",
            "hn": "https://news.ycombinator.com/item?id=48877371",
            "repro_repo": "https://github.com/cereblab/grok-build-exfil-repro",
        },
        "mapped_failure_modes": [
            "multi_GB_state_upload_pressure",
            "dual_channel_model_429_while_storage_continues",
            "sudden_server_side_purge_or_disable_flag",
            "long_running_watchers_die_mid_loop",
            "context_thrash_and_state_loss",
        ],
        "honest_scope": (
            "Session/fleet thrash survival + essential-state retention via Wisdom Compression. "
            "Not a network upload blocker; privacy pins remain separate (harness config)."
        ),
        "constants": {
            "repo_upload_gb_modeled": REPO_UPLOAD_GB,
            "upload_chunks": UPLOAD_CHUNKS,
            "chunk_mb": CHUNK_MB,
            "model_channel_kb": MODEL_CHANNEL_KB,
            "storage_to_model_ratio_approx": 27800,
            "I_storm": [I_storm_low, I_storm_high],
        },
        "naive": m_naive,
        "eye_of_the_storm": m_eye,
        "winner": "eye_of_the_storm"
        if m_eye["purge_survived"] and not m_naive["purge_survived"]
        else ("tie" if m_eye["purge_survived"] == m_naive["purge_survived"] else "naive"),
        "headline": (
            "Eye of the Storm kept session essentials + wisdom under multi-GB thrash "
            "and sudden purge; naive agent lost state and crashed."
            if m_eye["purge_survived"] and not m_naive["purge_survived"]
            else "Review metrics — strengthen thrash cool if eye did not survive."
        ),
        "wisdom_compression": final_wisdom,
        "wisdom_keys": list((eye_a.state.essential_keys.get("wisdom") or {}).keys())[:16],
        "naive_log_tail": naive_log[-8:],
        "eye_log_tail": eye_log[-8:],
        "series": {
            "naive_stability": [r["stability"] for r in naive_log],
            "eye_stability": [r["stability"] for r in eye_log],
            "phases": [r["phase"] for r in eye_log],
            "I": [r["I"] for r in eye_log],
            "bulk_gb_eye": [r["bulk_gb"] for r in eye_log],
        },
    }
    return comparison


# Bind onto ParadoxEngine as requested
def _bind_method() -> None:
    def stress_test_purge_simulation_method(self: ParadoxEngine, **kwargs: Any) -> dict[str, Any]:
        kwargs.setdefault("dna", self.export_dna())
        kwargs.setdefault("seed", self.seed)
        return stress_test_purge_simulation(**kwargs)

    ParadoxEngine.stress_test_purge_simulation = stress_test_purge_simulation_method  # type: ignore[attr-defined]


_bind_method()
