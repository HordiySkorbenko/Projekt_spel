import pygame
from settings import *

class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.font_big = pygame.font.Font("data/fonts/static/PixelifySans-Regular.ttf", 50)
        self.font_small = pygame.font.Font("data/fonts/static/PixelifySans-Regular.ttf", 35)
        
        
    def main_menu(self):
        running = True
        click = False
        
        while running:
        
            
            self.screen.fill((0, 255, 0))
            mouse_x, mouse_y = pygame.mouse.get_pos()
                    
            button_1 = pygame.Rect(WINDOW_WIDTH/2 - 250, WINDOW_HEIGHT/2, 400, 100)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        running = False
                    elif event.key == pygame.K_ESCAPE:
                        exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        click = True
                        
                        # om man klickar i start knappen stånger spelet
            if button_1.collidepoint((mouse_x, mouse_y)) and click:
                    running = False
                    
              
           

            # ritar ut knapparna
            pygame.draw.rect(self.screen, (250, 250, 250), button_1)
          
            # skapar texten och ritar ut texten  
            start_text = self.font_big.render("Start", True, (170, 150, 210))
            selection_text = self.font_small.render("Select level", True, (170, 150, 210))
            self.screen.blit(start_text, start_text.get_rect(center=button_1.center))
        
            pygame.display.update()
            click = False

    
