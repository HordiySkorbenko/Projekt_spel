from settings import *
import pygame
from player import Player
from groups import Allsprites
from sprites import *
from pytmx.util_pygame import load_pygame
from random import choice, randint
from menu import Menu
from ui import XPBar

class Game:
    def __init__(self):
        # setup
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT),pygame.FULLSCREEN)
        pygame.display.set_caption('Survivor')
        self.clock = pygame.time.Clock()
        self.running = True
        
        menu = Menu(self.display_surface)
        menu.main_menu()

        # groups 
        self.all_sprites = Allsprites()
        self.collision_sprites = pygame.sprite.Group()
        self.bullet_sprites = pygame.sprite.Group()  
        self.enemy_sprites = pygame.sprite.Group()        

        #gun timer
        self.can_shoot = True
        self.shoot_time = 0
        self.gun_cooldown = 450

        #enemy timer
        self.enemy_event = pygame.event.custom_type()
        pygame.time.set_timer(self.enemy_event,1000)# timer till 300 om hard difficulty
        self.spawn_pos = []

        self.shoot_sound = pygame.mixer.Sound(join('audio', 'shoot.wav'))
        self.shoot_sound.set_volume(0.2)
        
        self.load_images()
        self.setup()

    def bullet_collision(self):
        collision_dict = pygame.sprite.groupcollide(self.bullet_sprites, self.enemy_sprites, True, False)

        for bullet, enemies in collision_dict.items():
            for enemy in enemies:
                # Kontrollera att metoden finns innan vi anropar den
                if hasattr(enemy, 'destroy'):
                    enemy.destroy()

    def load_images(self):
        self.bullet_surf = pygame.image.load(join('image', 'gun','bullet.png')).convert_alpha()

        folders = list(walk(join('image','enemies')))[0][1]
        self.enemy_frames = {}
        for folder in folders:
            for folder_path,_,file_names in walk(join('image','enemies',folder)):
                self.enemy_frames[folder] = []
                for file_name in sorted(file_names, key= lambda name: int(name.split('.')[0])): # konvertera file path till int: 0.png till 0
                    full_path = join(folder_path,file_name)
                    surf = pygame.image.load(full_path).convert_alpha()
                    self.enemy_frames[folder].append(surf)




    def input(self):
        if pygame.mouse.get_pressed()[0] and self.can_shoot: #index 0 = vänster click
            self.shoot_sound.play()
            pos = self.gun.rect.center + self.gun.player_direction * 50
            Bullet(self.bullet_surf,pos,self.gun.player_direction,(self.all_sprites, self.bullet_sprites))
            self.can_shoot = False
            self.shoot_time = pygame.time.get_ticks()
    
    def gun_timer(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            
            # Minska cooldown med 10% av originalet för varje level efter den första
            reduction = (self.player.level - 1) * 0.25
            current_cooldown = self.gun_cooldown * (1 - reduction)
            
            # Max-gräns så man inte skjuter oändligt snabbt
            if current_time - self.shoot_time >= max(current_cooldown, 50):
                self.can_shoot = True
    
    def setup(self):
        map = load_pygame(join('data','maps', 'world.tmx'))
        
        for x,y, image in map.get_layer_by_name('Ground').tiles():
            Sprite((x * TILE_SIZE, y * TILE_SIZE), image, self.all_sprites,)  
        for obj in map.get_layer_by_name('Objects'):
            CollisionSprite((obj.x, obj.y), obj.image, (self.all_sprites, self.collision_sprites))
        for obj in map.get_layer_by_name('Collisions'):
            CollisionSprite((obj.x, obj.y), pygame.Surface((obj.width, obj.height)), self.collision_sprites)
        for obj in map.get_layer_by_name('Entities'):
            if obj.name == 'Player':
                self.player = Player((obj.x,obj.y),self.all_sprites,self.collision_sprites)
                self.gun = Gun(self.player,self.all_sprites)
                self.xp_bar = XPBar(self.player)

            else:
                self.spawn_pos.append((obj.x,obj.y))

    def bullet_collision(self):
        # Denna rad ersätter hela din nuvarande loop och är extremt snabb
        collision_dict = pygame.sprite.groupcollide(self.bullet_sprites, self.enemy_sprites, True, False)

        for bullet, enemies in collision_dict.items():
            for enemy in enemies:
                if enemy.death_time == 0:
                    enemy.destroy()
        
    def player_collision(self):
        if pygame.sprite.spritecollide(self.player, self.enemy_sprites, False, pygame.sprite.collide_mask):
            self.running = False
                        
    def run(self):
        font = pygame.font.SysFont("Arial", 18, bold=True)

        while self.running:
            # dt 
            dt = self.clock.tick() / 1000

            # event loop 
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                if event.type == self.enemy_event:
                    Enemy(choice(self.spawn_pos),choice(list(self.enemy_frames.values())), (self.all_sprites,self.enemy_sprites),self.player,self.collision_sprites)

            # update 
            self.gun_timer()
            self.input()
            self.all_sprites.update(dt)

            # draw
            self.display_surface.fill('black')
            self.all_sprites.draw(self.player.rect.center)
            fps_text = font.render(str(int(self.clock.get_fps())), True, (255, 0, 0))
            self.display_surface.blit(fps_text, (10, 10))

            self.xp_bar.draw(self.display_surface)


            pygame.display.update()
            self.bullet_collision()
            self.player_collision()

        pygame.quit()

if __name__ == '__main__':
    game = Game()
    game.run()