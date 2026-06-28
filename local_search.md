### Simple Hill Climbing
```python
def Simple_Hill_Climbing(problem):
    current = problem.initial_state
    
    while True:
        neighbors = problem.neighbors(current)
        found_better = False
        
        for neighbor in neighbors:
            if value(neighbor) > value(current):
                current = neighbor
                found_better = True
                break

        if not found_better:
            return current
```
---
### Beam Search
```python
def Beam_Search(problem, k):
    frontier = [problem.initial_state]
    while not goal_found:
        candidates = []
        for state in frontier:
            candidates.extend(problem.neighbors(state))
        frontier = select_best_k(candidates, k) # Giữ lại k trạng thái tốt nhất
        if goal in frontier: return goal
    return None
```
---
### Simulated Annealing
```python
def Simulated_Annealing(problem, schedule):
    current = problem.initial_state
    for t in range(1, infinity):
        T = schedule(t) # Nhiệt độ giảm dần
        if T == 0: return current
        next_state = random_select(problem.neighbors(current))
        delta_E = value(next_state) - value(current)
        if delta_E > 0:
            current = next_state
        else:
            # Chấp nhận trạng thái tệ hơn với xác suất e^(delta_E / T)
            current = next_state with probability e^(delta_E / T)
```
