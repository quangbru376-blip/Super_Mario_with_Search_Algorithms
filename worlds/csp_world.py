import pygame
from .base_world import BasePyGameWorld
from config import AssetManager, COLOR_RED, COLOR_WHITE, COLOR_BLACK, CSP_REGIONS_MAP
from algorithms.csp import backtracking_search, forward_checking_search, min_conflicts_search
from ui import ComboBox, Button, LogPanel

BLOCK_COLORS = {
    "Đỏ": (231, 76, 60),
    "Cam": (230, 126, 34),
    "Vàng": (241, 196, 15),
    "Lục": (46, 204, 113),
    "Lam": (52, 152, 219),
    "Tím": (155, 89, 182),
    "Đen": (0, 0, 0)
}

INITIAL_CONSTRAINTS = {
    0: "Đỏ",
    3: "Cam",
    5: "Tím"
}

class CspWorld(BasePyGameWorld):
    def __init__(self, screen):
        self.region_map = CSP_REGIONS_MAP
        self.rows = len(self.region_map)
        self.cols = len(self.region_map[0])
        self.variables, self.neighbors_map = self.extract_regions()
        super().__init__(screen, title="World 5: Giải đố xếp gạch (CSP)")
        self.log_panel_width = 220
        self.log_panel = LogPanel(0, 0, self.log_panel_width, screen.get_height(), "Nhật ký chạy", self.font)
        self.last_status = ""
        self.reset_simulation()

    def setup_ui(self):
        super().setup_ui()
        
        self.algos = [
            "Backtracking Search", 
            "Forward Checking", 
            "Min-Conflicts Search"
        ]
        self.algo_btn = ComboBox(0, 0, 240, 40, "Algo", self.algos, self.font, on_change=self.on_algo_changed)
        self.buttons.append(self.algo_btn)
        
        self.btn_run = Button(0, 0, 240, 40, "Tự động chạy ▶", self.font, (46, 204, 113), (60, 220, 130), COLOR_WHITE, self.toggle_run)
        self.buttons.append(self.btn_run)
        
        self.btn_step = Button(0, 0, 240, 40, "Chạy từng bước ⏭", self.font, (52, 152, 219), (70, 170, 230), COLOR_WHITE, self.step_one)
        self.buttons.append(self.btn_step)
        
        self.btn_reset = Button(0, 0, 240, 40, "Đặt lại (Reset) ↺", self.font, (231, 76, 60), (250, 90, 80), COLOR_WHITE, self.reset_simulation)
        self.buttons.append(self.btn_reset)
        
        self.stats = {"steps": 0, "backtracks": 0}

    def extract_regions(self):
        variables = set()
        neighbors_map = {}
        
        for r in range(self.rows):
            for c in range(self.cols):
                region_id = self.region_map[r][c]
                variables.add(region_id)
                if region_id not in neighbors_map:
                    neighbors_map[region_id] = set()
                    
                # Check 4 neighbors
                for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    nr, nc = r+dr, c+dc
                    if 0 <= nr < self.rows and 0 <= nc < self.cols:
                        neighbor_id = self.region_map[nr][nc]
                        if neighbor_id != region_id:
                            neighbors_map[region_id].add(neighbor_id)
                            
        for k in neighbors_map:
            neighbors_map[k] = list(neighbors_map[k])
            
        return list(variables), neighbors_map

    def on_algo_changed(self, algo_name):
        self.reset_simulation()

    def reset_simulation(self):
        self.stop_simulation()
        self.btn_run.set_text("Tự động chạy ▶")
        self.btn_run.bg_color = (46, 204, 113)
        self.current_generator = None
        self.current_state = None
        self.stats = {"steps": 0, "backtracks": 0}
        self.set_status("Sẵn sàng...")
        
        self.assignments = dict(INITIAL_CONSTRAINTS)
        self.current_cell = None
        self.conflict_cells = []
        self.domains = None
        if hasattr(self, 'log_panel'):
            self.log_panel.clear()
            self.last_status = ""

    def get_selected_generator(self):
        algo_name = self.algo_btn.get_current()
        domain = list(BLOCK_COLORS.keys())
        if "Backtracking" in algo_name:
            return backtracking_search(self.variables, self.neighbors_map, INITIAL_CONSTRAINTS, domain)
        elif "Forward Checking" in algo_name:
            return forward_checking_search(self.variables, self.neighbors_map, INITIAL_CONSTRAINTS, domain)
        elif "Min-Conflicts" in algo_name:
            return min_conflicts_search(self.variables, self.neighbors_map, INITIAL_CONSTRAINTS, domain)
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
        stats_y = 340
        texts = [
            f"Thử gán: {self.stats['steps']}",
            f"Backtracks: {self.stats['backtracks']}"
        ]
        for i, t in enumerate(texts):
            surf = self.font.render(t, True, COLOR_BLACK)
            surface.blit(surf, (self.sidebar_x + 20, stats_y + i*25))
            
        # Bảng màu
        legend_y = 390
        surf = self.font.render("Bảng màu (Colors):", True, COLOR_BLACK)
        surface.blit(surf, (self.sidebar_x + 20, legend_y))
        
        for i, (col_id, col_rgb) in enumerate(BLOCK_COLORS.items()):
            col_x = self.sidebar_x + 20 + (i % 2) * 130
            row_y = legend_y + 25 + (i // 2) * 25
            pygame.draw.rect(surface, col_rgb, (col_x, row_y, 15, 15))
            pygame.draw.rect(surface, COLOR_BLACK, (col_x, row_y, 15, 15), 1)
            num_surf = self.font.render(col_id, True, COLOR_BLACK)
            surface.blit(num_surf, (col_x + 20, row_y))
            
        # Miền giá trị
        domain_y = legend_y + 25 + (len(BLOCK_COLORS) // 2 + 1) * 25 + 10
        surf = self.font.render("Miền giá trị (Domains):", True, COLOR_BLACK)
        surface.blit(surf, (self.sidebar_x + 20, domain_y))
        
        if self.domains:
            small_font = pygame.font.SysFont("Arial", 12)
            sorted_vars = sorted(list(self.domains.keys()))
            for i, var in enumerate(sorted_vars):
                if self.assignments.get(var) is not None:
                    dom_str = f"Vùng {var}: ={self.assignments[var]}"
                    color = (39, 174, 96) # Green
                else:
                    dom_names = self.domains[var]
                    dom_str = f"Vùng {var}: " + ", ".join(dom_names)
                    color = COLOR_BLACK
                    
                d_surf = small_font.render(dom_str, True, color)
                col_x = self.sidebar_x + 20
                row_y = domain_y + 25 + i * 16
                surface.blit(d_surf, (col_x, row_y))

    def draw_state(self, state, surface, area):
        self.log_panel.update_height(surface.get_height())
        adjusted_area = pygame.Rect(self.log_panel_width, area.y, area.width - self.log_panel_width, area.height)
        
        cell_size = min(adjusted_area.width // self.cols, adjusted_area.height // self.rows)
        if cell_size < 1: cell_size = 1
        
        ox = adjusted_area.x + (adjusted_area.width - cell_size * self.cols) // 2
        oy = adjusted_area.y + (adjusted_area.height - cell_size * self.rows) // 2
        
        if state:
            self.assignments = state.get("assignments", {})
            self.current_cell = state.get("current")
            self.conflict_cells = state.get("conflict_cells", [])
            self.domains = state.get("domains")
            status_text = state.get("status", "")
            
            self.stats["steps"] = state.get("steps", 0)
            self.stats["backtracks"] = state.get("backtracks", 0)
            
            self.set_status(status_text)
            
            if status_text and status_text != self.last_status:
                self.log_panel.add_log(status_text)
                self.last_status = status_text
                
            if "Đã giải quyết" in status_text or "Đã hoàn thành" in status_text or "Không tìm thấy" in status_text:
                self.stop_simulation()
                self.btn_run.set_text("Tự động chạy ▶")
                self.btn_run.bg_color = (46, 204, 113)
                
        brick_img = AssetManager().get("brick", size=(int(cell_size*0.8), int(cell_size*0.8)))
        star_img = AssetManager().get("star", size=(int(cell_size*0.8), int(cell_size*0.8)))
        coin_img = AssetManager().get("coin", size=(int(cell_size*0.8), int(cell_size*0.8)))
        
        # Draw cells
        for r in range(self.rows):
            for c in range(self.cols):
                x = ox + c * cell_size
                y = oy + r * cell_size
                region_id = self.region_map[r][c]
                is_fixed = region_id in INITIAL_CONSTRAINTS
                val = self.assignments.get(region_id)
                
                if val is not None:
                    bg_color = BLOCK_COLORS.get(val, COLOR_WHITE)
                    pygame.draw.rect(surface, bg_color, (x, y, cell_size, cell_size))
                else:
                    pygame.draw.rect(surface, (235, 243, 249), (x, y, cell_size, cell_size))
                    
                if is_fixed:
                    pygame.draw.circle(surface, (39, 174, 96), (x + 10, y + 10), 4)
                    
                # In số ID của vùng vào giữa ô
                id_surf = self.font.render(str(region_id), True, COLOR_BLACK)
                surface.blit(id_surf, id_surf.get_rect(center=(x + cell_size//2, y + cell_size//2)))
                    
        # Draw Highlights for Current and Conflict
        for r in range(self.rows):
            for c in range(self.cols):
                x = ox + c * cell_size
                y = oy + r * cell_size
                region_id = self.region_map[r][c]
                if region_id == self.current_cell:
                    pygame.draw.rect(surface, (241, 196, 15), (x, y, cell_size, cell_size))
                    # Draw inner rect so we can still see the highlight clearly
                    if self.assignments.get(region_id) is not None:
                        bg_color = BLOCK_COLORS.get(self.assignments[region_id], COLOR_WHITE)
                        pygame.draw.rect(surface, bg_color, (x+4, y+4, cell_size-8, cell_size-8))
                        
                if region_id in self.conflict_cells:
                    pygame.draw.rect(surface, (231, 76, 60), (x, y, cell_size, cell_size))
                    if self.assignments.get(region_id) is not None:
                        bg_color = BLOCK_COLORS.get(self.assignments[region_id], COLOR_WHITE)
                        pygame.draw.rect(surface, bg_color, (x+4, y+4, cell_size-8, cell_size-8))

        # Draw Borders
        for r in range(self.rows):
            for c in range(self.cols):
                x = ox + c * cell_size
                y = oy + r * cell_size
                region_id = self.region_map[r][c]
                
                # Right border
                if c < self.cols - 1:
                    if self.region_map[r][c+1] != region_id:
                        pygame.draw.line(surface, COLOR_BLACK, (x + cell_size, y), (x + cell_size, y + cell_size), 4)
                    else:
                        pygame.draw.line(surface, (200, 200, 200), (x + cell_size, y), (x + cell_size, y + cell_size), 1)
                # Bottom border
                if r < self.rows - 1:
                    if self.region_map[r+1][c] != region_id:
                        pygame.draw.line(surface, COLOR_BLACK, (x, y + cell_size), (x + cell_size, y + cell_size), 4)
                    else:
                        pygame.draw.line(surface, (200, 200, 200), (x, y + cell_size), (x + cell_size, y + cell_size), 1)
                        
        # Outer border
        pygame.draw.rect(surface, COLOR_BLACK, (ox, oy, self.cols * cell_size, self.rows * cell_size), 4)
        
        self.log_panel.draw(surface)

    def draw_annotation(self, surface, area):
        adjusted_area = pygame.Rect(self.log_panel_width, area.y, area.width - self.log_panel_width, area.height)
        
        pygame.draw.rect(surface, (250, 250, 250), adjusted_area)
        pygame.draw.line(surface, (200, 200, 200), (adjusted_area.x, adjusted_area.y), (adjusted_area.x + adjusted_area.width, adjusted_area.y), 2)
        
        text_surf = self.font.render("Nhiệm vụ: Chọn thuật toán để tô màu bản đồ sao cho 2 vùng kề nhau không trùng màu.", True, COLOR_BLACK)
        surface.blit(text_surf, (adjusted_area.x + 10, adjusted_area.y + 10))
        
        legend_y = adjusted_area.y + 40
        
        # Vi phạm
        pygame.draw.rect(surface, (231, 76, 60), (adjusted_area.x + 10, legend_y, 20, 20))
        surface.blit(self.font.render("Vi phạm (Conflict)", True, COLOR_BLACK), (adjusted_area.x + 35, legend_y + 2))
        
        # Đang xét
        pygame.draw.rect(surface, (241, 196, 15), (adjusted_area.x + 200, legend_y, 20, 20))
        surface.blit(self.font.render("Đang xét", True, COLOR_BLACK), (adjusted_area.x + 225, legend_y + 2))
        
        # Cố định
        pygame.draw.circle(surface, (39, 174, 96), (adjusted_area.x + 320, legend_y + 10), 6)
        surface.blit(self.font.render("Vùng cố định ban đầu", True, COLOR_BLACK), (adjusted_area.x + 335, legend_y + 2))

