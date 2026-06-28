import pygame
from .base_world import BasePyGameWorld
from config import VACUUM_MAP, AssetManager, COLOR_BRICK, COLOR_COIN, COLOR_RED, COLOR_DARK, COLOR_PATH, COLOR_WHITE, COLOR_BLACK
from algorithms.complex_env import sensorless_bfs, partially_observable_bfs, and_or_search
from ui import ComboBox, Button, LogPanel

class FogWorld(BasePyGameWorld):
    def __init__(self, screen):
        self.grid = [row[:] for row in VACUUM_MAP]
        self.find_start_and_coins()
        super().__init__(screen, title="World 4: Mario Lụm Xu")
        self.log_panel_width = 220
        self.log_panel = LogPanel(0, 0, self.log_panel_width, screen.get_height(), "Nhật ký AI", self.font)
        self.last_status = None
        self.reset_simulation()

    def find_start_and_coins(self):
        self.start_pos = None
        self.initial_coins = []
        for r in range(len(self.grid)):
            for c in range(len(self.grid[0])):
                if self.grid[r][c] == "S":
                    self.start_pos = (r, c)
                elif self.grid[r][c] == "C":
                    self.initial_coins.append((r, c))

    def setup_ui(self):
        super().setup_ui()
        
        self.algos = [
            "Partially Observable",
            "Sensorless",
            "And-Or Search"
        ]
        self.algo_btn = ComboBox(0, 0, 240, 40, "Mode", self.algos, self.font, on_change=self.on_algo_changed)
        self.buttons.append(self.algo_btn)
        
        self.btn_run = Button(0, 0, 240, 40, "Tự động chạy ▶", self.font, (46, 204, 113), (60, 220, 130), COLOR_WHITE, self.toggle_run)
        self.buttons.append(self.btn_run)
        
        self.btn_step = Button(0, 0, 240, 40, "Chạy từng bước ⏭", self.font, (52, 152, 219), (70, 170, 230), COLOR_WHITE, self.step_one)
        self.buttons.append(self.btn_step)
        
        self.btn_reset = Button(0, 0, 240, 40, "Đặt lại (Reset) ↺", self.font, (231, 76, 60), (250, 90, 80), COLOR_WHITE, self.reset_simulation)
        self.buttons.append(self.btn_reset)
        
        self.stats = {"steps": 0, "ghosts": "-"}
        self.mode_info = ""

    def on_algo_changed(self, algo_name):
        self.reset_simulation()

    def reset_simulation(self):
        self.stop_simulation()
        self.btn_run.set_text("Tự động chạy ▶")
        self.btn_run.bg_color = (46, 204, 113)
        self.current_generator = None
        self.current_state = None
        self.stats = {"steps": 0, "ghosts": "-"}
        self.last_status = None
        if hasattr(self, 'log_panel'):
            self.log_panel.clear()
            self.log_panel.add_log("Bắt đầu khởi tạo...")
        self.set_status("Sẵn sàng...")
        
        self.find_start_and_coins()
        self.current_coins = list(self.initial_coins)
        
        self.real_sensorless_pos = self.start_pos
        self.sensorless_steps = 0
        
        algo_name = self.algo_btn.get_current()
        if algo_name == "Sensorless":
            self.mode_info = "Sensorless: 4 Mario độc lập tìm xu."
        elif algo_name == "Partially Observable":
            self.mode_info = "Partially Observable: Mô phỏng đồng thời 16 vũ trụ song song."
        elif algo_name == "And-Or Search":
            self.mode_info = "And-Or Search: Lập kế hoạch theo cây (Nondeterministic)."
        else:
            self.mode_info = ""

    def get_selected_generator(self):
        algo_name = self.algo_btn.get_current()
        if algo_name == "Sensorless":
            return sensorless_bfs(self.grid, self.start_pos, self.current_coins)
        elif algo_name == "Partially Observable":
            return partially_observable_bfs(self.grid, self.start_pos, self.initial_coins)
        elif algo_name == "And-Or Search":
            return and_or_search(self.grid, self.start_pos, self.initial_coins)
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
        stats_y = 380
        texts = [
            f"Bước đi: {self.stats['steps']}",
            f"Bóng ma: {self.stats['ghosts']}",
        ]
        for i, t in enumerate(texts):
            surf = self.font.render(t, True, COLOR_BLACK)
            surface.blit(surf, (self.sidebar_x + 20, stats_y + i*25))
            
        # Draw mode info
        # Break into multiple lines if needed
        words = self.mode_info.split(' ')
        lines = []
        current_line = ""
        for word in words:
            if self.font.size(current_line + word)[0] < 240:
                current_line += word + " "
            else:
                lines.append(current_line)
                current_line = word + " "
        lines.append(current_line)
        
        y_offset = stats_y + 60
        for line in lines:
            surf = self.font.render(line, True, (100, 100, 100))
            surface.blit(surf, (self.sidebar_x + 20, y_offset))
            y_offset += 20

    def draw_single_grid(self, surface, area, grid, current_pos, coins, known_grid=None, is_sensorless=False, belief_state=None):
        rows, cols = len(grid), len(grid[0])
        cell_size = min(area.width // cols, area.height // rows, 80)
        if cell_size < 1: cell_size = 1
        
        ox = area.x + (area.width - cell_size * cols) // 2
        oy = area.y + (area.height - cell_size * rows) // 2
        
        brick_img = AssetManager().get("brick", size=(cell_size, cell_size))
        coin_img = AssetManager().get("coin", size=(int(cell_size*0.6), int(cell_size*0.6)))
        mario_img = AssetManager().get("mario", size=(int(cell_size*0.8), int(cell_size*0.8)))
        
        for r in range(rows):
            for c in range(cols):
                x = ox + c * cell_size
                y = oy + r * cell_size
                
                # Nền
                if known_grid:
                    val = known_grid[r][c]
                    if val == -1:
                        pygame.draw.rect(surface, COLOR_DARK, (x, y, cell_size, cell_size))
                    elif val == 1:
                        if brick_img:
                            surface.blit(brick_img, (x, y))
                        else:
                            pygame.draw.rect(surface, COLOR_BRICK, (x, y, cell_size, cell_size))
                    else:
                        pygame.draw.rect(surface, (245, 245, 220), (x, y, cell_size, cell_size))
                else:
                    if grid[r][c] == 1:
                        if brick_img:
                            surface.blit(brick_img, (x, y))
                        else:
                            pygame.draw.rect(surface, COLOR_BRICK, (x, y, cell_size, cell_size))
                    else:
                        pygame.draw.rect(surface, (245, 245, 220), (x, y, cell_size, cell_size))
                        
                pygame.draw.rect(surface, (210, 180, 140), (x, y, cell_size, cell_size), 1)
                
                # Xu
                if (r, c) in coins:
                    cx, cy = x + cell_size//2, y + cell_size//2
                    if coin_img:
                        surface.blit(coin_img, (cx - coin_img.get_width()//2, cy - coin_img.get_height()//2))
                    else:
                        pygame.draw.circle(surface, COLOR_COIN, (cx, cy), int(cell_size*0.3))
                        pygame.draw.circle(surface, (230, 126, 34), (cx, cy), int(cell_size*0.3), 2)
                        
        # Vẽ Mario hoặc bóng ma
        if is_sensorless and belief_state is not None:
            for r, c in belief_state:
                cx, cy = ox + c * cell_size + cell_size//2, oy + r * cell_size + cell_size//2
                if len(belief_state) > 1:
                    if (r, c) == getattr(self, 'real_sensorless_pos', (-1, -1)):
                        pygame.draw.circle(surface, (0, 0, 255), (cx, cy), int(cell_size*0.4), 3)
                    else:
                        pygame.draw.circle(surface, COLOR_RED, (cx, cy), int(cell_size*0.4), 2)
                else:
                    if mario_img:
                        surface.blit(mario_img, (cx - mario_img.get_width()//2, cy - mario_img.get_height()//2))
                    else:
                        pygame.draw.circle(surface, COLOR_RED, (cx, cy), int(cell_size*0.4))
        else:
            if current_pos:
                r, c = current_pos
                cx, cy = ox + c * cell_size + cell_size//2, oy + r * cell_size + cell_size//2
                if mario_img:
                    surface.blit(mario_img, (cx - mario_img.get_width()//2, cy - mario_img.get_height()//2))
                else:
                    pygame.draw.circle(surface, COLOR_RED, (cx, cy), int(cell_size*0.4))


    def draw_state(self, state, surface, area):
        self.log_panel.update_height(surface.get_height())
        adjusted_area = pygame.Rect(self.log_panel_width, area.y, area.width - self.log_panel_width, area.height)
        
        rows, cols = len(self.grid), len(self.grid[0])
        algo_name = self.algo_btn.get_current()
        
        if state:
            status_text = state.get("status", "")
            if status_text and status_text != self.last_status:
                self.log_panel.add_log(status_text)
                self.last_status = status_text
            self.set_status(status_text)
            
            if "Thành công" in status_text or "Hoàn tất" in status_text:
                self.stop_simulation()
                self.btn_run.set_text("Tự động chạy ▶")
                self.btn_run.bg_color = (46, 204, 113)

            if algo_name == "Sensorless":
                m1 = state.get("mario1", {})
                m2 = state.get("mario2", {})
                m3 = state.get("mario3", {})
                m4 = state.get("mario4", {})
                
                half_w = adjusted_area.width // 2
                half_h = adjusted_area.height // 2
                
                area1 = pygame.Rect(adjusted_area.x, adjusted_area.y, half_w, half_h)
                area2 = pygame.Rect(adjusted_area.x + half_w, adjusted_area.y, half_w, half_h)
                area3 = pygame.Rect(adjusted_area.x, adjusted_area.y + half_h, half_w, half_h)
                area4 = pygame.Rect(adjusted_area.x + half_w, adjusted_area.y + half_h, half_w, half_h)
                
                # Draw separators
                pygame.draw.line(surface, COLOR_BLACK, (area2.x, adjusted_area.y), (area2.x, adjusted_area.y + adjusted_area.height), 3)
                pygame.draw.line(surface, COLOR_BLACK, (adjusted_area.x, area3.y), (adjusted_area.x + adjusted_area.width, area3.y), 3)
                
                self.draw_single_grid(surface, area1, self.grid, m1.get("current", self.start_pos), set(m1.get("coins_left", self.current_coins)))
                self.draw_single_grid(surface, area2, self.grid, m2.get("current", self.start_pos), set(m2.get("coins_left", self.current_coins)))
                self.draw_single_grid(surface, area3, self.grid, m3.get("current", self.start_pos), set(m3.get("coins_left", self.current_coins)))
                self.draw_single_grid(surface, area4, self.grid, m4.get("current", self.start_pos), set(m4.get("coins_left", self.current_coins)))
                self.log_panel.draw(surface)
                return
                
            elif algo_name == "Partially Observable":
                universes = state.get("universes", {})
                rows, cols = len(self.grid), len(self.grid[0])
                w = adjusted_area.width // cols
                h = adjusted_area.height // rows
                
                for r in range(rows):
                    for c in range(cols):
                        u_area = pygame.Rect(adjusted_area.x + c * w, adjusted_area.y + r * h, w, h)
                        u_data = universes.get((r, c))
                        
                        if u_data and u_data["status"] != "invalid":
                            inner_rect = u_area.inflate(-4, -4)
                            self.draw_single_grid(surface, inner_rect, self.grid, u_data["current"], u_data["coins_left"])
                            if (r, c) == self.start_pos:
                                pygame.draw.rect(surface, (0, 255, 0), u_area, 3) # True Mario border
                            
                            if u_data["status"] == "faded":
                                overlay = pygame.Surface((w, h), pygame.SRCALPHA)
                                overlay.fill((0, 0, 0, 180))
                                surface.blit(overlay, u_area.topleft)
                        else:
                            # Tường hoặc đã invalid
                            pygame.draw.rect(surface, (50, 50, 50), u_area)
                        pygame.draw.rect(surface, COLOR_BLACK, u_area, 1)
                self.log_panel.draw(surface)
                return

        # Non-independent single grid draw
        if algo_name == "Sensorless" and not state:
            half_w = adjusted_area.width // 2
            half_h = adjusted_area.height // 2
            
            area1 = pygame.Rect(adjusted_area.x, adjusted_area.y, half_w, half_h)
            area2 = pygame.Rect(adjusted_area.x + half_w, adjusted_area.y, half_w, half_h)
            area3 = pygame.Rect(adjusted_area.x, adjusted_area.y + half_h, half_w, half_h)
            area4 = pygame.Rect(adjusted_area.x + half_w, adjusted_area.y + half_h, half_w, half_h)
            
            # Draw separators
            pygame.draw.line(surface, COLOR_BLACK, (area2.x, adjusted_area.y), (area2.x, adjusted_area.y + adjusted_area.height), 3)
            pygame.draw.line(surface, COLOR_BLACK, (adjusted_area.x, area3.y), (adjusted_area.x + adjusted_area.width, area3.y), 3)
            
            self.draw_single_grid(surface, area1, self.grid, self.start_pos, self.current_coins)
            self.draw_single_grid(surface, area2, self.grid, self.start_pos, self.current_coins)
            self.draw_single_grid(surface, area3, self.grid, self.start_pos, self.current_coins)
            self.draw_single_grid(surface, area4, self.grid, self.start_pos, self.current_coins)
            self.log_panel.draw(surface)
            return
            
        if algo_name == "Partially Observable" and not state:
            rows, cols = len(self.grid), len(self.grid[0])
            w = adjusted_area.width // cols
            h = adjusted_area.height // rows
            
            for r in range(rows):
                for c in range(cols):
                    u_area = pygame.Rect(adjusted_area.x + c * w, adjusted_area.y + r * h, w, h)
                    if self.grid[r][c] != 1:
                        inner_rect = u_area.inflate(-4, -4)
                        self.draw_single_grid(surface, inner_rect, self.grid, (r, c), self.current_coins)
                        if (r, c) == self.start_pos:
                            pygame.draw.rect(surface, (0, 255, 0), u_area, 3)
                    else:
                        pygame.draw.rect(surface, (50, 50, 50), u_area)
                    pygame.draw.rect(surface, COLOR_BLACK, u_area, 1)
            self.log_panel.draw(surface)
            return

        if algo_name == "And-Or Search":
            if not state:
                self.draw_single_grid(surface, adjusted_area, self.grid, self.start_pos, self.current_coins)
            else:
                path = state.get("path", [])
                if path:
                    self.stats["steps"] = len(path)
                current_pos = state.get("current") if state else self.start_pos
                coins_left = state.get("coins_left", self.current_coins)
                self.draw_single_grid(surface, adjusted_area, self.grid, current_pos, coins_left)
                
                if state.get("trapped"):
                    rows, cols = len(self.grid), len(self.grid[0])
                    cell_size = min(adjusted_area.width // cols, adjusted_area.height // rows, 80)
                    if cell_size < 1: cell_size = 1
                    
                    ox = adjusted_area.x + (adjusted_area.width - cell_size * cols) // 2
                    oy = adjusted_area.y + (adjusted_area.height - cell_size * rows) // 2
                    
                    cx = ox + current_pos[1] * cell_size + cell_size // 2
                    cy = oy + current_pos[0] * cell_size + cell_size // 2
                    
                    # Draw a red cross over Mario
                    pygame.draw.line(surface, (255, 0, 0), (cx - cell_size//3, cy - cell_size//3), (cx + cell_size//3, cy + cell_size//3), 6)
                    pygame.draw.line(surface, (255, 0, 0), (cx + cell_size//3, cy - cell_size//3), (cx - cell_size//3, cy + cell_size//3), 6)
                    
                    # Draw TRAP text
                    trap_font = pygame.font.SysFont("Courier New", int(cell_size*0.4), bold=True)
                    text_surf = trap_font.render("TRAP!", True, (255, 0, 0))
                    outline_surf = trap_font.render("TRAP!", True, (255, 255, 255))
                    surface.blit(outline_surf, (cx - text_surf.get_width()//2 + 1, cy - cell_size//2 - text_surf.get_height() + 1))
                    surface.blit(text_surf, (cx - text_surf.get_width()//2, cy - cell_size//2 - text_surf.get_height()))
                    
            self.log_panel.draw(surface)
            return

    def draw_annotation(self, surface, area):
        adjusted_area = pygame.Rect(self.log_panel_width, area.y, area.width - self.log_panel_width, area.height)
        pygame.draw.rect(surface, (250, 250, 250), adjusted_area)
        pygame.draw.line(surface, (200, 200, 200), (adjusted_area.x, adjusted_area.y), (adjusted_area.x + adjusted_area.width, adjusted_area.y), 2)
        
        text_surf = self.font.render("Nhiệm vụ: Bản đồ bị sương mù che khuất, hãy chọn cách để gom toàn bộ xu vàng.", True, COLOR_BLACK)
        surface.blit(text_surf, (adjusted_area.x + 10, adjusted_area.y + 10))
        
        legend_y = adjusted_area.y + 40
        
        # Sương mù
        pygame.draw.rect(surface, COLOR_DARK, (adjusted_area.x + 10, legend_y, 20, 20))
        surface.blit(self.font.render("Sương mù", True, COLOR_BLACK), (adjusted_area.x + 35, legend_y + 2))
        
        # Đồng xu
        coin_img = AssetManager().get("coin", size=(20, 20))
        if coin_img:
            surface.blit(coin_img, (adjusted_area.x + 120, legend_y))
        else:
            pygame.draw.circle(surface, COLOR_COIN, (adjusted_area.x + 130, legend_y + 10), 10)
        surface.blit(self.font.render("Đồng xu", True, COLOR_BLACK), (adjusted_area.x + 145, legend_y + 2))
        
        # Mario
        mario_img = AssetManager().get("mario", size=(20, 20))
        if mario_img:
            surface.blit(mario_img, (adjusted_area.x + 220, legend_y))
        else:
            pygame.draw.circle(surface, COLOR_RED, (adjusted_area.x + 230, legend_y + 10), 10)
        surface.blit(self.font.render("Mario", True, COLOR_BLACK), (adjusted_area.x + 245, legend_y + 2))

