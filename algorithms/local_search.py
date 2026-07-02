import math
import random
from .core import Problem

class TerrainProblem(Problem):
    def __init__(self, grid, initial_state):
        super().__init__(initial_state, goal=None)
        self.grid = grid

    def value(self, state):
        r, c = state
        return self.grid[r][c]

    def actions(self, state):
        r, c = state
        rows, cols = len(self.grid), len(self.grid[0])
        moves = [(-1, 0), (1, 0), (0, -1), (0, 1)] # Up, Down, Left, Right
        valid_moves = []
        for dr, dc in moves:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                valid_moves.append((nr, nc)) # action is the next position
        return valid_moves

    def result(self, state, action):
        return action # state becomes the next position
        
    def is_goal(self, state):
        return self.value(state) == 9 # hardcode peak


def Simple_Hill_Climbing(problem):
    current = problem.initial_state
    path = [current]
    
    while True:
        current_val = problem.value(current)
        yield {
            "current": current,
            "visited": list(path),
            "evaluating": [],
            "status": f"[Ô {current}] Đang ở độ cao: {current_val}"
        }
        
        if problem.is_goal(current):
            yield {
                "current": current,
                "visited": list(path),
                "evaluating": [],
                "status": "[Hệ thống] Đã tìm thấy đỉnh cao nhất (9)!"
            }
            return
            
        neighbors = [problem.result(current, a) for a in problem.actions(current)]
        moved = False
        
        for neighbor in neighbors:
            n_val = problem.value(neighbor)
            yield {
                "current": current,
                "visited": list(path),
                "evaluating": [neighbor],
                "status": f"[Ô {neighbor}] Kiểm tra độ cao: {n_val}"
            }
            if n_val > current_val:
                current = neighbor
                path.append(current)
                moved = True
                break
                
        if not moved:
            yield {
                "current": current,
                "visited": list(path),
                "evaluating": [],
                "status": f"[Hệ thống] Bị kẹt ở đỉnh cục bộ tại {current} (độ cao: {current_val})"
            }
            return


def Simulated_Annealing(problem, schedule):
    current = problem.initial_state
    path = [current]
    t = 1
    
    while True:
        current_val = problem.value(current)
        T = schedule(t)
        
        yield {
            "current": current,
            "visited": list(path),
            "evaluating": [],
            "status": f"[Ô {current}] Đang ở độ cao: {current_val} | T = {T:.2f}"
        }
        
        if problem.is_goal(current):
            yield {
                "current": current,
                "visited": list(path),
                "evaluating": [],
                "status": "[Hệ thống] Đã tìm thấy đỉnh cao nhất (9)!"
            }
            return
            
        if T < 0.1: # T is too small
            yield {
                "current": current,
                "visited": list(path),
                "evaluating": [],
                "status": f"[Hệ thống] Hết nhiệt! Dừng ở đỉnh cục bộ tại {current} (độ cao: {current_val})"
            }
            return
            
        neighbors = [problem.result(current, a) for a in problem.actions(current)]
        if not neighbors:
            return
            
        next_state = random.choice(neighbors)
        next_val = problem.value(next_state)
        delta_E = next_val - current_val
        
        if delta_E > 0:
            prob = 1.0
        else:
            prob = math.exp(delta_E / T)
            
        yield {
            "current": current,
            "visited": list(path),
            "evaluating": [next_state],
            "status": f"[Ô {next_state}] Thử (cao {next_val}). dE={delta_E}, T={T:.1f}, P={prob:.2f}"
        }
        
        if random.random() <= prob:
            current = next_state
            path.append(current)
            
        t += 1


def Local_Beam_Search(problem, k=2):
    # beam is a list of tuples (state, path_history)
    beam = [(problem.initial_state, [problem.initial_state])]
    
    yield {
        "current": [b[0] for b in beam],
        "visited": [b[1] for b in beam],
        "evaluating": [],
        "status": f"[Hệ thống] Khởi tạo Local Beam với k={k}"
    }
    
    while True:
        peak_found = False
        for state, path in beam:
            if problem.is_goal(state):
                peak_found = True
                
        if peak_found:
            yield {
                "current": [b[0] for b in beam],
                "visited": [b[1] for b in beam],
                "evaluating": [],
                "status": "[Hệ thống] Đã tìm thấy đỉnh cao nhất (9)!"
            }
            return
            
        all_neighbors = []
        evaluating_cells = []
        
        for state, path in beam:
            for action in problem.actions(state):
                n_state = problem.result(state, action)
                n_val = problem.value(n_state)
                new_path = list(path)
                new_path.append(n_state)
                all_neighbors.append((n_state, n_val, new_path))
                evaluating_cells.append(n_state)
                
        if not all_neighbors:
            yield {
                "current": [b[0] for b in beam],
                "visited": [b[1] for b in beam],
                "evaluating": [],
                "status": "[Hệ thống] Bị kẹt! Không có ô lân cận."
            }
            return
            
        yield {
            "current": [b[0] for b in beam],
            "visited": [b[1] for b in beam],
            "evaluating": evaluating_cells,
            "status": f"[Hệ thống] Sinh ra {len(all_neighbors)} lân cận từ {len(beam)} trạng thái hiện tại."
        }
        
        # Pick best k
        sorted_neighbors = sorted(all_neighbors, key=lambda x: x[1], reverse=True)
        next_beam = []
        
        for n_state, n_val, new_path in sorted_neighbors:
            if n_state not in [b[0] for b in next_beam]:
                next_beam.append((n_state, new_path))
            if len(next_beam) == k:
                break
                
        if not next_beam:
            return
            
        max_current_height = max([problem.value(b[0]) for b in beam])
        max_next_height = max([problem.value(b[0]) for b in next_beam])
        
        if max_next_height <= max_current_height:
             yield {
                "current": [b[0] for b in next_beam], 
                "visited": [b[1] for b in next_beam],
                "evaluating": [],
                "status": f"[Hệ thống] Bị kẹt ở đỉnh cục bộ! (Max độ cao: {max_current_height})"
             }
             return
             
        beam = next_beam
        status_heights = [problem.value(b[0]) for b in beam]
        
        yield {
            "current": [b[0] for b in beam],
            "visited": [b[1] for b in beam],
            "evaluating": [],
            "status": f"[Hệ thống] Đã chọn {k} trạng thái tốt nhất: Độ cao {status_heights}"
        }


# ----------------- UI WRAPPERS -----------------

def simple_hill_climbing(grid, start):
    problem = TerrainProblem(grid, start)
    for step in Simple_Hill_Climbing(problem):
        yield step

def simulated_annealing(grid, start):
    problem = TerrainProblem(grid, start)
    
    def schedule(t):
        T_init = 100.0
        cooling_rate = 0.95
        return T_init * (cooling_rate ** (t - 1))
        
    for step in Simulated_Annealing(problem, schedule):
        yield step

def local_beam_search(grid, start, k=2):
    problem = TerrainProblem(grid, start)
    for step in Local_Beam_Search(problem, k):
        yield step