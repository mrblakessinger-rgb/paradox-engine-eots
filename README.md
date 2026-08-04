# Paradox Engine + Eye of the Storm (free sample)

**60-second thrash harness** for multi-agent / LLM fleet stability under load pressure.

MIT. No account. No Gumroad required.

**Paid pack (full proofs + plugins):** https://blakesinger.gumroad.com/l/wcorn  
**Full proof suite (open):** https://github.com/mrblakessinger-rgb/paradox-engine  

---

## What this is (3 seconds)

When **agent fleets thrash** (tool flakes, retry storms, high interference), this sample keeps a **synthetic fleet** near a health band — offline, re-runnable.

Not a chatbot. Not LangGraph. Not a CDN. A **fleet health layer** demo.

---

## Quick start (60 seconds)

```bash
cd paradox-engine-eots
pip install -e .
python -m paradox_engine.cli --I 14 --steps 100
pytest -q
```

**Expect:** process finishes · `zero_hard_break=True` · no crash.

If `cli` flags differ on your checkout:
```bash
python scripts/demo_purge_simulation.py
# or
pytest -q
```

---

## Why it exists

Agent fleets fail under thrash: tools flake, retries stampede, load spikes.  
Capability scores don’t measure whether the **fleet stays alive**.

This sample shows:

1. **Sustained high interference** (demo default **I = 14**) without hard fleet death in the harness  
2. **Thrash cool / storm latch** under pressure  
3. **Structured logging** of interference / stability / thrash  

Honest: **measured thrash harness**, not invincible production.

---

## Minimal API

```python
from paradox_engine import EyeOfTheStorm, ParadoxEngine

eye = EyeOfTheStorm(seed=42)
result = eye.run(steps=120, I=14.0)

print(result["zero_hard_break"])
print(result["summary"]["late_stability"])

eng = ParadoxEngine(seed=1)
eng.step_raw(2.5)
print(eng.stability, eng.alive)
```

### High-I train + recovery (if available in your build)

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

---

## Link to Soft Pack proofs (A/B/C)

Storefront lifts (re-runnable on the full repo / paid zip):

| Pain | Lift |
|------|------|
| Agent tool storms | **+0.22** success |
| Worker retry thrash | **+0.23** success |
| API rate-limit thrash | **+0.24** goodput |

This **eots** package is the **high-I thrash sample**.  
The **full Proof A/B/C runners + plugins** ship in the paid Eye of the Storm pack and/or the main paradox-engine tree.

---

## Product promise (honest)

> Eye of the Storm... Clarity Amongst the Chaos  
> Nothing is "unbreakable." But your system can't break this.

---

## License

MIT — see `LICENSE`.
