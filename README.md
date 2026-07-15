# Paradox Engine + Eye of the Storm

**Free open-source sample** for multi-agent / LLM fleet stability under **interference thrash**.

MIT licensed. Drop in, install, run. No account, no storefront, no pricing.

---

## What this is

A small Python package that keeps a **synthetic multi-agent fleet** near a target health band when interference (load thrash) spikes — including **high-I** pressure (**I ≥ 14**).

| Piece | Role |
|-------|------|
| **ParadoxEngine** | One-way health core: installs instinct, hive churn, **Wisdom Compression** |
| **EyeOfTheStorm** | Thrash cool + storm latch + **Interference Logging** |
| **Tests / scripts** | Anti-thrash demo and high-I recovery exams |

Not a chatbot. Not an agent framework. A **fleet health layer** you can re-run offline.

---

## Quick start (60 seconds)

```bash
cd paradox-engine-eots
pip install -e .
python -m paradox_engine.cli --I 14 --steps 100
pytest -q
```

Expected: process completes, **`zero_hard_break=True`**, no crash.

---

## Why it exists

Agent fleets fail under thrash: tool flakes, retry storms, load spikes. Capability scores do not measure whether the **fleet stays alive**.

This sample shows:

1. **Sustained high interference** (demo default **I = 14**) without hard fleet death in the harness  
2. **Wisdom Compression** — raw episode scars → compact rules (not a trauma dump)  
3. **Interference Logging** — structured I / felt_I / stability / thrash / storm telemetry  

Honest framing: this is a **measured thrash harness**, not a promise of invincible production systems.

---

## Minimal API

```python
from paradox_engine import EyeOfTheStorm, ParadoxEngine

# Full pack: cool thrash + log + wisdom
eye = EyeOfTheStorm(seed=42)
result = eye.run(steps=120, I=14.0)

print(result["zero_hard_break"])       # True if no hard fleet death
print(result["summary"]["late_stability"])
print(result["wisdom"])                # compressed wisdom rules

# Core only
eng = ParadoxEngine(seed=1)
eng.step_raw(2.5)
print(eng.stability, eng.alive)
```

### High-I train + recovery exam

```python
eye = EyeOfTheStorm(seed=7)
train = eye.train_high_I(
    I_levels=[8, 12, 14, 15, 16],
    steps_per=60,
    epochs=4,
)
exam = eye.recovery_exam(peak_I=15.0, hold_steps=40, recover_steps=80, dna=train["trained_dna"])
print(exam["zero_hard_break"], exam["steps_to_recover"], exam["recovered"])
```

```bash
python scripts/demo_thrash.py
python scripts/exam_i15_recovery.py
```

---

## Package layout

```
paradox-engine-eots/
├── LICENSE                 # MIT
├── README.md
├── pyproject.toml
├── paradox_engine/
│   ├── __init__.py
│   ├── engine.py           # ParadoxEngine
│   ├── eye.py              # EyeOfTheStorm
│   ├── interference_log.py # Interference Logging
│   ├── cli.py
│   └── _kernel_v1.py       # frozen swarm kernel
├── tests/
│   └── test_anti_thrash.py
└── scripts/
    ├── demo_thrash.py
    └── exam_i15_recovery.py
```

---

## Design notes

| Idea | Meaning here |
|------|----------------|
| **Target band ~0.92** | Hold useful health; soft ceiling ~0.97 (anti-lock) |
| **Hard break** | Fleet death / not-alive in harness |
| **Soft break** | Utility floor under thrash while still alive |
| **Wisdom Compression** | `absorb_scars` → `compress_wisdom` → rules + capped intuition |
| **Interference Logging** | Every step: I, felt_I, stability, thrash, storm |

---

## Requirements

- Python **3.10+**
- **numpy** ≥ 1.24

---

## License

MIT — see `LICENSE`.

---

## Tailored demo: session purge / multi-GB thrash (Grok Build failure *class*)

Public July 2026 wire analysis documented multi-GB repo/state uploads, dual-channel load (tiny model path vs huge storage path), and mid-session breakage when upload policy/flags flipped — with long-running work dying under thrash and state pressure.

Sources (independent, public):
- Wire analysis: https://gist.github.com/cereblab/dc9a40bc26120f4540e4e09b75ffb547
- HN: https://news.ycombinator.com/item?id=48877371
- Repro materials: https://github.com/cereblab/grok-build-exfil-repro

**What we simulate (synthetic, offline):**
1. Healthy long-running session (watchers looping)  
2. Multi-GB state/upload pressure with interference **I = 14 → 18**  
3. Sudden **purge / channel-disable** mid-flight (watchers die)  
4. Recovery window — **Wisdom Compression** keeps essentials; bulk is dropped  

**What we do *not* claim:** blocking network uploads or replacing privacy harness pins (`disable_codebase_upload`, telemetry env). Those are product/config controls. This demo is about **fleet/session thrash survival + essential-state retention** when bulk channels thrash and get cut.

```bash
python scripts/demo_purge_simulation.py
```

```python
from paradox_engine import ParadoxEngine

eng = ParadoxEngine(seed=42)
report = eng.stress_test_purge_simulation()
print(report["headline"])
print(report["naive"]["purge_survived"], report["eye_of_the_storm"]["purge_survived"])
```

Expect a clear **naive dies / loses essentials** vs **Eye stays alive / wisdom intact** comparison with metrics.

---

## Free sample intent

Built as a **clean, re-runnable thrash sample** for teams debugging multi-agent / LLM orchestration stability under load — including long-running coding-agent sessions that face state storms and mid-flight policy cuts. Feedback on failure modes, API clarity, and recovery behavior is welcome via issues on the distribution channel you received this from.
