from settings import * 

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.image = pygame.image.load(join('image', 'player', 'down', '0.png')).convert_alpha()
        self.rect = self.image.get_rect(center = pos)
    
        # movement 
        self.direction = pygame.Vector2()
        self.speed = 500

    def input(self):
        keys = pygame.key.get_pressed()
        self.direction.x = (keys[pygame.K_RIGHT] or keys[pygame.K_d]) - \
                   (keys[pygame.K_LEFT]  or keys[pygame.K_a])
        self.direction.y = (keys[pygame.K_DOWN] or keys[pygame.K_s]) - \
                   (keys[pygame.K_UP]   or keys[pygame.K_w])
        self.direction = self.direction.normalize() if self.direction else self.direction

    def move(self, dt):
        self.rect.center += self.direction * self.speed * dt

    def update(self, dt):
        self.input()
        self.move(dt)