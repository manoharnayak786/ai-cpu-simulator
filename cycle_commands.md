# 🔄 Cycle Testing Commands Reference

## Basic Cycle Testing
```bash
# Run normal simulation
python3 core_simulator.py

# Quick cycle demonstrations  
python3 quick_cycle_demo.py

# Comprehensive cycle analysis
python3 cycle_analysis.py
```

## Custom Cycle Experiments
```bash
# Test cycle limits
python3 -c "
from cycle_analysis import CycleControlledSimulator
tasks = [('BigTask', 20), ('SmallTask', 2)]
sim = CycleControlledSimulator(tasks, 2, 2)
result = sim.run_for_max_cycles(10)
print(f'Completed: {result[\"completion_rate\"]:.1f}%')
"

# Compare cycle efficiency
python3 -c "
from cycle_analysis import CycleControlledSimulator
tasks = [('Work1', 5), ('Work2', 5)]
for cores in [(4,0), (2,2), (0,4)]:
    sim = CycleControlledSimulator(tasks, cores[0], cores[1])
    sim.run_simulation()
    print(f'{cores[0]}P+{cores[1]}E: {sim.cycle} cycles')
"

# Test massive workloads  
python3 -c "
from cycle_analysis import CycleControlledSimulator
massive = [(f'T{i}', i%5+1) for i in range(100)]
sim = CycleControlledSimulator(massive, 4, 4)
sim.run_simulation()
print(f'100 tasks: {sim.cycle} cycles')
"
```

## Performance Testing
```bash
# Time different workload sizes
for size in 10 50 100 200; do
  echo "Testing $size tasks:"
  time python3 -c "
from cycle_analysis import CycleControlledSimulator
tasks = [('Task$i', ($i%5)+1) for i in range($size)]
sim = CycleControlledSimulator(tasks, 4, 4)
sim.run_simulation()
print(f'$size tasks: {sim.cycle} cycles')
"
done

# Benchmark different configurations
python3 -c "
from cycle_analysis import CycleControlledSimulator
import time
tasks = [('T$i', ($i%3)+2) for i in range(50)]
configs = [(1,1), (2,2), (4,4), (8,0), (0,8)]
for p, e in configs:
    start = time.time()
    sim = CycleControlledSimulator(tasks, p, e)
    sim.run_simulation()
    runtime = (time.time() - start) * 1000
    print(f'{p}P+{e}E: {sim.cycle} cycles, {runtime:.1f}ms')
"
```

## Cycle Limit Experiments  
```bash
# Test what happens with different cycle limits
python3 -c "
from cycle_analysis import CycleControlledSimulator
tasks = [('HeavyTask', 30)]
for limit in [5, 10, 15, 20, 25]:
    sim = CycleControlledSimulator(tasks, 2, 0)
    result = sim.run_for_max_cycles(limit, silent=True)
    status = '✅' if result['fully_completed'] else '⏸️'
    print(f'Limit {limit}: {result[\"completion_rate\"]:5.1f}% {status}')
"

# Interactive cycle control
python3 -c "
from cycle_analysis import CycleControlledSimulator
tasks = [('Interactive1', 8), ('Interactive2', 4)]
sim = CycleControlledSimulator(tasks, 1, 1)
result = sim.run_for_max_cycles(5)
if not result['fully_completed']:
    print('Continuing to finish...')
    sim.run_simulation()
    print(f'Total: {sim.cycle} cycles')
"
```

## Analysis Commands
```bash
# Save cycle analysis to file
python3 cycle_analysis.py > cycle_results.txt

# Extract key metrics
python3 cycle_analysis.py | grep "cycles" | head -10

# Compare energy efficiency
python3 cycle_analysis.py | grep "energy" | sort -k3 -n

# Find fastest configurations
python3 cycle_analysis.py | grep "cycles" | sort -k2 -n
```

## Quick Tests
```bash
# Single cycle step analysis
python3 -c "
from core_simulator import Task, Core
task = Task('Test', 10)
core = Core('P1', 'P', 1.5, 1.33)
core.assign_task(task)
for i in range(5):
    print(f'Cycle {i+1}: {task.remaining} remaining')
    core.process()
    if core.task is None: break
"

# Core utilization check
python3 -c "
from cycle_analysis import CycleControlledSimulator
tasks = [('T1', 10), ('T2', 1), ('T3', 1)]
sim = CycleControlledSimulator(tasks, 4, 1)
sim.run_simulation()
print(f'4P+1E completed in {sim.cycle} cycles')
sim2 = CycleControlledSimulator(tasks, 1, 4)  
sim2.run_simulation()
print(f'1P+4E completed in {sim2.cycle} cycles')
"
``` 