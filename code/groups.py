from settings import *

class Allsprites(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.Vector2
    def draw(self, target_pos):
        self.offset.x = -(target_pos[0]- WINDOW_WIDTH/2 )
        self.offset.y = -(target_pos[1]- WINDOW_HEIGHT/2 )
        # sorterar baseat på om center positionen av två sprites är över eller under varandra. Om en än under den andra kommer den ritas över spriten och vise versa, men ignorerar sprites utan collision
        # sorted sorterar fråm minsta till största värdet och key= lambda gör om värden så att dem är kompatibla
        ground_sprites = [sprite for sprite in self if hasattr (sprite,'ground')]
        object_sprites = [sprite for sprite in self if not hasattr (sprite,'ground')]
        for layer in [ground_sprites, object_sprites]:
            for sprite in sorted(layer, key = lambda sprite: sprite.rect.centery): 
                self.display_surface.blit(sprite.image,sprite.rect + self.offset)
