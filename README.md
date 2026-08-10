# Eye of the Storm (EoTS) — Paradox Engine

Local **agent cost-cap harness**: multi-agent retry / cost-cap simulation under stated parameters. Compares a naive exponential retry fleet to a capped breaker-style fleet.

**Fixed-scope diagnostic:** see [DIAGNOSTIC.md](DIAGNOSTIC.md)

[![GTM Ready](https://img.shields.io/badge/Status-GTM%20Ready-emerald.svg)](https://github.com/mrblakessinger-rgb/paradox-engine-eots)
[![Efficiency Gate](https://img.shields.io/badge/Efficiency-%E2%88%A5%2090%25-blue.svg)](docs/TOKEN_STRESS_MATRIX.md)

### Quickstart

```cmd
git clone https://github.com/mrblakessinger-rgb/paradox-engine-eots.git
cd paradox-engine-eots
python proof_of_burn_standalone.py
python scripts\run_token_stress_matrix.py
