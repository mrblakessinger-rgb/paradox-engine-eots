### Enterprise Token Stress Matrix (Stateful Cost-Cap Simulation)

All profiles execute via stateful module import (`proof_of_burn_standalone.py`) and verify $\ge 90\%$ token conservation efficiency against naive baselines.

| **Profile** | **Agents** | **Steps** | **Failure Rate** | **Efficiency** | **Absolute Saved** | **Status** |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Primary Gate E0** | 100 | 8 | 75% | 94.42% | 41.94M | PASS |
| **Cascade Outage** | 100 | 12 | 90% | 98.37% | 223.95M | PASS |
| **Long Stampede** | 100 | 16 | 75% | 99.23% | 637.32M | PASS |
| **Heavy Mult** | 100 | 8 | 75% | 96.55% | 69.34M | PASS |