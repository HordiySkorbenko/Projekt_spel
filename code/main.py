from settings import *
import pygame
from player import Player
from groups import Allsprites
from sprites import *
from pytmx.util_pygame import load_pygame
from random import choice, randint
from menu import Menu
from ui import XPBar, Clock, GameOver,Leaderboard
from mapgen_temp import MapGenerator
from threading import Thread

class Game:
    def __init__(self):
        # setup
        pygame.init()
        self.display_surface = pygame.display.set_mode(
            (WINDOW_WIDTH, WINDOW_HEIGHT),
            pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF,
            vsync=1
)        
        
        
        pygame.display.set_caption('Survivor')
        self.clock = pygame.time.Clock()
        self.running = True
        self.game_active = True
        self.game_over_screen = GameOver(self.display_surface)
        self.leaderboard_manager = Leaderboard()
        
        menu = Menu(self.display_surface)
        self.game_clock = menu.main_menu()
        self.difficulty = menu.difficulty
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
        pygame.time.set_timer(self.enemy_event,(1000//menu.difficulty))
        self.spawn_pos = []

        self.shoot_sound = pygame.mixer.Sound(join('audio', 'shoot.wav'))
        self.shoot_sound.set_volume(0.2)
        self.clock_display = Clock()
        self.load_images()
        self.setup()

    def load_images(self):
        self.bullet_surf = pygame.image.load(join('image', 'gun','bullet.png')).convert_alpha()

        folders = list(walk(join('image','enemies')))[0][1]
        self.enemy_frames = {}
        for folder in folders:
            for folder_path,_,file_names in walk(join('image','enemies',folder)):
                self.enemy_frames[folder] = []
                for file_name in sorted(file_names, key= lambda name: int(name.split('.')[0])):
                    full_path = join(folder_path,file_name)
                    surf = pygame.image.load(full_path).convert_alpha()
                    self.enemy_frames[folder].append(surf)

    def input(self):
        if pygame.mouse.get_pressed()[0] and self.can_shoot: 
            self.shoot_sound.play()
            pos = self.gun.rect.center + self.gun.player_direction * 50
            Bullet(self.bullet_surf,pos,self.gun.player_direction,(self.all_sprites, self.bullet_sprites))
            self.can_shoot = False
            self.shoot_time = pygame.time.get_ticks()
    
    def gun_timer(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            reduction = (self.player.level - 1) * 0.25
            current_cooldown = self.gun_cooldown * (1 - reduction)
            
            if current_time - self.shoot_time >= max(current_cooldown, 50):
                self.can_shoot = True
    
    def setup(self):
        self.spawn_pos = []  # alltid rensa innan vi bygger om
        map_gen = MapGenerator()
        map_data = map_gen.generate_map(50, 50)
        self.all_sprites.ground_surface = map_data['ground_surface']
        for obj in map_data['objects']:
            CollisionSprite(obj['pos'], obj['image'], (self.all_sprites, self.collision_sprites))
        start_x, start_y = map_data['spawn_pos']
        self.player = Player((start_x, start_y), self.all_sprites, self.collision_sprites)
        self.gun = Gun(self.player, self.all_sprites)
        self.xp_bar = XPBar(self.player)
        self.spawn_pos = map_data['grass_positions']  
    
    def bullet_collision(self):
        collision_dict = pygame.sprite.groupcollide(self.bullet_sprites, self.enemy_sprites, True, False)

        for bullet, enemies in collision_dict.items():
            for enemy in enemies:
                if enemy.death_time == 0:
                    enemy.destroy()
        
    def player_collision(self):
        if pygame.sprite.spritecollide(self.player, self.enemy_sprites, False, pygame.sprite.collide_mask):
            if self.game_active:
                # 1. Räkna ut värdena här i Game-klassen
                elapsed_ms = pygame.time.get_ticks() - self.clock_display.start_ticks
                time_str = f"{(elapsed_ms//60000):02}:{(elapsed_ms//1000)%60:02}"
                
                # 2. Skicka värdena till din leaderboard-instans
                self.leaderboard_manager.save_score(time_str, self.player.xp)
                
                self.game_active = False
    def reset_game(self):
        self.all_sprites.empty()
        self.collision_sprites.empty()
        self.enemy_sprites.empty()
        self.bullet_sprites.empty()
        self.spawn_pos = []
        self.can_shoot = True
        self.shoot_time = 0
        self.clock_display.reset()
        self.game_clock = self.clock_display
        
        self.setup()
        
        self.game_active = True
                        
    def run(self):
            font = pygame.font.SysFont("Arial", 18, bold=True)

            while self.running:
                # 1. EVENT LOOP
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            self.running = False
                        
                        
                        if not self.game_active and event.key == pygame.K_SPACE:
                            self.reset_game()
                            
                    
                    if self.game_active and event.type == self.enemy_event:
                        Enemy(choice(self.spawn_pos),choice(list(self.enemy_frames.values())), (self.all_sprites,self.enemy_sprites),self.player,self.collision_sprites, self.difficulty)
                
                
                if self.game_active:
                    dt = self.clock.tick() / 1000
                    
                    self.gun_timer()
                    self.input()
                    def update_enemies(dt):
                        for enemy in self.enemy_sprites:
                            enemy.update(dt)

                    enemy_thread = Thread(target=update_enemies, args=(dt,), daemon=True)
                    enemy_thread.start()

                    # Update non-enemy sprites on main thread:
                    for sprite in self.all_sprites:
                        if sprite not in self.enemy_sprites:
                            sprite.update(dt)

                    enemy_thread.join()
                    self.bullet_collision()
                    self.player_collision()
                    
                    self.display_surface.fill('black')
                    self.all_sprites.draw(self.player.rect.center)
                    
                    fps_text = font.render(str(int(self.clock.get_fps())), True, (255, 0, 0))
                    self.display_surface.blit(fps_text, (10, 10))
                    self.game_clock.draw(self.display_surface)
                    self.xp_bar.draw(self.display_surface)

                else:
                    top_five = self.leaderboard_manager.get_top_scores(5)
                    self.game_over_screen.draw(top_five)
                    

                pygame.display.update()


if __name__ == '__main__':
    game = Game()
    game.run()