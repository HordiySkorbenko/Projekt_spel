import pygame
import random
from os.path import join

class MapGenerator:
    def __init__(self, tile_size=64):
        self.tile_size = tile_size
        self.terrain_tiles = self.load_terrain_tiles()
        self.object_images = self.load_object_images()

    def load_terrain_tiles(self):
        # Laddar in din tileset och klipper ut gräset
        tileset_img = pygame.image.load(join('data', 'graphics', 'tilesets', 'world_tileset.png')).convert_alpha()
        columns = 10 
        tiles = {}
        
        # Gräs är index 41 (ID 42 i Tiled)
        grass_index = 41
        
        x = (grass_index % columns) * self.tile_size
        y = (grass_index // columns) * self.tile_size
        surf = pygame.Surface((self.tile_size, self.tile_size), pygame.SRCALPHA)
        surf.blit(tileset_img, (0, 0), (x, y, self.tile_size, self.tile_size))
        tiles['grass'] = surf
            
        return tiles

    def load_object_images(self):
        # Laddar alla objekt från din data-mapp
        return {
            'tree': pygame.image.load(join('data', 'graphics', 'objects', 'green_tree.png')).convert_alpha(),
            'tree_small': pygame.image.load(join('data', 'graphics', 'objects', 'green_tree_small.png')).convert_alpha(),
            'rock1': pygame.image.load(join('data', 'graphics', 'objects', 'grassrock1.png')).convert_alpha(),
            'ruin': pygame.image.load(join('data', 'graphics', 'objects', 'ruin_pillar.png')).convert_alpha()
        }

    def generate_clusters(self, width, height, fill_prob=0.45, steps=4):
        """Genererar kluster för skog och stenar"""
        grid = [[1 if random.random() < fill_prob else 0 for _ in range(width)] for _ in range(height)]

        for _ in range(steps):
            new_grid = [row[:] for row in grid]
            for y in range(height):
                for x in range(width):
                    # Räkna grannar för att bygga kluster
                    walls = 0
                    for dy in [-1, 0, 1]:
                        for dx in [-1, 0, 1]:
                            if dx == 0 and dy == 0: continue
                            nx, ny = x + dx, y + dy
                            if nx < 0 or ny < 0 or nx >= width or ny >= height or grid[ny][nx] == 1:
                                walls += 1
                    
                    # Jämna ut
                    if walls > 4: new_grid[y][x] = 1
                    elif walls < 4: new_grid[y][x] = 0
            grid = new_grid
        return grid

    def generate_map(self, width_tiles, height_tiles):
        """Skapar hela kartan med gräs och objekt"""
        map_width_px  = width_tiles  * self.tile_size
        map_height_px = height_tiles * self.tile_size

        # Baka alla grästiles till EN enda yta – noll per-frame-kostnad för marken
        ground_surface = pygame.Surface((map_width_px, map_height_px), pygame.SRCALPHA)
        grass = self.terrain_tiles['grass']
        for y in range(height_tiles):
            for x in range(width_tiles):
                ground_surface.blit(grass, (x * self.tile_size, y * self.tile_size))

        map_data = {
            'ground_surface': ground_surface,   # en enda yta istället för 2500 dicts
            'ground': [],                        # behålls tom för bakåtkompatibilitet
            'objects': [],
            'spawn_pos': (width_tiles // 2 * self.tile_size, height_tiles // 2 * self.tile_size),
            'grass_positions': []               # för enemy spawn-pos
        }

        forest_grid = self.generate_clusters(width_tiles, height_tiles, fill_prob=0.45)
        rock_grid   = self.generate_clusters(width_tiles, height_tiles, fill_prob=0.35)

        for y in range(height_tiles):
            for x in range(width_tiles):
                pos = (x * self.tile_size, y * self.tile_size)
                map_data['grass_positions'].append(pos)

                is_spawn_area = (abs(x - width_tiles//2) < 3 and abs(y - height_tiles//2) < 3)
                if not is_spawn_area:
                    if forest_grid[y][x] == 1:
                        img = self.object_images['tree'] if random.random() > 0.3 else self.object_images['tree_small']
                        map_data['objects'].append({'pos': pos, 'image': img, 'type': 'tree'})
                    elif rock_grid[y][x] == 1:
                        img = self.object_images['rock1'] if random.random() > 0.5 else self.object_images['ruin']
                        map_data['objects'].append({'pos': pos, 'image': img, 'type': 'rock'})

        return map_data