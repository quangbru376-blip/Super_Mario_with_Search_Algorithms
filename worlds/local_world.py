import pygame
from .base_world import BasePyGameWorld
from config import TERRAIN_MAPS, AssetManager, COLOR_RED, COLOR_COIN, COLOR_WHITE, COLOR_BLACK
from algorithms.local_search import simple_hill_climbing, simulated_annealing, local_beam_search
from ui import ComboBox, Button, LogPanel

HEIGHT_COLORS = [
    (39, 174, 96), (46, 204, 113), (162, 217, 206), (118, 215, 196), (247, 220, 111),
    (248, 196, 113), (240, 178, 122), (230, 126, 34), (236, 112, 99), (192, 57, 43)
]

class LocalWorld(BasePyGameWorld):
    def __init__(self, screen):
        super().__init__(screen, title="World 3: Local Search")
        self.map_names = list(TERRAIN_MAPS.keys())
        self.selected_map_name = self.map_names[0]
        self.grid = TERRAIN_MAPS[self.selected_map_name]
        
        self.log_panel_width = 220
        self.log_panel = LogPanel(0, 0, self.log_panel_width, screen.get_height(), "Nhật ký AI", self.font)
        self.last_status = None
        
        self.reset_simulation()
        self.map_btn.set_current(self.selected_map_name)

    def setup_ui(self):
        super().setup_ui()
        
        # Map
        self.map_names = list(TERRAIN_MAPS.keys())
        self.map_btn = ComboBox(0, 0, 240, 40, "Map", self.map_names, self.font, on_change=self.on_map_changed)
        self.buttons.append(self.map_btn)
        
        # Algo
        self.algos = ["Simple Hill Climbing", "Simulated Annealing", "Local Beam (k=2)"]
        self.algo_btn = ComboBox(0, 0, 240, 40, "Algo", self.algos, self.font)
        self.buttons.append(self.algo_btn)
        
        # Actions
        self.btn_run = Button(0, 0, 240, 40, "Tự động chạy ▶", self.font, (46, 204, 113), (60, 220, 130), COLOR_WHITE, self.toggle_run)
        self.buttons.append(self.btn_run)
        
        self.btn_step = Button(0, 0, 240, 40, "Chạy từng bước ⏭", self.font, (52, 152, 219), (70, 170, 230), COLOR_WHITE, self.step_one)
        self.buttons.append(self.btn_step)
        
        self.btn_reset = Button(0, 0, 240, 40, "Đặt lại (Reset) ↺", self.font, (231, 76, 60), (250, 90, 80), COLOR_WHITE, self.reset_simulation)
        self.buttons.append(self.btn_reset)
        
        self.stats = {"steps": 0, "height": "-", "peak_status": "Đang tìm..."}

    def on_map_changed(self, map_name):
        self.selected_map_name = map_name
        self.grid = TERRAIN_MAPS[self.selected_map_name]
        self.reset_simulation()

    def reset_simulation(self):
        self.stop_simulation()
        self.btn_run.set_text("Tự động chạy ▶")
        self.btn_run.bg_color = (46, 204, 113)
        self.current_generator = None
        self.current_state = None
        self.stats = {"steps": 0, "height": "-", "peak_status": "Đang tìm..."}
        self.last_status = None
        if hasattr(self, 'log_panel'):
            self.log_panel.clear()
            self.log_panel.add_log("Bắt đầu khởi tạo...")
        self.set_status("Sẵn sàng...")
        
        if self.selected_map_name == "Đồi đơn đỉnh (Single Peak)":
            self.start_pos = (11, 7)
        else:
            low_cells = []
            for r in range(len(self.grid)):
                for c in range(len(self.grid[0])):
                    if self.grid[r][c] <= 1:
                        low_cells.append((r, c))
            self.start_pos = low_cells[0] if low_cells else (10, 6)
            
        self.mario_pos = self.start_pos
        self.path = [self.mario_pos]

    def get_selected_generator(self):
        algo_name = self.algo_btn.get_current()
        if "Simple" in algo_name: return simple_hill_climbing(self.grid, self.start_pos)
        elif "Annealing" in algo_name: return simulated_annealing(self.grid, self.start_pos)
        elif "Beam" in algo_name: return local_beam_search(self.grid, self.start_pos, k=2)
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
        stats_y = 420
        texts = [
            f"Số bước đi: {self.stats['steps']}",
            f"Độ cao: {self.stats['height']}",
            f"Đỉnh: {self.stats['peak_status']}"
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
        
        star_img = AssetManager().get("star", size=(cell_size, cell_size))
        mario_img = AssetManager().get("mario", size=(cell_size, cell_size))
        
        evaluating = []
        if state:
            self.mario_pos = state.get("current")
            self.path = state.get("visited", [])
            evaluating = state.get("evaluating", [])
            status_text = state.get("status", "")
            
            if status_text != self.last_status:
                self.log_panel.add_log(status_text)
                self.last_status = status_text
            
            if isinstance(self.mario_pos, list):
                current_height = max([self.grid[r][c] for r, c in self.mario_pos])
                if self.path and isinstance(self.path[0], list):
                    self.stats["steps"] = max(len(p) - 1 for p in self.path)
                else:
                    self.stats["steps"] = len(self.path) - 1
            else:
                r, c = self.mario_pos
                current_height = self.grid[r][c]
                self.stats["steps"] = len(self.path) - 1
                
            self.stats["height"] = str(current_height)
            
            if current_height == 9:
                self.stats["peak_status"] = "THÀNH CÔNG (9)"
                self.set_status("Thành công!")
                self.stop_simulation()
                self.btn_run.set_text("Tự động chạy ▶")
                self.btn_run.bg_color = (46, 204, 113)
            elif "Bị kẹt" in status_text:
                self.stats["peak_status"] = f"THẤT BẠI (Kẹt ở {current_height})"
                self.set_status(status_text, is_error=True)
                self.stop_simulation()
                self.btn_run.set_text("Tự động chạy ▶")
                self.btn_run.bg_color = (46, 204, 113)
            else:
                self.set_status(status_text)
                
        # Draw cells
        for r in range(rows):
            for c in range(cols):
                x = ox + c * cell_size
                y = oy + r * cell_size
                h_val = self.grid[r][c]
                bg_color = HEIGHT_COLORS[h_val]
                
                pygame.draw.rect(surface, bg_color, (x, y, cell_size, cell_size))
                pygame.draw.rect(surface, (221, 221, 221), (x, y, cell_size, cell_size), 1)
                
                text_col = COLOR_WHITE if h_val > 4 else COLOR_BLACK
                text_surf = self.font.render(str(h_val), True, text_col)
                text_rect = text_surf.get_rect(center=(x + cell_size//2, y + cell_size//2))
                surface.blit(text_surf, text_rect)
                
                if h_val == 9:
                    if star_img:
                        surface.blit(star_img, (x, y))
                    else:
                        pygame.draw.rect(surface, COLOR_COIN, (x+4, y+4, cell_size-8, cell_size-8), 2)
                        
        # Draw path trace
        if self.path:
            if isinstance(self.path[0], list):
                for single_path in self.path:
                    if len(single_path) > 1:
                        points = [(ox + c*cell_size + cell_size//2, oy + r*cell_size + cell_size//2) for r, c in single_path]
                        pygame.draw.lines(surface, COLOR_RED, False, points, 3)
            elif len(self.path) > 1:
                points = [(ox + c*cell_size + cell_size//2, oy + r*cell_size + cell_size//2) for r, c in self.path]
                pygame.draw.lines(surface, COLOR_RED, False, points, 3)
            
        # Draw evaluating
        for r, c in evaluating:
            x = ox + c * cell_size
            y = oy + r * cell_size
            pygame.draw.rect(surface, (241, 196, 15), (x, y, cell_size, cell_size), 3)
            
        # Draw Mario
        if self.mario_pos:
            mario_positions = self.mario_pos if isinstance(self.mario_pos, list) else [self.mario_pos]
            for r, c in mario_positions:
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
        
        text_surf = self.font.render("Nhiệm vụ: Mario đang ở vùng đồi núi, hãy dùng thuật toán Local Search để tìm được đỉnh cao nhất.", True, COLOR_BLACK)
        surface.blit(text_surf, (adjusted_area.x + 10, adjusted_area.y + 10))
        
        legend_y = adjusted_area.y + 40
        
        # Độ cao
        surface.blit(self.font.render("Thấp", True, COLOR_BLACK), (adjusted_area.x + 10, legend_y + 2))
        for i, color in enumerate(HEIGHT_COLORS):
            pygame.draw.rect(surface, color, (adjusted_area.x + 45 + i*15, legend_y, 15, 20))
        surface.blit(self.font.render("Cao", True, COLOR_BLACK), (adjusted_area.x + 50 + len(HEIGHT_COLORS)*15, legend_y + 2))
        
        # Mario
        mario_img = AssetManager().get("mario", size=(20, 20))
        if mario_img:
            surface.blit(mario_img, (adjusted_area.x + 250, legend_y))
        else:
            pygame.draw.circle(surface, COLOR_RED, (adjusted_area.x + 260, legend_y + 10), 10)
        surface.blit(self.font.render("Mario", True, COLOR_BLACK), (adjusted_area.x + 275, legend_y + 2))
        
        # Đỉnh cao nhất
        star_img = AssetManager().get("star", size=(20, 20))
        if star_img:
            surface.blit(star_img, (adjusted_area.x + 330, legend_y))
        else:
            pygame.draw.rect(surface, COLOR_COIN, (adjusted_area.x + 330, legend_y, 20, 20), 2)
        surface.blit(self.font.render("Đỉnh", True, COLOR_BLACK), (adjusted_area.x + 355, legend_y + 2))

