# Paradox Engine EoTS â€“ Product One-Pager

## Stateful cost-cap simulation and token stress matrix

### Summary

EoTS is a multi-agent **retry / cost-cap simulation** under stated parameters. It compares a naive exponential retry fleet to a capped fleet (min(cost, cap)) and requires **>= 90%** token efficiency on every stress profile.

### Quickstart

`cmd
git clone https://github.com/mrblakessinger-rgb/paradox-engine-eots.git
cd paradox-engine-eots
python proof_of_burn_standalone.py
python scripts\run_token_stress_matrix.py
`

### Verified matrix (main)

| Profile | Agents | Steps | Fail Rate | Efficiency | Absolute Saved | Status |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Primary Gate E0** | 100 | 8 | 75% | 94.42% | 41.94M | PASS |
| **Cascade Outage** | 100 | 12 | 90% | 98.37% | 223.95M | PASS |
| **Long Stampede** | 100 | 16 | 75% | 99.23% | 637.32M | PASS |
| **Heavy Mult** | 100 | 8 | 75% | 96.55% | 69.34M | PASS |

### Pipeline

- Engine: proof_of_burn_standalone.py
- Matrix: scripts/run_token_stress_matrix.py
- Gate: efficiency **>= 90%** on all profiles

### Honesty and SLA

- Not a live proxy of your OpenAI/cloud account.
- Pilot SLA (if offered): ceiling protection + pilot-fee credit â€” not a guarantee of production API spend.
- MIT / AS IS.

