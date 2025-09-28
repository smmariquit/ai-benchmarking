import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os

# Set style for better-looking plots
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

# Check if CSV files exist
csv_files = {
    'BFS': {
        'fababeir': 'fababeir_bfs_performance.csv',
        'mariquit': 'mariquit_bfs_performance.csv'
    },
    'DFS': {
        'fababeir': 'fababeir_dfs_performance.csv',
        'mariquit': 'mariquit_dfs_performance.csv'
    },
    'A* Manhattan': {
        'fababeir': 'fababeir_astar_manhattan_performance.csv',
        'mariquit': 'mariquit_astar_manhattan_performance.csv'
    },
    'A* Misplaced': {
        'fababeir': 'fababeir_astar_misplaced_performance.csv',
        'mariquit': 'mariquit_astar_misplaced_performance.csv'
    },
    'Minimax': {
        'fababeir': 'fababeir_minimax_performance.csv',
        'mariquit': 'mariquit_minimax_performance.csv'
    }
}

def load_and_clean_data(filename):
    """Load CSV and convert numeric columns from strings to floats"""
    if not os.path.exists(filename):
        print(f"Warning: {filename} not found!")
        return None
    
    df = pd.read_csv(filename)
    
    # Convert string values like "12.34" to float 12.34
    numeric_columns = [col for col in df.columns if col not in ['Case #']]
    for col in numeric_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    
    return df

def create_comparison_chart(algorithm_name, fababeir_file, mariquit_file):
    """Create side-by-side comparison chart for an algorithm"""
    
    # Load data
    fab_data = load_and_clean_data(fababeir_file)
    mar_data = load_and_clean_data(mariquit_file)
    
    if fab_data is None or mar_data is None:
        return None
    
    fig, axes = plt.subplots(1, 2, figsize=(15, 6))
    fig.suptitle(f'{algorithm_name} Performance Comparison', fontsize=16, fontweight='bold')
    
    # Prepare data for plotting (exclude Case # and Average columns)
    run_columns = [col for col in fab_data.columns if col.isdigit()]
    
    if algorithm_name == 'Minimax':
        # Minimax has only one test case
        fab_times = fab_data[run_columns].iloc[0].values
        mar_times = mar_data[run_columns].iloc[0].values
        
        # Bar chart comparing average performance
        avg_fab = np.mean(fab_times)
        avg_mar = np.mean(mar_times)
        
        algorithms = ['Fababeir', 'Mariquit']
        averages = [avg_fab, avg_mar]
        colors = ['#ff7f0e', '#2ca02c']
        
        bars = axes[0].bar(algorithms, averages, color=colors, alpha=0.7, edgecolor='black')
        axes[0].set_title('Average Performance')
        axes[0].set_ylabel('Time (ms)')
        axes[0].grid(True, alpha=0.3)
        
        # Add value labels on bars
        for bar, avg in zip(bars, averages):
            height = bar.get_height()
            axes[0].text(bar.get_x() + bar.get_width()/2., height + height*0.01,
                        f'{avg:.2f} ms', ha='center', va='bottom', fontweight='bold')
        
        # Box plot for distribution
        axes[1].boxplot([fab_times, mar_times], labels=algorithms, patch_artist=True,
                       boxprops=dict(facecolor='lightblue', alpha=0.7))
        axes[1].set_title('Performance Distribution')
        axes[1].set_ylabel('Time (ms)')
        axes[1].grid(True, alpha=0.3)
        
    else:
        # Multi-test case algorithms
        test_cases = fab_data['Case #'].values
        
        # Line plot showing performance across test cases
        fab_averages = fab_data['Average'].values
        mar_averages = mar_data['Average'].values
        
        x_pos = np.arange(len(test_cases))
        width = 0.35
        
        bars1 = axes[0].bar(x_pos - width/2, fab_averages, width, label='Fababeir', 
                           color='#ff7f0e', alpha=0.7, edgecolor='black')
        bars2 = axes[0].bar(x_pos + width/2, mar_averages, width, label='Mariquit', 
                           color='#2ca02c', alpha=0.7, edgecolor='black')
        
        axes[0].set_title('Average Performance by Test Case')
        axes[0].set_xlabel('Test Case')
        axes[0].set_ylabel('Time (ms)')
        axes[0].set_xticks(x_pos)
        axes[0].set_xticklabels([f'Case {int(tc)}' for tc in test_cases])
        axes[0].legend()
        axes[0].grid(True, alpha=0.3)
        
        # Add value labels on bars
        for bars in [bars1, bars2]:
            for bar in bars:
                height = bar.get_height()
                axes[0].text(bar.get_x() + bar.get_width()/2., height + height*0.01,
                            f'{height:.1f}', ha='center', va='bottom', fontsize=8)
        
        # Performance ratio chart
        ratios = fab_averages / mar_averages
        colors = ['red' if r > 1 else 'green' for r in ratios]
        
        bars = axes[1].bar(x_pos, ratios, color=colors, alpha=0.7, edgecolor='black')
        axes[1].axhline(y=1, color='black', linestyle='--', alpha=0.5)
        axes[1].set_title('Fababeir/Mariquit Speed Ratio')
        axes[1].set_xlabel('Test Case')
        axes[1].set_ylabel('Ratio (>1 = Fababeir slower)')
        axes[1].set_xticks(x_pos)
        axes[1].set_xticklabels([f'Case {int(tc)}' for tc in test_cases])
        axes[1].grid(True, alpha=0.3)
        
        # Add ratio labels
        for bar, ratio in zip(bars, ratios):
            height = bar.get_height()
            axes[1].text(bar.get_x() + bar.get_width()/2., height + 0.02,
                        f'{ratio:.2f}x', ha='center', va='bottom', fontweight='bold')
    
    plt.tight_layout()
    return fig

def create_overall_summary():
    """Create an overall summary chart"""
    
    # Collect average performance data
    summary_data = []
    
    for alg_name, files in csv_files.items():
        fab_data = load_and_clean_data(files['fababeir'])
        mar_data = load_and_clean_data(files['mariquit'])
        
        if fab_data is not None and mar_data is not None:
            if alg_name == 'Minimax':
                # Single test case
                run_columns = [col for col in fab_data.columns if col.isdigit()]
                fab_avg = fab_data[run_columns].iloc[0].mean()
                mar_avg = mar_data[run_columns].iloc[0].mean()
            else:
                # Multiple test cases - take overall average
                fab_avg = fab_data['Average'].mean()
                mar_avg = mar_data['Average'].mean()
            
            summary_data.append({
                'Algorithm': alg_name,
                'Fababeir': fab_avg,
                'Mariquit': mar_avg,
                'Ratio': fab_avg / mar_avg
            })
    
    if not summary_data:
        print("No data available for summary chart")
        return None
    
    df_summary = pd.DataFrame(summary_data)
    
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    fig.suptitle('Algorithm Performance Summary', fontsize=16, fontweight='bold')
    
    # Grouped bar chart
    x_pos = np.arange(len(df_summary))
    width = 0.35
    
    bars1 = axes[0].bar(x_pos - width/2, df_summary['Fababeir'], width, 
                       label='Fababeir', color='#ff7f0e', alpha=0.7, edgecolor='black')
    bars2 = axes[0].bar(x_pos + width/2, df_summary['Mariquit'], width, 
                       label='Mariquit', color='#2ca02c', alpha=0.7, edgecolor='black')
    
    axes[0].set_title('Average Performance by Algorithm')
    axes[0].set_xlabel('Algorithm')
    axes[0].set_ylabel('Time (ms)')
    axes[0].set_xticks(x_pos)
    axes[0].set_xticklabels(df_summary['Algorithm'], rotation=45)
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)
    
    # Speed ratio chart
    colors = ['red' if r > 1 else 'green' for r in df_summary['Ratio']]
    bars = axes[1].bar(x_pos, df_summary['Ratio'], color=colors, alpha=0.7, edgecolor='black')
    axes[1].axhline(y=1, color='black', linestyle='--', alpha=0.5)
    axes[1].set_title('Fababeir/Mariquit Speed Ratio')
    axes[1].set_xlabel('Algorithm')
    axes[1].set_ylabel('Ratio (>1 = Fababeir slower)')
    axes[1].set_xticks(x_pos)
    axes[1].set_xticklabels(df_summary['Algorithm'], rotation=45)
    axes[1].grid(True, alpha=0.3)
    
    # Add ratio labels
    for bar, ratio in zip(bars, df_summary['Ratio']):
        height = bar.get_height()
        axes[1].text(bar.get_x() + bar.get_width()/2., height + 0.02,
                    f'{ratio:.2f}x', ha='center', va='bottom', fontweight='bold')
    
    plt.tight_layout()
    return fig

def main():
    """Generate all benchmark visualizations"""
    print("🎨 Generating Benchmark Visualizations...")
    print("=" * 50)
    
    # Create individual algorithm comparisons
    figures = []
    for alg_name, files in csv_files.items():
        print(f"Creating {alg_name} comparison chart...")
        fig = create_comparison_chart(alg_name, files['fababeir'], files['mariquit'])
        if fig:
            figures.append((alg_name, fig))
            # Save individual charts
            filename = f"{alg_name.lower().replace(' ', '_').replace('*', 'star')}_comparison.png"
            fig.savefig(filename, dpi=300, bbox_inches='tight')
            print(f"  ✅ Saved: {filename}")
    
    # Create overall summary
    print("Creating overall summary chart...")
    summary_fig = create_overall_summary()
    if summary_fig:
        summary_fig.savefig('benchmark_summary.png', dpi=300, bbox_inches='tight')
        print("  ✅ Saved: benchmark_summary.png")
    
    print("\n🎯 Visualization Summary:")
    print(f"  • Generated {len(figures)} algorithm comparison charts")
    print(f"  • Generated 1 overall summary chart")
    print(f"  • All charts saved as high-resolution PNG files")
    
    # Show all plots
    print("\n📊 Displaying charts...")
    plt.show()

if __name__ == "__main__":
    main()