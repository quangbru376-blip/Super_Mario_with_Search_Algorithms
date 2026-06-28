### Backtracking Search
```python
def Backtracking_Search(csp):
    return Backtrack({}, csp)

def Backtrack(assignment, csp):
    if is_complete(assignment, csp): return assignment
    var = select_unassigned_variable(assignment, csp)
    for value in order_domain_values(var, assignment, csp):
        if is_consistent(var, value, assignment, csp):
            assignment.add(var, value)
            result = Backtrack(assignment, csp)
            if result != failure: return result
            assignment.remove(var, value)
    return failure
```
---
### Forward Checking
```python
def Forward_Checking(assignment, csp, var, value):
    assignment.add(var, value)
    for neighbor in csp.neighbors(var):
        if neighbor not in assignment:
            remove value from neighbor.domain if it violates constraints
            if neighbor.domain is empty:
                return failure
    return success
```
---
### Min Conflicts
```python
def Min_Conflicts(csp, max_steps):
    assignment = random_assignment(csp)
    for i in range(max_steps):
        if assignment.is_complete(): return assignment
        var = conflicted_variable(assignment, csp)
        value = argmin(csp.domain[var], lambda val: count_conflicts(var, val, assignment, csp))
        assignment.add(var, value)
    return failure
```
