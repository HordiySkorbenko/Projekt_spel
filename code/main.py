from settings import *
from player import Player
from groups import Allsprites
from random import randint 
from sprites import *

class Game:
    def __init__(self):
        # setup
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Survivor')
        self.clock = pygame.time.Clock()
        self.running = True

        # groups 
        self.all_sprites = Allsprites()
        self.collision_sprites = pygame.sprite.Group()

        # sprites
        self.player = Player((400,300), self.all_sprites, self.collision_sprites)
        for i in range(6):
            x,y = randint(0, WINDOW_HEIGHT), randint(0, WINDOW_WIDTH)
            w,h = randint(60, 100), randint(50, 100)
            CollisionSprite((x,y),(w,h), (self.all_sprites, self.collision_sprites))

        #gun timer
        self.can_shoot = True
        self.shoot_time = 0
        self.gun_cooldown = 100

    def input(self):
        if pygame.mouse.get_pressed()[0] and self.can_shoot: #index 0 = vänster click
            self.can_shoot = False
            self.shoot_time = pygame.time.get_ticks
    
    def gun_timer(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.shoot_time >= self.gun_cooldown:
                self.can_shoot = True

    def run(self):
        while self.running:
            # dt 
            dt = self.clock.tick() / 1000

            # event loop 
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            # update 
            self.gun_timer()
            self.input()
            self.all_sprites.update(dt)

            # draw
            self.display_surface.fill('black')
            self.all_sprites.draw(self.player.rect.center)
            pygame.display.update()

        pygame.quit()

if __name__ == '__main__':
    game = Game()
    game.run()