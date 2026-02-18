import pygame
from settings import *
from ui import Clock

class Menu:
    def __init__(self, screen):
        self.screen = screen
        # Fallback to SysFont if the specific .ttf path isn't found
        try:
            self.font_big = pygame.font.Font("data/fonts/static/PixelifySans-Regular.ttf", 50)
            self.font_small = pygame.font.Font("data/fonts/static/PixelifySans-Regular.ttf", 35)
        except:
            self.font_big = pygame.font.SysFont("Arial", 50, bold=True)
            self.font_small = pygame.font.SysFont("Arial", 35, bold=True)
            
        self.clock_display = Clock()
        
    def main_menu(self):
        running = True
        click = False
        
        while running:
            self.screen.fill((0, 255, 0))
            mouse_x, mouse_y = pygame.mouse.get_pos()
                    
            button_1 = pygame.Rect(WINDOW_WIDTH/2 - 200, WINDOW_HEIGHT/2, 400, 100)
            button_2 = pygame.Rect(WINDOW_WIDTH/2 - 200, (WINDOW_HEIGHT/2)+ 150, 400, 100)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        # FIX: Reset and return the clock when Enter is pressed
                        self.clock_display.reset()
                        return self.clock_display
                    elif event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        exit()
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        click = True
            
            # Button Click Logic
            if button_1.collidepoint((mouse_x, mouse_y)) and click:
                self.clock_display.reset()
                return self.clock_display
                
            if button_2.collidepoint((mouse_x, mouse_y)) and click:
                pass

            # Draw buttons
            pygame.draw.rect(self.screen, (250, 250, 250), button_1)
            pygame.draw.rect(self.screen, (250, 250, 250), button_2)
          
            # Draw text
            start_text = self.font_big.render("Start", True, (170, 150, 210))
            highscores_text = self.font_big.render("Highscores", True, (170, 150, 210))
            self.screen.blit(start_text, start_text.get_rect(center=button_1.center))
            self.screen.blit(highscores_text, highscores_text.get_rect(center=button_2.center))
        
            pygame.display.update()
            click = False