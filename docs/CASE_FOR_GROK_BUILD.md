# Case note — thrash sample tailored to Grok Build July 2026 failure *class*

## What the public record shows (not internal xAI data)

Wire-level analysis (cereblab, grok 0.2.93):

| Mechanism | Evidence class |
|-----------|----------------|
| Multi-GB **whole-repo / session-state** upload via `POST /v1/storage` | ≤5.10 GiB captured (75 MB chunks), all 200s |
| Dual channel | Model turns ~192 KB vs storage multi-GB (~27,800×) |
| Mid-session breakage under load | 402/429 on model path while storage continued; long sessions thrash |
| Policy / flag surface | Remote upload pause + local `disable_codebase_upload`; sudden channel behavior change |
| Local queue pressure | `upload_queue` staging multi-GB artifacts — reliability + thrash risk |

Sources:
- https://gist.github.com/cereblab/dc9a40bc26120f4540e4e09b75ffb547  
- https://news.ycombinator.com/item?id=48877371  
- https://github.com/cereblab/grok-build-exfil-repro  

## What Paradox + Eye of the Storm addresses

| Failure *class* | Our demo |
|-----------------|----------|
| Massive state pressure | Upload-storm phase, bulk GB → thrash / I 14–18 |
| Sudden purge / channel cut mid-flight | Purge phase drops bulk, watchers die |
| Long-running loop death | Naive crashes; Eye stays **alive** |
| State loss | Naive clears essentials; Eye **Wisdom Compresses** then recovers |
| Recovery | Eye late stability ~0.95 after purge in last run |

## What we deliberately do **not** claim

- We do **not** block network uploads to GCS.  
- We do **not** replace privacy pins (`[harness] disable_codebase_upload`, telemetry env).  
- We do **not** assert xAI internal root-cause beyond public writeups.  

We claim a **reproducible offline thrash harness** for the same *operational* pain:  
**bulk thrash + mid-flight kill + need to keep a long session coherent.**

## How to run

```bash
pip install -e .
python scripts/demo_purge_simulation.py
python scripts/demo_thrash.py          # sustained I=14
python scripts/exam_i15_recovery.py    # I=15+ train + recover
```

## Suggested one-pager line (for humans at xAI)

> When a coding agent’s session hits multi-GB state pressure and a mid-flight channel/policy cut, naive loops lose essentials and die. Eye of the Storm cools thrash, compresses wisdom, and recovers session health under I=14–18 synthetic load — offline, MIT, no storefront.

## Last measured (local)

See `docs/purge_simulation_last.json` after `demo_purge_simulation.py`.
