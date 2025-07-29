#!/usr/bin/env python3
# test_configs.py - Test different CPU configurations

from core_simulator import CPUSimulator

def test_configuration(name, num_perf, num_eff, threshold=2):
    print(f"\n{'='*50}")
    print(f"🔬 TESTING: {name}")
    print(f"{'='*50}")
    
    tasks = [
        ("TranscribeDebate", 5),
        ("RenderQuiz", 2),
        ("EvaluateEssay", 3),
        ("GenerateFeedback", 4),
        ("MapGraph", 1),
        ("AudioSummary", 4),
        ("SpeechToText", 5),
        ("DataProcessing", 6),
        ("LightTask1", 1),
        ("LightTask2", 1),
    ]

    sim = CPUSimulator(
        tasks=tasks,
        num_perf=num_perf,
        num_eff=num_eff,
        threshold=threshold
    )
    
    sim.run_simulation()
    print(f"📊 RESULTS: {sim.cycle} cycles, {sim.total_energy:.2f} energy")
    return sim.cycle, sim.total_energy

if __name__ == "__main__":
    # Test different configurations
    configs = [
        ("Performance Heavy (4P + 0E)", 4, 0),
        ("Efficiency Heavy (0P + 4E)", 0, 4), 
        ("Balanced (2P + 2E)", 2, 2),
        ("Efficiency Focus (1P + 3E)", 1, 3),
        ("Performance Focus (3P + 1E)", 3, 1),
    ]
    
    results = []
    for name, p_cores, e_cores in configs:
        if p_cores + e_cores > 0:  # Skip invalid configs
            cycles, energy = test_configuration(name, p_cores, e_cores)
            results.append((name, cycles, energy))
    
    print(f"\n{'='*60}")
    print("📈 COMPARISON SUMMARY")
    print(f"{'='*60}")
    for name, cycles, energy in results:
        print(f"{name:25} | {cycles:2d} cycles | {energy:6.2f} energy") 