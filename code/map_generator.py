from settings import *
import pygame
import random
import math

class SimplexNoise:
    def __init__(self, seed=None):
        if seed is not None:
            random.seed(seed)
        self.perm = list(range(256))
        random.shuffle(self.perm)
        self.perm += self.perm

    def _fade(self, t):
        return t * t * t * (t * (t * 6 - 15) + 10)

    def _lerp(self, a, b, t):
        return a + t * (b - a)

    def _grad(self, h, x, y):
        h = h & 3
        if h == 0: return  x + y
        if h == 1: return -x + y
        if h == 2: return  x - y
        return -x - y

    def noise2(self, x, y):
        xi = int(math.floor(x)) & 255
        yi = int(math.floor(y)) & 255
        xf = x - math.floor(x)
        yf = y - math.floor(y)
        u = self._fade(xf)
        v = self._fade(yf)
        p = self.perm
        aa = p[p[xi]   + yi]
        ab = p[p[xi]   + yi + 1]
        ba = p[p[xi+1] + yi]
        bb = p[p[xi+1] + yi + 1]
        return self._lerp(
            self._lerp(self._grad(aa, xf,   yf),   self._grad(ba, xf-1, yf),   u),
            self._lerp(self._grad(ab, xf,   yf-1), self._grad(bb, xf-1, yf-1), u),
            v
        )


WATER = 12
GRASS = 42

ISLAND_PATTERNS = {
    "tl": 1,  "tc": 2,  "tr": 3,
    "ml": 11, "mc": 12, "mr": 13,
    "bl": 21, "bc": 22, "br": 23,
}

BORDER = {
    "tl": 94,  "tc": 95,  "tr": 96,
    "ml": 101, "mc": 102, "mr": 103,
    "bl": 111, "bc": 112, "br": 113,
}

GRASS_OBJECTS = [
    'grassrock1.png',
    'grassrock2.png',
    'green_tree.png',
    'green_tree_bushy.png',
    'green_tree_small.png',
    'ruin_pillar.png',
    'ruin_pillar_broke.png',
    'ruin_pillar_broke_alt.png',
]

SAND_OBJECTS = [
    'sandrock1.png',
    'sandrock2.png',
    'palm.png',
    'palm_alt.png',
    'palm_small.png',
]


class MapGenerator:
    def __init__(self, width_tiles=90, height_tiles=90):
        self.width  = width_tiles
        self.height = height_tiles
        self.tileset  = self._load_tileset()
        self.obj_surfs = self._load_objects()

    def _load_tileset(self):
        tileset = {}
        try:
            sheet = pygame.image.load(
                join('data', 'graphics', 'tilesets', 'world_tileset.png')
            ).convert_alpha()
            cols, tw, th = 10, 64, 64
            rows = sheet.get_height() // th
            tid = 1
            for r in range(rows):
                for c in range(cols):
                    surf = pygame.Surface((tw, th), pygame.SRCALPHA)
                    surf.blit(sheet, (0, 0), pygame.Rect(c*tw, r*th, tw, th))
                    tileset[tid] = surf
                    tid += 1
        except Exception as e:
            print(f"[MapGen] tileset error: {e}")
            surf = pygame.Surface((64, 64))
            surf.fill((34, 139, 34))
            for i in range(1, 220):
                tileset[i] = surf
        return tileset

    def _load_objects(self):
        surfs = {}
        base = join('data', 'graphics', 'objects')
        all_files = GRASS_OBJECTS + SAND_OBJECTS
        for fname in all_files:
            path = join(base, fname)
            try:
                surfs[fname] = pygame.image.load(path).convert_alpha()
            except:
                s = pygame.Surface((64, 64), pygame.SRCALPHA)
                pygame.draw.circle(s, (0, 150, 0), (32, 32), 28)
                surfs[fname] = s
        return surfs

    def _t(self, tid):
        return self.tileset.get(tid, self.tileset.get(GRASS))

    def generate(self):
        W, H = self.width, self.height
        seed = random.randint(0, 99999)
        noise  = SimplexNoise(seed=seed)
        noise2 = SimplexNoise(seed=seed + 1)
        scale  = 0.09

        heightmap = []
        for r in range(H):
            row = []
            for c in range(W):
                n  = noise.noise2(c * scale,     r * scale)
                n += 0.5  * noise.noise2(c * scale * 2, r * scale * 2)
                n += 0.25 * noise.noise2(c * scale * 4, r * scale * 4)
                row.append(n)
            heightmap.append(row)

        WATER_LVL = -0.1
        SHORE_LVL =  0.05

        biome = []
        for r in range(H):
            row = []
            for c in range(W):
                v = heightmap[r][c]
                if v < WATER_LVL:
                    row.append("water")
                elif v < SHORE_LVL:
                    row.append("shore")
                else:
                    row.append("land")
            biome.append(row)

        cx, cy = W // 2, H // 2
        for dr in range(-5, 6):
            for dc in range(-5, 6):
                if math.sqrt(dr*dr + dc*dc) <= 5:
                    biome[cy+dr][cx+dc] = "land"

        grid_surf = [[self._t(GRASS)] * W for _ in range(H)]
        grid_coll = [[False]          * W for _ in range(H)]

        for r in range(H):
            for c in range(W):
                if biome[r][c] == "water":
                    grid_surf[r][c] = self._t(WATER)

        def is_land(r, c):
            if r < 0 or r >= H or c < 0 or c >= W:
                return False
            return biome[r][c] == "land"

        for r in range(H):
            for c in range(W):
                if biome[r][c] != "land":
                    continue
                top   = not is_land(r-1, c)
                bot   = not is_land(r+1, c)
                left  = not is_land(r, c-1)
                right = not is_land(r, c+1)
                p = ISLAND_PATTERNS
                if   top  and left:  grid_surf[r][c] = self._t(p["tl"])
                elif top  and right: grid_surf[r][c] = self._t(p["tr"])
                elif bot  and left:  grid_surf[r][c] = self._t(p["bl"])
                elif bot  and right: grid_surf[r][c] = self._t(p["br"])
                elif top:            grid_surf[r][c] = self._t(p["tc"])
                elif bot:            grid_surf[r][c] = self._t(p["bc"])
                elif left:           grid_surf[r][c] = self._t(p["ml"])
                elif right:          grid_surf[r][c] = self._t(p["mr"])
                else:                grid_surf[r][c] = self._t(p["mc"])

        self._place_border(grid_surf, grid_coll, W, H)

        ground, objects = [], []

        for r in range(H):
            for c in range(W):
                x, y = c * TILE_SIZE, r * TILE_SIZE
                if grid_coll[r][c]:
                    objects.append((x, y, grid_surf[r][c], True))
                else:
                    ground.append((x, y, grid_surf[r][c]))

        obj_occupied = set()
        for r in range(2, H - 2):
            for c in range(2, W - 2):
                if biome[r][c] != "land":
                    continue
                if abs(r - cy) < 6 and abs(c - cx) < 6:
                    continue
                if not is_land(r, c):
                    continue
                if (c, r) in obj_occupied:
                    continue

                tv = noise2.noise2(c * 0.25, r * 0.25)
                if tv > 0.5:
                    fname = random.choice(GRASS_OBJECTS)
                    surf  = self.obj_surfs[fname]
                    sw, sh = surf.get_size()
                    px = c * TILE_SIZE + TILE_SIZE // 2 - sw // 2
                    py = r * TILE_SIZE + TILE_SIZE - sh
                    objects.append((px, py, surf, True))
                    for dc in range(-1, 2):
                        for dr in range(-1, 2):
                            obj_occupied.add((c+dc, r+dr))

        player_pos = (cx * TILE_SIZE, cy * TILE_SIZE)

        spawn_positions = []
        margin, step = 3, 5
        for c in range(margin, W - margin, step):
            spawn_positions.append((c * TILE_SIZE, margin * TILE_SIZE))
            spawn_positions.append((c * TILE_SIZE, (H - margin) * TILE_SIZE))
        for r in range(margin, H - margin, step):
            spawn_positions.append((margin * TILE_SIZE, r * TILE_SIZE))
            spawn_positions.append(((W - margin) * TILE_SIZE, r * TILE_SIZE))

        return {
            'ground':          ground,
            'objects':         objects,
            'player_pos':      player_pos,
            'spawn_positions': spawn_positions,
        }

    def _place_border(self, gs, gc, W, H):
        gs[0][0]     = self._t(BORDER["tl"]); gc[0][0]     = True
        gs[0][W-1]   = self._t(BORDER["tr"]); gc[0][W-1]   = True
        gs[H-1][0]   = self._t(BORDER["bl"]); gc[H-1][0]   = True
        gs[H-1][W-1] = self._t(BORDER["br"]); gc[H-1][W-1] = True
        for c in range(1, W-1):
            gs[0][c]   = self._t(BORDER["tc"]); gc[0][c]   = True
            gs[H-1][c] = self._t(BORDER["bc"]); gc[H-1][c] = True
        for r in range(1, H-1):
            gs[r][0]   = self._t(BORDER["ml"]); gc[r][0]   = True
            gs[r][W-1] = self._t(BORDER["mr"]); gc[r][W-1] = True
