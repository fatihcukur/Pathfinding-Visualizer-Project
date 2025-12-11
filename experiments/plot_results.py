import pandas as pd
import matplotlib.pyplot as plt

def main():
    try:
        # CSV dosyasını oku
        df = pd.read_csv("results.csv")
        
        # Grid boyutuna (n) ve Algoritmaya göre ortalama süreyi al
        avg_times = df.groupby(['algo', 'n'])['time_ms'].mean().unstack(level=0)

        # Grafiği çiz
        plt.figure(figsize=(10, 6))
        
        for algo in avg_times.columns:
            plt.plot(avg_times.index, avg_times[algo], marker='o', label=algo)
        
        plt.title("Algorithm Runtime Comparison")
        plt.xlabel("Grid Size (NxN)")
        plt.ylabel("Time (ms)")
        plt.legend()
        plt.grid(True)
        
        # Resmi kaydet (Bir üst klasördeki plots içine)
        plt.savefig("../plots/runtime_comparison.png")
        print("Grafik 'plots/runtime_comparison.png' olarak kaydedildi.")
        plt.show()

    except FileNotFoundError:
        print("HATA: 'results.csv' bulunamadi. Önce run_experiments.py calistirilmali.")

if __name__ == "__main__":
    main()