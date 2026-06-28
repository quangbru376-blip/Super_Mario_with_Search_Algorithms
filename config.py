import os
import pygame

# Brand Colors (Super Mario Theme)
COLOR_SKY = (92, 148, 252)      # Classic NES Mario sky blue
COLOR_RED = (229, 37, 33)       # Mario Red
COLOR_GREEN = (0, 177, 62)      # Luigi/Pipe Green
COLOR_COIN = (251, 208, 0)      # Golden Coin Yellow
COLOR_BRICK = (178, 95, 21)     # Brick Brown
COLOR_GROUND = (252, 188, 176)  # Ground peach color
COLOR_DARK = (42, 42, 46)       # Fog of war dark gray
COLOR_DARK_LIGHT = (58, 58, 62)
COLOR_PATH = (46, 204, 113)     # Path green
COLOR_VISITED = (170, 220, 255) # Expanded node blue
COLOR_FRONTIER = (255, 232, 160)# Frontier node yellow
COLOR_SWAMP = (101, 67, 33)     # Swamp brown
COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_GRAY = (200, 200, 200)

# UI Config
CELL_SIZE = 30             # Pixels per grid cell
DEFAULT_SPEED = 200        # ms delay between steps

# Asset Fallback Management
# Load pixel art if present, otherwise fall back to shapes
class AssetManager:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AssetManager, cls).__new__(cls)
            cls._instance.assets = {}
            cls._instance.original_images = {}
            cls._instance.loaded = False
        return cls._instance
        
    def load_assets(self):
        if self.loaded:
            return
        
        # Look for asset files in workspace
        asset_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "resources", "images")
        images = {
            "mario": "mario.png",
            "brick": "brick.png",
            "castle": "castle.png",
            "coin": "coin.png",
            "star": "star.png",
            "bowser": "bowser.png",
            "title": "menu_title_50percent.png"
        }
        
        for name, filename in images.items():
            path = os.path.join(asset_dir, filename)
            if os.path.exists(path):
                try:
                    img = pygame.image.load(path).convert_alpha()
                    self.original_images[name] = img
                    self.assets[name] = img
                except Exception as e:
                    print(f"Error loading {name}: {e}")
                    self.assets[name] = None
            else:
                self.assets[name] = None
        self.loaded = True

    def get(self, name, size=None):
        self.load_assets()
        if size is None or name not in self.original_images:
            return self.assets.get(name)
            
        w, h = int(size[0]), int(size[1])
        if w <= 0 or h <= 0:
            return self.assets.get(name)
            
        key = f"{name}_{w}x{h}"
        if key not in self.assets:
            img = pygame.transform.smoothscale(self.original_images[name], (w, h))
            self.assets[key] = img
            
        return self.assets.get(key)

# Predefined maps for World 1 & 2 (Maze Pathfinder)
# 0 = Empty, 1 = Wall, S = Start, G = Goal
MAZE_MAPS = {
    "Mê cung nhỏ (10x10)": [
        ["S", 0,  0,  0,  0,  0,  0,  0,  0,  0 ], # Dòng 0: Bẫy 1 của DFS
        [ 0,  1,  1,  1,  1,  1,  1,  1,  1,  0 ], 
        [ 0,  1,  0,  0,  0,  0,  0,  0,  0,  0 ], 
        [ 0,  1,  1,  1,  1,  1,  1,  1,  1,  1 ], 
        [ 0,  0,  0,  2,  2,  2,  2,  0,  0, "G"], # Dòng 4: Đường ngắn nhất nhưng nhiều Đầm lầy
        [ 0,  1,  1,  1,  1,  1,  1,  1,  1,  0 ], 
        [ 0,  1,  0,  0,  0,  0,  0,  0,  0,  0 ], # Dòng 6: Bẫy 2 của DFS
        [ 0,  1,  1,  1,  1,  1,  1,  1,  1,  0 ], 
        [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0 ], # Dòng 8: Đường vòng an toàn
        [ 1,  1,  1,  1,  1,  1,  1,  1,  1,  0 ]  
    ],

    "Mê cung trung bình (15x15)": [
        ["S", 0,  0,  1,  0,  0,  1,  0,  0,  0,  1,  0,  2,  0,  1], 
        [ 0,  1,  0,  1,  1,  0,  1,  1,  1,  0,  1,  1,  1,  1,  1], 
        [ 0,  1,  0,  1,  0,  0,  0,  2,  0,  1,  0,  0,  0,  0,  0], 
        [ 2,  1,  0,  1,  0,  1,  1,  1,  0,  1,  1,  1,  0,  1,  0], 
        [ 0,  1,  0,  1,  0,  2,  0,  1,  0,  0,  0,  1,  0,  1,  0], 
        [ 0,  1,  0,  1,  1,  1,  0,  1,  1,  1,  0,  1,  0,  1,  0], 
        [ 0,  1,  0,  0,  0,  1,  0,  0,  0,  1,  0,  1,  0,  1,  0], 
        [ 2,  1,  0,  1,  0,  1,  1,  1,  0,  1,  0,  1,  0,  1,  0], 
        [ 0,  1,  0,  1,  0,  0,  0,  1,  0,  1,  0,  1,  0,  1,  0], 
        [ 0,  1,  0,  1,  1,  1,  0,  1,  0,  1,  0,  1,  0,  1,  0], 
        [ 0,  1,  0,  1,  0,  0,  0,  1,  0,  1,  0,  1,  0,  1,  0], 
        [ 2,  1,  0,  1,  0,  1,  1,  1,  1,  1,  1,  1,  0,  1,  0], 
        [ 0,  1,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  1,  0], 
        [ 0,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  0], 
        [ 0,  0,  0,  2,  0,  0,  0,  2,  0,  0,  0,  2,  0,  0, "G"] 
    ],
    "Mê cung lớn (20x20)": [
        ["S", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0], # Row 0
        [1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 0, 1, 0, 0, 0], # Row 1
        [0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0], # Row 2
        [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0], # Row 3
        [1, 0, 1, 0, 1, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0], # Row 4
        [1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 1, 0], # Row 5
        [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 1], # Row 6
        [0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0], # Row 7
        [0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0], # Row 8
        [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0], # Row 9
        [0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0], # Row 10
        [0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0], # Row 11
        [0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0], # Row 12
        [0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0], # Row 13
        [0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0], # Row 14
        [1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0], # Row 15
        [0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0], # Row 16
        [1, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1], # Row 17
        [1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0], # Row 18
        [0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1, 0, 0, "G"]
    ]
}

# Terrain maps for World 3 (Local Search Elevation)
# Grid values: 0 to 9. Mario starts at valley, goal is peak(9).
TERRAIN_MAPS = {
    "Đồi đơn đỉnh (Single Peak)": [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 1, 2, 1, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 1, 2, 3, 2, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 2, 3, 4, 3, 2, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 2, 3, 4, 5, 4, 3, 2, 1, 0, 0, 0],
        [0, 0, 0, 1, 3, 4, 6, 7, 6, 4, 3, 2, 1, 0, 0], # <-- [5][7]: Cực đại ĐỊA PHƯƠNG (Đỉnh 7)
        [0, 0, 0, 1, 2, 3, 5, 6, 5, 8, 5, 3, 1, 0, 0],
        [0, 0, 0, 0, 1, 2, 4, 5, 4, 9, 8, 4, 1, 0, 0], # <-- [7][9]: Cực đại TOÀN CỤC (Đỉnh 9)
        [0, 0, 0, 0, 0, 1, 3, 4, 3, 8, 7, 3, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 2, 3, 2, 7, 6, 2, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 1, 2, 1, 6, 5, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 1, 4, 5, 4, 0, 0, 0, 0], # <-- [11][7]: ĐIỂM BẮT ĐẦU (Giá trị 1)
        [0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ],
    "Nhiều đỉnh núi (Multi-Peak)": [
        [0, 1, 2, 3, 2, 1, 0, 1, 2, 3, 4, 3, 2, 1, 0],
        [1, 2, 3, 4, 3, 2, 1, 2, 3, 4, 5, 4, 3, 2, 1],
        [2, 3, 5, 4, 2, 1, 2, 3, 4, 5, 6, 5, 4, 2, 1],
        [1, 2, 3, 2, 1, 0, 3, 4, 6, 7, 6, 4, 3, 1, 0],
        [0, 1, 1, 1, 0, 1, 4, 5, 7, 8, 7, 5, 2, 1, 0],
        [0, 0, 0, 0, 1, 2, 5, 6, 8, 9, 8, 6, 3, 1, 0],
        [1, 2, 1, 0, 2, 3, 4, 5, 7, 8, 7, 5, 4, 2, 1],
        [2, 4, 3, 1, 3, 4, 3, 4, 5, 6, 5, 4, 3, 2, 2],
        [3, 5, 4, 2, 4, 5, 2, 3, 4, 4, 4, 3, 2, 1, 1],
        [2, 4, 3, 1, 3, 4, 1, 2, 3, 3, 3, 2, 1, 0, 0],
        [1, 2, 2, 0, 2, 3, 2, 3, 4, 5, 4, 3, 2, 1, 0],
        [0, 1, 1, 0, 1, 2, 3, 4, 5, 6, 5, 4, 3, 2, 1],
        [0, 0, 0, 0, 0, 1, 4, 5, 6, 7, 6, 5, 4, 3, 2],
        [0, 1, 2, 1, 0, 2, 3, 4, 5, 6, 5, 4, 3, 2, 1],
        [0, 0, 1, 0, 0, 1, 2, 3, 4, 5, 4, 3, 2, 1, 0]
    ]
}

# Map for World 4 (Vacuum Cleaner Problem / Fog World)
# S = Start, C = Coin (Dirt), 0 = Empty floor, 1 = Wall
VACUUM_MAP = [
    [ 0,  0,  0,  0,  0],
    [ 0, "S", 0, "C", 0],
    [ 0,  0,  0,  0,  0],
    [ 0, "C", 0, "C", 0],
    [ 0,  0,  0,  0,  0]
]

# Map cho World 5 (CSP Map Coloring)
# Các số nguyên đại diện cho các Vùng (Regions) có hình dạng tùy ý.
CSP_REGIONS_MAP = [
    [ 0,  0,  0,  0,  1,  1,  1,  2,  2,  2],
    [ 0,  0,  3,  3,  1,  4,  1,  2,  5,  2],
    [ 0,  3,  3,  3,  4,  4,  4,  2,  5,  5],
    [ 6,  6,  3,  4,  4,  7,  7,  7,  5,  5],
    [ 6,  6,  8,  8,  4,  7,  9,  7,  7,  5],
    [ 6,  8,  8,  8,  8,  7,  9,  9,  9, 10],
    [11, 11, 11,  8, 12, 12, 12,  9, 10, 10],
    [11, 13, 11, 12, 12, 14, 12,  9, 10, 10],
    [13, 13, 13, 13, 14, 14, 14, 10, 10, 15],
    [13, 13, 13, 14, 14, 14, 14, 15, 15, 15]
]

BOSS_WORLD_MAP = [
    ["M", 0, 0, 1, 0],
    [0, 1, 0, 0, 0],
    [0, 0, 1, 0, 0],
    [1, 0, 0, 1, 0],
    [0, 0, 0, 0, "B"]
]
