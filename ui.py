import pygame

class Label:
    def __init__(self, x, y, text, font, color=(255, 255, 255)):
        self.x = x
        self.y = y
        self.text = text
        self.font = font
        self.color = color
        self.surface = self.font.render(self.text, True, self.color)
        self.rect = self.surface.get_rect(topleft=(x, y))

    def set_text(self, text):
        self.text = text
        self.surface = self.font.render(self.text, True, self.color)
        self.rect = self.surface.get_rect(topleft=(self.x, self.y))

    def draw(self, surface):
        surface.blit(self.surface, self.rect)

class Button:
    def __init__(self, x, y, width, height, text, font, bg_color=(100, 100, 100), hover_color=(150, 150, 150), text_color=(255, 255, 255), action=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.bg_color = bg_color
        self.hover_color = hover_color
        self.text_color = text_color
        self.action = action
        self.is_hovered = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.is_hovered:
                if self.action:
                    self.action()
                return True
        return False

    def set_text(self, text):
        self.text = text

    def draw(self, surface):
        color = self.hover_color if self.is_hovered else self.bg_color
        
        # 1. Hard shadow
        shadow_rect = self.rect.copy()
        shadow_rect.move_ip(4, 4)
        pygame.draw.rect(surface, (0, 0, 0), shadow_rect)
        
        # 2. Main face
        pygame.draw.rect(surface, color, self.rect)
        
        # 3. Inner Bevel
        light_color = (min(color[0]+60, 255), min(color[1]+60, 255), min(color[2]+60, 255))
        dark_color = (max(color[0]-60, 0), max(color[1]-60, 0), max(color[2]-60, 0))
        
        # Light edge (top and left)
        pygame.draw.rect(surface, light_color, (self.rect.x, self.rect.y, self.rect.width, 3))
        pygame.draw.rect(surface, light_color, (self.rect.x, self.rect.y, 3, self.rect.height))
        # Dark edge (bottom and right)
        pygame.draw.rect(surface, dark_color, (self.rect.x, self.rect.bottom - 3, self.rect.width, 3))
        pygame.draw.rect(surface, dark_color, (self.rect.right - 3, self.rect.y, 3, self.rect.height))
        
        # 4. Outer border (sharp)
        pygame.draw.rect(surface, (0, 0, 0), self.rect, 2)
        
        # 5. Text with drop shadow and no anti-aliasing
        text_shadow = self.font.render(self.text, False, (40, 40, 40))
        shadow_pos = text_shadow.get_rect(center=(self.rect.centerx + 2, self.rect.centery + 2))
        surface.blit(text_shadow, shadow_pos)
        
        text_surf = self.font.render(self.text, False, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

class ComboBox(Button):
    def __init__(self, x, y, width, height, prefix, options, font, bg_color=(70, 130, 180), hover_color=(100, 149, 237), text_color=(255, 255, 255), on_change=None):
        self.prefix = prefix
        self.options = list(options) if options else []
        self.current_index = 0
        self.on_change = on_change
        
        self.is_open = False
        self.hovered_option_index = -1
        self.item_height = height
        
        initial_text = f"{self.prefix}: {self.options[self.current_index]}" if self.options else self.prefix
        super().__init__(x, y, width, height, initial_text, font, bg_color, hover_color, text_color, action=self.toggle)

    def toggle(self):
        self.is_open = not self.is_open

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
            if self.is_open:
                dropdown_rect = pygame.Rect(self.rect.x, self.rect.bottom, self.rect.width, len(self.options) * self.item_height)
                if dropdown_rect.collidepoint(event.pos):
                    rel_y = event.pos[1] - self.rect.bottom
                    self.hovered_option_index = rel_y // self.item_height
                else:
                    self.hovered_option_index = -1
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.is_open:
                    dropdown_rect = pygame.Rect(self.rect.x, self.rect.bottom, self.rect.width, len(self.options) * self.item_height)
                    if dropdown_rect.collidepoint(event.pos):
                        rel_y = event.pos[1] - self.rect.bottom
                        idx = rel_y // self.item_height
                        if 0 <= idx < len(self.options):
                            self.current_index = idx
                            self.text = f"{self.prefix}: {self.options[self.current_index]}"
                            self.is_open = False
                            if self.on_change:
                                self.on_change(self.options[self.current_index])
                        return True
                    elif self.rect.collidepoint(event.pos):
                        self.is_open = False
                        return True
                    else:
                        self.is_open = False
                        # Clicked outside, don't return True so other elements can handle it
                else:
                    if self.is_hovered:
                        self.is_open = True
                        return True
        return False

    def draw(self, surface):
        color = self.hover_color if self.is_hovered or self.is_open else self.bg_color
        
        # 1. Hard shadow
        shadow_rect = self.rect.copy()
        shadow_rect.move_ip(4, 4)
        pygame.draw.rect(surface, (0, 0, 0), shadow_rect)
        
        # 2. Main face
        pygame.draw.rect(surface, color, self.rect)
        
        # 3. Inner Bevel
        light_color = (min(color[0]+60, 255), min(color[1]+60, 255), min(color[2]+60, 255))
        dark_color = (max(color[0]-60, 0), max(color[1]-60, 0), max(color[2]-60, 0))
        
        # Light edge (top and left)
        pygame.draw.rect(surface, light_color, (self.rect.x, self.rect.y, self.rect.width, 3))
        pygame.draw.rect(surface, light_color, (self.rect.x, self.rect.y, 3, self.rect.height))
        # Dark edge (bottom and right)
        pygame.draw.rect(surface, dark_color, (self.rect.x, self.rect.bottom - 3, self.rect.width, 3))
        pygame.draw.rect(surface, dark_color, (self.rect.right - 3, self.rect.y, 3, self.rect.height))
        
        # 4. Outer border (sharp)
        pygame.draw.rect(surface, (0, 0, 0), self.rect, 2)
        
        # 5. Text with drop shadow and no anti-aliasing
        text_shadow = self.font.render(self.text, False, (40, 40, 40))
        # Left-align text in combobox, leaving room for arrow
        shadow_pos = text_shadow.get_rect(midleft=(self.rect.left + 12, self.rect.centery + 2))
        surface.blit(text_shadow, shadow_pos)
        
        text_surf = self.font.render(self.text, False, self.text_color)
        text_rect = text_surf.get_rect(midleft=(self.rect.left + 10, self.rect.centery))
        surface.blit(text_surf, text_rect)
        
        # 6. Dropdown arrow
        arrow_color = (20, 20, 20)
        points = [
            (self.rect.right - 25, self.rect.centery - 4),
            (self.rect.right - 10, self.rect.centery - 4),
            (self.rect.right - 17, self.rect.centery + 6)
        ]
        pygame.draw.polygon(surface, arrow_color, points)

    def draw_dropdown(self, surface):
        if not self.is_open or not self.options: return
        
        total_height = len(self.options) * self.item_height
        dropdown_rect = pygame.Rect(self.rect.x, self.rect.bottom, self.rect.width, total_height)
        
        # Dropdown shadow
        shadow_rect = dropdown_rect.copy()
        shadow_rect.move_ip(4, 4)
        pygame.draw.rect(surface, (0, 0, 0), shadow_rect)
        
        # Dropdown background
        pygame.draw.rect(surface, self.bg_color, dropdown_rect)
        
        for i, option in enumerate(self.options):
            item_rect = pygame.Rect(self.rect.x, self.rect.bottom + i * self.item_height, self.rect.width, self.item_height)
            if i == self.hovered_option_index:
                pygame.draw.rect(surface, self.hover_color, item_rect)
            
            # Separator lines
            pygame.draw.line(surface, (0, 0, 0), (item_rect.left, item_rect.bottom - 1), (item_rect.right, item_rect.bottom - 1))
            
            text_surf = self.font.render(str(option), False, self.text_color)
            surface.blit(text_surf, (item_rect.left + 10, item_rect.centery - text_surf.get_height() // 2))
            
        # Border
        pygame.draw.rect(surface, (0, 0, 0), dropdown_rect, 2)

    def get_current(self):
        if not self.options: return None
        return self.options[self.current_index]

    def set_current(self, value):
        if value in self.options:
            self.current_index = self.options.index(value)
            self.text = f"{self.prefix}: {self.options[self.current_index]}"

class LogPanel:
    def __init__(self, x, y, width, height, title, font, bg_color=(245, 245, 245), text_color=(20, 20, 20)):
        self.rect = pygame.Rect(x, y, width, height)
        self.title = title
        self.font = font
        self.bg_color = bg_color
        self.text_color = text_color
        self.logs = []
        self.line_height = self.font.get_linesize() + 4
        self.padding = 10
        self.max_lines = (self.rect.height - 50) // self.line_height

    def update_height(self, height):
        self.rect.height = height
        self.max_lines = (self.rect.height - 50) // self.line_height

    def add_log(self, text):
        words = text.split(' ')
        current_line = ""
        for word in words:
            test_line = current_line + word + " "
            if self.font.size(test_line)[0] < self.rect.width - 2 * self.padding:
                current_line = test_line
            else:
                if current_line:
                    self.logs.append(current_line)
                current_line = word + " "
        if current_line:
            self.logs.append(current_line)

    def clear(self):
        self.logs = []

    def draw(self, surface):
        pygame.draw.rect(surface, self.bg_color, self.rect)
        pygame.draw.line(surface, (200, 200, 200), (self.rect.right, self.rect.y), (self.rect.right, self.rect.bottom), 2)
        
        title_surf = self.font.render(self.title, True, (41, 128, 185))
        surface.blit(title_surf, (self.rect.x + self.padding, self.rect.y + 15))
        pygame.draw.line(surface, (200, 200, 200), (self.rect.x + 10, self.rect.y + 40), (self.rect.right - 10, self.rect.y + 40), 1)
        
        start_idx = max(0, len(self.logs) - self.max_lines)
        visible_logs = self.logs[start_idx:]
        
        y = self.rect.y + 50
        for line in visible_logs:
            text_surf = self.font.render(line, True, self.text_color)
            surface.blit(text_surf, (self.rect.x + self.padding, y))
            y += self.line_height
