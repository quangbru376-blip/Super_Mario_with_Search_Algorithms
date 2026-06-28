import pygame
from config import COLOR_SKY, COLOR_RED, COLOR_GROUND, DEFAULT_SPEED, COLOR_WHITE, COLOR_BLACK, COLOR_GRAY
from ui import ComboBox, Button

class BasePyGameWorld:
    def __init__(self, screen, title="Simulation"):
        self.screen = screen
        self.title_text = title
        self.running = False
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Courier New", 14, bold=True)
        self.title_font = pygame.font.SysFont("Courier New", 20, bold=True)
        
        # State variables
        self.is_simulating = False
        self.current_generator = None
        self.speed = DEFAULT_SPEED
        self.last_step_time = 0
        self.status_text = "Sẵn sàng..."
        self.status_color = COLOR_BLACK
        
        # Sidebar layout constants
        self.sidebar_width = 280
        self.sidebar_x = self.screen.get_width() - self.sidebar_width
        
        self.buttons = []
        self.setup_ui()
        self.current_state = None
        
    def setup_ui(self):
        # Speed CycleButton
        speed_opts = [50, 100, 200, 500, 1000]
        self.speed_btn = ComboBox(self.sidebar_x + 20, 80, 240, 40, "Tốc độ (ms)", speed_opts, self.font, on_change=self.set_speed)
        self.speed_btn.set_current(DEFAULT_SPEED)
        self.buttons.append(self.speed_btn)
        
    def set_speed(self, val):
        self.speed = val

    def set_status(self, text, is_error=False):
        self.status_text = text
        self.status_color = (200, 0, 0) if is_error else COLOR_BLACK
        
    def start_simulation(self, generator):
        self.current_generator = generator
        self.is_simulating = True
        self.last_step_time = pygame.time.get_ticks()
        
    def stop_simulation(self):
        self.is_simulating = False
        
    def on_simulation_end(self):
        self.set_status("Hoàn thành!")

    def draw_sidebar(self, surface):
        w, h = surface.get_size()
        sidebar_rect = pygame.Rect(self.sidebar_x, 0, self.sidebar_width, h)
        pygame.draw.rect(surface, COLOR_WHITE, sidebar_rect)
        pygame.draw.line(surface, COLOR_GRAY, (self.sidebar_x, 0), (self.sidebar_x, h), 2)
        
        # Title
        title_surf = self.title_font.render(self.title_text, True, COLOR_RED)
        surface.blit(title_surf, (self.sidebar_x + 20, 20))
        
        # Status
        # Simple multiline render for status
        lines = self.status_text.split('\n')
        for i, line in enumerate(lines):
            status_surf = self.font.render(line, True, self.status_color)
            surface.blit(status_surf, (self.sidebar_x + 20, h - 80 + (i*20)))
        
        for btn in self.buttons:
            btn.draw(surface)
            
        for btn in self.buttons:
            if hasattr(btn, 'draw_dropdown'):
                btn.draw_dropdown(surface)

    def draw_state(self, state, surface, area):
        pass

    def draw_annotation(self, surface, area):
        pass

    def draw_grid(self, surface, area, rows, cols, cell_size):
        offset_x = area.x + (area.width - cols * cell_size) // 2
        offset_y = area.y + (area.height - rows * cell_size) // 2
        for r in range(rows + 1):
            pygame.draw.line(surface, COLOR_GRAY, (offset_x, offset_y + r * cell_size), (offset_x + cols * cell_size, offset_y + r * cell_size))
        for c in range(cols + 1):
            pygame.draw.line(surface, COLOR_GRAY, (offset_x + c * cell_size, offset_y), (offset_x + c * cell_size, offset_y + rows * cell_size))
        return offset_x, offset_y

    def run(self):
        self.running = True
        while self.running:
            current_time = pygame.time.get_ticks()
            events = pygame.event.get()
            
            if hasattr(self, 'process_events'):
                self.process_events(events)
                
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                    import sys; sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False # Return to main menu
                
                handled = False
                # Ưu tiên gửi event cho ComboBox đang mở trước (vì giao diện của nó đè lên các nút khác)
                for btn in self.buttons:
                    if hasattr(btn, 'is_open') and getattr(btn, 'is_open'):
                        if btn.handle_event(event):
                            handled = True
                            break
                            
                if not handled:
                    for btn in reversed(self.buttons):
                        # Bỏ qua các ComboBox đang mở vì đã xử lý ở trên,
                        # hoặc nếu nó xử lý click ra ngoài để đóng
                        if not (hasattr(btn, 'is_open') and getattr(btn, 'is_open')):
                            if btn.handle_event(event):
                                break
                        else:
                            # Nếu click không trúng dropdown mà trúng ra ngoài, combobox cũng tự đóng
                            # Nên vẫn gọi handle_event để nó nhận biết click outside
                            if btn.handle_event(event):
                                break
                    
            if self.is_simulating and self.current_generator:
                if current_time - self.last_step_time >= self.speed:
                    try:
                        self.current_state = next(self.current_generator)
                        self.last_step_time = current_time
                    except StopIteration:
                        self.is_simulating = False
                        self.on_simulation_end()

            if hasattr(self, 'update'):
                self.update()

            # Resize check
            w, h = self.screen.get_size()
            self.sidebar_x = w - self.sidebar_width
            
            # Position buttons
            start_y = 80
            for i, btn in enumerate(self.buttons):
                btn.rect.x = self.sidebar_x + 20
                btn.rect.y = start_y + (i * 50)

            # Draw
            self.screen.fill(COLOR_SKY)
            
            annotation_height = 110
            grid_area = pygame.Rect(0, 0, self.sidebar_x, h - annotation_height)
            annotation_area = pygame.Rect(0, h - annotation_height, self.sidebar_x, annotation_height)
            
            self.draw_state(self.current_state, self.screen, grid_area)
            self.draw_annotation(self.screen, annotation_area)
            
            self.draw_sidebar(self.screen)
            
            pygame.display.flip()
            self.clock.tick(60)
