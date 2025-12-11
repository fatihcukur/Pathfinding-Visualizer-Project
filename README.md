# Pathfinding Algorithm Visualizer

## Project Overview
This project visualizes and compares pathfinding algorithms (A*, Dijkstra, BFS) in Python using Pygame. It allows users to create barriers, generate maps, and analyze algorithm performance in real-time.

## Directory Structure
- `src/`: Contains the main source code (`main.py`).
- `experiments/`: Scripts for empirical analysis and CSV generation.
- `plots/`: Generated performance graphs.
- `data/`: Map data files (if applicable).

## Installation & Dependencies
Ensure Python 3.x is installed. Install dependencies:
```Bash
pip install pygame matplotlib pandas

## How to Run
- 1.Visualizer: To run the main application with the GUI:
```Bash
python src/main.py

*Controls:* Left Click to Draw Nodes, Right Click to Erase, Space Bar to Start.
*Panel:* Use the right-side panel to select algorithms (A*, Dijkstra, BFS) and load maps.

- 2.Experiments: To reproduce the empirical results and generate CSV files:
```Bash
cd experiments
python run_experiments.py
This will create a results.csv file.

- 3.Plotting: To generate the performance comparison graph from the results:
```Bash
cd experiments
python plot_results.py
The graph will be saved in the plots/ directory.

## Algorithms Implemented
- *A (A-Star):** Uses Manhattan distance heuristic. Fastest for pathfinding.
- *Dijkstra:* Guarantees shortest path, explores evenly.
- *BFS (Breadth-First Search):* Unweighted shortest path guarantee.

## *Demo Video Link:* https://youtu.be/4_cxe2um6Ec 