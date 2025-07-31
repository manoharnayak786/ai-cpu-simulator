# ⚙️ AI CPU Simulator - Simulation Parameters

This document provides a comprehensive overview of all simulation parameters used in the AI CPU Simulator project, their default values, ranges, and impact on simulation results.

---

## 🏗️ **Core Architecture Parameters**

### **1. CPU Core Configuration**
These parameters define the heterogeneous CPU architecture being simulated.

| Parameter | Type | Default Value | Range | Description |
|-----------|------|---------------|-------|-------------|
| `num_perf` | int | 2 | 0-8+ | Number of Performance (P) cores |
| `num_eff` | int | 2 | 0-8+ | Number of Efficiency (E) cores |

**Usage Examples**:
```python
# Balanced configuration (used in most tests)
CPUSimulator(tasks, num_perf=2, num_eff=2)

# Performance-heavy configuration  
CPUSimulator(tasks, num_perf=4, num_eff=0)

# Efficiency-heavy configuration
CPUSimulator(tasks, num_perf=0, num_eff=4)

# Extreme configurations (stress testing)
CPUSimulator(tasks, num_perf=8, num_eff=0)
```

---

## ⚡ **Performance Characteristics Parameters**

### **2. Processing Speed Multipliers**
Control how fast each core type processes tasks relative to baseline.

| Parameter | Type | Default Value | Range | Description |
|-----------|------|---------------|-------|-------------|
| `perf_speed` | float | 1.5 | 1.0-3.0+ | P-core processing speed multiplier |
| `eff_speed` | float | 1.0 | 0.5-2.0 | E-core processing speed multiplier |

**Based on Real Hardware**: Apple M1/M2 characteristics
- **P-cores**: 50% faster processing than baseline
- **E-cores**: Baseline processing speed

```python
# Default realistic values (Apple M1/M2 based)
CPUSimulator(tasks, perf_speed=1.5, eff_speed=1.0)

# Custom performance characteristics
CPUSimulator(tasks, perf_speed=2.0, eff_speed=0.8)  # More aggressive P-cores
```

### **3. Energy Consumption Multipliers**
Control energy usage per unit of work for each core type.

| Parameter | Type | Default Value | Range | Description |
|-----------|------|---------------|-------|-------------|
| `perf_energy` | float | 1.33 | 1.0-2.5+ | P-core energy consumption multiplier |
| `eff_energy` | float | 1.0 | 0.3-1.5 | E-core energy consumption multiplier |

**Energy Trade-offs**:
- **P-cores**: 33% more energy consumption for 50% more speed
- **E-cores**: Baseline energy consumption

```python
# Default energy characteristics
CPUSimulator(tasks, perf_energy=1.33, eff_energy=1.0)

# Power-efficient variant
CPUSimulator(tasks, perf_energy=1.2, eff_energy=0.8)
```

---

## 🧠 **Task Assignment Parameters**

### **4. Difficulty Threshold**
Controls which tasks are assigned to which core type.

| Parameter | Type | Default Value | Range | Description |
|-----------|------|---------------|-------|-------------|
| `threshold` | int | 2 | 1-15+ | Difficulty threshold for P-core assignment |

**Assignment Logic**:
- Tasks with `difficulty > threshold` → P-cores (heavy tasks)
- Tasks with `difficulty ≤ threshold` → E-cores (light tasks)

```python
# Default threshold (used in most configurations)
CPUSimulator(tasks, threshold=2)

# Conservative threshold (more tasks to P-cores)
CPUSimulator(tasks, threshold=1)

# Aggressive threshold (more tasks to E-cores)  
CPUSimulator(tasks, threshold=5)

# High threshold (stress testing)
CPUSimulator(tasks, threshold=10)
```

**Threshold Impact Analysis**:
```python
# Example tasks and their assignment based on threshold
tasks = [
    ("LightUI", 1),        # → E-cores (≤ threshold)
    ("RenderQuiz", 2),     # → E-cores if threshold ≥ 2
    ("EvaluateEssay", 3),  # → P-cores if threshold < 3
    ("GenerateFeedback", 4), # → P-cores (> most thresholds)
    ("TranscribeAudio", 5), # → P-cores (heavy task)
]

# threshold=2: [1,2] → E-cores, [3,4,5] → P-cores
# threshold=3: [1,2,3] → E-cores, [4,5] → P-cores
```

---

## 🤖 **AI Workload Parameters**

### **5. Real AI Workload Characteristics**
Based on actual AI system measurements and research.

| AI Workload | Difficulty | Tokens | Latency (ms) | Category |
|-------------|------------|--------|--------------|----------|
| **Language Models** |
| GPT-3.5-Turbo | 8 | 150 | 1200 | LLM |
| GPT-4-Reasoning | 12 | 200 | 3500 | Advanced LLM |
| Claude-3-Analysis | 10 | 180 | 2100 | LLM |
| BERT-Sentiment | 6 | 50 | 300 | NLP |
| **Computer Vision** |
| YOLO-ObjectDetection | 9 | 100 | 850 | CV |
| ResNet-ImageClassify | 7 | 80 | 450 | CV |
| StyleGAN-Generation | 15 | 300 | 5000 | Generative |
| FaceNet-Recognition | 8 | 90 | 650 | CV |
| **Speech & Audio** |
| Whisper-Large-V3 | 10 | 120 | 1800 | ASR |
| TTS-ElevenLabs | 7 | 75 | 900 | TTS |
| AudioSeparation | 11 | 140 | 2200 | Audio |
| **EdTech Specific** |
| EssayGrading-AI | 9 | 110 | 1500 | Education |
| MathSolver-WolframAlpha | 13 | 160 | 2800 | Education |
| CodeReview-Copilot | 8 | 95 | 1100 | Education |
| QuizGeneration-AI | 6 | 70 | 800 | Education |
| PersonalizedTutor | 11 | 130 | 2000 | Education |

**Parameter Mapping**:
```python
# Real AI workload with realistic parameters
AI_WORKLOADS = {
    "GPT-4-Reasoning": {
        "difficulty": 12,      # High computational complexity
        "tokens": 200,         # Output token count
        "latency_ms": 3500     # Realistic API response time
    }
}
```

### **6. Workload Variance Parameters**
Simulate realistic variation in AI system performance.

| Parameter | Type | Value | Description |
|-----------|------|-------|-------------|
| `variance_range` | tuple | (0.7, 1.3) | ±30% latency variation |
| `base_difficulty` | int | 1-20 | Task complexity scale |

```python
# Realistic latency simulation with variance
def simulate_with_realistic_delays(cls, workload_name):
    base_latency = cls.AI_WORKLOADS[workload_name]["latency_ms"]
    variance = random.uniform(0.7, 1.3)  # ±30% realistic variance
    actual_latency = base_latency * variance
    return actual_latency / 1000.0
```

---

## 🔄 **Simulation Control Parameters**

### **7. Cycle Control Parameters**
For advanced simulation control and analysis.

| Parameter | Type | Default | Range | Description |
|-----------|------|---------|-------|-------------|
| `max_cycles` | int | ∞ | 1-1000+ | Maximum simulation cycles |
| `silent_mode` | bool | False | True/False | Suppress output during simulation |

```python
# Cycle-limited simulation (battery constraints)
sim = CycleControlledSimulator(tasks, 2, 2)
result = sim.run_for_max_cycles(max_cycles=10, silent=True)

# Normal unlimited simulation  
sim = CPUSimulator(tasks, 2, 2)
sim.run_simulation()
```

### **8. Testing Parameters**
Used in stress testing and edge case validation.

| Parameter | Type | Example Values | Description |
|-----------|------|----------------|-------------|
| `workload_sizes` | list | [10, 50, 100, 500] | Scalability test sizes |
| `stress_configs` | list | [(8,0), (0,8), (1,7)] | Extreme core configurations |
| `massive_task_size` | int | 50, 100 | Individual task complexity |

```python
# Scalability testing parameters
workload_sizes = [10, 25, 50, 100, 200, 500]

# Stress test configurations
stress_configs = [
    ("Extreme Performance", 8, 0),
    ("Extreme Efficiency", 0, 8), 
    ("Unbalanced Heavy", 1, 7),
    ("Unbalanced Performance", 7, 1)
]

# Massive individual tasks
massive_tasks = [("Massive1", 50), ("Massive2", 100)]
```

---

## 📊 **Visualization Parameters**

### **9. Chart Configuration Parameters**

| Parameter | Type | Default Value | Description |
|-----------|------|---------------|-------------|
| `fig_size` | tuple | (16, 12) | Figure dimensions for plots |
| `dpi` | int | 300 | Resolution for saved images |
| `style` | string | 'seaborn-v0_8' | Plot styling theme |
| `colormap` | string | 'RdYlBu_r' | Heatmap color scheme |

```python
# Visualization configuration
class CPUSimulatorVisualizer:
    def __init__(self):
        self.fig_size = (16, 12)    # Large figure for detail
        self.dpi = 300              # High resolution
        
    # Professional styling
    plt.style.use('seaborn-v0_8')
    sns.set_palette("husl")
```

---

## 🧪 **Configuration Test Matrix**

### **10. Standard Test Configurations**
These configurations are used throughout the project for consistent testing.

| Configuration Name | P-cores | E-cores | Use Case | Expected Performance |
|-------------------|---------|---------|----------|---------------------|
| **Performance Heavy** | 4 | 0 | Real-time AI processing | ~7 cycles, high energy |
| **Efficiency Heavy** | 0 | 4 | Maximum battery life | ~11 cycles, low energy |
| **Balanced** | 2 | 2 | **Optimal for EdTech** | ~8 cycles, balanced |
| **Efficiency Focus** | 1 | 3 | Extended battery usage | ~10 cycles, efficient |
| **Performance Focus** | 3 | 1 | Fast processing priority | ~8 cycles, fast |

```python
# Standard test matrix
TEST_CONFIGS = [
    ("Performance Heavy (4P + 0E)", 4, 0),
    ("Efficiency Heavy (0P + 4E)", 0, 4), 
    ("Balanced (2P + 2E)", 2, 2),
    ("Efficiency Focus (1P + 3E)", 1, 3),
    ("Performance Focus (3P + 1E)", 3, 1),
]
```

---

## 📈 **Parameter Impact Analysis**

### **11. Performance vs Energy Trade-offs**

#### **Speed Multiplier Impact**:
```python
# Sensitivity analysis on P-core speed
speed_values = [1.2, 1.5, 2.0, 2.5]
for speed in speed_values:
    sim = CPUSimulator(tasks, 2, 2, perf_speed=speed)
    # Higher speed = fewer cycles, more energy per cycle
```

#### **Threshold Sensitivity**:
```python
# Task distribution based on threshold
thresholds = [1, 2, 3, 5, 10]
for threshold in thresholds:
    sim = CPUSimulator(tasks, 2, 2, threshold=threshold)
    # Lower threshold = more tasks to P-cores = faster but more energy
```

#### **Core Count Scaling**:
```python
# Core count impact on performance
core_counts = [(1,1), (2,2), (4,4), (8,8)]
for p, e in core_counts:
    sim = CPUSimulator(tasks, p, e)
    # More cores = better parallelism = fewer cycles
```

---

## 🎯 **Parameter Selection Guidelines**

### **12. Choosing Optimal Parameters**

#### **For EdTech Applications**:
```python
# Recommended EdTech configuration
EDTECH_OPTIMAL = {
    'num_perf': 2,          # Balanced performance
    'num_eff': 2,           # Good battery life
    'perf_speed': 1.5,      # Realistic P-core advantage
    'perf_energy': 1.33,    # Realistic energy cost
    'eff_speed': 1.0,       # Baseline efficiency
    'eff_energy': 1.0,      # Baseline energy
    'threshold': 2          # Light tasks to E-cores
}
```

#### **For Battery-Critical Scenarios**:
```python
# Battery-optimized configuration
BATTERY_OPTIMIZED = {
    'num_perf': 1,          # Minimal P-cores
    'num_eff': 3,           # Maximize E-cores
    'threshold': 5          # Most tasks to E-cores
}
```

#### **For Performance-Critical Scenarios**:
```python
# Performance-optimized configuration  
PERFORMANCE_OPTIMIZED = {
    'num_perf': 4,          # Maximize P-cores
    'num_eff': 0,           # No E-cores
    'threshold': 1          # Most tasks to P-cores
}
```

---

## 🔧 **Parameter Validation**

### **13. Parameter Constraints and Validation**

#### **Core Count Constraints**:
```python
# Validation rules
assert num_perf >= 0 and num_eff >= 0
assert num_perf + num_eff > 0  # At least one core required
assert num_perf <= 16 and num_eff <= 16  # Reasonable upper bounds
```

#### **Performance Parameter Constraints**:
```python
# Realistic bounds based on hardware research
assert 0.5 <= perf_speed <= 4.0   # Reasonable speed range
assert 0.5 <= eff_speed <= 2.0    # E-cores shouldn't be too fast
assert 0.8 <= perf_energy <= 3.0  # Energy consumption bounds
assert 0.3 <= eff_energy <= 1.5   # E-cores are energy efficient
```

#### **Threshold Validation**:
```python
# Threshold should match task difficulty range
task_difficulties = [task[1] for task in tasks]
min_difficulty = min(task_difficulties)
max_difficulty = max(task_difficulties)
assert min_difficulty <= threshold <= max_difficulty
```

---

## 📊 **Parameter Impact Summary**

### **Key Parameter Effects**:

1. **`num_perf` ↑** → Fewer cycles, higher energy consumption
2. **`num_eff` ↑** → More cycles, lower energy consumption  
3. **`perf_speed` ↑** → Fewer cycles, higher energy efficiency
4. **`threshold` ↓** → More tasks to P-cores → faster, more energy
5. **`max_cycles` ↓** → Partial completion, battery constraint simulation

### **Optimization Targets**:
- **Minimize cycles**: High P-core count, low threshold
- **Minimize energy**: High E-core count, high threshold
- **Balance**: Equal P/E cores, moderate threshold (2-3)

The simulation parameters provide comprehensive control over the AI CPU simulation, enabling detailed analysis of performance vs energy trade-offs for EdTech applications.