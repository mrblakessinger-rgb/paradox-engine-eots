#!/usr/bin/env python3
"""
Grok Build July-2026-class purge / thrash simulation.

Mimics (public wire analysis): multi-GB state pressure, dual-channel stress,
sudden server-side purge flag, watcher death — then compares naive vs Eye.

  python scripts/demo_purge_simulation.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from paradox_engine import ParadoxEngine, stress_test_purge_simulation


def main() -> int:
    print("=" * 64)
    print(" PURGE SIMULATION — Grok Build failure class (synthetic)")
    print(" Ref: gist.github.com/cereblab/dc9a40bc26120f4540e4e09b75ffb547")
    print("=" * 64)

    # Prefer trained high-I DNA if present from prior exam
    dna = None
    train_path = ROOT / "docs" / "i15_recovery_last.json"
    # always start from engine DNA after optional train
    eng = ParadoxEngine(seed=42)
    # light high-I warm from Eye train API
    from paradox_engine import EyeOfTheStorm

    eye = EyeOfTheStorm(seed=42)
    train = eye.train_high_I(I_levels=[12.0, 14.0, 15.0, 16.0], steps_per=40, epochs=3, seed=42)
    dna = train.get("trained_dna")
    eng.load_dna(dna)

    result = eng.stress_test_purge_simulation()
    n, e = result["naive"], result["eye_of_the_storm"]

    print("\n--- NAIVE agent ---")
    for k, v in n.items():
        print(f"  {k}: {v}")
    print("\n--- EYE OF THE STORM ---")
    for k, v in e.items():
        print(f"  {k}: {v}")
    print("\n--- COMPARISON ---")
    print(f"  winner: {result['winner']}")
    print(f"  headline: {result['headline']}")
    print(f"  honest_scope: {result['honest_scope']}")
    print(f"  wisdom_keys: {result.get('wisdom_keys')}")

    out = ROOT / "docs" / "purge_simulation_last.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    slim = {k: v for k, v in result.items() if k not in ("naive_log_tail", "eye_log_tail", "series")}
    slim["series_len"] = len(result["series"]["phases"])
    slim["train_best"] = train.get("best")
    out.write_text(json.dumps(slim, indent=2, default=str), encoding="utf-8")
    print(f"\n  wrote {out}")

    ok = e["purge_survived"] and not n["purge_survived"]
    print("\n  DEMO PASS" if ok else "\n  DEMO NEEDS STRENGTHENING")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
