import pygame
import sys
import os
import cv2
from config import COLOR_SKY, COLOR_RED, COLOR_COIN, COLOR_GREEN, AssetManager, COLOR_WHITE, COLOR_BLACK
from ui import Button
from worlds.maze_world import MazeWorld
from worlds.local_world import LocalWorld
from worlds.fog_world import FogWorld
from worlds.csp_world import CspWorld
from worlds.boss_world import BossWorld

class MarioAIVisualizerApp:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
        pygame.display.set_caption("Super Mario AI Project Visualizer")
        self.clock = pygame.time.Clock()
        
        self.font = pygame.font.SysFont("Courier New", 14, bold=True)
        self.title_font = pygame.font.SysFont("Courier New", 28, bold=True)
        
        AssetManager().load_assets()
        
        self.setup_video_bg()
        self.setup_ui()
        self.running = True

    def setup_video_bg(self):
        self.video_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "resources", "menu_background_video.mp4")
        self.cap = None
        if os.path.exists(self.video_path):
            self.cap = cv2.VideoCapture(self.video_path)
            
    def get_video_frame(self, w, h):
        if not self.cap or not self.cap.isOpened():
            return None
            
        ret, frame = self.cap.read()
        if not ret:
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            ret, frame = self.cap.read()
            
        if ret:
            frame = cv2.resize(frame, (w, h))
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = frame.swapaxes(0, 1)
            surface = pygame.surfarray.make_surface(frame)
            return surface
        return None

    def setup_ui(self):
        self.buttons = [
            Button(0, 0, 280, 80, "WORLD 1 & 2: Pathfinding", self.font, (46, 204, 113), (60, 220, 130), COLOR_WHITE, self.open_world12),
            Button(0, 0, 280, 80, "WORLD 3: Local Search", self.font, (230, 126, 34), (250, 140, 50), COLOR_WHITE, self.open_world3),
            Button(0, 0, 280, 80, "WORLD 4: Complex Env", self.font, (52, 73, 94), (70, 90, 110), COLOR_WHITE, self.open_world4),
            Button(0, 0, 280, 80, "WORLD 5: CSP Solver", self.font, (155, 89, 182), (170, 100, 200), COLOR_WHITE, self.open_world5),
            Button(0, 0, 280, 80, "WORLD 6: Boss Battle", self.font, (192, 57, 43), (210, 70, 60), COLOR_WHITE, self.open_world6),
            Button(0, 0, 280, 80, "EXIT", self.font, (100, 100, 100), (130, 130, 130), COLOR_WHITE, self.exit_app)
        ]

    def exit_app(self):
        self.running = False

    def layout_ui(self):
        w, h = self.screen.get_size()
        cx, cy = w // 2, h // 2
        btn_cy = cy + 20
        
        self.buttons[0].rect.center = (cx - 150, btn_cy - 50)
        self.buttons[1].rect.center = (cx + 150, btn_cy - 50)
        self.buttons[2].rect.center = (cx - 150, btn_cy + 50)
        self.buttons[3].rect.center = (cx + 150, btn_cy + 50)
        self.buttons[4].rect.center = (cx - 150, btn_cy + 150)
        self.buttons[5].rect.center = (cx + 150, btn_cy + 150)

    def draw_title(self, cx, cy):
        title_img = AssetManager().get("title")
        if title_img:
            rect = title_img.get_rect(center=(cx, cy))
            self.screen.blit(title_img, rect)
        else:
            title = "SUPER MARIO AI VISUALIZER"
            shadow = self.title_font.render(title, True, (34, 34, 34))
            text = self.title_font.render(title, True, COLOR_COIN)
            rect = text.get_rect(center=(cx, cy))
            shadow_rect = shadow.get_rect(center=(cx+3, cy+3))
            self.screen.blit(shadow, shadow_rect)
            self.screen.blit(text, rect)

    def open_world12(self):
        world = MazeWorld(self.screen)
        world.run()

    def open_world3(self):
        world = LocalWorld(self.screen)
        world.run()

    def open_world4(self):
        world = FogWorld(self.screen)
        world.run()

    def open_world5(self):
        world = CspWorld(self.screen)
        world.run()

    def open_world6(self):
        world = BossWorld(self.screen)
        world.run()

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        # Toggle fullscreen by simply setting mode again
                        self.screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
                for btn in self.buttons:
                    btn.handle_event(event)
            
            w, h = self.screen.get_size()
            self.layout_ui()
            
            # Draw bg
            bg = self.get_video_frame(w, h)
            if bg:
                self.screen.blit(bg, (0, 0))
            else:
                self.screen.fill(COLOR_SKY)
                
            self.draw_title(w // 2, h // 2 - 200)
            
            for btn in self.buttons:
                btn.draw(self.screen)
                
            # Footer
            footer_text = "Nhấn ESC để thoát chế độ Toàn màn hình"
            footer = self.font.render(footer_text, True, COLOR_WHITE)
            footer_shadow = self.font.render(footer_text, True, COLOR_BLACK)
            footer_rect = footer.get_rect(center=(w//2, h - 30))
            self.screen.blit(footer_shadow, (footer_rect.x+2, footer_rect.y+2))
            self.screen.blit(footer, footer_rect)
                
            pygame.display.flip()
            self.clock.tick(30)
            
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    app = MarioAIVisualizerApp()
    app.run()
