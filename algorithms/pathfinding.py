import heapq
from .core import Node, Problem

def get_cost(grid, pos):
    r, c = pos
    return 5 if grid[r][c] == 2 else 1

def get_neighbors(pos, grid):
    r, c = pos
    rows, cols = len(grid), len(grid[0])
    moves = [(-1, 0), (1, 0), (0, -1), (0, 1)] # Up, Down, Left, Right
    neighbors = []
    for dr, dc in moves:
        nr, nc = r + dr, c + dc
        if 0 <= nr < rows and 0 <= nc < cols:
            if grid[nr][nc] != 1:
                neighbors.append((nr, nc))
    return neighbors

def heuristic(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

class GridPathfindingProblem(Problem):
    def __init__(self, grid, initial_state, goal=None):
        super().__init__(initial_state, goal)
        self.grid = grid

    def actions(self, state):
        return get_neighbors(state, self.grid)

    def result(self, state, action):
        return action # The action itself is the neighbor coordinate

    def is_goal(self, state):
        return state == self.goal

    def step_cost(self, state, action, next_state):
        return get_cost(self.grid, next_state)

    def heuristic(self, state):
        if self.goal is None:
            return 0
        return heuristic(state, self.goal)

# ----------------- GENERIC ALGORITHMS -----------------

def BFS(problem):
    node = Node(state=problem.initial_state)
    if problem.is_goal(node.state):
        yield {"current": node, "frontier": [], "visited": set(), "path": node.path()}
        return
        
    frontier = [node] # Queue
    explored = set()
    
    while frontier:
        node = frontier.pop(0)
        explored.add(node.state)
        
        yield {"current": node, "frontier": list(frontier), "visited": set(explored), "path": None}
        
        for action in problem.actions(node.state):
            child = problem.child_node(node, action)
            if child.state not in explored and not any(n.state == child.state for n in frontier):
                if problem.is_goal(child.state):
                    yield {"current": child, "frontier": list(frontier), "visited": set(explored), "path": child.path()}
                    return
                frontier.append(child)
                
    yield {"current": None, "frontier": [], "visited": set(explored), "path": []}

def DFS(problem):
    frontier = [Node(state=problem.initial_state)] # Stack
    explored = set()
    
    while frontier:
        node = frontier.pop()
        
        if problem.is_goal(node.state):
            yield {"current": node, "frontier": list(frontier), "visited": set(explored), "path": node.path()}
            return
            
        if node.state not in explored:
            explored.add(node.state)
            
            yield {"current": node, "frontier": list(frontier), "visited": set(explored), "path": None}
            
            for action in problem.actions(node.state):
                frontier.append(problem.child_node(node, action))
                
    yield {"current": None, "frontier": [], "visited": set(explored), "path": []}

def UCS(problem):
    node = Node(state=problem.initial_state)
    counter = 0
    frontier_pq = [(node.path_cost, counter, node)]
    frontier_dict = {node.state: node}
    explored = set()
    
    while frontier_pq:
        _, _, node = heapq.heappop(frontier_pq)
        
        if node.state in explored:
            continue
            
        if problem.is_goal(node.state):
            yield {"current": node, "frontier": list(frontier_dict.values()), "visited": set(explored), "path": node.path()}
            return
            
        explored.add(node.state)
        if node.state in frontier_dict:
            del frontier_dict[node.state]
            
        yield {"current": node, "frontier": list(frontier_dict.values()), "visited": set(explored), "path": None}
        
        for action in problem.actions(node.state):
            child = problem.child_node(node, action)
            if child.state not in explored and child.state not in frontier_dict:
                counter += 1
                frontier_dict[child.state] = child
                heapq.heappush(frontier_pq, (child.path_cost, counter, child))
            elif child.state in frontier_dict and child.path_cost < frontier_dict[child.state].path_cost:
                counter += 1
                frontier_dict[child.state] = child
                heapq.heappush(frontier_pq, (child.path_cost, counter, child))
                
    yield {"current": None, "frontier": [], "visited": set(explored), "path": []}

def Greedy_Best_First(problem):
    node = Node(state=problem.initial_state)
    counter = 0
    frontier_pq = [(problem.heuristic(node.state), counter, node)]
    frontier_dict = {node.state: node}
    explored = set()
    
    while frontier_pq:
        _, _, node = heapq.heappop(frontier_pq)
        
        if node.state in explored:
            continue
            
        if problem.is_goal(node.state):
            yield {"current": node, "frontier": list(frontier_dict.values()), "visited": set(explored), "path": node.path()}
            return
            
        explored.add(node.state)
        if node.state in frontier_dict:
            del frontier_dict[node.state]
            
        yield {"current": node, "frontier": list(frontier_dict.values()), "visited": set(explored), "path": None}
        
        for action in problem.actions(node.state):
            child = problem.child_node(node, action)
            if child.state not in explored and child.state not in frontier_dict:
                counter += 1
                frontier_dict[child.state] = child
                heapq.heappush(frontier_pq, (problem.heuristic(child.state), counter, child))
                
    yield {"current": None, "frontier": [], "visited": set(explored), "path": []}

def A_Star(problem):
    node = Node(state=problem.initial_state)
    counter = 0
    f_cost = node.path_cost + problem.heuristic(node.state)
    frontier_pq = [(f_cost, counter, node)]
    frontier_dict = {node.state: node}
    explored = set()
    
    while frontier_pq:
        _, _, node = heapq.heappop(frontier_pq)
        
        if node.state in explored:
            continue
            
        if problem.is_goal(node.state):
            yield {"current": node, "frontier": list(frontier_dict.values()), "visited": set(explored), "path": node.path()}
            return
            
        explored.add(node.state)
        if node.state in frontier_dict:
            del frontier_dict[node.state]
            
        yield {"current": node, "frontier": list(frontier_dict.values()), "visited": set(explored), "path": None}
        
        for action in problem.actions(node.state):
            child = problem.child_node(node, action)
            if child.state not in explored and child.state not in frontier_dict:
                counter += 1
                frontier_dict[child.state] = child
                f_child = child.path_cost + problem.heuristic(child.state)
                heapq.heappush(frontier_pq, (f_child, counter, child))
            elif child.state in frontier_dict and child.path_cost < frontier_dict[child.state].path_cost:
                counter += 1
                frontier_dict[child.state] = child
                f_child = child.path_cost + problem.heuristic(child.state)
                heapq.heappush(frontier_pq, (f_child, counter, child))
                
    yield {"current": None, "frontier": [], "visited": set(explored), "path": []}

def IDA_Star(problem):
    node = Node(state=problem.initial_state, path_cost=0)
    limit = node.path_cost + problem.heuristic(node.state)
    visited_all_rounds = set()
    total_steps = 0
    
    while True:
        visited_this_round = set()
        stack = [(node, [node.state])]
        next_limit = float('inf')
        min_g = {}
        
        goal_node = None
        
        while stack:
            current_node, path_states = stack.pop()
            total_steps += 1
            f = current_node.path_cost + problem.heuristic(current_node.state)
            
            if f > limit:
                next_limit = min(next_limit, f)
                continue
                
            if current_node.state in min_g and min_g[current_node.state] <= current_node.path_cost:
                continue
            min_g[current_node.state] = current_node.path_cost
            
            visited_this_round.add(current_node.state)
            visited_all_rounds.add(current_node.state)
            
            yield {"current": current_node, "frontier": [n for n, p in stack], "visited": set(visited_this_round), "path": None, "total_steps": total_steps}
            
            if problem.is_goal(current_node.state):
                goal_node = current_node
                break
                
            for action in reversed(problem.actions(current_node.state)):
                child = problem.child_node(current_node, action)
                if child.state not in path_states:
                    stack.append((child, path_states + [child.state]))
                    
        if goal_node:
            yield {"current": goal_node, "frontier": [n for n, p in stack], "visited": set(visited_this_round), "path": goal_node.path(), "total_steps": total_steps}
            return
            
        if next_limit == float('inf'):
            break
            
        limit = next_limit
        
    yield {"current": None, "frontier": [], "visited": set(visited_all_rounds), "path": [], "total_steps": total_steps}

# ----------------- UI WRAPPERS -----------------

def format_yield(step):
    current_pos = step["current"].state if step["current"] else None
    frontier_pos = [n.state for n in step["frontier"]]
    visited_pos = list(step["visited"])
    path_pos = [n.state for n in step["path"]] if step["path"] else None
    
    if path_pos is not None and not path_pos:
        path_pos = [] # Ensure it returns [] when no path found at end
        
    # Explicitly yield final state when no path is found
    if step["current"] is None:
        path_pos = []
    
    status_text = ""
    if path_pos:
        status_text = f"[Hệ thống] Đã tìm thấy đích!"
    elif current_pos is not None:
        status_text = f"[Ô {current_pos}] Đang duyệt..."
    else:
        status_text = f"[Hệ thống] Không tìm thấy đường!"
        
    return {
        "current": current_pos,
        "frontier": frontier_pos,
        "visited": visited_pos,
        "path": path_pos,
        "status": status_text,
        "total_steps": step.get("total_steps")
    }

def bfs(grid, start, goal):
    problem = GridPathfindingProblem(grid, start, goal)
    for step in BFS(problem):
        yield format_yield(step)

def dfs(grid, start, goal):
    problem = GridPathfindingProblem(grid, start, goal)
    for step in DFS(problem):
        yield format_yield(step)

def ucs(grid, start, goal):
    problem = GridPathfindingProblem(grid, start, goal)
    for step in UCS(problem):
        yield format_yield(step)

def greedy(grid, start, goal):
    problem = GridPathfindingProblem(grid, start, goal)
    for step in Greedy_Best_First(problem):
        yield format_yield(step)

def astar(grid, start, goal):
    problem = GridPathfindingProblem(grid, start, goal)
    for step in A_Star(problem):
        yield format_yield(step)

def idastar(grid, start, goal):
    problem = GridPathfindingProblem(grid, start, goal)
    for step in IDA_Star(problem):
        yield format_yield(step)
