# Paradox Engine â€“ Enterprise Token Stress (EoTS)
**Fixed-scope diagnostic:** see [DIAGNOSTIC.md](DIAGNOSTIC.md)

[![GTM Ready](https://img.shields.io/badge/Status-GTM%20Ready-emerald.svg)](https://github.com/mrblakessinger-rgb/paradox-engine-eots)
[![Efficiency Gate](https://img.shields.io/badge/Efficiency-%E2%88%A5%2090%25-blue.svg)](docs/TOKEN_STRESS_MATRIX.md)

Multi-agent **retry / cost-cap simulation** under stated parameters. Measures token spend of a naive exponential retry fleet vs a capped breaker-style fleet.

### Quickstart Clone & Run

```cmd
git clone https://github.com/mrblakessinger-rgb/paradox-engine-eots.git
cd paradox-engine-eots
python proof_of_burn_standalone.py
python scripts\run_token_stress_matrix.py
```

### Token Stress Matrix (verified on main)

All profiles import `proof_of_burn_standalone.py` and require **>= 90%** efficiency vs naive.

| Profile | Agents | Steps | Fail Rate | Efficiency | Absolute Saved | Status |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Primary Gate E0** | 100 | 8 | 75% | 94.42% | 41.94M | PASS |
| **Cascade Outage** | 100 | 12 | 90% | 98.37% | 223.95M | PASS |
| **Long Stampede** | 100 | 16 | 75% | 99.23% | 637.32M | PASS |
| **Heavy Mult** | 100 | 8 | 75% | 96.55% | 69.34M | PASS |

Full telemetry: [docs/TOKEN_STRESS_MATRIX.md](docs/TOKEN_STRESS_MATRIX.md)

### Honesty & Scope

- Harness is a multi-agent retry/cost model with per-attempt caps (`min(cost, cap)`); **not** a live proxy of your cloud/API account.
- Pilot SLA (if offered): budget **ceiling** protection + **pilot-fee credit** â€” not a guarantee of your production API bill.
- MIT / AS IS. See `LICENSE`.

