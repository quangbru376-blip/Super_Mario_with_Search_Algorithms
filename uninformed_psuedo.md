### BFS
```python
def BFS(problem):
    node = Node(state=problem.initial_state)
    if problem.is_goal(node.state): return node
    frontier = Queue([node]) # Hàng đợi FIFO
    explored = Set()
    while not frontier.is_empty():
        node = frontier.pop()
        explored.add(node.state)
        for action in problem.actions(node.state):
            child = child_node(problem, node, action)
            if child.state not in explored and child.state not in frontier:
                if problem.is_goal(child.state): return child
                frontier.push(child)
    return None
```
---
### DFS
```python
def DFS(problem):
    frontier = Stack([Node(state=problem.initial_state)]) # Ngăn xếp LIFO
    explored = Set()
    while not frontier.is_empty():
        node = frontier.pop()
        if problem.is_goal(node.state): return node
        if node.state not in explored:
            explored.add(node.state)
            for action in problem.actions(node.state):
                frontier.push(child_node(problem, node, action))
    return None
```
---
### UCS
```python
def UCS(problem):
    node = Node(state=problem.initial_state)
    frontier = PriorityQueue(node, key=lambda n: n.path_cost) # Hàng đợi ưu tiên theo g(n)
    explored = Set()
    while not frontier.is_empty():
        node = frontier.pop() # Lấy nút có chi phí g(n) nhỏ nhất
        if problem.is_goal(node.state): return node
        explored.add(node.state)
        for action in problem.actions(node.state):
            child = child_node(problem, node, action)
            if child.state not in explored and child.state not in frontier:
                frontier.push(child)
            elif child.state in frontier với chi phí cao hơn:
                thay thế nút đó trong frontier bằng child
    return None
```