# EoTS: Enterprise Token Shield — Product One-Pager

## Empirical Token Defense Matrix (Simulation Model)
The EoTS simulation harness models multi-agent retry loops and circuit breaker cost-caps under brutal failure distributions. 

| Profile | Agents | Steps | Fail Rate | Efficiency | Absolute Saved | Status |
|---|---:|---:|---:|---:|---:|:---:|
| **Primary Gate E0** | 100 | 8 | 75% | 94.42% | 41.94M | PASS |
| **Cascade Outage** | 100 | 12 | 90% | 99.76% | 1,729.53M | PASS |
| **Long Stampede** | 100 | 16 | 75% | 99.23% | 637.32M | PASS |
| **Heavy Mult** | 100 | 8 | 75% | 98.60% | 226.00M | PASS |

### Reproduce Locally
`ash
python proof_of_burn_standalone.py
python scripts/run_token_stress_matrix.py
`

## Honesty & SLA Terms
* **Disclaimer:** Harness is a multi-agent retry/cost model under stated parameters; not a live proxy of your OpenAI account.
* **Pilot SLA:** Structured around ceiling protection + pilot-fee credit, not a generic guarantee of your infrastructure API spend.
