import random
from .core import CSP

class GraphColoringCSP(CSP):
    def __init__(self, variables, domains, neighbors, initial_assignments):
        def constraint(A, a, B, b):
            return a != b
        super().__init__(variables, domains, neighbors, constraint)
        self.initial_assignments = initial_assignments

# ----------------- GENERIC ALGORITHMS -----------------

def Backtracking_Search(csp):
    assignments = dict(csp.initial_assignments)
    unassigned_vars = [v for v in csp.variables if v not in assignments]
    
    steps = [0]
    backtracks = [0]
    
    def backtrack():
        unassigned = [v for v in csp.variables if v not in assignments]
        if not unassigned:
            yield {
                "assignments": dict(assignments),
                "current": None,
                "conflict_cells": [],
                "steps": steps[0],
                "backtracks": backtracks[0],
                "status": "Đã giải quyết xong mọi ràng buộc!",
                "success": True
            }
            return
            
        var = unassigned[0] # Select unassigned variable
        
        for val in csp.domains[var]:
            steps[0] += 1
            if csp.nconflicts(var, val, assignments) == 0:
                csp.assign(var, val, assignments)
                yield {
                    "assignments": dict(assignments),
                    "current": var,
                    "conflict_cells": [],
                    "steps": steps[0],
                    "backtracks": backtracks[0],
                    "status": f"[Vùng {var}] Gán bằng Loại {val}"
                }
                
                for state in backtrack():
                    yield state
                    if state.get("success"):
                        return
                        
                csp.unassign(var, assignments)
            else:
                conflicts = [n for n in csp.neighbors[var] if n in assignments and assignments[n] == val]
                yield {
                    "assignments": dict(assignments),
                    "current": var,
                    "conflict_cells": conflicts,
                    "steps": steps[0],
                    "backtracks": backtracks[0],
                    "status": f"[Vùng {var}] Xung đột với Loại {val}!"
                }
                
        backtracks[0] += 1
        yield {
            "assignments": dict(assignments),
            "current": None,
            "conflict_cells": [],
            "steps": steps[0],
            "backtracks": backtracks[0],
            "status": f"[Vùng {var}] Không có giá trị hợp lệ! Quay lui (Backtrack)..."
        }
        return False

    for state in backtrack():
        yield state


def Forward_Checking_Search(csp):
    assignments = dict(csp.initial_assignments)
    unassigned_vars = [v for v in csp.variables if v not in assignments]
    
    current_domains = {var: list(csp.domains[var]) for var in unassigned_vars}
    
    for pos, val in csp.initial_assignments.items():
        for neighbor in csp.neighbors[pos]:
            if neighbor in current_domains and val in current_domains[neighbor]:
                current_domains[neighbor].remove(val)
                
    steps = [0]
    backtracks = [0]
    
    def fc_backtrack(domains):
        unassigned = [v for v in csp.variables if v not in assignments]
        if not unassigned:
            yield {
                "assignments": dict(assignments),
                "current": None,
                "domains": domains,
                "conflict_cells": [],
                "steps": steps[0],
                "backtracks": backtracks[0],
                "status": "Đã giải quyết xong mọi ràng buộc!",
                "success": True
            }
            return
            
        var = unassigned[0]
        var_domain = list(domains[var])
        
        for val in var_domain:
            steps[0] += 1
            if csp.nconflicts(var, val, assignments) != 0:
                continue
                
            csp.assign(var, val, assignments)
            
            new_domains = {v: list(d) for v, d in domains.items()}
            domain_empty = False
            pruned_neighbors = []
            
            for neighbor in csp.neighbors[var]:
                if neighbor in unassigned and neighbor != var:
                    if val in new_domains[neighbor]:
                        new_domains[neighbor].remove(val)
                        pruned_neighbors.append(neighbor)
                        if not new_domains[neighbor]:
                            domain_empty = True
                            
            yield {
                "assignments": dict(assignments),
                "current": var,
                "domains": new_domains,
                "conflict_cells": pruned_neighbors if domain_empty else [],
                "steps": steps[0],
                "backtracks": backtracks[0],
                "status": f"[Vùng {var}] Gán = {val}. Lọc bớt miền giá trị lân cận."
            }
            
            if not domain_empty:
                for state in fc_backtrack(new_domains):
                    yield state
                    if state.get("success"):
                        return
            else:
                backtracks[0] += 1
                yield {
                    "assignments": dict(assignments),
                    "current": var,
                    "domains": new_domains,
                    "conflict_cells": pruned_neighbors,
                    "steps": steps[0],
                    "backtracks": backtracks[0],
                    "status": f"[Vùng {var}] Phát hiện miền giá trị của hàng xóm trống! Quay lui..."
                }
                
            csp.unassign(var, assignments)
            
        return False
        
    for state in fc_backtrack(current_domains):
        yield state


def Min_Conflicts_Search(csp, max_steps=1000):
    assignments = dict(csp.initial_assignments)
    unassigned_vars = [v for v in csp.variables if v not in assignments]
    
    for var in unassigned_vars:
        csp.assign(var, random.choice(csp.domains[var]), assignments)
        
    def get_conflicted_vars():
        conflicts = set()
        for var in csp.variables:
            val = assignments[var]
            if csp.nconflicts(var, val, assignments) > 0:
                conflicts.add(var)
                for neighbor in csp.neighbors[var]:
                    if neighbor in assignments and assignments[neighbor] == val:
                        conflicts.add(neighbor)
        return list(conflicts)
        
    yield {
        "assignments": dict(assignments),
        "current": None,
        "conflict_cells": get_conflicted_vars(),
        "steps": 0,
        "status": "Khởi tạo ngẫu nhiên đầy đủ bảng."
    }
    
    for step in range(1, max_steps + 1):
        conflicted = get_conflicted_vars()
        if not conflicted:
            yield {
                "assignments": dict(assignments),
                "current": None,
                "conflict_cells": [],
                "steps": step,
                "status": "Đã giải quyết xong mọi ràng buộc!"
            }
            return
            
        conflicted_vars = [v for v in conflicted if v in unassigned_vars]
        if not conflicted_vars:
            break
            
        var = random.choice(conflicted_vars)
        
        min_c = float('inf')
        min_vals = []
        for val in csp.domains[var]:
            c = csp.nconflicts(var, val, assignments)
            if c < min_c:
                min_c = c
                min_vals = [val]
            elif c == min_c:
                min_vals.append(val)
                
        chosen_val = random.choice(min_vals)
        csp.assign(var, chosen_val, assignments)
        
        yield {
            "assignments": dict(assignments),
            "current": var,
            "conflict_cells": get_conflicted_vars(),
            "steps": step,
            "status": f"Bước {step}: Chọn [Vùng {var}], đổi sang Loại {chosen_val} để giảm xung đột."
        }
        
    yield {
        "assignments": dict(assignments),
        "current": None,
        "conflict_cells": get_conflicted_vars(),
        "steps": max_steps,
        "status": "Không tìm thấy lời giải sau số bước tối đa!"
    }


# ----------------- UI WRAPPERS -----------------

def backtracking_search(variables, neighbors_map, initial_assignments, domain):
    domains = {v: list(domain) for v in variables}
    csp = GraphColoringCSP(variables, domains, neighbors_map, initial_assignments)
    for step in Backtracking_Search(csp):
        yield step

def forward_checking_search(variables, neighbors_map, initial_assignments, domain):
    domains = {v: list(domain) for v in variables}
    csp = GraphColoringCSP(variables, domains, neighbors_map, initial_assignments)
    for step in Forward_Checking_Search(csp):
        yield step

def min_conflicts_search(variables, neighbors_map, initial_assignments, domain, max_steps=1000):
    domains = {v: list(domain) for v in variables}
    csp = GraphColoringCSP(variables, domains, neighbors_map, initial_assignments)
    for step in Min_Conflicts_Search(csp, max_steps):
        yield step
