import pygame
from settings import *
class XPBar:
    def __init__(self, player, width=300, height=20, pos=(WINDOW_HEIGHT-300, (WINDOW_WIDTH/2))):
        self.player = player
        self.width = width
        self.height = height
        self.x, self.y = pos

        # färger
        self.bg_color = (60, 60, 60)
        self.fill_color = (0, 200, 0)
        self.border_color = (255, 255, 255)

        self.font = pygame.font.SysFont("Arial", 18, bold=True)

    def draw(self, surface):
        
        pygame.draw.rect(surface, self.bg_color,
                         (self.x, self.y, self.width, self.height))

        # procent
        xp_ratio = self.player.xp / self.player.xp_to_next_level
        fill_width = self.width * xp_ratio

        pygame.draw.rect(surface, self.fill_color,
                         (self.x, self.y, fill_width, self.height))

        # border
        pygame.draw.rect(surface, self.border_color,
                         (self.x, self.y, self.width, self.height), 2)

        #text
        level_text = self.font.render(
            f"Level {self.player.level}", True, (255, 255, 255))
        surface.blit(level_text, (self.x, self.y - 25))

class Clock:
    def __init__(self):
        # Position: Top Middle
        # WINDOW_WIDTH / 2 centers the starting point, so we subtract 
        # a bit to center the actual text block
        self.x = WINDOW_WIDTH // 2
        self.y = 20
        
        # Font setup
        self.font = pygame.font.SysFont("Arial", 24, bold=True)
        self.text_color = (255, 255, 255)
        self.shadow_color = (0, 0, 0)

    def draw(self, surface):
        # pygame.time.get_ticks() returns total milliseconds
        total_seconds = pygame.time.get_ticks() // 1000
        minutes = total_seconds // 60
        seconds = total_seconds % 60

        # Format string to always show two digits 
        time_string = f"{minutes:02}:{seconds:02}"
        
        # Render text
        time_text = self.font.render(time_string, True, self.text_color)
        
        # Get rect for precise centering
        text_rect = time_text.get_rect(midtop=(self.x, self.y))
        
        # Optional: Draw a subtle shadow for readability
        shadow_text = self.font.render(time_string, True, self.shadow_color)
        surface.blit(shadow_text, (text_rect.x + 2, text_rect.y + 2))
        
        # Draw the main text
        surface.blit(time_text, text_rect)
