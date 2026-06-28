import pygame
from .base_world import BasePyGameWorld
from config import AssetManager, COLOR_RED, COLOR_GREEN, COLOR_WHITE, COLOR_BLACK, COLOR_GRAY, COLOR_SKY
from algorithms.adversarial import minimax_gen, alphabeta_gen, expectimax_gen, check_winner
from ui import ComboBox, Button, LogPanel

class BossWorld(BasePyGameWorld):
    def __init__(self, screen):
        self.log_panel_width = 220
        super().__init__(screen, title="World 6: Boss Battle (Tic-Tac-Toe)")
        self.log_panel = LogPanel(0, 0, self.log_panel_width, screen.get_height(), "Nhật ký AI", self.font)
        
        self.board = [0] * 9
        self.turn = 1 # 1: X, -1: O
        self.game_over = False
        self.scores = {}
        self.last_status = None
        
        self.reset_game()

    def setup_ui(self):
        super().setup_ui()
        
        # Cập nhật danh sách ComboBoxes
        self.algos_x = ["Người chơi (Human)", "Minimax", "Alpha-Beta", "Expectimax"]
        self.algos_o = ["Minimax", "Alpha-Beta", "Expectimax"]
        
        self.player_x_btn = ComboBox(0, 0, 240, 40, "X", self.algos_x, self.font)
        self.player_x_btn.set_current("Người chơi (Human)")
        self.buttons.append(self.player_x_btn)
        
        self.player_o_btn = ComboBox(0, 0, 240, 40, "O", self.algos_o, self.font)
        self.player_o_btn.set_current("Minimax")
        self.buttons.append(self.player_o_btn)
        
        self.btn_run = Button(0, 0, 240, 40, "Tự động chạy ▶", self.font, (46, 204, 113), (60, 220, 130), COLOR_WHITE, self.toggle_run)
        self.buttons.append(self.btn_run)
        
        self.btn_step = Button(0, 0, 240, 40, "Chạy từng bước ⏭", self.font, (52, 152, 219), (70, 170, 230), COLOR_WHITE, self.step_one)
        self.buttons.append(self.btn_step)
        
        self.btn_reset = Button(0, 0, 240, 40, "Đặt lại (Reset) ↺", self.font, (231, 76, 60), (250, 90, 80), COLOR_WHITE, self.reset_game)
        self.buttons.append(self.btn_reset)
        
        # Chỉnh lại speed cho hợp lý (vì đệ quy top-level không chạy ngầm mà gộp vào generator)
        # Nút speed_btn đã được thêm ở BasePyGameWorld, set về 500ms
        self.speed_btn.set_current(500)

    def reset_game(self):
        self.board = [0] * 9
        self.turn = 1
        self.game_over = False
        self.scores = {}
        self.stop_simulation()
        if hasattr(self, 'btn_run'):
            self.btn_run.set_text("Tự động chạy ▶")
            self.btn_run.bg_color = (46, 204, 113)
        self.current_generator = None
        self.current_state = None
        self.log_panel.clear()
        self.log_panel.add_log("Đã bắt đầu ván mới. Lượt của X.")
        self.set_status("Lượt của X")

    def get_algo_generator(self, player_type, is_max):
        if "Minimax" in player_type:
            return minimax_gen(self.board, is_max)
        elif "Alpha-Beta" in player_type:
            return alphabeta_gen(self.board, is_max)
        elif "Expectimax" in player_type:
            return expectimax_gen(self.board, is_max)
        return None

    def process_events(self, events):
        if self.game_over or self.is_simulating:
            return
            
        current_player_type = self.player_x_btn.get_current() if self.turn == 1 else self.player_o_btn.get_current()
        
        if "Human" in current_player_type and self.turn == 1:
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    area = pygame.Rect(0, 0, self.sidebar_x, self.screen.get_height() - 110)
                    adjusted_area = pygame.Rect(self.log_panel_width, area.y, area.width - self.log_panel_width, area.height)
                    
                    cell_size = min(adjusted_area.width // 3, adjusted_area.height // 3)
                    if cell_size < 1: cell_size = 1
                    
                    ox = adjusted_area.x + (adjusted_area.width - cell_size * 3) // 2
                    oy = adjusted_area.y + (adjusted_area.height - cell_size * 3) // 2
                    
                    mx, my = event.pos
                    if ox <= mx < ox + 3 * cell_size and oy <= my < oy + 3 * cell_size:
                        c = int((mx - ox) // cell_size)
                        r = int((my - oy) // cell_size)
                        idx = r * 3 + c
                        if self.board[idx] == 0:
                            self.board[idx] = self.turn
                            self.scores = {}
                            self.check_game_state()

    def toggle_run(self):
        if self.is_simulating:
            self.stop_simulation()
            self.btn_run.set_text("Tiếp tục ▶")
            self.btn_run.bg_color = (46, 204, 113)
        else:
            self.btn_run.set_text("Tạm dừng ⏸")
            self.btn_run.bg_color = (241, 196, 15)
            self.check_and_start_ai()
            if self.current_generator:
                self.is_simulating = True

    def step_one(self):
        if self.is_simulating:
            self.toggle_run()
            
        self.check_and_start_ai()
        if self.current_generator:
            try:
                self.current_state = next(self.current_generator)
                self.process_current_state()
            except StopIteration:
                self.current_generator = None

    def check_and_start_ai(self):
        if not self.current_generator and not self.game_over:
            current_player_type = self.player_x_btn.get_current() if self.turn == 1 else self.player_o_btn.get_current()
            if "Human" not in current_player_type:
                is_max = (self.turn == 1)
                self.current_generator = self.get_algo_generator(current_player_type, is_max)

    def process_current_state(self):
        if self.current_state:
            self.scores = self.current_state.get("scores", {})
            status = self.current_state.get("status", "")
            if status != self.last_status:
                self.log_panel.add_log(status)
                self.set_status(status)
                self.last_status = status
                
            if self.current_state.get("done", False):
                best_action = self.current_state.get("best_action")
                if best_action is not None:
                    self.board[best_action] = self.turn
                    self.scores = {}
                self.current_generator = None
                self.current_state = None
                self.check_game_state()

    def update(self):
        if self.game_over:
            return
            
        # Nếu đang ở chế độ "Tự động chạy"
        if self.is_simulating:
            self.check_and_start_ai()
            self.process_current_state()

    def check_game_state(self):
        w = check_winner(self.board)
        if w is not None:
            self.game_over = True
            if w == 1:
                msg = "X Thắng!"
            elif w == -1:
                msg = "Bowser (O) Thắng!"
            else:
                msg = "Hòa!"
            self.log_panel.add_log(msg)
            self.set_status(msg)
        else:
            self.turn *= -1
            player = "X" if self.turn == 1 else "O"
            self.log_panel.add_log(f"Lượt của {player}")
            self.set_status(f"Lượt của {player}")

    def draw_state(self, state, surface, area):
        self.log_panel.update_height(surface.get_height())
        adjusted_area = pygame.Rect(self.log_panel_width, area.y, area.width - self.log_panel_width, area.height)
        
        pygame.draw.rect(surface, (245, 246, 250), adjusted_area)
        
        cell_size = min(adjusted_area.width // 3, adjusted_area.height // 3)
        if cell_size < 1: cell_size = 1
        
        ox = adjusted_area.x + (adjusted_area.width - cell_size * 3) // 2
        oy = adjusted_area.y + (adjusted_area.height - cell_size * 3) // 2
        
        # Draw background grid cells
        pygame.draw.rect(surface, COLOR_WHITE, (ox, oy, 3 * cell_size, 3 * cell_size))
        
        # Draw grid lines
        for i in range(1, 3):
            pygame.draw.line(surface, COLOR_BLACK, (ox + i * cell_size, oy), (ox + i * cell_size, oy + 3 * cell_size), 4)
            pygame.draw.line(surface, COLOR_BLACK, (ox, oy + i * cell_size), (ox + 3 * cell_size, oy + i * cell_size), 4)
            
        # Draw Outer border
        pygame.draw.rect(surface, COLOR_BLACK, (ox, oy, 3 * cell_size, 3 * cell_size), 6)
            
        font_large = pygame.font.SysFont("Arial", int(cell_size * 0.7), bold=True)
        font_small = pygame.font.SysFont("Arial", int(cell_size * 0.25), bold=True)
        
        for i in range(9):
            r = i // 3
            c = i % 3
            cx = ox + c * cell_size + cell_size // 2
            cy = oy + r * cell_size + cell_size // 2
            
            val = self.board[i]
            if val == 1:
                text = font_large.render("X", True, COLOR_RED)
                surface.blit(text, text.get_rect(center=(cx, cy)))
            elif val == -1:
                text = font_large.render("O", True, COLOR_GREEN)
                surface.blit(text, text.get_rect(center=(cx, cy)))
            else:
                if i in self.scores:
                    score_val = self.scores[i]
                    text = font_small.render(str(score_val), True, (52, 152, 219))
                    surface.blit(text, text.get_rect(center=(cx, cy)))

        self.log_panel.draw(surface)

    def draw_annotation(self, surface, area):
        adjusted_area = pygame.Rect(self.log_panel_width, area.y, area.width - self.log_panel_width, area.height)
        
        pygame.draw.rect(surface, (250, 250, 250), adjusted_area)
        pygame.draw.line(surface, (200, 200, 200), (adjusted_area.x, adjusted_area.y), (adjusted_area.x + adjusted_area.width, adjusted_area.y), 2)
        
        text_surf = self.font.render("Luật: Cờ Caro 3x3. Điểm số đánh giá sẽ hiện lên khi AI suy nghĩ.", True, COLOR_BLACK)
        surface.blit(text_surf, (adjusted_area.x + 10, adjusted_area.y + 10))
        
        legend_y = adjusted_area.y + 40
        
        # X
        x_text = pygame.font.SysFont("Arial", 20, bold=True).render("X", True, COLOR_RED)
        surface.blit(x_text, (adjusted_area.x + 20, legend_y))
        surface.blit(self.font.render("Người chơi (MAX)", True, COLOR_BLACK), (adjusted_area.x + 40, legend_y + 4))
        
        # O
        o_text = pygame.font.SysFont("Arial", 20, bold=True).render("O", True, COLOR_GREEN)
        surface.blit(o_text, (adjusted_area.x + 220, legend_y))
        surface.blit(self.font.render("Bowser AI (MIN)", True, COLOR_BLACK), (adjusted_area.x + 240, legend_y + 4))
        
        # Score
        score_text = pygame.font.SysFont("Arial", 20, bold=True).render("-1", True, (52, 152, 219))
        surface.blit(score_text, (adjusted_area.x + 400, legend_y))
        surface.blit(self.font.render("Điểm số tính toán", True, COLOR_BLACK), (adjusted_area.x + 430, legend_y + 4))
