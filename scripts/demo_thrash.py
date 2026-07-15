#!/usr/bin/env python3
"""Anti-thrash demo: sustained I=14 with interference logging."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from paradox_engine import EyeOfTheStorm


def main() -> int:
    print("=" * 60)
    print(" Eye of the Storm — sustained I=14 thrash demo")
    print("=" * 60)
    eye = EyeOfTheStorm(seed=42)
    out = eye.run(steps=120, I=14.0)
    s = out["summary"]
    print(f"  steps={out['steps']}")
    print(f"  max_I={s.get('max_I')}")
    print(f"  late_stability={s.get('late_stability'):.4f}")
    print(f"  min_stability={s.get('min_stability'):.4f}")
    print(f"  mean_thrash={s.get('mean_thrash'):.3f}")
    print(f"  zero_hard_break={out['zero_hard_break']}")
    print(f"  crashed={out['crashed']}")
    print(f"  storm_frac={s.get('storm_frac'):.2f}")
    print(f"  wisdom_keys={list(out.get('wisdom', {}).keys())[:10]}")
    ok = out["zero_hard_break"] and not out["crashed"]
    print("  PASS" if ok else "  FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
