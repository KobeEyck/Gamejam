import pygame
from src.settings import SCREEN_WIDTH, SCREEN_HEIGHT, TITLE

class MainMenu:
    def __init__(self):
        self.font_title = pygame.font.Font(None, 80)
        self.font_btn = pygame.font.Font(None, 40)
        
        btn_w, btn_h = 240, 50
        spacing = 15
        
        start_y = SCREEN_HEIGHT//2 - 20
        self.normal_rect = pygame.Rect(SCREEN_WIDTH//2 - btn_w//2, start_y, btn_w, btn_h)
        self.hard_rect = pygame.Rect(SCREEN_WIDTH//2 - btn_w//2, start_y + btn_h + spacing, btn_w, btn_h)
        self.insane_rect = pygame.Rect(SCREEN_WIDTH//2 - btn_w//2, start_y + 2*(btn_h + spacing), btn_w, btn_h)
        self.how_to_play_rect = pygame.Rect(SCREEN_WIDTH//2 - btn_w//2, start_y + 3*(btn_h + spacing), btn_w, btn_h)
        self.quit_rect = pygame.Rect(SCREEN_WIDTH//2 - btn_w//2, start_y + 4*(btn_h + spacing), btn_w, btn_h)
        self.show_how_to_play = False

    def handle_event(self, event) -> str:
        """Returns action string or None based on user interaction."""
        if self.show_how_to_play:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.show_how_to_play = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.show_how_to_play = False
            return None

        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                return "PLAY_NORMAL"
            elif event.key == pygame.K_ESCAPE:
                return "QUIT"
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.normal_rect.collidepoint(event.pos):
                    return "PLAY_NORMAL"
                elif self.hard_rect.collidepoint(event.pos):
                    return "PLAY_HARD"
                elif self.insane_rect.collidepoint(event.pos):
                    return "PLAY_INSANE"
                elif self.how_to_play_rect.collidepoint(event.pos):
                    self.show_how_to_play = True
                elif self.quit_rect.collidepoint(event.pos):
                    return "QUIT"
        return None

    def draw(self, surface: pygame.Surface):
        surface.fill((20, 20, 30))

        if self.show_how_to_play:
            self.draw_how_to_play(surface)
            return
        
        # Title
        title_surf = self.font_title.render(TITLE, True, (255, 100, 50))
        title_rect = title_surf.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 150))
        surface.blit(title_surf, title_rect)
        
        # Subtitle
        sub_font = pygame.font.Font(None, 32)
        sub_surf = sub_font.render("Prevent the volcano from erupting! Choose difficulty:", True, (200, 200, 200))
        sub_rect = sub_surf.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 90))
        surface.blit(sub_surf, sub_rect)

        mouse_pos = pygame.mouse.get_pos()
        
        def draw_btn(rect, text, normal_color, hover_color):
            color = hover_color if rect.collidepoint(mouse_pos) else normal_color
            pygame.draw.rect(surface, color, rect, border_radius=8)
            pygame.draw.rect(surface, (255, 255, 255), rect, 2, border_radius=8)
            txt_surf = self.font_btn.render(text, True, (255, 255, 255))
            surface.blit(txt_surf, txt_surf.get_rect(center=rect.center))

        draw_btn(self.normal_rect, "NORMAL", (50, 160, 80), (80, 200, 100))
        draw_btn(self.hard_rect, "HARD", (160, 100, 40), (200, 140, 60))
        draw_btn(self.insane_rect, "INSANE", (180, 50, 50), (220, 80, 80))
        draw_btn(self.how_to_play_rect, "HOW TO PLAY", (50, 100, 150), (80, 140, 200))
        draw_btn(self.quit_rect, "QUIT", (100, 100, 100), (140, 140, 140))

    def draw_how_to_play(self, surface: pygame.Surface):
        title = self.font_title.render("HOW TO PLAY", True, (255, 215, 60))
        surface.blit(title, title.get_rect(center=(SCREEN_WIDTH // 2, 90)))

        heading_font = pygame.font.Font(None, 34)
        text_font = pygame.font.Font(None, 28)
        lines = [
            ("CONTROLS", heading_font, (255, 215, 60)),
            ("W / UP ARROW - Fly forward", text_font, (235, 235, 240)),
            ("A / LEFT ARROW - Tilt left", text_font, (235, 235, 240)),
            ("D / RIGHT ARROW - Tilt right", text_font, (235, 235, 240)),
            ("SPACE / S / DOWN ARROW - Drop your water", text_font, (235, 235, 240)),
            ("H - Open the shop when landed on the helipad", text_font, (235, 235, 240)),
            ("ESC - Exit the game", text_font, (235, 235, 240)),
            ("", text_font, (235, 235, 240)),
            ("OBJECTIVE", heading_font, (255, 215, 60)),
            ("Collect water from the lake and drop it into the caldera.", text_font, (235, 235, 240)),
            ("Accurate drops cool the volcano and earn more money.", text_font, (235, 235, 240)),
            ("Upgrade your aircraft at the helipad and stop the eruption.", text_font, (235, 235, 240)),
        ]

        y = 150
        for text, font, color in lines:
            rendered = font.render(text, True, color)
            surface.blit(rendered, rendered.get_rect(center=(SCREEN_WIDTH // 2, y)))
            y += 34

        hint = text_font.render("Press ESC or click to return to the menu.", True, (160, 160, 180))
        surface.blit(hint, hint.get_rect(center=(SCREEN_WIDTH // 2, 650)))
