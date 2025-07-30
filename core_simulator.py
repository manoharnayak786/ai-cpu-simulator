# core_simulator.py

class Task:
    def __init__(self, name, difficulty):
        self.name = name
        self.difficulty = difficulty
        self.remaining = difficulty  # work left to do

    def __repr__(self):
        return f"{self.name}(Diff:{self.difficulty}, Rem:{self.remaining})"


class Core:
    def __init__(self, name, core_type, speed_multiplier, energy_multiplier):
        self.name = name
        self.core_type = core_type  # "P" or "E"
        self.speed = speed_multiplier
        self.energy_multiplier = energy_multiplier
        self.task = None
        self.energy_used = 0.0

    def assign_task(self, task):
        self.task = task

    def is_idle(self):
        return self.task is None

    def process(self):
        if self.task:
            work_done = min(self.task.remaining, self.speed)
            self.task.remaining -= work_done
            self.energy_used += work_done * self.energy_multiplier
            if self.task.remaining <= 0:
                finished_task = self.task
                self.task = None
                return finished_task
        return None

    def __repr__(self):
        return f"{self.name}-{self.core_type} [{self.task}]"


class CPUSimulator:
    def __init__(self, tasks, num_perf, num_eff,
                 perf_speed=1.5, perf_energy=1.33,
                 eff_speed=1.0, eff_energy=1.0,
                 threshold=2):
        self.tasks = [Task(name, diff) for name, diff in tasks]
        self.threshold = threshold
        self.cycle = 0
        self.total_energy = 0.0
        self.perf_cores = [Core(f"P{i+1}", "P", perf_speed, perf_energy) for i in range(num_perf)]
        self.eff_cores = [Core(f"E{i+1}", "E", eff_speed, eff_energy) for i in range(num_eff)]
        self.wait_queue_perf = []
        self.wait_queue_eff = []
        self.completed_tasks = []

    def assign_tasks(self):
        for task in self.tasks:
            if task.difficulty > self.threshold:
                self.wait_queue_perf.append(task)
            else:
                self.wait_queue_eff.append(task)
        # Don't clear self.tasks - keep original list for reference

    def assign_to_cores(self):
        # Assign tasks to preferred core types first
        for core in self.perf_cores:
            if core.is_idle() and self.wait_queue_perf:
                core.assign_task(self.wait_queue_perf.pop(0))
        for core in self.eff_cores:
            if core.is_idle() and self.wait_queue_eff:
                core.assign_task(self.wait_queue_eff.pop(0))
        
        # Fallback: If no efficiency cores exist, performance cores handle light tasks
        if not self.eff_cores and self.wait_queue_eff:
            for core in self.perf_cores:
                if core.is_idle() and self.wait_queue_eff:
                    core.assign_task(self.wait_queue_eff.pop(0))
        
        # Fallback: If no performance cores exist, efficiency cores handle heavy tasks  
        if not self.perf_cores and self.wait_queue_perf:
            for core in self.eff_cores:
                if core.is_idle() and self.wait_queue_perf:
                    core.assign_task(self.wait_queue_perf.pop(0))
        


    def run_cycle(self):
        self.cycle += 1
        for core in self.perf_cores + self.eff_cores:
            completed = core.process()
            if completed:
                self.completed_tasks.append(completed)

    def run_simulation(self):
        self.assign_tasks()
        print(f"\nStarting Simulation...\n")
        total_tasks = len(self.wait_queue_perf) + len(self.wait_queue_eff)

        while len(self.completed_tasks) < total_tasks:
            print(f"Cycle {self.cycle + 1}")
            self.assign_to_cores()
            self.run_cycle()
            self.print_core_status()
            # Check if all tasks are completed after this cycle
            if len(self.completed_tasks) >= total_tasks:
                break
        # Calculate total energy from all cores
        self.total_energy = sum(core.energy_used for core in self.perf_cores + self.eff_cores)

    def print_core_status(self):
        for core in self.perf_cores + self.eff_cores:
            print(f"  {core}")
        print()


if __name__ == "__main__":
    tasks = [
        ("TranscribeDebate", 5),
        ("RenderQuiz", 2),
        ("EvaluateEssay", 3),
        ("GenerateFeedback", 4),
        ("MapGraph", 1),
        ("AudioSummary", 4),
        ("SpeechToText", 5)
    ]

    sim = CPUSimulator(
        tasks=tasks,
        num_perf=2,
        num_eff=2,
        perf_speed=1.5,
        perf_energy=1.33,
        eff_speed=1.0,
        eff_energy=1.0,
        threshold=2
    )

    sim.run_simulation()
    print(f"Total CPU Cycles: {sim.cycle}")
    print(f"Total Energy Used: {sim.total_energy:.2f}")
