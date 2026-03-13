from settings import *
import pygame
import random

# ─────────────────────────────────────────────
# Тайлсет: 10 колонок, 64x64, 210 тайлів
# Індекси (як в TMX, починаються з 1)
# ─────────────────────────────────────────────

# ЗЕМЛЯ
GRASS   = 42   # зелена трава (основний фон)
SAND    = 52   # пісок / світла земля (якщо є)
WATER   = 102  # вода / темні тайли

# ПАТЕРНИ ДЛЯ ОСТРІВЦІВ (з TMX: рядки типу кутів+стін)
# Формат: верхній-лівий кут починається, рядки знизу вниз
ISLAND_PATTERNS = [
    # Маленький острівець 3x3 (зелений)
    [
        [ 1,  2,  3],
        [11, 12, 13],
        [21, 22, 23],
    ],
    # Середній острівець 4x3
    [
        [ 1,  2,  2,  3],
        [11, 12, 12, 13],
        [21, 22, 22, 23],
    ],
    # Великий острівець 5x4
    [
        [ 1,  2,  2,  2,  3],
        [11, 12, 12, 12, 13],
        [11, 12, 12, 12, 13],
        [21, 22, 22, 22, 23],
    ],
    # Піщаний острівець
    [
        [31, 32, 33],
        [41, 42, 43],
        [51, 52, 53],
    ],
    # Ще один варіант (зі зміщенням у тайлсеті)
    [
        [61, 62, 63],
        [71, 72, 73],
        [81, 82, 83],
    ],
]

# Декоративні елементи (1 тайл, без колізії)
DECO_TILES = [34, 35, 36, 44, 45, 46, 54, 55, 56]

# Тайли з колізією (стіни, об'єкти)
COLLISION_TILE_IDS = set(range(91, 115))  # верхні рядки тайлсету — об'єкти


class MapGenerator:
    def __init__(self, width_tiles=52, height_tiles=50):
        self.width = width_tiles
        self.height = height_tiles
        self.tileset = self._load_tileset()

    def _load_tileset(self):
        """Нарізає world_tileset.png на словник {tile_id: Surface}"""
        tileset = {}
        try:
            sheet = pygame.image.load(
                join('data', 'graphics', 'tilesets', 'world_tileset.png')
            ).convert_alpha()

            cols = 10   # з .tsx: columns="10"
            tile_w = 64
            tile_h = 64

            tile_id = 1
            sheet_w, sheet_h = sheet.get_size()
            rows = sheet_h // tile_h

            for row in range(rows):
                for col in range(cols):
                    surf = pygame.Surface((tile_w, tile_h), pygame.SRCALPHA)
                    surf.blit(sheet, (0, 0),
                              pygame.Rect(col * tile_w, row * tile_h, tile_w, tile_h))
                    tileset[tile_id] = surf
                    tile_id += 1

            print(f"[MapGen] Завантажено {len(tileset)} тайлів")
        except Exception as e:
            print(f"[MapGen] ПОМИЛКА завантаження тайлсету: {e}")
            # Fallback — зелений квадрат під ID 42
            surf = pygame.Surface((64, 64))
            surf.fill((34, 139, 34))
            for i in range(1, 211):
                tileset[i] = surf

        return tileset

    def get_tile(self, tile_id):
        """Безпечно отримати тайл за ID"""
        return self.tileset.get(tile_id, self.tileset.get(GRASS))

    # ─────────────────────────────────────────
    def generate(self):
        """
        Генерує карту і повертає:
        {
          'ground':   [(x, y, surf), ...],
          'objects':  [(x, y, surf, has_collision), ...],
          'player_pos': (x, y),
          'spawn_positions': [(x, y), ...]
        }
        """
        ground  = []
        objects = []
        blocked = set()   # (col, row) зайняті об'єктами

        # ── 1. ФОН — заповнюємо ВОДОЮ (тайл 102) ──
        bg_tile = self.get_tile(WATER)
        for row in range(self.height):
            for col in range(self.width):
                ground.append((col * TILE_SIZE, row * TILE_SIZE, bg_tile))

        # ── 2. ОСТРІВЦІ ──
        # Гарантований великий острів у центрі
        center_col = self.width  // 2
        center_row = self.height // 2
        self._place_pattern(
            ground, blocked,
            ISLAND_PATTERNS[2],   # великий зелений острів
            center_col - 2, center_row - 2
        )

        # Рандомні острівці по карті
        num_islands = random.randint(8, 16)
        for _ in range(num_islands):
            pattern = random.choice(ISLAND_PATTERNS)
            ph = len(pattern)
            pw = len(pattern[0])

            # Не перетинаємо центральний спавн гравця
            attempts = 0
            while attempts < 20:
                col = random.randint(1, self.width  - pw - 1)
                row = random.randint(1, self.height - ph - 1)

                too_close = (
                    abs(col - center_col) < 6 and
                    abs(row - center_row) < 6
                )
                if not too_close:
                    self._place_pattern(ground, blocked, pattern, col, row)
                    break
                attempts += 1

        # ── 3. ДЕКОРАЦІЇ на острівцях ──
        island_cells = {(x // TILE_SIZE, y // TILE_SIZE)
                        for x, y, _ in ground
                        if self._is_land_tile(x // TILE_SIZE, y // TILE_SIZE, blocked)}

        num_decos = random.randint(15, 30)
        deco_placed = 0
        for _ in range(200):
            if deco_placed >= num_decos:
                break
            col = random.randint(0, self.width  - 1)
            row = random.randint(0, self.height - 1)

            if (col, row) in blocked:
                continue
            # Тільки не в зоні спавну гравця
            if abs(col - center_col) < 3 and abs(row - center_row) < 3:
                continue

            deco_id = random.choice(DECO_TILES)
            surf = self.get_tile(deco_id)
            objects.append((col * TILE_SIZE, row * TILE_SIZE, surf, False))
            deco_placed += 1

        # ── 4. ПОЗИЦІЯ ГРАВЦЯ ──
        player_pos = (center_col * TILE_SIZE, center_row * TILE_SIZE)

        # ── 5. СПАВН ВОРОГІВ — на краях карти ──
        spawn_positions = []
        step = 4
        for col in range(0, self.width, step):
            spawn_positions.append((col * TILE_SIZE, 0))
            spawn_positions.append((col * TILE_SIZE, (self.height - 1) * TILE_SIZE))
        for row in range(0, self.height, step):
            spawn_positions.append((0, row * TILE_SIZE))
            spawn_positions.append(((self.width - 1) * TILE_SIZE, row * TILE_SIZE))

        return {
            'ground':          ground,
            'objects':         objects,
            'player_pos':      player_pos,
            'spawn_positions': spawn_positions,
        }

    # ─────────────────────────────────────────
    def _place_pattern(self, ground, blocked, pattern, start_col, start_row):
        """Малює патерн тайлів поверх фону"""
        for dr, row_ids in enumerate(pattern):
            for dc, tile_id in enumerate(row_ids):
                col = start_col + dc
                row = start_row + dr
                if 0 <= col < self.width and 0 <= row < self.height:
                    x = col * TILE_SIZE
                    y = row * TILE_SIZE
                    surf = self.get_tile(tile_id)
                    # Замінюємо існуючий тайл (перебираємо список і міняємо)
                    # Простіший спосіб — просто додаємо зверху (останній bulit перекриє)
                    ground.append((x, y, surf))
                    blocked.add((col, row))

    def _is_land_tile(self, col, row, blocked):
        return (col, row) in blocked