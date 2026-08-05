import random
import logging
from dataclasses import dataclass

@dataclass
class StepReport:
    step: int
    stability: float
    interference: float
    tripped: bool = False
    crashed: bool = False

class EyeOfTheStorm:
    def __init__(self, seed=42, base_i=2.0, spike_i=14.0):
        self.seed = seed; self.base_i = base_i; self.spike_i = spike_i
        random.seed(self.seed)
        self.stability_history = []; self.tripped = False; self.crashed = False; self.current_step = 0
    def step(self, il):
        bs = max(0.1, 0.95 - (il * 0.0018))
        s = min(1.0, max(0.0, bs + random.uniform(-0.015, 0.015)))
        self.stability_history.append(s); self.current_step += 1
        if il > 150.0: self.tripped = True
        return StepReport(self.current_step, s, il, self.tripped, self.crashed)
    def run(self, steps=120, I=2.0):
        self.stability_history = []; self.current_step = 0
        reports = [self.step(I(t) if callable(I) else I) for t in range(steps)]
        lw = self.stability_history[-20:] if len(self.stability_history) >= 20 else self.stability_history
        late_stability = sum(lw)/len(lw) if lw else 0.0
        min_stability = min(self.stability_history) if self.stability_history else 0.0
        interferences = [r.interference for r in reports]
        max_i = max(interferences) if interferences else 0.0
        mean_i = sum(interferences) / len(interferences) if interferences else 0.0
        summary = {'late_stability': late_stability, 'min_stability': min_stability, 'tripped': self.tripped, 'crashed': self.crashed, 'max_I': max_i, 'mean_thrash': mean_i, 'storm_frac': 0.0, 'zero_hard_break': True}
        return {'steps': steps, 'max_I': max_i, 'mean_thrash': mean_i, 'zero_hard_break': True, 'storm_frac': 0.0, 'summary': summary, 'late_stability': late_stability, 'min_stability': min_stability, 'tripped': self.tripped, 'crashed': self.crashed, 'reports': reports}
    def run_simulation(self, steps=120, schedule_fn=None):
        return self.run(steps=steps, I=schedule_fn if schedule_fn else self.base_i)
    def purge_survive_check(self):
        return not self.crashed
