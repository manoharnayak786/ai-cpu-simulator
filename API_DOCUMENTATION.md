# 🔌 AI CPU Simulator - API Documentation

Complete API reference for all classes, methods, and functions in the AI CPU Simulator.

---

## 🔧 `core_simulator.py` API Reference

### Class: `Task`
Represents a computational workload with difficulty and progress tracking.

```python
class Task:
    def __init__(self, name: str, difficulty: int)
```

**Parameters**:
- `name` (str): Human-readable task identifier
- `difficulty` (int): Computational complexity (1-20+ scale)

**Attributes**:
- `name` (str): Task identifier
- `difficulty` (int): Original difficulty level
- `remaining` (float): Work remaining to complete

**Methods**:
- `__repr__()`: String representation showing name, difficulty, and remaining work

**Example**:
```python
task = Task("VideoTranscode", 8)
print(task)  # VideoTranscode(Diff:8, Rem:8)
```

---

### Class: `Core`
Models individual CPU cores with type-specific performance characteristics.

```python
class Core:
    def __init__(self, name: str, core_type: str, speed_multiplier: float, energy_multiplier: float)
```

**Parameters**:
- `name` (str): Core identifier (e.g., "P1", "E2")
- `core_type` (str): Core type ("P" for Performance, "E" for Efficiency)
- `speed_multiplier` (float): Processing speed multiplier (e.g., 1.5 for P-cores)
- `energy_multiplier` (float): Energy consumption multiplier (e.g., 1.33 for P-cores)

**Attributes**:
- `name` (str): Core identifier
- `core_type` (str): "P" or "E"
- `speed` (float): Processing speed per cycle
- `energy_multiplier` (float): Energy cost per unit work
- `task` (Task|None): Currently assigned task
- `energy_used` (float): Cumulative energy consumption

**Methods**:
- `assign_task(task: Task)`: Assign a task to this core
- `is_idle() -> bool`: Check if core has no assigned task
- `process() -> Task|None`: Process one cycle, return completed task if finished
- `__repr__()`: String representation showing core status and assigned task

**Example**:
```python
p_core = Core("P1", "P", speed_multiplier=1.5, energy_multiplier=1.33)
e_core = Core("E1", "E", speed_multiplier=1.0, energy_multiplier=1.0)

p_core.assign_task(Task("HeavyWork", 10))
completed = p_core.process()  # Process one cycle
```

---

### Class: `CPUSimulator`
Main simulation controller for heterogeneous CPU simulation.

```python
class CPUSimulator:
    def __init__(self, tasks: List[Tuple[str, int]], num_perf: int, num_eff: int,
                 perf_speed: float = 1.5, perf_energy: float = 1.33,
                 eff_speed: float = 1.0, eff_energy: float = 1.0,
                 threshold: int = 2)
```

**Parameters**:
- `tasks` (List[Tuple[str, int]]): List of (task_name, difficulty) tuples
- `num_perf` (int): Number of Performance cores
- `num_eff` (int): Number of Efficiency cores  
- `perf_speed` (float): P-core speed multiplier (default: 1.5)
- `perf_energy` (float): P-core energy multiplier (default: 1.33)
- `eff_speed` (float): E-core speed multiplier (default: 1.0)
- `eff_energy` (float): E-core energy multiplier (default: 1.0)
- `threshold` (int): Difficulty threshold for P-core assignment (default: 2)

**Attributes**:
- `tasks` (List[Task]): Task objects created from input
- `threshold` (int): Difficulty threshold for core assignment
- `cycle` (int): Current simulation cycle
- `total_energy` (float): Total energy consumed
- `perf_cores` (List[Core]): Performance cores
- `eff_cores` (List[Core]): Efficiency cores
- `wait_queue_perf` (List[Task]): Queue for Performance cores
- `wait_queue_eff` (List[Task]): Queue for Efficiency cores
- `completed_tasks` (List[Task]): Completed tasks

**Methods**:
- `assign_tasks()`: Sort tasks into appropriate queues based on difficulty
- `assign_to_cores()`: Assign queued tasks to available cores
- `run_cycle()`: Execute one simulation cycle
- `run_simulation()`: Run complete simulation until all tasks done
- `print_core_status()`: Display current state of all cores

**Example**:
```python
tasks = [("TranscribeAudio", 5), ("RenderUI", 2), ("ProcessData", 8)]
sim = CPUSimulator(tasks, num_perf=2, num_eff=2, threshold=3)
sim.run_simulation()

print(f"Completed in {sim.cycle} cycles")
print(f"Energy used: {sim.total_energy:.2f}")
```

---

## 🤖 `ai_workloads.py` API Reference

### Class: `AIWorkloadProfiler`
Profiles and models real AI workloads for CPU simulation.

**Class Attributes**:
- `AI_WORKLOADS` (Dict): Database of real AI workload characteristics

**Class Methods**:

```python
@classmethod
def create_realistic_edtech_workload(cls) -> List[Tuple[str, int]]
```
Creates a realistic EdTech AI workload for simulation.
- **Returns**: List of (task_name, difficulty) tuples representing a full day of EdTech AI operations

```python
@classmethod  
def create_realtime_ai_workload(cls) -> List[Tuple[str, int]]
```
Creates real-time AI workload simulation.
- **Returns**: List of tasks optimized for real-time interactive scenarios

```python
@classmethod
def create_research_ai_workload(cls) -> List[Tuple[str, int]]
```
Creates research-intensive AI workload.
- **Returns**: List of tasks for research and development scenarios

```python
@classmethod
def simulate_with_realistic_delays(cls, workload_name: str) -> float
```
Simulates actual AI API call delays.
- **Parameters**: `workload_name` (str) - Name of AI workload
- **Returns**: Simulated delay in seconds with realistic variance

**Functions**:

```python
def run_ai_workload_comparison() -> List[Dict]
```
Compares different AI workload scenarios across configurations.
- **Returns**: List of result dictionaries with performance metrics

**Example**:
```python
from ai_workloads import AIWorkloadProfiler, run_ai_workload_comparison

# Create realistic workloads
edtech_tasks = AIWorkloadProfiler.create_realistic_edtech_workload()
realtime_tasks = AIWorkloadProfiler.create_realtime_ai_workload()

# Run comprehensive comparison
results = run_ai_workload_comparison()
```

---

## 📊 `cycle_analysis.py` API Reference

### Class: `CycleControlledSimulator`
Extended simulator with cycle control features, inherits from `CPUSimulator`.

```python
class CycleControlledSimulator(CPUSimulator):
    def __init__(self, tasks: List[Tuple[str, int]], num_perf: int, num_eff: int, **kwargs)
```

**Additional Attributes**:
- `max_cycles` (int|None): Maximum cycles for limited runs
- `silent_mode` (bool): Whether to suppress output

**Methods**:

```python
def run_for_max_cycles(self, max_cycles: int, silent: bool = False) -> Dict
```
Runs simulation for maximum number of cycles.
- **Parameters**:
  - `max_cycles` (int): Maximum cycles to run
  - `silent` (bool): Suppress output if True
- **Returns**: Dictionary with completion analysis:
  ```python
  {
      'cycles_used': int,
      'max_cycles': int, 
      'tasks_completed': int,
      'total_tasks': int,
      'completion_rate': float,
      'energy_used': float,
      'fully_completed': bool
  }
  ```

```python
def estimate_remaining_cycles(self) -> int
```
Estimates cycles needed to complete remaining work.
- **Returns**: Estimated cycles remaining

**Functions**:

```python
def analyze_cycle_patterns() -> List[Dict]
```
Analyzes how different configurations affect cycle counts.
- **Returns**: List of performance results across configurations

```python
def cycle_limit_experiment() -> None
```
Tests what happens with different cycle limits.

```python
def massive_workload_test() -> None
```
Tests performance with very large workloads (10-500 tasks).

**Example**:
```python
from cycle_analysis import CycleControlledSimulator

tasks = [("BigTask", 20), ("SmallTask", 2)]
sim = CycleControlledSimulator(tasks, 2, 2)

# Run with cycle limit
result = sim.run_for_max_cycles(10, silent=False)
if not result['fully_completed']:
    print(f"Need {sim.estimate_remaining_cycles()} more cycles")
```

---

## 📈 `visualizer.py` API Reference

### Class: `CPUSimulatorVisualizer`
Professional visualization suite for CPU simulator results.

```python
class CPUSimulatorVisualizer:
    def __init__(self)
```

**Attributes**:
- `fig_size` (Tuple[int, int]): Default figure size (12, 8)
- `dpi` (int): Resolution for saved figures (300)

**Methods**:

```python
def plot_cycles_vs_energy(self, results: List[Dict] = None, save_path: str = None) -> Figure
```
Creates comprehensive cycles vs energy analysis plots.
- **Parameters**:
  - `results` (List[Dict], optional): Pre-computed results, generates if None
  - `save_path` (str, optional): Path to save figure
- **Returns**: matplotlib Figure object

**Private Methods**:
- `_plot_scalability_analysis(ax)`: Plots scalability for different workload sizes
- `_plot_performance_heatmap(ax, results)`: Creates performance heatmap

**Functions**:

```python
def main() -> None
```
Runs comprehensive visualization suite.

**Example**:
```python
from visualizer import CPUSimulatorVisualizer

viz = CPUSimulatorVisualizer()
fig = viz.plot_cycles_vs_energy(save_path="performance_analysis.png")
```

---

## 🧪 Testing APIs

### `test_configs.py`

```python
def test_configuration(name: str, num_perf: int, num_eff: int, threshold: int = 2) -> Tuple[int, float]
```
Tests a specific CPU configuration.
- **Parameters**: Configuration name, core counts, threshold
- **Returns**: (cycles, energy) tuple

### `stress_test.py`

```python
def stress_test(name: str, tasks: List[Tuple[str, int]], num_perf: int, num_eff: int, **kwargs) -> None
```
Runs a named stress test scenario.
- **Parameters**: Test name, tasks, core configuration, additional kwargs

### `quick_cycle_demo.py`

```python
def demo_cycle_scenarios() -> None
```
Demonstrates different cycle scenarios with explanations.

---

## 🎯 Common Usage Patterns

### Basic Simulation
```python
from core_simulator import CPUSimulator

tasks = [("Task1", 5), ("Task2", 2)]
sim = CPUSimulator(tasks, num_perf=2, num_eff=2)
sim.run_simulation()
```

### Cycle-Limited Simulation
```python
from cycle_analysis import CycleControlledSimulator

sim = CycleControlledSimulator(tasks, 2, 2)
result = sim.run_for_max_cycles(10)
print(f"Completion: {result['completion_rate']:.1f}%")
```

### Performance Comparison
```python
from ai_workloads import run_ai_workload_comparison
from visualizer import CPUSimulatorVisualizer

results = run_ai_workload_comparison()
viz = CPUSimulatorVisualizer()
viz.plot_cycles_vs_energy(results, "comparison.png")
```

### Custom Workload Testing
```python
from core_simulator import CPUSimulator

# Test different configurations
configs = [(4,0), (2,2), (0,4)]
for p, e in configs:
    sim = CPUSimulator(tasks, p, e)
    sim.run_simulation()
    print(f"{p}P+{e}E: {sim.cycle} cycles, {sim.total_energy:.1f} energy")
```