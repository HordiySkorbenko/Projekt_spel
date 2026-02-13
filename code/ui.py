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
