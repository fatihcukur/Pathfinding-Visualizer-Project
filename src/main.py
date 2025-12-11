import pygame
import math
from queue import PriorityQueue, Queue
import time

# --- SETTINGS & COLORS ---
WIDTH = 1000  # Window Width (800 Grid + 200 Panel)
HEIGHT = 800  # Window Height
GRID_WIDTH = 800
ROWS = 50     # 50x50 Grid

# Colors (RGB)
RED = (255, 0, 0)         # Closed Nodes
GREEN = (0, 255, 0)       # Open Nodes
WHITE = (255, 255, 255)   # Empty
BLACK = (0, 0, 0)         # Barrier/Wall
PURPLE = (128, 0, 128)    # End Node
ORANGE = (255, 165, 0)    # Start Node
GREY = (128, 128, 128)    # Grid Lines
TURQUOISE = (64, 224, 208) # Path
PANEL_COLOR = (40, 40, 40) # Right Panel Background
TEXT_COLOR = (255, 255, 255)

# Initialize Pygame
pygame.init()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pathfinding Algorithm Visualizer")
FONT = pygame.font.SysFont('arial', 16)
HEADER_FONT = pygame.font.SysFont('arial', 20, bold=True)

# --- NODE CLASS ---
class Node:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        # X is horizontal (Column * Width)
        # Y is vertical (Row * Width)
        self.x = col * width
        self.y = row * width
        self.color = WHITE
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows

    def get_pos(self):
        return self.row, self.col

    def is_closed(self):
        return self.color == RED

    def is_open(self):
        return self.color == GREEN

    def is_barrier(self):
        return self.color == BLACK

    def is_start(self):
        return self.color == ORANGE

    def is_end(self):
        return self.color == PURPLE

    def reset(self):
        self.color = WHITE

    def make_start(self):
        self.color = ORANGE

    def make_closed(self):
        self.color = RED

    def make_open(self):
        self.color = GREEN

    def make_barrier(self):
        self.color = BLACK

    def make_end(self):
        self.color = PURPLE

    def make_path(self):
        self.color = TURQUOISE

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid):
        self.neighbors = []
        # DOWN
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier():
            self.neighbors.append(grid[self.row + 1][self.col])
        # UP
        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():
            self.neighbors.append(grid[self.row - 1][self.col])
        # RIGHT
        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier():
            self.neighbors.append(grid[self.row][self.col + 1])
        # LEFT
        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():
            self.neighbors.append(grid[self.row][self.col - 1])

    def __lt__(self, other):
        return False

# --- ALGORITHMS ---

def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)

def reconstruct_path(came_from, current, draw):
    path_len = 0
    while current in came_from:
        current = came_from[current]
        current.make_path()
        path_len += 1
        draw()
    return path_len

def algorithm_astar(draw, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g_score = {spot: float("inf") for row in grid for spot in row}
    g_score[start] = 0
    f_score = {spot: float("inf") for row in grid for spot in row}
    f_score[start] = h(start.get_pos(), end.get_pos())
    
    open_set_hash = {start}
    visited_nodes = 0

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            path_len = reconstruct_path(came_from, end, draw)
            end.make_end()
            return True, visited_nodes, path_len

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1
            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()
                    visited_nodes += 1
        
        draw()

        if current != start:
            current.make_closed()
    return False, visited_nodes, 0

def algorithm_dijkstra(draw, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    dist = {spot: float("inf") for row in grid for spot in row}
    dist[start] = 0
    
    open_set_hash = {start}
    visited_nodes = 0

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            path_len = reconstruct_path(came_from, end, draw)
            end.make_end()
            return True, visited_nodes, path_len

        for neighbor in current.neighbors:
            if dist[current] + 1 < dist[neighbor]:
                dist[neighbor] = dist[current] + 1
                came_from[neighbor] = current
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((dist[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()
                    visited_nodes += 1
        
        draw()

        if current != start:
            current.make_closed()
    return False, visited_nodes, 0

def algorithm_bfs(draw, grid, start, end):
    q = Queue()
    q.put(start)
    came_from = {}
    visited = {start}
    visited_nodes = 0

    while not q.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        
        current = q.get()

        if current == end:
            path_len = reconstruct_path(came_from, end, draw)
            end.make_end()
            return True, visited_nodes, path_len

        for neighbor in current.neighbors:
            if neighbor not in visited:
                came_from[neighbor] = current
                visited.add(neighbor)
                q.put(neighbor)
                neighbor.make_open()
                visited_nodes += 1
        
        draw()
        if current != start:
            current.make_closed()
            
    return False, visited_nodes, 0

# --- GRID & DRAW FUNCTIONS ---

def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(i, j, gap, rows)
            grid[i].append(node)
    return grid

def draw_grid_lines(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))

def draw_panel(win, stats, selected_algo):
    pygame.draw.rect(win, PANEL_COLOR, (GRID_WIDTH, 0, WIDTH - GRID_WIDTH, HEIGHT))
    
    # Header
    title = HEADER_FONT.render("CONTROLS", 1, WHITE)
    win.blit(title, (GRID_WIDTH + 45, 20))

    # Button helper
    def draw_button(y, text, color=(100, 100, 100)):
        pygame.draw.rect(win, color, (GRID_WIDTH + 20, y, 160, 40))
        label = FONT.render(text, 1, WHITE)
        # Center text roughly
        text_rect = label.get_rect(center=(GRID_WIDTH + 20 + 80, y + 20))
        win.blit(label, text_rect)
        return pygame.Rect(GRID_WIDTH + 20, y, 160, 40)

    # Algo Buttons
    btn_astar = draw_button(70, "A* Algorithm", (0, 150, 0) if selected_algo == 'A*' else (100,100,100))
    btn_dijkstra = draw_button(120, "Dijkstra", (0, 150, 0) if selected_algo == 'Dijkstra' else (100,100,100))
    btn_bfs = draw_button(170, "BFS", (0, 150, 0) if selected_algo == 'BFS' else (100,100,100))
    
    # Map Buttons
    btn_map1 = draw_button(250, "Map 1 (Maze)")
    btn_map2 = draw_button(300, "Map 2 (Spiral)")
    btn_reset = draw_button(350, "Reset Grid", RED)

    # Start Button
    btn_start = draw_button(430, "START (SPACE)", ORANGE)

    # Metrics
    pygame.draw.line(win, WHITE, (GRID_WIDTH + 10, 500), (WIDTH - 10, 500))
    stats_title = HEADER_FONT.render("METRICS", 1, WHITE)
    win.blit(stats_title, (GRID_WIDTH + 50, 510))

    time_txt = FONT.render(f"Time: {stats['time']:.4f} s", 1, WHITE)
    node_txt = FONT.render(f"Visited: {stats['visited']}", 1, WHITE)
    path_txt = FONT.render(f"Path Len: {stats['path']}", 1, WHITE)

    win.blit(time_txt, (GRID_WIDTH + 20, 550))
    win.blit(node_txt, (GRID_WIDTH + 20, 580))
    win.blit(path_txt, (GRID_WIDTH + 20, 610))

    return {
        "A*": btn_astar, "Dijkstra": btn_dijkstra, 
        "BFS": btn_bfs,
        "Map1": btn_map1, "Map2": btn_map2, 
        "Reset": btn_reset, "Start": btn_start
    }

def draw(win, grid, rows, width, stats, selected_algo):
    for row in grid:
        for node in row:
            node.draw(win)
    draw_grid_lines(win, rows, width)
    buttons = draw_panel(win, stats, selected_algo)
    pygame.display.update()
    return buttons

# --- PRE-MADE MAPS ---
def generate_map_1(grid): # Simple Maze
    for i in range(0, 50):
        if i % 2 == 1:
            for j in range(5, 45):
                grid[i][j].make_barrier()

def generate_map_2(grid): # Spiral
    for i in range(5, 45):
        grid[10][i].make_barrier() # Top
        grid[40][i].make_barrier() # Bottom
    for i in range(10, 41):
        grid[i][5].make_barrier()  # Left
        grid[i][45].make_barrier() # Right
    for i in range(15, 35):
        grid[20][i].make_barrier()
    
# --- MAIN LOOP ---
def main(win, width):
    grid = make_grid(ROWS, GRID_WIDTH)
    start = None
    end = None
    run = True
    started = False
    
    current_algo = "A*"
    stats = {"time": 0, "visited": 0, "path": 0}

    while run:
        buttons = draw(win, grid, ROWS, GRID_WIDTH, stats, current_algo)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            # MOUSE CLICKS
            if pygame.mouse.get_pressed()[0]: # Left Click
                pos = pygame.mouse.get_pos()
                
                # Check if click is within Grid
                if pos[0] < GRID_WIDTH:
                    if started: continue 
                    
                    # --- FIXED LOGIC HERE ---
                    gap = GRID_WIDTH // ROWS
                    
                    mouse_x = pos[0] # Horizontal
                    mouse_y = pos[1] # Vertical
                    
                    row = mouse_y // gap # Row determined by Y
                    col = mouse_x // gap # Col determined by X
                    
                    spot = grid[row][col]
                    if not start and spot != end:
                        start = spot
                        start.make_start()
                    elif not end and spot != start:
                        end = spot
                        end.make_end()
                    elif spot != end and spot != start:
                        spot.make_barrier()
                
                # Panel Interaction
                else:
                    if buttons["A*"].collidepoint(pos): current_algo = "A*"
                    if buttons["Dijkstra"].collidepoint(pos): current_algo = "Dijkstra"
                    if buttons["BFS"].collidepoint(pos): current_algo = "BFS"
                    
                    if buttons["Reset"].collidepoint(pos):
                        start = None
                        end = None
                        grid = make_grid(ROWS, GRID_WIDTH)
                        stats = {"time": 0, "visited": 0, "path": 0}
                        started = False

                    if buttons["Map1"].collidepoint(pos):
                        start = None; end = None; started = False
                        grid = make_grid(ROWS, GRID_WIDTH)
                        generate_map_1(grid)
                    
                    if buttons["Map2"].collidepoint(pos):
                        start = None; end = None; started = False
                        grid = make_grid(ROWS, GRID_WIDTH)
                        generate_map_2(grid)

                    if buttons["Start"].collidepoint(pos) and start and end and not started:
                        started = True
                        for row in grid:
                            for spot in row:
                                spot.update_neighbors(grid)
                        
                        start_time = time.time()
                        found = False
                        visited = 0
                        path_len = 0

                        if current_algo == "A*":
                            found, visited, path_len = algorithm_astar(lambda: draw(win, grid, ROWS, GRID_WIDTH, stats, current_algo), grid, start, end)
                        elif current_algo == "Dijkstra":
                            found, visited, path_len = algorithm_dijkstra(lambda: draw(win, grid, ROWS, GRID_WIDTH, stats, current_algo), grid, start, end)
                        elif current_algo == "BFS":
                            found, visited, path_len = algorithm_bfs(lambda: draw(win, grid, ROWS, GRID_WIDTH, stats, current_algo), grid, start, end)
                        
                        end_time = time.time()
                        stats["time"] = end_time - start_time
                        stats["visited"] = visited
                        stats["path"] = path_len
                        started = False


            elif pygame.mouse.get_pressed()[2]: # Right Click (Delete)
                pos = pygame.mouse.get_pos()
                if pos[0] < GRID_WIDTH:
                    # --- FIXED LOGIC HERE ALSO ---
                    gap = GRID_WIDTH // ROWS
                    
                    mouse_x = pos[0] 
                    mouse_y = pos[1]
                    
                    row = mouse_y // gap
                    col = mouse_x // gap
                    
                    spot = grid[row][col]
                    spot.reset()
                    if spot == start:
                        start = None
                    elif spot == end:
                        end = None

            # KEYBOARD
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end and not started:
                    # Space trigger same as Start button logic if needed
                    pass

    pygame.quit()

main(WIN, WIDTH)