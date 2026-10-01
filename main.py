import sys
import pygame

def main():
    pygame.init()
    screen_width, screen_height = 800, 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Gamejam - Pygame Setup Test")

    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 42)
    small_font = pygame.font.Font(None, 28)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        # Background color
        screen.fill((30, 30, 45))

        # Title text
        title_surf = font.render("🎮 Pygame is successfully installed!", True, (100, 255, 150))
        title_rect = title_surf.get_rect(center=(screen_width // 2, 220))
        screen.blit(title_surf, title_rect)

        # Subtitle / instructions
        info_surf = small_font.render("Your virtual environment is ready for the Gamejam.", True, (220, 220, 220))
        info_rect = info_surf.get_rect(center=(screen_width // 2, 280))
        screen.blit(info_surf, info_rect)

        esc_surf = small_font.render("Press ESC or close this window to exit.", True, (160, 160, 180))
        esc_rect = esc_surf.get_rect(center=(screen_width // 2, 340))
        screen.blit(esc_surf, esc_rect)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
