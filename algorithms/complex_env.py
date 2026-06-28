import heapq
import random
from collections import deque

def four_combined_bfs(grid, start=None, initial_coins=None):
    rows, cols = len(grid), len(grid[0])
    valid_positions = [(r, c) for r in range(rows) for c in range(cols) if grid[r][c] != 1]
    
    if len(valid_positions) >= 4:
        start_positions = random.sample(valid_positions, 4)
    else:
        start_positions = ([valid_positions[0]] * 4) if valid_positions else [(0,0)] * 4
        
    initial_coins_set = frozenset(initial_coins) if initial_coins else frozenset()
    
    # State: tuple of 4 elements, each is (r, c, coins_left)
    initial_state = []
    for pos in start_positions:
        coins = set(initial_coins_set)
        if pos in coins:
            coins.remove(pos)
        initial_state.append((pos[0], pos[1], frozenset(coins)))
    initial_state = tuple(initial_state)
    
    queue = deque([(initial_state, [])])
    visited = {initial_state}
    actions = [(-1, 0, "Lên"), (0, -1, "Trái"), (1, 0, "Xuống"), (0, 1, "Phải")]
    
    def create_yield_state(marios_state, status):
        state = {"status": status}
        for i in range(4):
            state[f"mario{i+1}"] = {"current": (marios_state[i][0], marios_state[i][1]), "coins_left": list(marios_state[i][2])}
        return state

    yield create_yield_state(initial_state, "[BFS Đồng bộ] Đang tính toán đường đi đồng bộ (BFS)...")
    
    found_path = None
    
    while queue:
        curr_state, path = queue.popleft()
        
        # Check if all marios have 0 coins
        if all(len(m[2]) == 0 for m in curr_state):
            found_path = path
            break
            
        for dr, dc, name in actions:
            next_state = []
            moved = False
            for r, c, coins in curr_state:
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] != 1:
                    moved = True
                    ncoins = set(coins)
                    if (nr, nc) in ncoins: ncoins.remove((nr, nc))
                    next_state.append((nr, nc, frozenset(ncoins)))
                else:
                    next_state.append((r, c, coins))
            if moved:
                next_state = tuple(next_state)
                if next_state not in visited:
                    visited.add(next_state)
                    queue.append((next_state, path + [(name, next_state)]))
                    
    if found_path is None:
        yield create_yield_state(initial_state, "[BFS Đồng bộ] Không tìm thấy đường đi chung!")
        return
        
    step = 1
    for name, nxt_state in found_path:
        yield create_yield_state(nxt_state, f"[BFS Đồng bộ] Bước {step}: Đi {name}. Còn lại: " + ", ".join([str(len(m[2])) for m in nxt_state]) + " xu")
        step += 1
        
    yield create_yield_state(found_path[-1][1], "[BFS Đồng bộ] Hoàn tất! Cả 4 Mario đều đã dọn sạch xu bằng một chuỗi hành động chung.")


def multiverse_search(grid, start, initial_coins):
    """
    Tìm kiếm Đa vũ trụ: Khởi tạo 16 vũ trụ cho tất cả vị trí khả dĩ.
    Mario thật (ở vị trí start) sẽ tìm đường ăn toàn bộ xu bằng BFS.
    Tại mỗi bước di chuyển, tất cả các vũ trụ cùng thực hiện thao tác tương tự.
    Sau mỗi bước, kiểm tra cảm biến: vũ trụ nào có cảm biến không khớp với thế giới thật sẽ bị loại (faded -> invalid).
    """
    rows, cols = len(grid), len(grid[0])
    
    # Hàm lấy cảm biến (Kề cận 4 hướng)
    def get_sensor(pos, current_coins):
        r, c = pos
        reading = []
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r+dr, c+dc
            if (nr, nc) in current_coins:
                reading.append("C") # Xu
            elif 0 <= nr < rows and 0 <= nc < cols:
                reading.append("W" if grid[nr][nc] == 1 else "0") # Vật cản hoặc Trống
            else:
                reading.append("OOB") # Rìa bản đồ
        return tuple(reading)

    # Khởi tạo các vũ trụ
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

    true_pos = start
    true_coins = set(initial_coins)
    
    # Kiểm tra ăn xu ở vị trí xuất phát cho tất cả các vũ trụ
    if true_pos in true_coins:
        true_coins.remove(true_pos)
    for u_start, u_data in universes.items():
        if u_data["status"] == "active" and u_data["current"] in u_data["coins_left"]:
            u_data["coins_left"].remove(u_data["current"])

    # Lọc ban đầu
    true_sensor = get_sensor(true_pos, true_coins)
    for u_start, u_data in universes.items():
        if u_data["status"] == "active":
            if get_sensor(u_data["current"], u_data["coins_left"]) != true_sensor:
                u_data["status"] = "faded"

    yield {
        "true_pos": true_pos,
        "universes": {k: {"current": v["current"], "coins_left": list(v["coins_left"]), "status": v["status"]} for k, v in universes.items()},
        "status": "[Đa vũ trụ] Khởi tạo Đa vũ trụ. Lọc cảm biến ban đầu."
    }

    # Chuyển faded thành invalid
    for u_start, u_data in universes.items():
        if u_data["status"] == "faded":
            u_data["status"] = "invalid"

    from collections import deque

    while true_coins:
        # Dùng BFS để tìm xu gần nhất cho True Mario
        queue = deque([(true_pos, [])])
        visited = {true_pos}
        found_path = None
        
        while queue:
            curr, p = queue.popleft()
            if curr in true_coins:
                found_path = p
                break
            for dr, dc, name in [(-1, 0, "Lên"), (1, 0, "Xuống"), (0, -1, "Trái"), (0, 1, "Phải")]:
                nr, nc = curr[0] + dr, curr[1] + dc
                if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] != 1:
                    if (nr, nc) not in visited:
                        visited.add((nr, nc))
                        queue.append(((nr, nc), p + [(dr, dc, name)]))
                        
        if not found_path:
            yield {
                "true_pos": true_pos,
                "universes": {k: {"current": v["current"], "coins_left": list(v["coins_left"]), "status": v["status"]} for k, v in universes.items()},
                "status": "[Đa vũ trụ] Không tìm thấy đường tới xu. Kết thúc."
            }
            break

        for dr, dc, name in found_path:
            # 1. Di chuyển True Mario
            true_pos = (true_pos[0] + dr, true_pos[1] + dc)
            if true_pos in true_coins:
                true_coins.remove(true_pos)
                
            # 2. Đồng bộ di chuyển cho các vũ trụ
            for u_start, u_data in universes.items():
                if u_data["status"] == "active":
                    r, c = u_data["current"]
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] != 1:
                        u_data["current"] = (nr, nc)
                    else:
                        u_data["current"] = (r, c) # Đụng tường, đứng lại
                        
                    if u_data["current"] in u_data["coins_left"]:
                        u_data["coins_left"].remove(u_data["current"])
                        
            yield {
                "true_pos": true_pos,
                "universes": {k: {"current": v["current"], "coins_left": list(v["coins_left"]), "status": v["status"]} for k, v in universes.items()},
                "status": f"[Đa vũ trụ] Đi {name}. Còn {len(true_coins)} xu thật."
            }

            # 3. Lấy cảm biến và làm mờ các vũ trụ sai
            true_sensor = get_sensor(true_pos, true_coins)
            has_faded = False
            for u_start, u_data in universes.items():
                if u_data["status"] == "active":
                    if get_sensor(u_data["current"], u_data["coins_left"]) != true_sensor:
                        u_data["status"] = "faded"
                        has_faded = True
                        
            if has_faded:
                yield {
                    "true_pos": true_pos,
                    "universes": {k: {"current": v["current"], "coins_left": list(v["coins_left"]), "status": v["status"]} for k, v in universes.items()},
                    "status": "[Đa vũ trụ] Cảm biến! Làm mờ các vũ trụ sai lệnh."
                }
                # Chuyển faded thành invalid
                for u_start, u_data in universes.items():
                    if u_data["status"] == "faded":
                        u_data["status"] = "invalid"

    # Hoàn thành
    yield {
        "true_pos": true_pos,
        "universes": {k: {"current": v["current"], "coins_left": list(v["coins_left"]), "status": v["status"]} for k, v in universes.items()},
        "status": "[Đa vũ trụ] Hoàn tất! Mario thật đã gom hết xu."
    }


def and_or_search(grid, start, initial_coins):
    """
    Sử dụng And-Or Search để tìm một kế hoạch (plan) thu thập tất cả đồng xu.
    Đã bổ sung 30% tỷ lệ dẫm bẫy trong phase thực thi.
    """
    rows, cols = len(grid), len(grid[0])
    
    def get_results(state, action):
        r, c, coins = state
        dr, dc = action
        nr, nc = r + dr, c + dc
        
        if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] != 1:
            new_coins = set(coins)
            if (nr, nc) in new_coins:
                new_coins.remove((nr, nc))
            return [(nr, nc, frozenset(new_coins))]
        return [(r, c, coins)]
        
    def or_search(state, path):
        r, c, coins = state
        if not coins:
            return []
        if state in path:
            return None
            
        for action in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            results = get_results(state, action)
            plan = and_search(results, path + [state])
            if plan is not None:
                return [action, plan]
        return None
        
    def and_search(results, path):
        plan = {}
        for s in results:
            p = or_search(s, path)
            if p is None: return None
            plan[s] = p
        return plan

    yield {
        "current": start,
        "path": [start],
        "coins_left": list(initial_coins),
        "status": "[And-Or] Khởi chạy And-Or Search xây dựng cây kế hoạch..."
    }
    
    plan = or_search((start[0], start[1], frozenset(initial_coins)), [])
    
    if plan is None:
        yield {
            "current": start,
            "path": [start],
            "coins_left": list(initial_coins),
            "status": "[And-Or] Hoàn tất. (Không tìm thấy kế hoạch And-Or)"
        }
        return
        
    current_state = (start[0], start[1], frozenset(initial_coins))
    path_coords = [start]
    current_plan = plan
    
    while current_plan:
        action, subplan = current_plan
        
        # 30% trap chance
        if random.random() < 0.3:
            yield {
                "current": current_state[:2],
                "path": list(path_coords),
                "coins_left": list(current_state[2]),
                "status": f"[And-Or] Đạp bẫy! Đứng im. (Thử lại {action}...)",
                "trapped": True
            }
            continue # Retry the same action
            
        results = get_results(current_state, action)
        next_state = results[0]
        
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
