import json
import pygame
from settings import *
import os

class XPBar:
    def __init__(self, player, width=300, height=20, pos=None):
        self.player = player
        self.width = width
        self.height = height
        self.x, self.y = pos if pos else (WINDOW_WIDTH // 2 - width // 2, WINDOW_HEIGHT - 50)
        self.bg_color = (60, 60, 60)
        self.fill_color = (0, 200, 0)
        self.border_color = (255, 255, 255)
        self.font = pygame.font.SysFont("Arial", 18, bold=True)
        self._cached_level = None
        self._cached_level_surf = None

    def draw(self, surface):
        pygame.draw.rect(surface, self.bg_color, (self.x, self.y, self.width, self.height))
        xp_ratio = self.player.xp / self.player.xp_to_next_level
        fill_width = int(self.width * xp_ratio)
        pygame.draw.rect(surface, self.fill_color, (self.x, self.y, fill_width, self.height))
        pygame.draw.rect(surface, self.border_color, (self.x, self.y, self.width, self.height), 2)

        # Re-render bara när leveln faktiskt ändras, inte varje frame
        if self._cached_level != self.player.level:
            self._cached_level = self.player.level
            self._cached_level_surf = self.font.render(f"Level {self.player.level}", True, (255, 255, 255))
        surface.blit(self._cached_level_surf, (self.x, self.y - 25))

class Clock:
    def __init__(self):
        self.x = WINDOW_WIDTH // 2
        self.y = 20
        self.font = pygame.font.SysFont("Arial", 24, bold=True)
        self.text_color = (255, 255, 255)
        self.shadow_color = (0, 0, 0)
        self.start_ticks = pygame.time.get_ticks()
        self._cached_second = -1
        self._cached_surf = None
        self._cached_shadow = None
        self._cached_rect = None

    def reset(self):
        self.start_ticks = pygame.time.get_ticks()
        self._cached_second = -1
        return self

    def draw(self, surface):
        elapsed_milliseconds = pygame.time.get_ticks() - self.start_ticks
        total_seconds = elapsed_milliseconds // 1000

        # Re-render bara en gång per sekund — inte 60 gånger
        if self._cached_second != total_seconds:
            self._cached_second = total_seconds
            minutes = total_seconds // 60
            seconds = total_seconds % 60
            time_string = f"{minutes:02}:{seconds:02}"
            self._cached_surf   = self.font.render(time_string, True, self.text_color)
            self._cached_shadow = self.font.render(time_string, True, self.shadow_color)
            self._cached_rect   = self._cached_surf.get_rect(midtop=(self.x, self.y))

        surface.blit(self._cached_shadow, (self._cached_rect.x + 2, self._cached_rect.y + 2))
        surface.blit(self._cached_surf,    self._cached_rect)

class GameOver:
    def __init__(self, display_surface):
        self.display_surface = display_surface
        self.font = pygame.font.SysFont("Arial", 40, bold=True)
        self.small_font = pygame.font.SysFont("Arial", 24)

        # Skapa overlay EN gång — återanvänd varje frame
        self.overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.overlay.set_alpha(150)
        self.overlay.fill((0, 0, 0))

        # Cacha statiska texter som aldrig ändras
        self.title_surf = self.font.render("GAME OVER", True, "white")
        self.title_rect = self.title_surf.get_rect(center=(WINDOW_WIDTH // 2, 100))
        self.lb_title   = self.small_font.render("TOP 5 SURVIVORS", True, "yellow")
        self.lb_rect    = self.lb_title.get_rect(center=(WINDOW_WIDTH // 2, 200))
        self.hint_surf  = self.small_font.render("Press SPACE to Restart, Press ESC to close", True, "gray")
        self.hint_rect  = self.hint_surf.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 100))

        # Cacha score-rader — uppdateras bara när top_scores ändras
        self._cached_scores = None
        self._cached_score_surfs = []

    def draw(self, top_scores):
        self.display_surface.blit(self.overlay, (0, 0))
        self.display_surface.blit(self.title_surf, self.title_rect)
        self.display_surface.blit(self.lb_title,   self.lb_rect)

        # Re-rendera score-rader bara om listan faktiskt ändrats
        if top_scores != self._cached_scores:
            self._cached_scores = top_scores
            self._cached_score_surfs = []
            for i, entry in enumerate(top_scores):
                score_text = f"{i+1}. XP: {entry['xp']} | Time: {entry['time']}"
                surf = self.small_font.render(score_text, True, "white")
                rect = surf.get_rect(center=(WINDOW_WIDTH // 2, 250 + i * 40))
                self._cached_score_surfs.append((surf, rect))

        for surf, rect in self._cached_score_surfs:
            self.display_surface.blit(surf, rect)

        self.display_surface.blit(self.hint_surf, self.hint_rect)

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
                except:
                    data = []
        data.append(new_entry)
        with open(self.filename, 'w') as f:
            json.dump(data, f, indent=4)

    def get_top_scores(self, limit=5):
        if not os.path.exists(self.filename):
            return []
        try:
            with open(self.filename, 'r') as f:
                data = json.load(f)
            sorted_data = sorted(data, key=lambda x: x['xp'], reverse=True)
            return sorted_data[:limit]
        except (json.JSONDecodeError, KeyError):
            return []

class DisplayLeaderboard:
    def __init__(self, display_surface):
        self.display_surface = display_surface
        self.title_font = pygame.font.SysFont("Arial", 48, bold=True)
        self.header_font = pygame.font.SysFont("Arial", 28, bold=True)
        self.font = pygame.font.SysFont("Arial", 24)
        self.scroll_y = 0
        self.colors = {
            'text': (255, 255, 255),
            'gold': (255, 215, 0),
            'background': (20, 20, 30),
            'row_even': (40, 40, 50),
            'row_odd': (30, 30, 40)
        }

    def truncate_text(self, text, max_chars=12):
        string_text = str(text)
        return string_text[:max_chars] + ".." if len(string_text) > max_chars else string_text

    def draw(self, top_scores):
        bg_rect = pygame.Rect(0, 0, 600, 500)
        bg_rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 20)
        pygame.draw.rect(self.display_surface, self.colors['background'], bg_rect, border_radius=15)
        pygame.draw.rect(self.display_surface, self.colors['gold'], bg_rect, width=2, border_radius=15)
        title_surf = self.title_font.render("LEADERBOARD", True, self.colors['gold'])
        self.display_surface.blit(title_surf, title_surf.get_rect(center=(WINDOW_WIDTH // 2, bg_rect.top - 50)))
        list_surface = pygame.Surface((bg_rect.width - 40, bg_rect.height - 100), pygame.SRCALPHA)
        rank_h = self.header_font.render("Rank", True, self.colors['gold'])
        xp_h = self.header_font.render("Total XP", True, self.colors['gold'])
        time_h = self.header_font.render("Time", True, self.colors['gold'])
        self.display_surface.blit(rank_h, (bg_rect.left + 50, bg_rect.top + 30))
        self.display_surface.blit(xp_h, (bg_rect.left + 220, bg_rect.top + 30))
        self.display_surface.blit(time_h, (bg_rect.left + 420, bg_rect.top + 30))
        for i, entry in enumerate(top_scores):
            row_y = (i * 50) + self.scroll_y
            if -50 < row_y < list_surface.get_height():
                if i % 2 == 0:
                    pygame.draw.rect(list_surface, self.colors['row_even'], (0, row_y, list_surface.get_width(), 40), border_radius=5)
                rank_txt = self.font.render(f"#{i+1}", True, self.colors['text'])
                xp_txt = self.font.render(self.truncate_text(entry['xp'], 12), True, self.colors['text'])
                time_txt = self.font.render(self.truncate_text(entry['time'], 10), True, self.colors['text'])
                list_surface.blit(rank_txt, (30, row_y + 8))
                list_surface.blit(xp_txt, (200, row_y + 8))
                list_surface.blit(time_txt, (400, row_y + 8))
        self.display_surface.blit(list_surface, (bg_rect.left + 20, bg_rect.top + 80))
        exit_text = self.font.render("Use MOUSE WHEEL to scroll | Press ESC to go back", True, (180, 180, 180))
        self.display_surface.blit(exit_text, exit_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 40)))