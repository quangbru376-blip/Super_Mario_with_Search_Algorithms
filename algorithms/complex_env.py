import random
from collections import deque
from .core import Problem

# ==========================================================
# SENSORLESS SEARCH (BELIEF STATE SEARCH)
# ==========================================================

class SensorlessProblem(Problem):
    def __init__(self, initial_state, grid):
        super().__init__(initial_state)
        self.grid = grid
        self.rows = len(grid)
        self.cols = len(grid[0])
        
    def actions(self, state):
        return [(-1, 0, "Lên"), (0, -1, "Trái"), (1, 0, "Xuống"), (0, 1, "Phải")]
        
    def result(self, state, action):
        dr, dc, name = action
        next_state = []
        for r, c, coins in state:
            nr, nc = r + dr, c + dc
            if 0 <= nr < self.rows and 0 <= nc < self.cols and self.grid[nr][nc] != 1:
                ncoins = set(coins)
                if (nr, nc) in ncoins: ncoins.remove((nr, nc))
                next_state.append((nr, nc, frozenset(ncoins)))
            else:
                next_state.append((r, c, coins))
        return tuple(next_state)
        
    def is_goal(self, state):
        return all(len(m[2]) == 0 for m in state)

def create_yield_state(marios_state, status):
    state = {"status": status}
    for i in range(4):
        state[f"mario{i+1}"] = {"current": (marios_state[i][0], marios_state[i][1]), "coins_left": list(marios_state[i][2])}
    return state

def Belief_State_BFS(problem):
    initial_state = problem.initial_state
    queue = deque([(initial_state, [])])
    visited = {initial_state}
    
    yield create_yield_state(initial_state, "[BFS Đồng bộ] Đang tính toán đường đi đồng bộ (BFS)...")
    
    found_path = None
    while queue:
        curr_state, path = queue.popleft()
        if problem.is_goal(curr_state):
            found_path = path
            break
            
        for action in problem.actions(curr_state):
            next_state = problem.result(curr_state, action)
            if next_state != curr_state and next_state not in visited:
                visited.add(next_state)
                queue.append((next_state, path + [(action, next_state)]))
                
    if found_path is None:
        yield create_yield_state(initial_state, "[BFS Đồng bộ] Không tìm thấy đường đi chung!")
        return
        
    step = 1
    for action, nxt_state in found_path:
        dr, dc, name = action
        yield create_yield_state(nxt_state, f"[BFS Đồng bộ] Bước {step}: Đi {name}. Còn lại: " + ", ".join([str(len(m[2])) for m in nxt_state]) + " xu")
        step += 1
        
    yield create_yield_state(found_path[-1][1], "[BFS Đồng bộ] Hoàn tất! Cả 4 Mario đều đã dọn sạch xu bằng một chuỗi hành động chung.")

def sensorless_bfs(grid, start=None, initial_coins=None):
    rows, cols = len(grid), len(grid[0])
    valid_positions = [(r, c) for r in range(rows) for c in range(cols) if grid[r][c] != 1]
    
    if len(valid_positions) >= 4:
        start_positions = random.sample(valid_positions, 4)
    else:
        start_positions = ([valid_positions[0]] * 4) if valid_positions else [(0,0)] * 4
        
    initial_coins_set = frozenset(initial_coins) if initial_coins else frozenset()
    
    initial_state = []
    for pos in start_positions:
        coins = set(initial_coins_set)
        if pos in coins:
            coins.remove(pos)
        initial_state.append((pos[0], pos[1], frozenset(coins)))
    initial_state = tuple(initial_state)
    
    problem = SensorlessProblem(initial_state, grid)
    for step in Belief_State_BFS(problem):
        yield step

# ==========================================================
# PARTIALLY OBSERVABLE SEARCH (MULTIVERSE)
# ==========================================================

class PartiallyObservableProblem(Problem):
    def __init__(self, initial_state, grid):
        super().__init__(initial_state)
        self.grid = grid
        self.rows = len(grid)
        self.cols = len(grid[0])
        
    def actions(self, state):
        return [(-1, 0, "Lên"), (1, 0, "Xuống"), (0, -1, "Trái"), (0, 1, "Phải")]
        
    def result(self, state, action):
        dr, dc, name = action
        r, c, coins = state
        nr, nc = r + dr, c + dc
        if 0 <= nr < self.rows and 0 <= nc < self.cols and self.grid[nr][nc] != 1:
            ncoins = set(coins)
            if (nr, nc) in ncoins: ncoins.remove((nr, nc))
            return (nr, nc, frozenset(ncoins))
        return state
        
    def is_goal(self, state):
        return len(state[2]) == 0
        
    def get_percept(self, state):
        r, c, coins = state
        reading = []
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r+dr, c+dc
            if (nr, nc) in coins:
                reading.append("C")
            elif 0 <= nr < self.rows and 0 <= nc < self.cols:
                reading.append("W" if self.grid[nr][nc] == 1 else "0")
            else:
                reading.append("OOB")
        return tuple(reading)

def Multiverse_BFS(problem, true_start, universes):
    true_pos = true_start[0:2]
    true_coins = set(true_start[2])
    
    def yield_state(status):
        return {
            "true_pos": true_pos,
            "universes": {k: {"current": v["current"], "coins_left": list(v["coins_left"]), "status": v["status"]} for k, v in universes.items()},
            "status": status
        }
        
    true_sensor = problem.get_percept((true_pos[0], true_pos[1], frozenset(true_coins)))
    for u_start, u_data in universes.items():
        if u_data["status"] == "active":
            u_state = (u_data["current"][0], u_data["current"][1], frozenset(u_data["coins_left"]))
            if problem.get_percept(u_state) != true_sensor:
                u_data["status"] = "faded"
                
    yield yield_state("[Đa vũ trụ] Khởi tạo Đa vũ trụ. Lọc cảm biến ban đầu.")
    
    for u_start, u_data in universes.items():
        if u_data["status"] == "faded": u_data["status"] = "invalid"

    while true_coins:
        queue = deque([(true_pos, [])])
        visited = {true_pos}
        found_path = None
        
        while queue:
            curr, p = queue.popleft()
            if curr in true_coins:
                found_path = p
                break
            for action in problem.actions(None):
                dr, dc, name = action
                nr, nc = curr[0] + dr, curr[1] + dc
                if 0 <= nr < problem.rows and 0 <= nc < problem.cols and problem.grid[nr][nc] != 1:
                    if (nr, nc) not in visited:
                        visited.add((nr, nc))
                        queue.append(((nr, nc), p + [(dr, dc, name)]))
                        
        if not found_path:
            yield yield_state("[Đa vũ trụ] Không tìm thấy đường tới xu. Kết thúc.")
            break
            
        for dr, dc, name in found_path:
            action = (dr, dc, name)
            true_state = problem.result((true_pos[0], true_pos[1], frozenset(true_coins)), action)
            true_pos = true_state[0:2]
            true_coins = set(true_state[2])
            
            for u_start, u_data in universes.items():
                if u_data["status"] == "active":
                    u_state = (u_data["current"][0], u_data["current"][1], frozenset(u_data["coins_left"]))
                    next_u_state = problem.result(u_state, action)
                    u_data["current"] = next_u_state[0:2]
                    u_data["coins_left"] = set(next_u_state[2])
                    
            yield yield_state(f"[Đa vũ trụ] Đi {name}. Còn {len(true_coins)} xu thật.")
            
            true_sensor = problem.get_percept((true_pos[0], true_pos[1], frozenset(true_coins)))
            has_faded = False
            for u_start, u_data in universes.items():
                if u_data["status"] == "active":
                    u_state = (u_data["current"][0], u_data["current"][1], frozenset(u_data["coins_left"]))
                    if problem.get_percept(u_state) != true_sensor:
                        u_data["status"] = "faded"
                        has_faded = True
                        
            if has_faded:
                yield yield_state("[Đa vũ trụ] Cảm biến! Làm mờ các vũ trụ sai lệnh.")
                for u_start, u_data in universes.items():
                    if u_data["status"] == "faded":
                        u_data["status"] = "invalid"

    yield yield_state("[Đa vũ trụ] Hoàn tất! Mario thật đã gom hết xu.")

def partially_observable_bfs(grid, start, initial_coins):
    rows, cols = len(grid), len(grid[0])
    universes = {}
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] != 1:
                universes[(r, c)] = {
                    "current": (r, c),
                    "coins_left": set(initial_coins),
                    "status": "active"
                }
            else:
                universes[(r, c)] = {
                    "current": (r, c),
                    "coins_left": set(initial_coins),
                    "status": "invalid"
                }
                
    true_coins = set(initial_coins)
    if start in true_coins: true_coins.remove(start)
    for u_start, u_data in universes.items():
        if u_data["status"] == "active" and u_data["current"] in u_data["coins_left"]:
            u_data["coins_left"].remove(u_data["current"])
            
    problem = PartiallyObservableProblem((start[0], start[1], frozenset(true_coins)), grid)
    for step in Multiverse_BFS(problem, (start[0], start[1], frozenset(true_coins)), universes):
        yield step

# ==========================================================
# AND-OR SEARCH (NON-DETERMINISTIC ENVIRONMENT)
# ==========================================================

class NonDeterministicProblem(Problem):
    def __init__(self, initial_state, grid):
        super().__init__(initial_state)
        self.grid = grid
        self.rows = len(grid)
        self.cols = len(grid[0])
        
    def actions(self, state):
        return [(-1, 0), (1, 0), (0, -1), (0, 1)]
        
    def results(self, state, action):
        r, c, coins = state
        dr, dc = action
        nr, nc = r + dr, c + dc
        
        if 0 <= nr < self.rows and 0 <= nc < self.cols and self.grid[nr][nc] != 1:
            new_coins = set(coins)
            if (nr, nc) in new_coins:
                new_coins.remove((nr, nc))
            return [(nr, nc, frozenset(new_coins))]
        return [(r, c, coins)]
        
    def is_goal(self, state):
        return len(state[2]) == 0

def And_Or_Graph_Search(problem):
    def or_search(state, path):
        if problem.is_goal(state): return []
        if state in path: return None
        for action in problem.actions(state):
            results = problem.results(state, action)
            plan = and_search(results, path + [state])
            if plan is not None:
                return [action, plan]
        return None
        
    def and_search(states, path):
        plan = {}
        for s in states:
            p = or_search(s, path)
            if p is None: return None
            plan[s] = p
        return plan
        
    return or_search(problem.initial_state, [])

def and_or_search(grid, start, initial_coins):
    problem = NonDeterministicProblem((start[0], start[1], frozenset(initial_coins)), grid)
    
    yield {
        "current": start,
        "path": [start],
        "coins_left": list(initial_coins),
        "status": "[And-Or] Khởi chạy And-Or Search xây dựng cây kế hoạch..."
    }
    
    plan = And_Or_Graph_Search(problem)
    
    if plan is None:
        yield {
            "current": start,
            "path": [start],
            "coins_left": list(initial_coins),
            "status": "[And-Or] Hoàn tất. (Không tìm thấy kế hoạch And-Or)"
        }
        return
        
    current_state = problem.initial_state
    path_coords = [start]
    current_plan = plan
    
    while current_plan:
        action, subplan = current_plan
        if random.random() < 0.3:
            yield {
                "current": current_state[:2],
                "path": list(path_coords),
                "coins_left": list(current_state[2]),
                "status": f"[And-Or] Đạp bẫy! Đứng im. (Thử lại {action}...)",
                "trapped": True
            }
            continue
            
        next_state = problem.results(current_state, action)[0]
        current_state = next_state
        current_plan = subplan[next_state]
        
        nr, nc = current_state[0], current_state[1]
        path_coords.append((nr, nc))
        new_coins = current_state[2]
        
        yield {
            "current": (nr, nc),
            "path": list(path_coords),
            "coins_left": list(new_coins),
            "status": f"[And-Or] Hành động {action} thành công. Còn {len(new_coins)} xu."
        }
        
    yield {
        "current": current_state[:2],
        "path": path_coords,
        "coins_left": [],
        "status": "[And-Or] Thành công! And-Or Search đã hoàn tất kế hoạch."
    }
