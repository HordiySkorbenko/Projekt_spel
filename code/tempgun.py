#todo lägg in dethär i sprites
"""todo: i game setup 'entities' lägga till:
self.gun = Gun(self.player, self.all_sprites)
from math import atan2,degrees
5:34:18
"""
from settings import *
from math import atan2,degrees

class Gun(pygame.sprite.Sprite):
    def __init__(self, player,groups):
        # koppling till player
        self.player = player
        self.distance = 90
        self.player_direction = pygame.Vector2(0,1)
        #pistol sprite position
        super().__init__(groups)
        self.gun_surf = pygame.image.load(join('images','gun','gun.png')).convert_alpha()
        self.image = self.gun_surf
        self.rect= self.image.get_rect(center = self.player.rect.center + self.player_direction * self.distance)

    def get_driection(self):
        mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
        player_pos = pygame.Vector2(WINDOW_WIDTH/2 ,WINDOW_HEIGHT/2)
        self.player_direction =(mouse_pos-player_pos).normalize()

    def rotate_gun(self):
        angle = degrees(atan2(self.player_direction.x, self.player_direction.y)) - 90
        if self.player_direction.x > 0:
            self.image = pygame.transform.rotozoom(self.gun_surf,angle,1)
        else:
            self.image = pygame.transform.rotozoom(self.gun_surf,abs(angle),1)
            self.image = pygame.transform.flip(self.image,False,True)


    #pistolen flyttar med spelaren
    def update(self, _):
        self.get_direction()
        self.rotate_gun()
        self.rect.center = self.player.rect.center + self.player_direction * self.distance

class Bullet(pygame.sprite.Sprite):
    def __init__( self, surface, pos, direction, groups):
        super().__init__(groups)
        self.image = surface
        self.rect = self.image.get_rect(center = pos)

