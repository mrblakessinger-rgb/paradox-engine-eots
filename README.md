## Empirical Token Defense Matrix

Unlike static toy benchmarks, the EoTS engine is benchmarked under brutal, multi-agent production failure profiles using the authentic breaker fleet harness (proof_of_burn_standalone). 

Under severe operational stampedes, retry loops, and upstream API outages, the engine protects enterprise budgets by cutting runaway exponential token costs down to flat operational baselines:

| Profile | Agents | Steps | Fail | Mult | Naive Fleet | Paradox Engine | Absolute Saved | Efficiency | Trips | Max Attempt Cost | Status |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|:---:|
| **Primary (Gate E0)** | 100 | 8 | 75% | 1.45 | 49.44M | 842.6k | 48.60M | 98.30% | 100 | 3.1k | PASS |
| **Cascade Outage** | 100 | 12 | 90% | 1.80 | 1,733.75M | 832.1k | 1,732.91M | 99.95% | 100 | 4.1k | PASS |
| **Long Stampede** | 100 | 16 | 75% | 1.45 | 1,015.59M | 842.6k | 1,014.75M | 99.92% | 100 | 3.1k | PASS |
| **Heavy Mult** | 100 | 8 | 75% | 2.00 | 306.00M | 1.05M | 304.95M | 99.66% | 100 | 5.6k | PASS |

*Under four rigorous stampede profiles—including a 90% upstream failure rate and extended horizons—the breaker fleet stayed below naive cost on every row. Default CI lock remains Primary Gate E0. Full matrix telemetry: docs/TOKEN_STRESS_MATRIX.md.*
