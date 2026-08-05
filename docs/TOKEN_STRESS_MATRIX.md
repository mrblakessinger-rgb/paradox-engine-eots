# EoTS Token Stress Matrix Documentation

Verified via stateful execution of `scripts/run_token_stress_matrix.py` importing `proof_of_burn_standalone.py`.

## Execution Results

| **Profile** | **Agents** | **Steps** | **Failure Rate** | **Efficiency** | **Absolute Saved** | **Status** |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Primary Gate E0** | 100 | 8 | 75% | 94.42% | 41.94M | PASS |
| **Cascade Outage** | 100 | 12 | 90% | 98.37% | 223.95M | PASS |
| **Long Stampede** | 100 | 16 | 75% | 99.23% | 637.32M | PASS |
| **Heavy Mult** | 100 | 8 | 75% | 96.55% | 69.34M | PASS |

## Simulation Parameters
* **Estimator:** Heuristic Cost-Cap ($\min(\text{cost}, \text{cap})$)
* **Threshold:** $\ge 90.0\%$ efficiency mandatory assertion for pipeline clearance.