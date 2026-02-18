import pygame
from settings import *

class XPBar:
    def __init__(self, player, width=300, height=20, pos=None):
        self.player = player
        self.width = width
        self.height = height
        # Default position at bottom center if not provided
        self.x, self.y = pos if pos else (WINDOW_WIDTH // 2 - width // 2, WINDOW_HEIGHT - 50)

        # colors
        self.bg_color = (60, 60, 60)
        self.fill_color = (0, 200, 0)
        self.border_color = (255, 255, 255)

        self.font = pygame.font.SysFont("Arial", 18, bold=True)

    def draw(self, surface):
        # Background
        pygame.draw.rect(surface, self.bg_color, (self.x, self.y, self.width, self.height))

        # XP fill
        xp_ratio = self.player.xp / self.player.xp_to_next_level
        fill_width = self.width * xp_ratio
        pygame.draw.rect(surface, self.fill_color, (self.x, self.y, fill_width, self.height))

        # Border
        pygame.draw.rect(surface, self.border_color, (self.x, self.y, self.width, self.height), 2)

        # Level text
        level_text = self.font.render(f"Level {self.player.level}", True, (255, 255, 255))
        surface.blit(level_text, (self.x, self.y - 25))

class Clock:
    def __init__(self):
        self.x = WINDOW_WIDTH // 2
        self.y = 20
        self.font = pygame.font.SysFont("Arial", 24, bold=True)
        self.text_color = (255, 255, 255)
        self.shadow_color = (0, 0, 0)
        
        # Initialize start_ticks so draw() works even if reset() hasn't been called
        self.start_ticks = pygame.time.get_ticks()

    def reset(self):
        """Captures the current time as the new starting point (0:00)"""
        self.start_ticks = pygame.time.get_ticks()
            
    def draw(self, surface):
        # FIX: Subtract start_ticks from current time to get elapsed time
        elapsed_milliseconds = pygame.time.get_ticks() - self.start_ticks
        total_seconds = elapsed_milliseconds // 1000
        
        minutes = total_seconds // 60
        seconds = total_seconds % 60

        # Format string to always show two digits 
        time_string = f"{minutes:02}:{seconds:02}"
        
        # Render text
        time_text = self.font.render(time_string, True, self.text_color)
        text_rect = time_text.get_rect(midtop=(self.x, self.y))
        
        # Draw shadow
        shadow_text = self.font.render(time_string, True, self.shadow_color)
        surface.blit(shadow_text, (text_rect.x + 2, text_rect.y + 2))
        
        # Draw main text
        surface.blit(time_text, text_rect)