import pygame
import math
from settings import *
from ui import Clock, DisplayLeaderboard, Leaderboard

class Menu:
    def __init__(self, screen):
        self.screen = screen
        try:
            self.font_big = pygame.font.Font("data/fonts/static/PixelifySans-Regular.ttf", 50)
            self.font_small = pygame.font.Font("data/fonts/static/PixelifySans-Regular.ttf", 35)
        except:
            self.font_big = pygame.font.SysFont("Arial", 50, bold=True)
            self.font_small = pygame.font.SysFont("Arial", 35, bold=True)
        
        self.difficulty = 1
        self.clock_display = Clock()
        self.logo = pygame.image.load("image/logo/logo1.png").convert_alpha()
        self.logo_rect = self.logo.get_rect()
        self.leaderboard_view = DisplayLeaderboard(self.screen)
        self.leaderboard_manager = Leaderboard()
        
    def main_menu(self):
        running = True
        click = False
        while running:
            current_time = pygame.time.get_ticks()
            for y in range(WINDOW_HEIGHT):
                color = (20 + y//20, 10, 30 + y//25)
                pygame.draw.line(self.screen, color, (0,y), (WINDOW_WIDTH,y))
            
            self.logo_rect.centerx = WINDOW_WIDTH // 2
            self.logo_rect.y = 50 + math.sin(current_time / 600) * 15
            self.screen.blit(self.logo, self.logo_rect)
            
            mouse_pos = pygame.mouse.get_pos()
            btn_w, btn_h = 400, 90
            b1 = pygame.Rect(WINDOW_WIDTH/2 - btn_w/2, WINDOW_HEIGHT/2 - 50, btn_w, btn_h)
            b2 = pygame.Rect(WINDOW_WIDTH/2 - btn_w/2, WINDOW_HEIGHT/2 - 160, btn_w, btn_h)
            b3 = pygame.Rect(WINDOW_WIDTH/2 - btn_w/2, WINDOW_HEIGHT/2 + 60, btn_w, btn_h)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    click = True

            if b1.collidepoint(mouse_pos) and click:
                self.clock_display.reset()
                return self.clock_display
            if b2.collidepoint(mouse_pos) and click:
                self.difficulty_select()
            if b3.collidepoint(mouse_pos) and click:
                self.show_leaderboard()

            self.draw_button(b1, "Start", self.font_big)
            self.draw_button(b2, "Difficulty", self.font_small)
            self.draw_button(b3, "Highscores", self.font_big)

            pygame.display.update()
            click = False

    def draw_button(self, rect, text, font):
        is_h = rect.collidepoint(pygame.mouse.get_pos())
        col = (200, 250, 200) if is_h else (250, 250, 250)
        d_rect = rect.inflate(10, 10) if is_h else rect
        pygame.draw.rect(self.screen, (10,10,10), d_rect.move(4,4), border_radius=12)
        pygame.draw.rect(self.screen, col, d_rect, border_radius=12)
        pygame.draw.rect(self.screen, (0,0,0), d_rect, 4, border_radius=12)
        txt = font.render(text, True, (40,40,40))
        self.screen.blit(txt, txt.get_rect(center=d_rect.center))

    def difficulty_select(self):
        running = True
        click = False
        while running:
            current_time = pygame.time.get_ticks()
            self.screen.fill((20, 10, 30))
            
            offset = math.sin(current_time / 500) * 15
            title = self.font_big.render("SELECT DIFFICULTY", True, (255,255,255))
            self.screen.blit(title, title.get_rect(center=(WINDOW_WIDTH//2, 100+offset)))

            mouse_pos = pygame.mouse.get_pos()
            levels = [
                (pygame.Rect(WINDOW_WIDTH//2-200, 250, 400, 80), "Too Easy", (150,255,150), 1),
                (pygame.Rect(WINDOW_WIDTH//2-200, 360, 400, 80), "Average", (255,255,150), 2),
                (pygame.Rect(WINDOW_WIDTH//2-200, 470, 400, 80), "Impossible", (255,100,100), 3)
            ]

            for r, txt, col, val in levels:
                is_h = r.collidepoint(mouse_pos)
                self.draw_fancy_button(r.inflate(15,10) if is_h else r, txt, col, is_h)
                if is_h and click:
                    self.difficulty = val
                    running = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    click = True
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    running = False
            
            pygame.display.update()
            click = False

    def draw_fancy_button(self, rect, text, hover_color, is_hovered):
        color = hover_color if is_hovered else (240, 240, 240)
        pygame.draw.rect(self.screen, (10, 10, 20), rect.move(6, 6), border_radius=12)
        pygame.draw.rect(self.screen, color, rect, border_radius=12)
        pygame.draw.rect(self.screen, (255, 255, 255) if is_hovered else (0, 0, 0), rect, 4, border_radius=12)
        text_surf = self.font_small.render(text, True, (30, 30, 30))
        self.screen.blit(text_surf, text_surf.get_rect(center=rect.center))

    def show_leaderboard(self):
        running = True
        scores = self.leaderboard_manager.get_top_scores(50)
        while running:
            self.screen.fill((20, 20, 30))
            self.leaderboard_view.draw(scores)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 4:
                        self.leaderboard_view.scroll_y = min(0, self.leaderboard_view.scroll_y + 40)
                    if event.button == 5:
                        self.leaderboard_view.scroll_y -= 40
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    running = False 
            pygame.display.update()