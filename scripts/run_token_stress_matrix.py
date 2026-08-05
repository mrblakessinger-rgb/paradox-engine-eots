import proof_of_burn_standalone as pob

def evaluate_profile(name, agents, steps, fail_rate, base_tokens, cap, multiplier):
    naive = pob.run_naive_fleet(agents=agents, steps=steps, fail_rate=fail_rate, base_tokens=base_tokens, multiplier=multiplier)
    paradox, _, _ = pob.run_breaker_fleet(agents=agents, steps=steps, fail_rate=fail_rate, base_tokens=base_tokens, multiplier=multiplier, cap=cap)
    saved = naive - paradox
    eff = (saved / naive) * 100
    assert eff >= 90.0
    saved_str = f"{saved / 1_000_000:.2f}M"
    print(f"[PASS] Profile: {name} | Efficiency: {eff:.2f}% | Absolute Saved: saved_str tokens")
    return f"|**{name}**| {agents} | {steps} | {int(fail_rate*100)}% | {eff:.2f}% | {saved_str} | PASS |"

def main():
    print("Initializing EoTS Enterprise Token Stress Matrix (Stateful Breaker Importer)...")
    profiles = [
        ("Primary Gate E0", 100, 8, 0.75, 12000, 3100, 1.45),
        *Cascade Outage", 100, 12, 0.90, 12000, 3100, 1.45),
        ("Long Stampede", 100, 16, 0.75, 12000, 3100, 1.45),
        ("Heavy Mult", 100, 8, 0.75, 12000, 3100, 1.60),
    ]
    for p in profiles:
        evaluate_profile(*p)
    print("\nMatrix execution complete. All profiles verified via stateful module import.")

if __name__ == '__main__':
    main()
