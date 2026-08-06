# Agentic Leak Diagnostic — Fixed Scope

## Offer

A one-shot stress diagnostic for multi-agent / retry fleets. We compare naive exponential retry cost vs a capped breaker-style fleet under **your** parameters and return a short exposure report.

Not a live proxy of your cloud account. Not a guarantee of your production API bill.

### What you send
- Approximate agent count
- Steps / horizon per run
- Failure or retry rate (or short description)
- Base tokens per attempt (or order of magnitude)
- Optional: orchestrator (LangGraph, CrewAI, custom)

No API keys. No customer data. No PHI.

### What you get
1. Exposure under cascade / stampede-style profiles (matched to the open harness where applicable)
2. Naive vs capped comparison under stated parameters
3. Recommended stateful cost-cap posture for your own stack
4. Optional: short recorded walkthrough (async)

### How to start
DM or email parameters above.  
Harness: https://github.com/mrblakessinger-rgb/paradox-engine-eots

---

# Exposure Report Template

**Target system:** [name or redacted]  
**Date:** [YYYY-MM-DD]  
**Run ID:** [short id]  
**Harness:** proof_of_burn_standalone.py + stress matrix

## 1. Structural parameters

| Input | Value |
|---|---|
| Agents / fleet size | |
| Steps / horizon | |
| Failure / retry rate | |
| Base tokens per attempt | |
| Multiplier (if used) | |
| Orchestrator pattern | |

## 2. Exposure topology

**Mechanism:**  
[2-5 sentences: unbounded retry, growing context, no session cap, stampede after 429s, etc.]

**Profiles simulated:**  
[Primary / Cascade / Long stampede / Heavy mult / custom]

## 3. Cost matrix (harness numbers only)

| Profile | Naive | Capped | Saved | Efficiency |
|---|---:|---:|---:|---:|
| | | | | |
| | | | | |

## 4. Recommended stateful posture

- Hard session cap: 
- Retry / recursion bound: 
- Breaker idea: 

Guidelines for their orchestrator — not a managed service.

## 5. Honesty and scope

**What this is:** Structural stress diagnostic under stated parameters using an open local harness.

**What this is not:** Not a live cloud proxy. Not a guarantee production bills match these figures. Not a fix for prompts or flaky tools. Caps limit runaway loops; they are not managed infrastructure.

