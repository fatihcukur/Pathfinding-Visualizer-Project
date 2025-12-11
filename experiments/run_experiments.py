import time
import random
import csv
import heapq
from collections import deque

# --- ALGORİTMA MANTIKLARI (Görselsiz) ---

def heuristic(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

def get_neighbors(node, grid_size, barriers):
    r, c = node
    neighbors = []
    # Aşağı, Yukarı, Sağ, Sol
    directions = [(r+1, c), (r-1, c), (r, c+1), (r, c-1)]
    for nr, nc in directions:
        if 0 <= nr < grid_size and 0 <= nc < grid_size:
            if (nr, nc) not in barriers:
                neighbors.append((nr, nc))
    return neighbors

def run_astar(grid_size, start, end, barriers):
    count = 0
    open_set = []
    heapq.heappush(open_set, (0, count, start))
    came_from = {}
    
    g_score = {start: 0}
    f_score = {start: heuristic(start, end)}
    open_set_hash = {start}
    
    visited_count = 0

    while open_set:
        current = heapq.heappop(open_set)[2]
        open_set_hash.remove(current)
        visited_count += 1

        if current == end:
            return True, visited_count

        for neighbor in get_neighbors(current, grid_size, barriers):
            temp_g = g_score[current] + 1
            if temp_g < g_score.get(neighbor, float('inf')):
                came_from[neighbor] = current
                g_score[neighbor] = temp_g
                f_score[neighbor] = temp_g + heuristic(neighbor, end)
                if neighbor not in open_set_hash:
                    count += 1
                    heapq.heappush(open_set, (f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
    return False, visited_count

def run_dijkstra(grid_size, start, end, barriers):
    count = 0
    open_set = []
    heapq.heappush(open_set, (0, count, start))
    dist = {start: 0}
    visited_count = 0
    open_set_hash = {start}

    while open_set:
        current = heapq.heappop(open_set)[2]
        open_set_hash.remove(current)
        visited_count += 1

        if current == end:
            return True, visited_count

        for neighbor in get_neighbors(current, grid_size, barriers):
            if dist[current] + 1 < dist.get(neighbor, float('inf')):
                dist[neighbor] = dist[current] + 1
                count += 1
                if neighbor not in open_set_hash:
                    heapq.heappush(open_set, (dist[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
    return False, visited_count

def run_bfs(grid_size, start, end, barriers):
    q = deque([start])
    visited = {start}
    visited_count = 0

    while q:
        current = q.popleft()
        visited_count += 1
        
        if current == end:
            return True, visited_count
        
        for neighbor in get_neighbors(current, grid_size, barriers):
            if neighbor not in visited:
                visited.add(neighbor)
                q.append(neighbor)
    return False, visited_count

# --- DENEY KURULUMU ---

def generate_random_barriers(grid_size, probability=0.2):
    barriers = set()
    for r in range(grid_size):
        for c in range(grid_size):
            if random.random() < probability:
                barriers.add((r, c))
    return barriers

def main():
    sizes = [20, 50, 100] # Farklı grid boyutları
    trials = 10 # Her boyut için kaç deneme yapılsın
    filename = "results.csv"
    
    print("Deneyler basliyor... (Bu islem biraz surebilir)")

    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["algo", "n", "trial", "time_ms", "visited_nodes"])

        for n in sizes:
            print(f"Grid boyutu test ediliyor: {n}x{n}")
            for t in range(trials):
                start = (0, 0)
                end = (n-1, n-1)
                barriers = generate_random_barriers(n)
                
                # Start ve End bariyer olmasın
                if start in barriers: barriers.remove(start)
                if end in barriers: barriers.remove(end)

                # A*
                st = time.time()
                run_astar(n, start, end, barriers)
                et = time.time()
                writer.writerow(["A*", n, t, (et-st)*1000, 0]) 
                
                # Dijkstra
                st = time.time()
                run_dijkstra(n, start, end, barriers)
                et = time.time()
                writer.writerow(["Dijkstra", n, t, (et-st)*1000, 0])

                # BFS
                st = time.time()
                run_bfs(n, start, end, barriers)
                et = time.time()
                writer.writerow(["BFS", n, t, (et-st)*1000, 0])
    
    print(f"Deney tamamlandi! Sonuclar '{filename}' dosyasina kaydedildi.")

if __name__ == "__main__":
    main()