### Sensorless Search (Belief State Search with BFS)
```python
def Sensorless_Search(problem):
    # problem.initial_state là một tập hợp (belief state) gồm 4 physical states
    # Ví dụ: { state1, state2, state3, state4 }
    belief_node = Node(state=problem.initial_state)
    
    if problem.is_goal(belief_node.state): 
        return belief_node
        
    frontier = Queue([belief_node])
    explored = Set()
    
    while not frontier.is_empty():
        belief_node = frontier.pop()
        explored.add(belief_node.state)
        
        for action in problem.actions(belief_node.state):
            # child_belief_state được tạo bằng cách áp dụng action lên MỌI physical state trong belief_node.state
            child_belief = child_node(problem, belief_node, action)
            
            if child_belief.state not in explored and child_belief.state not in frontier:
                if problem.is_goal(child_belief.state): 
                    return child_belief
                frontier.push(child_belief)
                
    return None
```
---
### Partially Observable Search (Multiverse BFS)
```python
def Partially_Observable_Search(problem):
    # Khởi tạo tập hợp tất cả các trạng thái có thể có ban đầu (Belief state / Multiverses)
    belief_state = problem.initial_belief_state()
    
    # Kế hoạch hành động rỗng
    plan = []
    
    while not problem.is_goal(problem.true_state):
        # Lấy thông tin cảm biến từ môi trường thật
        percept = problem.get_percept(problem.true_state)
        
        # Cập nhật belief_state: Loại bỏ các trạng thái không khớp với percept
        belief_state = problem.update_belief_state(belief_state, percept)
        
        # Dùng BFS tìm đường đi từ true_state tới mục tiêu (xu gần nhất)
        path = BFS(problem.true_state, problem.goal)
        
        if not path:
            return "Failure"
            
        # Thực thi hành động đầu tiên trong kế hoạch tìm được
        action = path[0]
        plan.append(action)
        
        # Cập nhật true_state sau khi thực hiện hành động
        problem.true_state = problem.result(problem.true_state, action)
        
        # Cập nhật tất cả các trạng thái trong belief_state theo action đó
        belief_state = problem.predict_belief_state(belief_state, action)
        
    return plan
```
---
### And-Or Graph Search
```python
def And_Or_Graph_Search(problem):
    return Or_Search(problem.initial_state, problem, [])

def Or_Search(state, problem, path):
    if problem.is_goal(state): 
        return []
    if state in path: 
        return "Failure"
        
    for action in problem.actions(state):
        # Lấy tất cả các kết quả có thể xảy ra từ môi trường không tất định (AND node)
        results = problem.results(state, action)
        
        # Gọi And_Search để xem hành động này có dẫn tới đích trong mọi trường hợp không
        plan = And_Search(results, problem, path + [state])
        
        if plan != "Failure":
            return [action, plan]
            
    return "Failure"

def And_Search(states, problem, path):
    plan = {}
    for state in states:
        # Gọi đệ quy Or_Search cho từng trạng thái kết quả có thể xảy ra
        sub_plan = Or_Search(state, problem, path)
        if sub_plan == "Failure":
            return "Failure"
        plan[state] = sub_plan
    return plan
```
