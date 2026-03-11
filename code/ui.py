import json
import pygame
from settings import *
import os

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
        return self
            
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

# ui.py (eller där din GameOver-klass bor)
import pygame
from settings import *

class GameOver:
    def __init__(self, display_surface):
        self.display_surface = display_surface
        self.font = pygame.font.SysFont("Arial", 40, bold=True)
        self.small_font = pygame.font.SysFont("Arial", 24)

    def draw(self, top_scores):
        # Rita bakgrund (t.ex. halvgenomskinlig svart)
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.set_alpha(150)
        overlay.fill((0, 0, 0))
        self.display_surface.blit(overlay, (0,0))

        # Rita "GAME OVER"
        title_surf = self.font.render("GAME OVER", True, "white")
        title_rect = title_surf.get_rect(center=(WINDOW_WIDTH // 2, 100))
        self.display_surface.blit(title_surf, title_rect)

        # Rita Leaderboard-rubrik
        lb_title = self.small_font.render("TOP 5 SURVIVORS", True, "yellow")
        self.display_surface.blit(lb_title, lb_title.get_rect(center=(WINDOW_WIDTH // 2, 200)))

        # Loopa igenom poängen och rita dem
        for i, entry in enumerate(top_scores):
            score_text = f"{i+1}. XP: {entry['xp']} | Time: {entry['time']}"
            score_surf = self.small_font.render(score_text, True, "white")
            y_pos = 250 + (i * 40) # 40 pixlar mellan varje rad
            self.display_surface.blit(score_surf, score_surf.get_rect(center=(WINDOW_WIDTH // 2, y_pos)))

        # Instruktion
        hint_surf = self.small_font.render("Press SPACE to Restart, Press ESC to close ", True, "gray")
        self.display_surface.blit(hint_surf, hint_surf.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 100)))


class Leaderboard:
    def __init__(self, filename='leaderboard.json'):
        self.filename = filename

    def save_score(self, time_str, xp_val):
            new_entry = {"time": time_str, "xp": xp_val}
            data = []

            if os.path.exists(self.filename):
                with open(self.filename, 'r') as f:
                    try:
                        data = json.load(f)
                    except: data = []

            data.append(new_entry)

            with open(self.filename, 'w') as f:
                json.dump(data, f, indent=4)

    def get_top_scores(self, limit=5):
        if not os.path.exists(self.filename):
            return []
        
        try:
            with open(self.filename, 'r') as f:
                data = json.load(f)
            
            # Sortera listan baserat på XP (högst först)
            # x['xp'] antar att din XP sparas som ett heltal
            sorted_data = sorted(data, key=lambda x: x['xp'], reverse=True)
            return sorted_data[:limit] # Returnera endast de 'limit' bästa
        except (json.JSONDecodeError, KeyError):
            return []