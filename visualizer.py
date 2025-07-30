#!/usr/bin/env python3
# visualizer.py - Professional visualizations for CPU simulator results

try:
    import matplotlib
    matplotlib.use('Agg')  # Use non-interactive backend for file generation
    import matplotlib.pyplot as plt
    import numpy as np
    import seaborn as sns
    
    # Set professional styling with fallback
    try:
        plt.style.use('seaborn-v0_8')
    except OSError:
        try:
            plt.style.use('seaborn')
        except OSError:
            # Use default matplotlib style if seaborn styles are not available
            plt.style.use('default')
    
    try:
        sns.set_palette("husl")
    except NameError:
        pass  # seaborn not available, skip palette setting
    
    VISUALIZATION_AVAILABLE = True
except ImportError as e:
    print(f"📊 Visualization dependencies not available: {e}")
    print("📦 To enable visualizations, install: pip install matplotlib seaborn numpy")
    VISUALIZATION_AVAILABLE = False
    
    # Create dummy classes to prevent import errors
    class plt:
        @staticmethod
        def subplots(*args, **kwargs):
            return None, None
        @staticmethod
        def show():
            pass
        @staticmethod
        def savefig(*args, **kwargs):
            pass
        @staticmethod
        def tight_layout():
            pass
        @staticmethod
        def colorbar(*args, **kwargs):
            pass
        class cm:
            @staticmethod
            def Set3(x):
                return [[0.1, 0.2, 0.3]] * len(x) if hasattr(x, '__len__') else [0.1, 0.2, 0.3]
    
    class np:
        @staticmethod
        def linspace(start, stop, num):
            return [start + i * (stop - start) / (num - 1) for i in range(num)]
        @staticmethod
        def mean(x):
            return sum(x) / len(x) if x else 0
        @staticmethod
        def zeros(shape):
            if isinstance(shape, tuple):
                return [[0] * shape[1] for _ in range(shape[0])]
            return [0] * shape

from ai_workloads import run_ai_workload_comparison, AIWorkloadProfiler
from core_simulator import CPUSimulator
from cycle_analysis import CycleControlledSimulator

class CPUSimulatorVisualizer:
    """Professional visualization suite for CPU simulator results"""
    
    def __init__(self):
        self.fig_size = (12, 8)
        self.dpi = 300
        
    def plot_cycles_vs_energy(self, results=None, save_path=None):
        """Create comprehensive cycles vs energy analysis plots"""
        
        if not VISUALIZATION_AVAILABLE:
            print("❌ Visualization not available - missing matplotlib/seaborn dependencies")
            print("📊 Results summary instead:")
            if results is None:
                results = run_ai_workload_comparison()
            self._print_text_summary(results)
            return None
        
        if results is None:
            print("🔄 Generating AI workload data...")
            results = run_ai_workload_comparison()
        
        # Create subplot layout
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12), dpi=self.dpi)
        fig.suptitle('🖥️ AI CPU Simulator: Cycles vs Energy Analysis', fontsize=16, fontweight='bold')
        
        # 1. Scatter plot: Cycles vs Energy by Configuration
        configs = list(set([r['config'] for r in results]))
        colors = plt.cm.Set3(np.linspace(0, 1, len(configs)))
        
        for i, config in enumerate(configs):
            config_data = [r for r in results if r['config'] == config]
            cycles = [r['cycles'] for r in config_data]
            energy = [r['energy'] for r in config_data]
            
            ax1.scatter(cycles, energy, c=[colors[i]], label=config, s=100, alpha=0.7, edgecolors='black')
        
        ax1.set_xlabel('CPU Cycles', fontweight='bold')
        ax1.set_ylabel('Energy Consumption', fontweight='bold')
        ax1.set_title('⚡ Performance vs Energy Trade-off', fontweight='bold')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # 2. Bar chart: Energy efficiency by scenario
        scenarios = list(set([r['scenario'] for r in results]))
        scenario_efficiency = {}
        
        for scenario in scenarios:
            scenario_data = [r for r in results if r['scenario'] == scenario]
            avg_efficiency = np.mean([r['efficiency'] for r in scenario_data])
            scenario_efficiency[scenario] = avg_efficiency
        
        bars = ax2.bar(range(len(scenarios)), list(scenario_efficiency.values()), 
                      color=['#FF6B6B', '#4ECDC4', '#45B7D1'], alpha=0.8)
        ax2.set_xlabel('AI Workload Scenarios', fontweight='bold')
        ax2.set_ylabel('Energy Efficiency (Energy/Cycle)', fontweight='bold')
        ax2.set_title('🔋 Energy Efficiency by Workload', fontweight='bold')
        ax2.set_xticks(range(len(scenarios)))
        ax2.set_xticklabels([s.replace(' ', '\n') for s in scenarios], rotation=0)
        
        # Add value labels on bars
        for bar, value in zip(bars, scenario_efficiency.values()):
            ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
                    f'{value:.2f}', ha='center', va='bottom', fontweight='bold')
        
        # 3. Line plot: Scalability analysis
        self._plot_scalability_analysis(ax3)
        
        # 4. Heatmap: Configuration performance matrix
        self._plot_performance_heatmap(ax4, results)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=self.dpi, bbox_inches='tight')
            print(f"📊 Visualization saved to: {save_path}")
        
        plt.show()
        return fig
    
    def _plot_scalability_analysis(self, ax):
        """Plot scalability analysis for different workload sizes"""
        
        workload_sizes = [10, 25, 50, 100, 200]
        configs = [("2P+2E", 2, 2), ("4P+0E", 4, 0), ("0P+4E", 0, 4)]
        
        for config_name, p_cores, e_cores in configs:
            cycles_data = []
            energy_data = []
            
            for size in workload_sizes:
                # Generate test workload
                tasks = [(f"Task{i}", (i % 5) + 3) for i in range(size)]
                sim = CPUSimulator(tasks, p_cores, e_cores)
                sim.run_simulation()
                
                cycles_data.append(sim.cycle)
                energy_data.append(sim.total_energy)
            
            # Plot both cycles and energy (normalized)
            ax_twin = ax.twinx()
            
            line1 = ax.plot(workload_sizes, cycles_data, marker='o', linewidth=2, 
                           label=f'{config_name} (Cycles)', alpha=0.8)
            line2 = ax_twin.plot(workload_sizes, energy_data, marker='s', linewidth=2, 
                                linestyle='--', label=f'{config_name} (Energy)', alpha=0.8)
        
        ax.set_xlabel('Number of Tasks', fontweight='bold')
        ax.set_ylabel('CPU Cycles', fontweight='bold', color='blue')
        ax_twin.set_ylabel('Energy Consumption', fontweight='bold', color='red')
        ax.set_title('📈 Scalability Analysis', fontweight='bold')
        ax.grid(True, alpha=0.3)
        
        # Combine legends
        lines1, labels1 = ax.get_legend_handles_labels()
        lines2, labels2 = ax_twin.get_legend_handles_labels()
        ax.legend(lines1 + lines2, labels1 + labels2, loc='upper left')
    
    def _plot_performance_heatmap(self, ax, results):
        """Plot performance heatmap for different configurations"""
        
        # Create performance matrix
        configs = list(set([r['config'] for r in results]))
        scenarios = list(set([r['scenario'] for r in results]))
        
        # Create matrix for cycles
        matrix = np.zeros((len(scenarios), len(configs)))
        
        for i, scenario in enumerate(scenarios):
            for j, config in enumerate(configs):
                scenario_result = [r for r in results if r['scenario'] == scenario and r['config'] == config]
                if scenario_result:
                    matrix[i, j] = scenario_result[0]['cycles']
        
        # Create heatmap
        im = ax.imshow(matrix, cmap='RdYlBu_r', aspect='auto')
        
        # Set labels
        ax.set_xticks(range(len(configs)))
        ax.set_yticks(range(len(scenarios)))
        ax.set_xticklabels([c.replace(' ', '\n') for c in configs], rotation=45, ha='right')
        ax.set_yticklabels([s.replace(' ', '\n') for s in scenarios])
        
        # Add values to heatmap
        for i in range(len(scenarios)):
            for j in range(len(configs)):
                text = ax.text(j, i, f'{int(matrix[i, j])}', 
                             ha="center", va="center", color="white", fontweight='bold')
        
        ax.set_title('🗺️ Performance Heatmap (Cycles)', fontweight='bold')
        
        # Add colorbar
        plt.colorbar(im, ax=ax, label='CPU Cycles')

    def _print_text_summary(self, results):
        """Print text-based summary when visualization is not available"""
        print("\n" + "="*60)
        print("📊 CPU SIMULATOR ANALYSIS SUMMARY")
        print("="*60)
        
        # Group by scenario
        scenarios = list(set([r['scenario'] for r in results]))
        for scenario in scenarios:
            print(f"\n🎯 {scenario}:")
            scenario_data = [r for r in results if r['scenario'] == scenario]
            for result in scenario_data:
                print(f"   {result['config']}: {result['cycles']} cycles, {result['energy']:.1f} energy")

def main():
    """Run comprehensive visualization suite"""
    
    print("🎨 Starting CPU Simulator Visualization Suite...")
    print("=" * 60)
    
    # Initialize visualizer
    viz = CPUSimulatorVisualizer()
    
    # Create visualizations
    print("\n📊 Creating Cycles vs Energy Analysis...")
    viz.plot_cycles_vs_energy(save_path="cycles_vs_energy_analysis.png")
    
    print("\n✅ Visualization Complete!")
    print("📁 Saved files:")
    print("  - cycles_vs_energy_analysis.png")

if __name__ == "__main__":
    main()
