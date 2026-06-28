import pygame
from .base_world import BasePyGameWorld
from config import MAZE_MAPS, AssetManager, COLOR_BRICK, COLOR_COIN, COLOR_RED, COLOR_VISITED, COLOR_FRONTIER, COLOR_PATH, COLOR_SWAMP, COLOR_SKY, COLOR_WHITE, COLOR_BLACK
from algorithms.pathfinding import bfs, dfs, ucs, greedy, astar, idastar
from ui import ComboBox, Button, LogPanel

class MazeWorld(BasePyGameWorld):
    def __init__(self, screen):
        super().__init__(screen, title="World 1 & 2: Maze")
        self.map_names = list(MAZE_MAPS.keys())
        self.selected_map_name = self.map_names[0]
        self.grid = MAZE_MAPS[self.selected_map_name]
        self.log_panel_width = 220
        self.log_panel = LogPanel(0, 0, self.log_panel_width, screen.get_height(), "Nhật ký AI", self.font)
        self.last_status = None
        self.find_start_and_goal()
        self.map_btn.set_current(self.selected_map_name)
        
    def find_start_and_goal(self):
        self.start_pos = None
        self.goal_pos = None
        for r in range(len(self.grid)):
            for c in range(len(self.grid[0])):
                if self.grid[r][c] == "S":
                    self.start_pos = (r, c)
                elif self.grid[r][c] == "G":
                    self.goal_pos = (r, c)

    def setup_ui(self):
        super().setup_ui()
        
        # Map CycleButton
        self.map_names = list(MAZE_MAPS.keys())
        self.map_btn = ComboBox(0, 0, 240, 40, "Map", self.map_names, self.font, on_change=self.on_map_changed)
        self.buttons.append(self.map_btn)
        
        # Algo CycleButton
        self.algos = ["BFS", "DFS", "UCS", "Greedy", "A*", "IDA*"]
        self.algo_btn = ComboBox(0, 0, 240, 40, "Algo", self.algos, self.font)
        self.buttons.append(self.algo_btn)
        
        # Action Buttons
        self.btn_run = Button(0, 0, 240, 40, "Tự động chạy ▶", self.font, (46, 204, 113), (60, 220, 130), COLOR_WHITE, self.toggle_run)
        self.buttons.append(self.btn_run)
        
        self.btn_step = Button(0, 0, 240, 40, "Chạy từng bước ⏭", self.font, (52, 152, 219), (70, 170, 230), COLOR_WHITE, self.step_one)
        self.buttons.append(self.btn_step)
        
        self.btn_reset = Button(0, 0, 240, 40, "Đặt lại (Reset) ↺", self.font, (231, 76, 60), (250, 90, 80), COLOR_WHITE, self.reset_simulation)
        self.buttons.append(self.btn_reset)
        
        self.stats = {"steps": 0, "visited": 0, "path_len": 0, "path_cost": 0}

    def on_map_changed(self, map_name):
        self.selected_map_name = map_name
        self.grid = MAZE_MAPS[self.selected_map_name]
        self.find_start_and_goal()
        self.reset_simulation()

    def reset_simulation(self):
        self.stop_simulation()
        self.btn_run.set_text("Tự động chạy ▶")
        self.btn_run.bg_color = (46, 204, 113)
        self.current_generator = None
        self.current_state = None
        self.stats = {"steps": 0, "visited": 0, "path_len": 0, "path_cost": 0}
        self.last_status = None
        if hasattr(self, 'log_panel'):
            self.log_panel.clear()
            self.log_panel.add_log("Bắt đầu khởi tạo...")
        self.set_status("Sẵn sàng...")

    def get_selected_generator(self):
        algo_name = self.algo_btn.get_current()
        if algo_name == "BFS": return bfs(self.grid, self.start_pos, self.goal_pos)
        elif algo_name == "DFS": return dfs(self.grid, self.start_pos, self.goal_pos)
        elif algo_name == "UCS": return ucs(self.grid, self.start_pos, self.goal_pos)
        elif algo_name == "Greedy": return greedy(self.grid, self.start_pos, self.goal_pos)
        elif algo_name == "A*": return astar(self.grid, self.start_pos, self.goal_pos)
        elif algo_name == "IDA*": return idastar(self.grid, self.start_pos, self.goal_pos)
        return None

    def toggle_run(self):
        if self.is_simulating:
            self.stop_simulation()
            self.btn_run.set_text("Tiếp tục ▶")
            self.btn_run.bg_color = (46, 204, 113)
        else:
            if not self.current_generator:
                self.current_generator = self.get_selected_generator()
            self.btn_run.set_text("Tạm dừng ⏸")
            self.btn_run.bg_color = (241, 196, 15)
            self.start_simulation(self.current_generator)

    def step_one(self):
        if self.is_simulating:
            self.toggle_run()
        if not self.current_generator:
            self.current_generator = self.get_selected_generator()
        try:
            self.current_state = next(self.current_generator)
        except StopIteration:
            self.on_simulation_end()

    def draw_sidebar(self, surface):
        super().draw_sidebar(surface)
        w, h = surface.get_size()
        stats_y = 420
        texts = [
            f"Số bước duyệt: {self.stats['steps']}",
            f"Số ô đã qua (visited): {self.stats['visited']}",
            f"Số ô đường đi: {self.stats['path_len']}",
            f"Tổng chi phí: {self.stats.get('path_cost', 0)}"
        ]
        for i, t in enumerate(texts):
            surf = self.font.render(t, True, COLOR_BLACK)
            surface.blit(surf, (self.sidebar_x + 20, stats_y + i*25))

    def draw_state(self, state, surface, area):
        self.log_panel.update_height(surface.get_height())
        adjusted_area = pygame.Rect(self.log_panel_width, area.y, area.width - self.log_panel_width, area.height)
        
        rows, cols = len(self.grid), len(self.grid[0])
        cell_size = min(adjusted_area.width // cols, adjusted_area.height // rows)
        if cell_size < 1: cell_size = 1
        
        ox, oy = self.draw_grid(surface, adjusted_area, rows, cols, cell_size)
        
        mario_img = AssetManager().get("mario", size=(cell_size, cell_size))
        brick_img = AssetManager().get("brick", size=(cell_size, cell_size))
        castle_img = AssetManager().get("castle", size=(cell_size, cell_size))
        
        # Base grid
        for r in range(rows):
            for c in range(cols):
                x = ox + c * cell_size
                y = oy + r * cell_size
                cell = self.grid[r][c]
                if cell == 1:
                    if brick_img:
                        surface.blit(brick_img, (x, y))
                    else:
                        pygame.draw.rect(surface, COLOR_BRICK, (x, y, cell_size, cell_size))
                elif cell == "G":
                    if castle_img:
                        surface.blit(castle_img, (x, y))
                    else:
                        pygame.draw.rect(surface, COLOR_COIN, (x+4, y+4, cell_size-8, cell_size-8))
                elif cell == 2:
                    pygame.draw.rect(surface, COLOR_SWAMP, (x, y, cell_size, cell_size))
        
        current = None
        visited = []
        frontier = []
        path = None
        
        if state:
            status_text = state.get("status", "")
            if status_text and status_text != self.last_status:
                self.log_panel.add_log(status_text)
                self.last_status = status_text
                
            current = state.get("current")
            frontier = state.get("frontier", [])
            visited = state.get("visited", [])
            path = state.get("path")
            
            self.stats["steps"] = len(visited)
            self.stats["visited"] = len(visited)
            
            for r, c in visited:
                if (r, c) != self.start_pos and (r, c) != self.goal_pos:
                    pygame.draw.rect(surface, COLOR_VISITED, (ox+c*cell_size, oy+r*cell_size, cell_size, cell_size))
            
            for r, c in frontier:
                if (r, c) != self.start_pos and (r, c) != self.goal_pos:
                    pygame.draw.rect(surface, COLOR_FRONTIER, (ox+c*cell_size, oy+r*cell_size, cell_size, cell_size))
                    
            if path:
                self.stats["path_len"] = len(path)
                
                # Calculate total cost
                cost = 0
                for r, c in path:
                    if (r, c) != self.start_pos: # Usually we don't count start pos cost, but here each move to a cell has a cost
                        cost += 5 if self.grid[r][c] == 2 else 1
                self.stats["path_cost"] = cost
                
                points = [(ox + c*cell_size + cell_size//2, oy + r*cell_size + cell_size//2) for r, c in path]
                if len(points) > 1:
                    pygame.draw.lines(surface, COLOR_PATH, False, points, 4)
                self.stop_simulation()
                self.btn_run.set_text("Tự động chạy ▶")
                self.btn_run.bg_color = (46, 204, 113)
            elif path is not None and len(path) == 0:
                self.set_status("Mê cung không có lối thoát!", is_error=True)
                self.stop_simulation()
                self.btn_run.set_text("Tự động chạy ▶")
                self.btn_run.bg_color = (46, 204, 113)
                
            if current and not path:
                r, c = current
                pygame.draw.rect(surface, (231, 76, 60), (ox+c*cell_size, oy+r*cell_size, cell_size, cell_size), 3)

        # Draw Mario
        mario_pos = self.start_pos
        if current: mario_pos = current
        if path and len(path) > 0: mario_pos = self.goal_pos
        
        r, c = mario_pos
        x = ox + c * cell_size
        y = oy + r * cell_size
        if mario_img:
            surface.blit(mario_img, (x, y))
        else:
            pygame.draw.circle(surface, COLOR_RED, (x+cell_size//2, y+cell_size//2), cell_size//2 - 2)
            
        self.log_panel.draw(surface)

    def draw_annotation(self, surface, area):
        adjusted_area = pygame.Rect(self.log_panel_width, area.y, area.width - self.log_panel_width, area.height)
        pygame.draw.rect(surface, (250, 250, 250), adjusted_area)
        pygame.draw.line(surface, (200, 200, 200), (adjusted_area.x, adjusted_area.y), (adjusted_area.x + adjusted_area.width, adjusted_area.y), 2)
        
        text_surf = self.font.render("Nhiệm vụ: Mario bị lạc vào mê cung, hãy chọn thuật toán để giúp Mario thoát khỏi đây.", True, COLOR_BLACK)
        surface.blit(text_surf, (adjusted_area.x + 10, adjusted_area.y + 10))
        
        legend_y = adjusted_area.y + 40
        
        # Tường
        brick_img = AssetManager().get("brick", size=(20, 20))
        if brick_img:
            surface.blit(brick_img, (adjusted_area.x + 10, legend_y))
        else:
            pygame.draw.rect(surface, COLOR_BRICK, (adjusted_area.x + 10, legend_y, 20, 20))
        surface.blit(self.font.render("Tường", True, COLOR_BLACK), (adjusted_area.x + 35, legend_y + 2))
        
        # Đầm lầy
        pygame.draw.rect(surface, COLOR_SWAMP, (adjusted_area.x + 110, legend_y, 20, 20))
        surface.blit(self.font.render("Đầm lầy (C: 5)", True, COLOR_BLACK), (adjusted_area.x + 135, legend_y + 2))
        
        # Đích
        castle_img = AssetManager().get("castle", size=(20, 20))
        if castle_img:
            surface.blit(castle_img, (adjusted_area.x + 290, legend_y))
        else:
            pygame.draw.rect(surface, COLOR_COIN, (adjusted_area.x + 290, legend_y, 20, 20))
        surface.blit(self.font.render("Đích", True, COLOR_BLACK), (adjusted_area.x + 315, legend_y + 2))
        
        legend_y2 = legend_y + 30
        
        # Đã duyệt
        pygame.draw.rect(surface, COLOR_VISITED, (adjusted_area.x + 10, legend_y2, 20, 20))
        surface.blit(self.font.render("Đã duyệt", True, COLOR_BLACK), (adjusted_area.x + 35, legend_y2 + 2))
        
        # Frontier
        pygame.draw.rect(surface, COLOR_FRONTIER, (adjusted_area.x + 130, legend_y2, 20, 20))
        surface.blit(self.font.render("Frontier", True, COLOR_BLACK), (adjusted_area.x + 155, legend_y2 + 2))
        
        # Đường đi
        pygame.draw.rect(surface, COLOR_PATH, (adjusted_area.x + 260, legend_y2, 20, 20))
        surface.blit(self.font.render("Đường đi", True, COLOR_BLACK), (adjusted_area.x + 285, legend_y2 + 2))

