\# Enterprise Token Shield: Stress Matrix Telemetry



This document details the telemetry and parameters for the four rigorous breaker fleet stress profiles used to benchmark the EoTS engine.



\## Telemetry Summary

\- \*\*Primary Gate E0:\*\* 100 agents, 8 steps, 75% failure rate -> 98.30% efficiency (48.60M tokens saved).

\- \*\*Cascade Outage:\*\* 100 agents, 12 steps, 90% failure rate -> 99.95% efficiency (1,732.91M tokens saved).

\- \*\*Long Stampede:\*\* 100 agents, 16 steps, 75% failure rate -> 99.92% efficiency (1,014.75M tokens saved).

\- \*\*Heavy Mult:\*\* 100 agents, 8 steps, 75% failure rate, 2.0x multiplier -> 99.66% efficiency (304.95M tokens saved).



Reproduce locally via:

```bash

python proof\_of\_burn\_standalone.py

python scripts/run\_token\_stress\_matrix.py

