import pygame
from src.settings import SCREEN_WIDTH, SCREEN_HEIGHT, TITLE

class MainMenu:
    def __init__(self):
        self.font_title = pygame.font.Font(None, 80)
        self.font_btn = pygame.font.Font(None, 48)
        
        btn_w, btn_h = 240, 60
        self.start_rect = pygame.Rect(SCREEN_WIDTH//2 - btn_w//2, SCREEN_HEIGHT//2 - 40, btn_w, btn_h)
        self.quit_rect = pygame.Rect(SCREEN_WIDTH//2 - btn_w//2, SCREEN_HEIGHT//2 + 50, btn_w, btn_h)

    def handle_event(self, event) -> str:
        """Returns 'PLAY', 'QUIT', or None based on user interaction."""
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                return "PLAY"
            elif event.key == pygame.K_ESCAPE:
                return "QUIT"
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.start_rect.collidepoint(event.pos):
                    return "PLAY"
                elif self.quit_rect.collidepoint(event.pos):
                    return "QUIT"
        return None

    def draw(self, surface: pygame.Surface):
        surface.fill((20, 20, 30))
        
        # Title
        title_surf = self.font_title.render(TITLE, True, (255, 100, 50))
        title_rect = title_surf.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 150))
        surface.blit(title_surf, title_rect)
        
        # Subtitle
        sub_font = pygame.font.Font(None, 32)
        sub_surf = sub_font.render("Prevent the volcano from erupting!", True, (200, 200, 200))
        sub_rect = sub_surf.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 90))
        surface.blit(sub_surf, sub_rect)

        mouse_pos = pygame.mouse.get_pos()
        
        # Start button
        start_color = (80, 200, 100) if self.start_rect.collidepoint(mouse_pos) else (50, 160, 80)
        pygame.draw.rect(surface, start_color, self.start_rect, border_radius=8)
        pygame.draw.rect(surface, (200, 255, 200), self.start_rect, 2, border_radius=8)
        start_txt = self.font_btn.render("START", True, (255, 255, 255))
        surface.blit(start_txt, start_txt.get_rect(center=self.start_rect.center))
        
        # Quit button
        quit_color = (200, 80, 80) if self.quit_rect.collidepoint(mouse_pos) else (160, 50, 50)
        pygame.draw.rect(surface, quit_color, self.quit_rect, border_radius=8)
        pygame.draw.rect(surface, (255, 200, 200), self.quit_rect, 2, border_radius=8)
        quit_txt = self.font_btn.render("QUIT", True, (255, 255, 255))
        surface.blit(quit_txt, quit_txt.get_rect(center=self.quit_rect.center))
