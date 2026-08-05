# Token Stress Matrix (Dynamic Telemetry)

This document tracks the verified multi-agent stress matrix execution under the simulation harness model.

| Profile | Agents | Steps | Fail Rate | Efficiency | Absolute Saved | Status |
|---|---:|---:|---:|---:|---:|:---:|
| **Primary Gate E0** | 100 | 8 | 75% | 94.42% | 41.94M | PASS |
| **Cascade Outage** | 100 | 12 | 90% | 99.76% | 1,729.53M | PASS |
| **Long Stampede** | 100 | 16 | 75% | 99.23% | 637.32M | PASS |
| **Heavy Mult** | 100 | 8 | 75% | 98.60% | 226.00M | PASS |

## Execution Command
```bash
python scripts/run_token_stress_matrix.py
```
