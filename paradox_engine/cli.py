"""CLI: paradox-demo"""

from __future__ import annotations

import argparse
import json

from .eye import EyeOfTheStorm


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Paradox Engine + Eye of the Storm demo")
    ap.add_argument("--steps", type=int, default=100)
    ap.add_argument("--I", type=float, default=14.0, help="Sustained interference level")
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)

    eye = EyeOfTheStorm(seed=args.seed)
    out = eye.run(steps=args.steps, I=args.I)
    if args.json:
        print(json.dumps({k: out[k] for k in out if k != "series"}, indent=2, default=str))
    else:
        s = out["summary"]
        print("Paradox Engine + Eye of the Storm")
        print(f"  I={args.I}  steps={args.steps}  seed={args.seed}")
        print(f"  late_stability={s.get('late_stability'):.4f}  min={s.get('min_stability'):.4f}")
        print(f"  zero_hard_break={out['zero_hard_break']}  crashed={out['crashed']}")
        print(f"  max_I={s.get('max_I')}  mean_thrash={s.get('mean_thrash'):.3f}")
        print(f"  wisdom_keys={list(out.get('wisdom', {}).keys())[:8]}")
    return 0 if out["zero_hard_break"] and not out["crashed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
