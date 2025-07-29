#!/usr/bin/env python3
# cycle_analysis.py - Cycle behavior analysis and control

from core_simulator import CPUSimulator
import time

class CycleControlledSimulator(CPUSimulator):
    """Extended simulator with cycle control features"""
    
    def __init__(self, tasks, num_perf, num_eff, **kwargs):
        super().__init__(tasks, num_perf, num_eff, **kwargs)
        self.max_cycles = None
        self.silent_mode = False
        
    def run_for_max_cycles(self, max_cycles, silent=False):
        """Run simulation for maximum number of cycles"""
        self.max_cycles = max_cycles
        self.silent_mode = silent
        
        self.assign_tasks()
        if not silent:
            print(f"\nRunning for maximum {max_cycles} cycles...\n")
        
        total_tasks = len(self.wait_queue_perf) + len(self.wait_queue_eff)
        
        while (len(self.completed_tasks) < total_tasks and 
               self.cycle < max_cycles):
            if not silent:
                print(f"Cycle {self.cycle + 1}")
            self.assign_to_cores()
            self.run_cycle()
            if not silent:
                self.print_core_status()
        
        self.total_energy = sum(core.energy_used for core in self.perf_cores + self.eff_cores)
        
        # Analysis
        remaining_tasks = total_tasks - len(self.completed_tasks)
        completion_rate = len(self.completed_tasks) / total_tasks * 100
        
        if not silent:
            print(f"📊 CYCLE ANALYSIS:")
            print(f"   Cycles Used: {self.cycle}/{max_cycles}")
            print(f"   Tasks Completed: {len(self.completed_tasks)}/{total_tasks}")
            print(f"   Completion Rate: {completion_rate:.1f}%")
            print(f"   Tasks Remaining: {remaining_tasks}")
            print(f"   Energy Used: {self.total_energy:.2f}")
            
            if remaining_tasks > 0:
                print(f"   ⚠️ Simulation incomplete - would need ~{self.estimate_remaining_cycles()} more cycles")
        
        return {
            'cycles_used': self.cycle,
            'max_cycles': max_cycles,
            'tasks_completed': len(self.completed_tasks),
            'total_tasks': total_tasks,
            'completion_rate': completion_rate,
            'energy_used': self.total_energy,
            'fully_completed': remaining_tasks == 0
        }
    
    def estimate_remaining_cycles(self):
        """Estimate cycles needed to complete remaining work"""
        remaining_work = 0
        for task in self.wait_queue_perf + self.wait_queue_eff:
            remaining_work += task.remaining
        
        # Add work from currently running tasks
        for core in self.perf_cores + self.eff_cores:
            if core.task:
                remaining_work += core.task.remaining
        
        # Estimate based on average core speed
        total_cores = len(self.perf_cores) + len(self.eff_cores)
        if total_cores == 0:
            return float('inf')
        
        avg_speed = (len(self.perf_cores) * 1.5 + len(self.eff_cores) * 1.0) / total_cores
        return int(remaining_work / avg_speed) + 1

def analyze_cycle_patterns():
    """Analyze how different configurations affect cycle counts"""
    print("🔬 CYCLE PATTERN ANALYSIS")
    print("=" * 50)
    
    # Test workload
    test_tasks = [
        ("Heavy1", 8), ("Heavy2", 6), ("Heavy3", 10),
        ("Medium1", 3), ("Medium2", 4), ("Medium3", 3),
        ("Light1", 1), ("Light2", 2), ("Light3", 1)
    ]
    
    configs = [
        ("1P+1E", 1, 1),
        ("2P+2E", 2, 2), 
        ("4P+0E", 4, 0),
        ("0P+4E", 0, 4),
        ("1P+7E", 1, 7),
        ("7P+1E", 7, 1)
    ]
    
    results = []
    
    for name, p_cores, e_cores in configs:
        sim = CycleControlledSimulator(test_tasks, p_cores, e_cores)
        start_time = time.time()
        sim.run_simulation()
        end_time = time.time()
        
        results.append({
            'config': name,
            'cycles': sim.cycle,
            'energy': sim.total_energy,
            'runtime_ms': (end_time - start_time) * 1000,
            'efficiency': sim.total_energy / sim.cycle if sim.cycle > 0 else 0
        })
    
    # Display results
    print(f"\n{'Config':<8} {'Cycles':<8} {'Energy':<8} {'Runtime':<10} {'Efficiency':<10}")
    print("-" * 50)
    for r in results:
        print(f"{r['config']:<8} {r['cycles']:<8} {r['energy']:<8.1f} {r['runtime_ms']:<10.1f}ms {r['efficiency']:<10.2f}")
    
    return results

def cycle_limit_experiment():
    """Test what happens with different cycle limits"""
    print("\n🎯 CYCLE LIMIT EXPERIMENT")
    print("=" * 40)
    
    tasks = [("BigTask", 20), ("MedTask", 5), ("SmallTask", 2)]
    
    cycle_limits = [5, 10, 15, 20, 25, 50]
    
    for limit in cycle_limits:
        sim = CycleControlledSimulator(tasks, 2, 2)
        result = sim.run_for_max_cycles(limit, silent=True)
        
        status = "✅ Complete" if result['fully_completed'] else "⏸️ Partial"
        print(f"Limit {limit:2d} cycles: {result['tasks_completed']}/{result['total_tasks']} tasks, "
              f"{result['completion_rate']:5.1f}% complete, {result['energy_used']:6.2f} energy - {status}")

def massive_workload_test():
    """Test performance with very large workloads"""
    print("\n🚀 MASSIVE WORKLOAD TEST")
    print("=" * 30)
    
    # Create increasingly large workloads
    workload_sizes = [10, 50, 100, 500]
    
    for size in workload_sizes:
        massive_tasks = [(f"Task{i}", (i % 5) + 1) for i in range(size)]
        
        sim = CycleControlledSimulator(massive_tasks, 4, 4)
        start_time = time.time()
        sim.run_simulation()
        end_time = time.time()
        
        print(f"{size:3d} tasks: {sim.cycle:4d} cycles, "
              f"{sim.total_energy:7.1f} energy, "
              f"{(end_time-start_time)*1000:6.1f}ms runtime")

if __name__ == "__main__":
    # Run all cycle analyses
    analyze_cycle_patterns()
    cycle_limit_experiment() 
    massive_workload_test()
    
    print("\n" + "="*60)
    print("🎮 INTERACTIVE CYCLE CONTROL EXAMPLE")
    print("="*60)
    
    # Interactive example
    tasks = [("InteractiveTask1", 10), ("InteractiveTask2", 5), ("InteractiveTask3", 3)]
    sim = CycleControlledSimulator(tasks, 2, 1)
    
    print("\n📋 Testing cycle-controlled simulation:")
    result = sim.run_for_max_cycles(8)
    
    if not result['fully_completed']:
        print(f"\n🔄 Continuing simulation to completion...")
        sim.run_simulation()
        print(f"Final completion: {sim.cycle} total cycles") 