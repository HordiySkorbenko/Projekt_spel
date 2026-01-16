from settings import *
import pygame


class Allsprites(pygame.sprite.Group):
    def __init__(self):
        super().__init__()

        # Ytan vi ritar på (skärmen)
        self.display_surface = pygame.display.get_surface()

        # Kamera-offset (MÅSTE vara en instans, inte klassen)
        self.offset = pygame.Vector2(0, 0)

    def draw(self, target_pos):
        """
        target_pos = positionen som kameran ska följa
        (t.ex. player.rect.center)
        """

        # Räkna ut kameraoffset så att spelaren hamnar i mitten
        self.offset.x = -(target_pos[0] - WINDOW_WIDTH / 2)
        self.offset.y = -(target_pos[1] - WINDOW_HEIGHT / 2)

        # Dela upp sprites i mark och objekt
        ground_sprites = [sprite for sprite in self if hasattr(sprite, 'ground')]
        object_sprites = [sprite for sprite in self if not hasattr(sprite, 'ground')]

        # Rita först mark, sedan objekt
        for layer in [ground_sprites, object_sprites]:

            # Y-sortering (djup)
            for sprite in sorted(layer, key=lambda sprite: sprite.rect.centery):

                # Flytta recten med kamerans offset
                offset_rect = sprite.rect.move(self.offset)

                # Rita sprite
                self.display_surface.blit(sprite.image, offset_rect)
