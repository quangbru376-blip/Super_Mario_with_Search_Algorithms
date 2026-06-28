### Greedy Best-First Search
```python
def Greedy_Best_First(problem):
    node = Node(state=problem.initial_state)
    frontier = PriorityQueue(node, key=lambda n: heuristic(n.state)) # Theo h(n)
    explored = Set()
    while not frontier.is_empty():
        node = frontier.pop()
        if problem.is_goal(node.state): return node
        explored.add(node.state)
        for action in problem.actions(node.state):
            child = child_node(problem, node, action)
            if child.state not in explored and child.state not in frontier:
                frontier.push(child)
    return None
```
---
### A Star
```python
def A_Star(problem):
    node = Node(state=problem.initial_state)
    # Sắp xếp theo f(n) = g(n) + h(n)
    frontier = PriorityQueue(node, key=lambda n: n.path_cost + heuristic(n.state))
    explored = Set()
    while not frontier.is_empty():
        node = frontier.pop()
        if problem.is_goal(node.state): return node
        explored.add(node.state)
        for action in problem.actions(node.state):
            child = child_node(problem, node, action)
            if child.state not in explored and child.state not in frontier:
                frontier.push(child)
            elif child.state in frontier với f(n) lớn hơn:
                thay thế nút đó trong frontier bằng child
    return None
```
---
### IDA Star
```python
def IDA_Star(problem):
    node = Node(state=problem.initial_state, path_cost=0)
    limit = node.path_cost + heuristic(node.state) # f(n) ban đầu
    while True:
        result, next_limit = search(problem, node, limit)
        if result == "Found": return solution_path
        if result == "No solution": return None
        limit = next_limit # Tăng ngưỡng cắt bằng f(n) nhỏ nhất vượt ngưỡng

def search(problem, node, limit):
    f_n = node.path_cost + heuristic(node.state)
    if f_n > limit: return "Cutoff", f_n
    if problem.is_goal(node.state): return "Found", limit
    
    min_exceeded = infinity
    for action in problem.actions(node.state):
        child = child_node(problem, node, action)
        result, next_limit = search(problem, child, limit)
        if result == "Found": return "Found", limit
        if result == "Cutoff": 
            min_exceeded = min(min_exceeded, next_limit)
    
    if min_exceeded == infinity:
        return "No solution", limit
    return "Cutoff", min_exceeded
```
