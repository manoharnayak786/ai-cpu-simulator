#!/usr/bin/env python3
# quick_cycle_demo.py - Quick cycle scenario demonstrations

from cycle_analysis import CycleControlledSimulator

def demo_cycle_scenarios():
    """Demonstrate different cycle scenarios"""
    
    print("🔄 CYCLE SCENARIO DEMONSTRATIONS")
    print("=" * 40)
    
    # Scenario 1: Normal completion
    print("\n1️⃣ NORMAL SCENARIO:")
    tasks1 = [("Task1", 3), ("Task2", 2)]
    sim1 = CycleControlledSimulator(tasks1, 2, 1)
    sim1.run_simulation()
    
    # Scenario 2: Limited cycles
    print("\n2️⃣ LIMITED CYCLES SCENARIO:")
    tasks2 = [("BigTask", 15), ("SmallTask", 2)]
    sim2 = CycleControlledSimulator(tasks2, 1, 1)
    result = sim2.run_for_max_cycles(5)
    
    # Scenario 3: What if we have too many cycles?
    print("\n3️⃣ EXCESS CYCLES SCENARIO:")
    tasks3 = [("QuickTask", 1)]
    sim3 = CycleControlledSimulator(tasks3, 4, 4)
    result3 = sim3.run_for_max_cycles(20)  # Way more than needed
    
    # Scenario 4: Efficiency comparison
    print("\n4️⃣ EFFICIENCY COMPARISON:")
    same_tasks = [("Work1", 4), ("Work2", 4), ("Work3", 4)]
    
    configs = [
        ("Fast Setup", 3, 0),
        ("Balanced", 2, 2), 
        ("Efficient", 0, 4)
    ]
    
    for name, p, e in configs:
        sim = CycleControlledSimulator(same_tasks, p, e)
        sim.run_simulation()
        print(f"  {name}: {sim.cycle} cycles, {sim.total_energy:.1f} energy")

if __name__ == "__main__":
    demo_cycle_scenarios() 