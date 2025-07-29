#!/usr/bin/env python3
# stress_test.py - Stress test and edge cases

from core_simulator import CPUSimulator

def stress_test(name, tasks, num_perf, num_eff, **kwargs):
    print(f"\n🚨 STRESS TEST: {name}")
    print("-" * 40)
    
    sim = CPUSimulator(
        tasks=tasks,
        num_perf=num_perf,
        num_eff=num_eff,
        **kwargs
    )
    
    sim.run_simulation()
    print(f"✅ COMPLETED: {sim.cycle} cycles, {sim.total_energy:.2f} energy")

if __name__ == "__main__":
    # Edge Case 1: Only heavy tasks
    stress_test(
        "Only Heavy Tasks", 
        [("HeavyTask1", 10), ("HeavyTask2", 8), ("HeavyTask3", 12)],
        2, 2
    )
    
    # Edge Case 2: Only light tasks  
    stress_test(
        "Only Light Tasks",
        [("Light1", 1), ("Light2", 1), ("Light3", 1), ("Light4", 1)],
        2, 2
    )
    
    # Edge Case 3: Many small tasks
    stress_test(
        "Many Small Tasks",
        [(f"Task{i}", 1) for i in range(20)],
        1, 1
    )
    
    # Edge Case 4: Few huge tasks
    stress_test(
        "Few Huge Tasks",
        [("Massive1", 50), ("Massive2", 30)],
        2, 2
    )
    
    # Edge Case 5: High threshold test
    stress_test(
        "High Threshold (threshold=10)",
        [("Task1", 5), ("Task2", 8), ("Task3", 12), ("Task4", 2)],
        2, 2,
        threshold=10
    )
    
    # Edge Case 6: Extreme core configurations
    stress_test(
        "8 Performance Cores",
        [("Task1", 5), ("Task2", 3), ("Task3", 4)],
        8, 0
    )
    
    stress_test(
        "8 Efficiency Cores", 
        [("Task1", 1), ("Task2", 2), ("Task3", 1)],
        0, 8
    ) 