#!/usr/bin/env python3
"""Train toward I=15+, then recovery exam (spike → calm, measure climb)."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from paradox_engine import EyeOfTheStorm


def main() -> int:
    print("=" * 60)
    print(" High-I train + recovery exam (peak I=15)")
    print("=" * 60)
    eye = EyeOfTheStorm(seed=7)
    train = eye.train_high_I(
        I_levels=[8.0, 12.0, 14.0, 15.0, 16.0],
        steps_per=50,
        epochs=4,
        seed=7,
    )
    print(f"  train best epoch={train['best']['epoch']} score={train['best']['score']:.3f} ok_all={train['best']['ok_all']}")
    for row in train["best"]["rows"]:
        print(
            f"    I={row['I']:>5.1f}  late={row['late_stability']:.3f}  "
            f"min={row['min_stability']:.3f}  hard_ok={row['zero_hard_break']}"
        )
    exam = eye.recovery_exam(
        peak_I=15.0,
        hold_steps=40,
        recover_steps=80,
        calm_I=1.2,
        seed=99,
        dna=train.get("trained_dna"),
    )
    print(f"  recovery zero_hard_break={exam['zero_hard_break']}")
    print(f"  recovery crashed={exam['crashed']}")
    print(f"  steps_to_recover={exam['steps_to_recover']}")
    print(f"  recovered={exam['recovered']}")
    print(f"  late_mean_stability={exam['late_mean_stability']:.3f}")
    out_path = ROOT / "docs" / "i15_recovery_last.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(
        json.dumps({"train_best": train["best"], "recovery": {k: v for k, v in exam.items() if k != "summary"}, "summary": exam.get("summary")}, indent=2, default=str),
        encoding="utf-8",
    )
    print(f"  wrote {out_path}")
    ok = exam["zero_hard_break"] and not exam["crashed"]
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
