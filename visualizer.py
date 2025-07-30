#!/usr/bin/env python3
# visualizer.py - Professional visualizations for CPU simulator results

import matplotlib.pyplot as plt
import numpy as np
from ai_workloads import run_ai_workload_comparison, AIWorkloadProfiler
from core_simulator import CPUSimulator
from cycle_analysis import CycleControlledSimulator
import seaborn as sns

# Set professional styling
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

class CPUSimulatorVisualizer:
    """Professional visualization suite for CPU simulator results"""
    
    def __init__(self):
        self.fig_size = (12, 8)
        self.dpi = 300
        
    def plot_cycles_vs_energy(self, results=None, save_path=None):
        """Create comprehensive cycles vs energy analysis plots"""
        
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
