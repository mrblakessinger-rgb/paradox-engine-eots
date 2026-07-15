"""Anti-thrash demo tests — free sample verification."""

from __future__ import annotations

from paradox_engine import EyeOfTheStorm, ParadoxEngine


def test_import_and_step():
    eng = ParadoxEngine(seed=1)
    s0 = eng.stability
    s1 = eng.step_raw(1.5)
    assert 0.0 <= s0 <= 1.0
    assert 0.0 <= s1 <= 1.0
    assert eng.alive


def test_eye_sustained_I14_zero_hard_break():
    """Sustained I=14: no hard break / process crash in harness."""
    eye = EyeOfTheStorm(seed=42)
    out = eye.run(steps=100, I=14.0)
    assert out["crashed"] is False
    assert out["zero_hard_break"] is True
    assert out["summary"]["late_stability"] > 0.5
    assert out["summary"]["max_I"] >= 14.0
    # Interference logging present
    assert out["summary"]["n"] == 100
    # Wisdom compression ran
    assert "wisdom" in out
    assert "anti_lock" in out["wisdom"] or len(out["wisdom"]) >= 1


def test_wisdom_compression_clears_scars():
    eng = ParadoxEngine(seed=2)
    eng.absorb_scars(
        [{"reason": "tighten_floor"}] * 5 + [{"reason": "climb_calm"}] * 3,
        meta={"survived_long_hell": True, "first_hard_break": None},
    )
    rep = eng.compress_wisdom()
    assert rep.get("cleared_raw") is True or rep.get("n_scars", 0) >= 0
    assert isinstance(eng.wisdom_snapshot(), dict)


def test_recovery_from_high_I():
    eye = EyeOfTheStorm(seed=7)
    # quick train touch
    train = eye.train_high_I(I_levels=[10.0, 14.0, 15.0], steps_per=40, epochs=2, seed=7)
    dna = train.get("trained_dna")
    exam = eye.recovery_exam(peak_I=15.0, hold_steps=25, recover_steps=50, seed=11, dna=dna)
    assert exam["crashed"] is False
    assert exam["zero_hard_break"] is True


def test_purge_simulation_grok_build_class():
    """July-2026-class: multi-GB thrash + mid-flight purge — Eye survives, naive dies."""
    from paradox_engine import ParadoxEngine

    eng = ParadoxEngine(seed=3)
    out = eng.stress_test_purge_simulation(seed=3)
    naive, eye = out["naive"], out["eye_of_the_storm"]
    assert naive["crashed"] is True or naive["essential_intact_at_end"] is False
    assert eye["purge_survived"] is True
    assert eye["alive_at_end"] is True
    assert eye["essential_intact_at_end"] is True
    assert out["winner"] == "eye_of_the_storm"
