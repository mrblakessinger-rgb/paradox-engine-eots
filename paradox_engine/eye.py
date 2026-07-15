"""
Eye of the Storm — thrash cool + storm latch over ParadoxEngine.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

import numpy as np

from .engine import ParadoxEngine
from .interference_log import InterferenceEvent, InterferenceLog


@dataclass
class StepReport:
    t: int
    I: float
    felt_I: float
    stability: float
    thrash: float
    storm_active: bool
    alive: bool
    shell: float
    target: float


@dataclass
class EyeOfTheStorm:
    """
    Fleet health governor under interference thrash.

    - Logs nominal interference I (including I ≥ 14)
    - Cools thrash via storm shell before swarm feels load
    - Wisdom compression after episodes
    - Zero hard-break goal under sustained high I (process + fleet alive)
    """

    seed: int = 42
    engine: ParadoxEngine | None = None
    log: InterferenceLog = field(default_factory=InterferenceLog)
    storm_active: bool = False
    thrash: float = 0.0
    shell: float = 1.0
    _storm_hold: int = 0
    _calm_hold: int = 0
    history: list[StepReport] = field(default_factory=list)

    def __post_init__(self) -> None:
        if self.engine is None:
            self.engine = ParadoxEngine(seed=self.seed)

    @property
    def stability(self) -> float:
        assert self.engine is not None
        return self.engine.stability

    @property
    def alive(self) -> bool:
        assert self.engine is not None
        return self.engine.alive

    def _update_storm(self, I: float, stability: float) -> None:
        # Engage storm under extreme I or thrash / low stability
        want = I >= 3.5 or self.thrash >= 0.55 or stability < 0.72
        if want:
            self.storm_active = True
            self._storm_hold = 12
            self._calm_hold = 0
        elif self.storm_active:
            if stability >= 0.88 and I < 2.5 and self.thrash < 0.35:
                self._calm_hold += 1
                if self._calm_hold >= 6:
                    self.storm_active = False
                    self._storm_hold = 0
            else:
                self._calm_hold = 0
                self._storm_hold = max(0, self._storm_hold - 1)
                if self._storm_hold == 0 and stability >= 0.85:
                    self.storm_active = False

    def cool_interference(self, I: float) -> tuple[float, float]:
        """
        Map external interference → felt load.
        High I is real pressure; shell prevents instant fleet death.
        """
        I = float(max(0.0, I))
        storm = 1.0 if self.storm_active else 0.0
        # shell grows with thrash + storm + extreme I
        shell = (
            1.0
            + 0.65 * storm
            + 0.45 * self.thrash
            + 0.10 * max(0.0, I - 3.0)
            + 0.06 * max(0.0, I - 10.0)
        )
        self.shell = float(shell)
        felt = I / shell
        # still transmit serious pressure at I=14–15
        felt = float(np.clip(felt, 0.0, 9.5))
        return felt, shell

    def step(self, I: float) -> StepReport:
        assert self.engine is not None
        I = float(I)
        pre = self.engine.stability
        self._update_storm(I, pre)
        felt, shell = self.cool_interference(I)
        stab = self.engine.step_raw(felt)
        # thrash estimate: instability + I pressure + flux-ish proxy
        gap = abs(stab - self.engine.target)
        self.thrash = float(
            np.clip(0.45 * gap / 0.25 + 0.25 * max(0.0, I - 2.0) / 8.0 + 0.30 * (1.0 - stab), 0.0, 1.0)
        )
        if self.storm_active:
            self.thrash *= 0.82  # cool while latched
        alive = self.engine.alive
        rep = StepReport(
            t=self.engine.cycle,
            I=I,
            felt_I=felt,
            stability=stab,
            thrash=self.thrash,
            storm_active=self.storm_active,
            alive=alive,
            shell=shell,
            target=self.engine.target,
        )
        self.history.append(rep)
        self.log.record(
            InterferenceEvent(
                t=rep.t,
                I=rep.I,
                felt_I=rep.felt_I,
                stability=rep.stability,
                thrash=rep.thrash,
                storm_active=rep.storm_active,
                alive=rep.alive,
                note="storm" if rep.storm_active else "",
            )
        )
        # scar when thrash high
        if self.thrash >= 0.5 or I >= 8.0:
            self.engine.absorb_scars(
                [{"reason": "tighten_high_I", "I": I, "stability": stab, "thrash": self.thrash}],
                meta={"I": I, "alive": alive},
            )
        elif stab >= 0.9 and I < 2.0:
            self.engine.absorb_scars(
                [{"reason": "climb_calm", "I": I, "stability": stab}],
                meta={"I": I, "alive": alive, "optimistic_pass": True},
            )
        return rep

    def run(
        self,
        steps: int = 120,
        *,
        I: float | None = 2.5,
        I_schedule: list[float] | None = None,
        seed: int | None = None,
    ) -> dict[str, Any]:
        if seed is not None:
            self.engine = ParadoxEngine(seed=seed, dna=self.engine.export_dna() if self.engine else None)
            self.log = InterferenceLog()
            self.history = []
            self.storm_active = False
            self.thrash = 0.0
        reports = []
        for t in range(steps):
            if I_schedule is not None:
                i_t = float(I_schedule[min(t, len(I_schedule) - 1)])
            else:
                i_t = float(I if I is not None else 2.0)
            reports.append(self.step(i_t))
        # Wisdom Compression at end of run
        wisdom_report = self.engine.compress_wisdom() if self.engine else {}
        summ = self.log.summary()
        return {
            "steps": steps,
            "summary": summ,
            "wisdom_compression": wisdom_report,
            "wisdom": self.engine.wisdom_snapshot() if self.engine else {},
            "zero_hard_break": bool(summ.get("zero_hard_break")),
            "crashed": not all(r.alive for r in reports),
            "series": [
                {
                    "t": r.t,
                    "I": r.I,
                    "felt_I": r.felt_I,
                    "stability": r.stability,
                    "thrash": r.thrash,
                    "storm": r.storm_active,
                }
                for r in reports
            ],
        }

    def train_high_I(
        self,
        *,
        I_levels: list[float] | None = None,
        steps_per: int = 80,
        epochs: int = 5,
        seed: int = 7,
    ) -> dict[str, Any]:
        """
        Multi-epoch thrash training toward high interference (default includes 14–16).
        Compresses wisdom after each epoch. Returns best DNA + pass table.
        """
        levels = I_levels or [4.0, 8.0, 12.0, 14.0, 15.0, 16.0]
        history = []
        best = None
        dna = self.engine.export_dna() if self.engine else None
        for ep in range(epochs):
            ep_rows = []
            ok_all = True
            for I in levels:
                eye = EyeOfTheStorm(seed=seed + ep * 17 + int(I), engine=ParadoxEngine(seed=seed + ep, dna=dna))
                out = eye.run(steps=steps_per, I=I)
                row = {
                    "epoch": ep,
                    "I": I,
                    "late_stability": out["summary"].get("late_stability"),
                    "min_stability": out["summary"].get("min_stability"),
                    "zero_hard_break": out["zero_hard_break"],
                    "crashed": out["crashed"],
                    "mean_thrash": out["summary"].get("mean_thrash"),
                }
                ep_rows.append(row)
                if out["crashed"] or not out["zero_hard_break"]:
                    ok_all = False
                # train DNA from this eye
                dna = eye.engine.export_dna()
            score = float(
                np.mean([r["late_stability"] or 0 for r in ep_rows])
                + (0.15 if ok_all else -0.5)
                - 0.1 * sum(1 for r in ep_rows if not r["zero_hard_break"])
            )
            pack = {"epoch": ep, "score": score, "ok_all": ok_all, "rows": ep_rows, "dna": dna}
            history.append(pack)
            if best is None or score > best["score"]:
                best = pack
            # install best-so-far back into self
            if best and best.get("dna"):
                self.engine = ParadoxEngine(seed=seed + 100 + ep, dna=best["dna"])
        return {
            "epochs": epochs,
            "I_levels": levels,
            "history": history,
            "best": {
                "epoch": best["epoch"] if best else None,
                "score": best["score"] if best else None,
                "ok_all": best["ok_all"] if best else False,
                "rows": best["rows"] if best else [],
            },
            "trained_dna": best["dna"] if best else dna,
        }

    def recovery_exam(
        self,
        *,
        peak_I: float = 15.0,
        hold_steps: int = 40,
        recover_steps: int = 80,
        calm_I: float = 1.2,
        seed: int = 99,
        dna: dict | None = None,
    ) -> dict[str, Any]:
        """
        Spike to peak_I, hold, then drop to calm_I.
        Measures steps-to-recover near target band without hard break.
        """
        eng_dna = dna if dna is not None else (self.engine.export_dna() if self.engine else None)
        eye = EyeOfTheStorm(seed=seed, engine=ParadoxEngine(seed=seed, dna=eng_dna))
        schedule = [peak_I] * hold_steps + [calm_I] * recover_steps
        out = eye.run(steps=len(schedule), I_schedule=schedule)
        series = out["series"]
        target = eye.engine.target if eye.engine else 0.92
        # recovery: first t after hold where stability >= target - 0.06 for 5 consecutive
        recover_t = None
        run = 0
        for i in range(hold_steps, len(series)):
            if series[i]["stability"] >= target - 0.06 and series[i]["alive"] if "alive" in series[i] else True:
                # series may not have alive - use stability only
                run += 1
                if run >= 5:
                    recover_t = i - hold_steps  # steps after drop
                    break
            else:
                run = 0
        # fix alive check - StepReport has alive but series dict might not
        for i, r in enumerate(eye.history):
            if i >= hold_steps and r.stability >= target - 0.06 and r.alive:
                # recount properly
                pass
        recover_t = None
        run = 0
        for i in range(hold_steps, len(eye.history)):
            r = eye.history[i]
            if r.stability >= target - 0.06 and r.alive:
                run += 1
                if run >= 5:
                    recover_t = i - hold_steps - 4  # first of the 5
                    break
            else:
                run = 0
        late = [r.stability for r in eye.history[hold_steps:]]
        return {
            "peak_I": peak_I,
            "hold_steps": hold_steps,
            "recover_steps": recover_steps,
            "zero_hard_break": out["zero_hard_break"],
            "crashed": out["crashed"],
            "steps_to_recover": recover_t,
            "recovered": recover_t is not None,
            "late_mean_stability": float(np.mean(late)) if late else 0.0,
            "min_stability": float(min(r.stability for r in eye.history)),
            "summary": out["summary"],
            "wisdom_keys": list((out.get("wisdom") or {}).keys())[:12],
        }
