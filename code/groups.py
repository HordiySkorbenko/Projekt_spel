from settings import *
import pygame

class Allsprites(pygame.sprite.Group):
    def __init__(self):
        super().__init__()

        self.display_surface = pygame.display.get_surface()

        self.offset = pygame.Vector2(0, 0)
        
        
        self.cull_margin = 0
        self.screen_rect = pygame.Rect(
            -self.cull_margin,
            -self.cull_margin,
            WINDOW_WIDTH  + self.cull_margin * 2,
            WINDOW_HEIGHT + self.cull_margin * 2
        )

        self.ground_surface = None

    def draw(self, target_pos):
            self.offset.x = -(target_pos[0] - WINDOW_WIDTH / 2)
            self.offset.y = -(target_pos[1] - WINDOW_HEIGHT / 2)

            if self.ground_surface:
                self.display_surface.blit(self.ground_surface, self.offset)

            visible_objects = []
            for sprite in self:
                if hasattr(sprite, 'ground'):
                    continue  
                offset_rect = sprite.rect.move(self.offset)
                if self.screen_rect.colliderect(offset_rect):
                    visible_objects.append((sprite, offset_rect))

            for sprite, offset_rect in sorted(visible_objects, key=lambda item: item[0].rect.centery):
                self.display_surface.blit(sprite.image, offset_rect)