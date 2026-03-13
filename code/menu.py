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
        
        self.difficulty = 1
        self.clock_display = Clock()
        
        self.logo = pygame.image.load("image/logo/logo1.png").convert_alpha()
        self.logo_rect = self.logo.get_rect()
        self.logo_rect.centerx = WINDOW_WIDTH // 2
        self.logo_rect.y = 40
        self.logo_y = 40
        self.logo_dir = 1
        
    def main_menu(self):
        running = True
        click = False
        
        while running:
            for y in range(WINDOW_HEIGHT):
                color = (20 + y//20, 10, 30 + y//25)
                pygame.draw.line(self.screen, color, (0,y), (WINDOW_WIDTH,y))
            self.screen.blit(self.logo, self.logo_rect)
            mouse_x, mouse_y = pygame.mouse.get_pos()
            
            
                    
            button_1 = pygame.Rect(WINDOW_WIDTH/2 - 940, WINDOW_HEIGHT/2, 400, 100)
            button_2 = pygame.Rect(WINDOW_WIDTH/2 - 940, WINDOW_HEIGHT/2 - 200, 400, 100)
            button_3 = pygame.Rect(WINDOW_WIDTH/2 - 940, (WINDOW_HEIGHT/2)+ 200, 400, 100)
            
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
                self.difficulty_select()
            
            if button_3.collidepoint((mouse_x, mouse_y)) and click:
                pass
            
                    
              
           

            # ritar ut knapparna
            self.draw_button(button_1, "Start", self.font_big)
            self.draw_button(button_2, "Difficulty", self.font_small)
            self.draw_button(button_3, "Highscores", self.font_big)

          
            # Draw text
            start_text = self.font_big.render("Start", True, (0, 0, 0))
            selection_text = self.font_small.render("Difficulty", True, (0, 0, 0))
            highscores_text = self.font_big.render("Highscores", True, (0, 0, 0))
            self.screen.blit(start_text, start_text.get_rect(center=button_1.center))
            self.screen.blit(selection_text, selection_text.get_rect(center=button_2.center))
            self.screen.blit(highscores_text, highscores_text.get_rect(center=button_3.center))


        
            pygame.display.update()
            click = False
    
    def draw_button(self, rect, text, font):
        mouse_pos = pygame.mouse.get_pos()

        if rect.collidepoint(mouse_pos):
            color = (200, 250, 200)   
            border = (250, 0, 0)
        else:
            color = (250, 250, 250)
            border = (80, 80, 80)

        pygame.draw.rect(self.screen, color, rect)
        pygame.draw.rect(self.screen, (0,0,0), rect, 6)
        pygame.draw.rect(self.screen, border, rect.inflate(-6,-6), 3)
        

        text_surface = font.render(text, True, (40, 40, 40))
        self.screen.blit(text_surface, text_surface.get_rect(center=rect.center))       
         
    def difficulty_select(self):
        running = True
        
        click = False

        while running:
            # bakgrund     
            self.screen.fill((0, 255, 0))
            mouse_x, mouse_y = pygame.mouse.get_pos()

            # skapar knapparna
            level_button_1 = pygame.Rect(200, 150, 200, 50)
            level_button_2 = pygame.Rect(200, 250, 200, 50)
            level_button_3 = pygame.Rect(200, 350, 200, 50)
            

           # returnar om man antingen valde level 1 2 eler 3
            if level_button_1.collidepoint((mouse_x, mouse_y)) and click:
                self.difficulty = 1
                return self.difficulty
            if level_button_2.collidepoint((mouse_x, mouse_y)) and click:  
                self.difficulty = 2
                return self.difficulty
            if level_button_3.collidepoint((mouse_x, mouse_y)) and click:
                self.difficulty = 3
                return self.difficulty
            
            pygame.draw.rect(self.screen, (250, 250, 250), level_button_1) 
            pygame.draw.rect(self.screen, (250, 250, 250), level_button_2)
            pygame.draw.rect(self.screen, (250, 250, 250), level_button_3)
            
            # ritar texten för varje knapp
            diff1_text = self.font_big.render("Too Easy", True, (170, 150, 210))
            diff2_text = self.font_big.render("Average", True, (170, 150, 210))
            diff3_text = self.font_big.render("Imposible", True, (170, 150, 210))
            self.screen.blit(diff1_text, diff1_text.get_rect(center=level_button_1.center))
            self.screen.blit(diff2_text, diff2_text.get_rect(center=level_button_2.center))
            self.screen.blit(diff3_text, diff3_text.get_rect(center=level_button_3.center))
            
            


           
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        click = True
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    running = False

            pygame.display.update()


    
