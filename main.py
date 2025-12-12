import pygame
import sys
from settings import *


class Game:
    def __init__(self):
        pygame.init()
        #screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Projekt Spel")
        self.clock = pygame.time.Clock()
        self.run = True
        
        self.load_assets()
    
    def load_assets(self):
        pass

    def handle_events(self):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False




    player = pygame.Rect((300,250,50,50))

    def update(self):
        pass
    
    def render(self):
        self.screen.fill((30, 30, 50)) 
        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(FPS)
        pygame.quit()
        sys.exit()

                