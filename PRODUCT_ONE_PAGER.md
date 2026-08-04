# Eye of the Storm (EoTS): Agent-Runtime Reliability & Thrash Defense

## Overview
Eye of the Storm (`EoTS`) is a deterministic kernel-level control plane and evaluation harness designed to prevent runaway token expenditure and recursive retry stampedes in multi-agent AI systems. Under heavy tool failure rates ($75\%+$), naive backoff strategies cause exponential cost explosions. EoTS implements strict circuit breaking, fleet-wide budget allocation, and local trajectory auditing to cut waste by **~98.3%**.

---

## Core Architecture (`kernel/`)
- **Circuit Breaker (`breaker.py`):** Halts recursive failure cascades instantly when error thresholds are breached, preventing compound API costs.
- **Shared Token Budget (`fleet_wallet.py`):** Enforces hard global expenditure caps across 100+ concurrent agents.
- **Local Audit & Grounding Flag:** Analyzes redacted local execution trajectories to flag ungrounded IDs and hallucinated tool calls without transmitting raw telemetry off-device.

---

## Benchmark Results (Harness Output)
Evaluated across a standard 100-agent, 8-step execution harness under a $75\%$ simulated tool-failure rate:
- **Naive Backoff Cost:** Baseline scaling with exponential token waste.
- **EoTS Kernel Cost:** **~98.3% token savings** achieved via deterministic pruning and circuit-breaking.

---

## Honesty & Non-Claims
- **Not a Production Promise:** This repository provides an architectural reference implementation and evaluation harness, not a drop-in replacement for enterprise cloud gateway infrastructure.
- **Not a Hallucination Oracle:** The grounding flag detects ungrounded or orphaned ID references in local logs; it does not verify semantic truth or eliminate LLM hallucinations entirely.
- **License:** MIT / AS IS. See repository LICENSE for details.