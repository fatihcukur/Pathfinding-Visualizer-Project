import pandas as pd
import matplotlib.pyplot as plt

def main():
    try:
        # Read file CSV 
        df = pd.read_csv("results.csv")
        
        # Calculate the average time based on the grid size (n) and the algorithm
        avg_times = df.groupby(['algo', 'n'])['time_ms'].mean().unstack(level=0)

        # Draw the graph
        plt.figure(figsize=(10, 6))
        
        for algo in avg_times.columns:
            plt.plot(avg_times.index, avg_times[algo], marker='o', label=algo)
        
        plt.title("Algorithm Runtime Comparison")
        plt.xlabel("Grid Size (NxN)")
        plt.ylabel("Time (ms)")
        plt.legend()
        plt.grid(True)
        
        # Save the image (into the plots folder in the parent directory)
        plt.savefig("../plots/runtime_comparison.png")
        print("The graph was saved as 'plots/runtime_comparison.png'")
        plt.show()

    except FileNotFoundError:
        print("ERROR: 'results.csv' has not found. Firstly run_experiments.py should be run.")

if __name__ == "__main__":

    main()
