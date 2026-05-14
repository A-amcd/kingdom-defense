# ================================
# 塔防游戏 - 鸿蒙防线
# 第五关：终末地
# 主题：末世废土、废墟、融合生物、最终决战
# ================================

import pygame
import math
import random

pygame.init()

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
GRID_SIZE = 40
FPS = 60

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("鸿蒙防线 - 终末地")
clock = pygame.time.Clock()

def get_chinese_font(size):
    import os
    font_dirs = [os.path.join(os.environ.get('WINDIR', 'C:\\Windows'), 'Fonts'), '.']
    font_files = ["msyh.ttc", "simhei.ttf", "simsun.ttc", None]
    for font_dir in font_dirs:
        for font_file in font_files[:-1]:
            font_path = os.path.join(font_dir, font_file)
            if os.path.exists(font_path):
                try:
                    return pygame.font.Font(font_path, size)
                except:
                    continue
    return pygame.font.Font(None, size)

font = get_chinese_font(28)
small_font = get_chinese_font(18)
large_font = get_chinese_font(72)

EMPTY = (0, 0, 0, 0)
YELLOW = (255, 215, 0, 255)
BROWN = (139, 90, 43, 255)
BLUE = (65, 105, 225, 255)
BLACK = (0, 0, 0, 255)
WHITE = (255, 255, 255, 255)
SKIN = (255, 218, 185, 255)

HERO_FRAME_1 = [
    [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
    [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, YELLOW, YELLOW, YELLOW, YELLOW, YELLOW, YELLOW, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
    [EMPTY, EMPTY, EMPTY, EMPTY, YELLOW, YELLOW, YELLOW, YELLOW, YELLOW, YELLOW, YELLOW, YELLOW, EMPTY, EMPTY, EMPTY, EMPTY],
    [EMPTY, EMPTY, EMPTY, EMPTY, YELLOW, YELLOW, YELLOW, YELLOW, YELLOW, YELLOW, YELLOW, YELLOW, EMPTY, EMPTY, EMPTY, EMPTY],
    [EMPTY, EMPTY, EMPTY, EMPTY, YELLOW, YELLOW, BLACK, BLACK, BLACK, BLACK, YELLOW, YELLOW, EMPTY, EMPTY, EMPTY, EMPTY],
    [EMPTY, EMPTY, EMPTY, EMPTY, YELLOW, YELLOW, BLACK, BLACK, WHITE, BLACK, YELLOW, YELLOW, EMPTY, EMPTY, EMPTY, EMPTY],
    [EMPTY, EMPTY, EMPTY, EMPTY, YELLOW, YELLOW, BLACK, BLACK, BLACK, BLACK, YELLOW, YELLOW, EMPTY, EMPTY, EMPTY, EMPTY],
    [EMPTY, EMPTY, EMPTY, EMPTY, YELLOW, YELLOW, YELLOW, YELLOW, YELLOW, YELLOW, YELLOW, YELLOW, EMPTY, EMPTY, EMPTY, EMPTY],
    [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, YELLOW, YELLOW, YELLOW, YELLOW, YELLOW, YELLOW, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
    [EMPTY, EMPTY, EMPTY, BLUE, BLUE, BLUE, BLUE, BLUE, BLUE, BLUE, BLUE, BLUE, BLUE, EMPTY, EMPTY, EMPTY],
    [EMPTY, EMPTY, EMPTY, BLUE, BLUE, BLUE, BLUE, BLUE, BLUE, BLUE, BLUE, BLUE, BLUE, EMPTY, EMPTY, EMPTY],
    [EMPTY, EMPTY, EMPTY, EMPTY, BLUE, BLUE, BLUE, BLUE, BLUE, BLUE, BLUE, BLUE, EMPTY, EMPTY, EMPTY, EMPTY],
    [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, BROWN, BROWN, BROWN, BROWN, BROWN, BROWN, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
    [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, BROWN, BROWN, BROWN, BROWN, BROWN, BROWN, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
    [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, BROWN, BROWN, EMPTY, EMPTY, BROWN, BROWN, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
    [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, BROWN, BROWN, EMPTY, EMPTY, BROWN, BROWN, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
]

HERO_FRAME_2 = [
    [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
    [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
    [EMPTY, EMPTY, EMPTY, EMPTY, YELLOW, YELLOW, YELLOW, YELLOW, YELLOW, YELLOW, YELLOW, YELLOW, EMPTY, EMPTY, EMPTY, EMPTY],
    [EMPTY, EMPTY, EMPTY, EMPTY, YELLOW, YELLOW, YELLOW, YELLOW, YELLOW, YELLOW, YELLOW, YELLOW, EMPTY, EMPTY, EMPTY, EMPTY],
    [EMPTY, EMPTY, EMPTY, EMPTY, YELLOW, YELLOW, BLACK, BLACK, BLACK, BLACK, YELLOW, YELLOW, EMPTY, EMPTY, EMPTY, EMPTY],
    [EMPTY, EMPTY, EMPTY, EMPTY, YELLOW, YELLOW, BLACK, BLACK, WHITE, BLACK, YELLOW, YELLOW, EMPTY, EMPTY, EMPTY, EMPTY],
    [EMPTY, EMPTY, EMPTY, EMPTY, YELLOW, YELLOW, BLACK, BLACK, BLACK, BLACK, YELLOW, YELLOW, EMPTY, EMPTY, EMPTY, EMPTY],
    [EMPTY, EMPTY, EMPTY, EMPTY, YELLOW, YELLOW, YELLOW, YELLOW, YELLOW, YELLOW, YELLOW, YELLOW, EMPTY, EMPTY, EMPTY, EMPTY],
    [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, YELLOW, YELLOW, YELLOW, YELLOW, YELLOW, YELLOW, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
    [EMPTY, EMPTY, EMPTY, BLUE, BLUE, BLUE, BLUE, BLUE, BLUE, BLUE, BLUE, BLUE, BLUE, EMPTY, EMPTY, EMPTY],
    [EMPTY, EMPTY, EMPTY, BLUE, BLUE, BLUE, BLUE, BLUE, BLUE, BLUE, BLUE, BLUE, BLUE, EMPTY, EMPTY, EMPTY],
    [EMPTY, EMPTY, EMPTY, EMPTY, BLUE, BLUE, BLUE, BLUE, BLUE, BLUE, BLUE, BLUE, EMPTY, EMPTY, EMPTY, EMPTY],
    [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, BROWN, BROWN, BROWN, BROWN, BROWN, BROWN, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
    [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, BROWN, BROWN, BROWN, BROWN, BROWN, BROWN, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
    [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, BROWN, BROWN, EMPTY, EMPTY, BROWN, BROWN, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
    [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, BROWN, BROWN, EMPTY, EMPTY, BROWN, BROWN, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
]

HERO_FRAMES = [HERO_FRAME_1, HERO_FRAME_2]

class CharacterPortrait:
    def __init__(self, character_id='hero'):
        self.character_id = character_id
        self.scale = 6
        self.animation_frame = 0
        self.animation_timer = 0
        self.animation_speed = 500
        self.x_offset = 0
        self.target_x_offset = 0
        self.y_offset = 0
        self.alpha = 0
        self.target_alpha = 255
        self.bounce_offset = 0
        self.bounce_timer = 0
        self.is_active = False
        
    def show(self, side='left'):
        self.is_active = True
        self.x_offset = -200 if side == 'left' else 200
        self.target_x_offset = 0
        self.alpha = 0
        self.target_alpha = 255
        
    def hide(self):
        self.target_x_offset = -200 if self.x_offset < 0 else 200
        self.target_alpha = 0
        
    def update(self):
        self.x_offset += (self.target_x_offset - self.x_offset) * 0.15
        self.alpha += (self.target_alpha - self.alpha) * 0.15
        self.bounce_timer += 0.05
        self.bounce_offset = math.sin(self.bounce_timer) * 3
        self.animation_timer += 16
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.animation_frame = (self.animation_frame + 1) % 2

    def draw(self, surface, x, y):
        if not self.is_active or self.alpha < 10:
            return
        sprite = HERO_FRAMES[self.animation_frame]
        sprite_surface = pygame.Surface((16 * self.scale, 16 * self.scale), pygame.SRCALPHA)
        for py, row in enumerate(sprite):
            for px, pixel in enumerate(row):
                if pixel[3] > 0:
                    pygame.draw.rect(sprite_surface, pixel, (px * self.scale, py * self.scale, self.scale, self.scale))
        sprite_surface.set_alpha(int(self.alpha))
        draw_x = x + self.x_offset
        draw_y = y + self.bounce_offset
        surface.blit(sprite_surface, (draw_x, draw_y))

TOWER_CONFIG = {
    'arrow': {'name': '破晓箭塔', 'cost': 100, 'damage': 15, 'range': 150, 'attack_speed': 0.8, 'color': (180, 100, 80), 'shape': 'triangle'},
    'cannon': {'name': '烈焰炮塔', 'cost': 200, 'damage': 60, 'range': 120, 'attack_speed': 0.4, 'splash_radius': 60, 'color': (200, 80, 50), 'shape': 'hexagon'},
    'ice': {'name': '寒霜塔', 'cost': 150, 'damage': 10, 'range': 130, 'attack_speed': 1.0, 'slow_factor': 0.35, 'color': (120, 180, 200), 'shape': 'diamond'},
    'lightning': {'name': '雷霆塔', 'cost': 250, 'damage': 30, 'range': 140, 'attack_speed': 0.5, 'chain_count': 4, 'chain_range': 70, 'color': (220, 180, 80), 'shape': 'star'},
    'magic': {'name': '终末魔法塔', 'cost': 300, 'damage': 45, 'range': 150, 'attack_speed': 0.6, 'magic_radius': 50, 'color': (160, 80, 180), 'shape': 'octagon'},
}

ENEMY_CONFIG = {
    'ash_walker': {'name': '灰烬行者', 'health': 120, 'speed': 1.5, 'reward': 35, 'color': (90, 85, 80), 'eye_color': (255, 100, 80)},
    'fusion_plains': {'name': '平原融合体', 'health': 200, 'speed': 1.2, 'reward': 50, 'color': (80, 150, 60), 'eye_color': (100, 200, 100), 'feature': 'goblin'},
    'fusion_swamp': {'name': '沼泽融合体', 'health': 250, 'speed': 0.8, 'reward': 60, 'color': (40, 100, 80), 'eye_color': (150, 200, 100), 'feature': 'slime'},
    'fusion_sky': {'name': '天空融合体', 'health': 180, 'speed': 2.0, 'reward': 55, 'color': (180, 160, 200), 'eye_color': (255, 200, 220), 'feature': 'spirit'},
    'fusion_corrupt': {'name': '腐蚀融合体', 'health': 300, 'speed': 0.6, 'reward': 70, 'color': (100, 60, 100), 'eye_color': (200, 100, 150), 'feature': 'corrupt'},
    'boss': {'name': '终末之主', 'health': 3000, 'speed': 0.3, 'reward': 1000, 'color': (140, 30, 50), 'eye_color': (255, 200, 50)},
}

PATH_POINTS = [
    (0, 6), (4, 6), (4, 3), (9, 3), (9, 8), (14, 8),
    (14, 4), (19, 4), (19, 10), (24, 10), (24, 6), (29, 6), (31, 6)
]

def create_polygon_points(center_x, center_y, size, sides):
    angle_offset = -math.pi / 2
    return [(center_x + size * math.cos(i * 2 * math.pi / sides + angle_offset),
             center_y + size * math.sin(i * 2 * math.pi / sides + angle_offset)) for i in range(sides)]

def create_star_points(center_x, center_y, size):
    angle_offset = -math.pi / 2
    points = []
    for i in range(10):
        r = size if i % 2 == 0 else size * 0.5
        angle = i * math.pi / 5 + angle_offset
        points.append((center_x + r * math.cos(angle), center_y + r * math.sin(angle)))
    return points

class ParticleSystem:
    def __init__(self):
        self.particles = []
        
    def add_ember(self, x, y):
        for _ in range(3):
            self.particles.append({
                'x': x + random.uniform(-10, 10),
                'y': y + random.uniform(-10, 10),
                'vx': random.uniform(-0.5, 0.5),
                'vy': random.uniform(-1, -0.3),
                'life': random.randint(30, 60),
                'max_life': 60,
                'size': random.uniform(2, 5),
                'color': random.choice([(255, 100, 50), (200, 60, 40), (255, 150, 80)])
            })
    
    def update(self):
        for p in self.particles[:]:
            p['x'] += p['vx']
            p['y'] += p['vy']
            p['life'] -= 1
            if p['life'] <= 0:
                self.particles.remove(p)
    
    def draw(self):
        for p in self.particles:
            alpha = int(255 * (p['life'] / p['max_life']))
            size = int(p['size'] * (p['life'] / p['max_life']))
            if size > 0:
                surf = pygame.Surface((size * 4, size * 4), pygame.SRCALPHA)
                pygame.draw.circle(surf, (*p['color'], alpha), (size * 2, size * 2), size)
                screen.blit(surf, (int(p['x'] - size * 2), int(p['y'] - size * 2)))

class RuinDecoration:
    def __init__(self):
        self.ruins = []
        for _ in range(12):
            self.ruins.append({
                'x': random.randint(50, SCREEN_WIDTH - 50),
                'y': random.randint(SCREEN_HEIGHT // 2 + 80, SCREEN_HEIGHT - 60),
                'width': random.randint(40, 100),
                'height': random.randint(60, 140),
                'type': random.randint(0, 2),
                'damage': random.randint(0, 4)
            })
    
    def draw(self):
        for ruin in self.ruins:
            x, y = ruin['x'], ruin['y']
            w, h = ruin['width'], ruin['height']
            
            if ruin['type'] == 0:
                pygame.draw.rect(screen, (70, 65, 60), (x - w//2, y, w, h//3))
                for i in range(random.randint(2, 4)):
                    pw = random.randint(10, 20)
                    ph = h * random.uniform(0.5, 1.0)
                    px = x - w//2 + random.randint(5, w - pw - 5)
                    pygame.draw.rect(screen, (60, 55, 50), (px, y - ph, pw, ph))
                    for d in range(ruin['damage']):
                        crack_y = y - ph + d * ph // 4
                        pygame.draw.line(screen, (40, 35, 30), (px, crack_y), (px + pw, crack_y), 1)
            elif ruin['type'] == 1:
                pygame.draw.ellipse(screen, (75, 70, 65), (x - w//2, y - h//2, w, h))
                for d in range(ruin['damage']):
                    angle = d * 0.5
                    pygame.draw.line(screen, (50, 45, 40), 
                                   (x, y - h//3), 
                                   (x + int(math.cos(angle) * w//2), y - h//3 + int(math.sin(angle) * h//3)), 2)
            else:
                pygame.draw.polygon(screen, (65, 60, 55), [
                    (x, y - h), (x - w//2, y), (x + w//2, y)
                ])
                pygame.draw.line(screen, (45, 40, 35), (x, y - h + 10), (x, y), 2)

class ApocalypticBackground:
    def __init__(self):
        self.background_surface = None
        self.ruins = RuinDecoration()
        self.ember_system = ParticleSystem()
        self.cloud_offset = 0
        self.create_background_surface()
        
    def create_background_surface(self):
        self.background_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        
        for y in range(SCREEN_HEIGHT):
            ratio = y / SCREEN_HEIGHT
            if ratio < 0.35:
                r = int(50 + (70 - 50) * (ratio / 0.35))
                g = int(45 + (65 - 45) * (ratio / 0.35))
                b = int(55 + (60 - 55) * (ratio / 0.35))
            elif ratio < 0.55:
                r = int(70 + (55 - 70) * ((ratio - 0.35) / 0.2))
                g = int(65 + (50 - 65) * ((ratio - 0.35) / 0.2))
                b = int(60 + (45 - 60) * ((ratio - 0.35) / 0.2))
            else:
                r = int(55 + (45 - 55) * ((ratio - 0.55) / 0.45))
                g = int(50 + (40 - 50) * ((ratio - 0.55) / 0.45))
                b = int(45 + (35 - 45) * ((ratio - 0.55) / 0.45))
            pygame.draw.line(self.background_surface, (r, g, b), (0, y), (SCREEN_WIDTH, y))
        
        self.draw_sky_cracks()
        self.draw_ground_details()
        
    def draw_sky_cracks(self):
        for _ in range(5):
            start_x = random.randint(100, SCREEN_WIDTH - 100)
            start_y = random.randint(50, SCREEN_HEIGHT // 3)
            points = [(start_x, start_y)]
            for _ in range(random.randint(3, 6)):
                last = points[-1]
                points.append((last[0] + random.randint(-50, 50), last[1] + random.randint(20, 60)))
            pygame.draw.lines(self.background_surface, (30, 25, 35), False, points, 2)
    
    def draw_ground_details(self):
        ground_y = int(SCREEN_HEIGHT * 0.6)
        for x in range(0, SCREEN_WIDTH, 30):
            crack_start = ground_y + random.randint(0, 50)
            crack_len = random.randint(5, 20)
            pygame.draw.line(self.background_surface, (35, 30, 25), 
                           (x + random.randint(-5, 5), crack_start), 
                           (x + random.randint(-5, 5), crack_start + crack_len), 1)
        
        for _ in range(20):
            x = random.randint(0, SCREEN_WIDTH)
            y = random.randint(ground_y + 20, SCREEN_HEIGHT - 20)
            size = random.randint(3, 8)
            pygame.draw.circle(self.background_surface, (40, 35, 30), (x, y), size)
            
    def update(self):
        self.cloud_offset += 0.1
        if random.random() < 0.1:
            x = random.randint(0, SCREEN_WIDTH)
            y = random.randint(SCREEN_HEIGHT // 4, SCREEN_HEIGHT // 2)
            self.ember_system.add_ember(x, y)
        self.ember_system.update()
        
    def draw(self):
        screen.blit(self.background_surface, (0, 0))
        
        self.draw_toxic_clouds()
        
        for ruin in self.ruins.ruins:
            if not self.is_on_path(ruin['x'], ruin['y']):
                pass
        
        self.ember_system.draw()
        
        fog_y = int(SCREEN_HEIGHT * 0.45)
        for y in range(fog_y, SCREEN_HEIGHT, 3):
            ratio = (y - fog_y) / (SCREEN_HEIGHT - fog_y)
            alpha = int(40 * ratio)
            surf = pygame.Surface((SCREEN_WIDTH, 3), pygame.SRCALPHA)
            surf.fill((180, 60, 50, alpha))
            screen.blit(surf, (0, y))
    
    def draw_toxic_clouds(self):
        for i in range(8):
            x = ((i * 200 + self.cloud_offset * 20) % (SCREEN_WIDTH + 200)) - 100
            y = 80 + i * 30
            for j in range(4):
                size = 40 + j * 15
                alpha = 25 - j * 5
                surf = pygame.Surface((size * 3, size), pygame.SRCALPHA)
                pygame.draw.ellipse(surf, (160, 50, 45, alpha), (0, 0, size * 3, size))
                screen.blit(surf, (int(x - size), int(y - size // 2)))
    
    def is_on_path(self, x, y):
        for i in range(len(PATH_POINTS) - 1):
            x1, y1 = PATH_POINTS[i]
            x2, y2 = PATH_POINTS[i + 1]
            min_x = min(x1, x2) * GRID_SIZE - GRID_SIZE
            max_x = max(x1, x2) * GRID_SIZE + GRID_SIZE * 2
            min_y = min(y1, y2) * GRID_SIZE - GRID_SIZE
            max_y = max(y1, y2) * GRID_SIZE + GRID_SIZE * 2
            if min_x <= x <= max_x and min_y <= y <= max_y:
                return True
        return False

background = ApocalypticBackground()

class IntroSequence:
    def __init__(self):
        self.phase = 'fade_in'
        self.alpha = 255
        self.dialogue_index = 0
        self.dialogues = [
            {"text": "四道裂缝在终末之地交汇...", "speaker": None},
            {"text": "平原的哥布林、沼泽的史莱姆...", "speaker": "向导", "color": (180, 140, 160)},
            {"text": "天空的樱灵、腐蚀的枯萎灵...", "speaker": "向导", "color": (180, 140, 160)},
            {"text": "它们融合成了更为恐怖的存在...", "speaker": "???", "color": (200, 100, 150)},
            {"text": "而终末之主，在废墟中等待着...", "speaker": "???", "color": (200, 100, 150)},
            {"text": "这是最后的防线，也是终末之战！", "speaker": "英雄", "color": (255, 200, 100)},
            {"text": "守护这片土地，直到最后一刻！", "speaker": "英雄", "color": (255, 200, 100)},
        ]
        self.text_appear_timer = 0
        self.current_text = ""
        self.target_text = ""
        self.text_index = 0
        self.wait_timer = 0
        self.character = CharacterPortrait('hero')
        self.character.show('left')
        self.background_surface = None
        self.fade_surface = None
        self.create_background()
        
    def create_background(self):
        self.background_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        for y in range(SCREEN_HEIGHT):
            ratio = y / SCREEN_HEIGHT
            r = int(50 + (35 - 50) * ratio)
            g = int(45 + (30 - 45) * ratio)
            b = int(55 + (40 - 55) * ratio)
            pygame.draw.line(self.background_surface, (r, g, b), (0, y), (SCREEN_WIDTH, y))
        self.fade_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.fade_surface.fill((0, 0, 0))
        
    def update(self):
        current_time = pygame.time.get_ticks()
        self.character.update()
        
        if self.phase == 'fade_in':
            self.alpha = max(0, self.alpha - 2)
            if self.alpha <= 0:
                self.phase = 'text_appear'
                
        elif self.phase == 'text_appear':
            if self.text_appear_timer == 0:
                self.target_text = self.dialogues[self.dialogue_index]["text"]
                self.text_appear_timer = current_time
                
            if self.text_index < len(self.target_text):
                if current_time - self.text_appear_timer >= 30:
                    self.current_text += self.target_text[self.text_index]
                    self.text_index += 1
                    self.text_appear_timer = current_time
            else:
                self.phase = 'dialogue_wait'
                
        elif self.phase == 'dialogue_wait':
            self.wait_timer += 1
            if self.wait_timer > 150:
                self.dialogue_index += 1
                if self.dialogue_index >= len(self.dialogues):
                    self.phase = 'fade_out'
                else:
                    self.phase = 'text_appear'
                    self.current_text = ""
                    self.target_text = self.dialogues[self.dialogue_index]["text"]
                    self.text_index = 0
                    self.text_appear_timer = 0
                self.wait_timer = 0
                
        elif self.phase == 'fade_out':
            self.alpha = min(255, self.alpha + 3)
            if self.alpha >= 255:
                return True
        return False
    
    def draw(self):
        screen.blit(self.background_surface, (0, 0))
        self.character.draw(screen, 80, SCREEN_HEIGHT - 200)
        
        if self.dialogue_index < len(self.dialogues):
            self.draw_intro_text()
            
        if self.alpha > 0:
            self.fade_surface.set_alpha(self.alpha)
            screen.blit(self.fade_surface, (0, 0))
    
    def draw_intro_text(self):
        dialogue = self.dialogues[self.dialogue_index]
        speaker = dialogue.get("speaker")
        color = dialogue.get("color", (220, 200, 180))
        
        box_width = min(SCREEN_WIDTH - 100, 800)
        box_height = 130
        box_x = (SCREEN_WIDTH - box_width) // 2
        box_y = SCREEN_HEIGHT - 170
        
        pygame.draw.rect(screen, (10, 8, 8, 230), (box_x, box_y, box_width, box_height))
        pygame.draw.rect(screen, (140, 30, 50), (box_x, box_y, box_width, box_height), 3)
        
        for i, (cx, cy) in enumerate([(box_x, box_y), (box_x + box_width, box_y), 
                                       (box_x + box_width, box_y + box_height), (box_x, box_y + box_height)]):
            pygame.draw.circle(screen, (140, 30, 50), (cx, cy), 8, 3)
        
        if speaker:
            name_surface = font.render(speaker, True, color)
            name_rect = name_surface.get_rect(center=(box_x + 80, box_y - 18))
            pygame.draw.rect(screen, (10, 8, 8), (name_rect.left - 8, name_rect.top - 2, name_rect.width + 16, name_rect.height + 4))
            pygame.draw.rect(screen, color, (name_rect.left - 8, name_rect.top - 2, name_rect.width + 16, name_rect.height + 4), 2)
            screen.blit(name_surface, name_rect)
        
        text_x = box_x + 25
        text_y = box_y + 20
        max_width = box_width - 50
        
        words = self.current_text.split(' ')
        line = ""
        lines = []
        for word in words:
            test_line = line + word + " "
            if font.size(test_line)[0] <= max_width:
                line = test_line
            else:
                if line:
                    lines.append(line.strip())
                line = word + " "
        if line:
            lines.append(line.strip())
        
        for i, line_text in enumerate(lines[:3]):
            if line_text:
                screen.blit(font.render(line_text, True, color), (text_x, text_y + i * 32))
        
        if self.text_index >= len(self.target_text):
            heart_x = box_x + 25
            heart_y = box_y + box_height - 30
            pygame.draw.polygon(screen, (140, 30, 50), [
                (heart_x, heart_y - 10), (heart_x - 10, heart_y), 
                (heart_x, heart_y + 8), (heart_x + 10, heart_y)
            ])
    
    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in [pygame.K_SPACE, pygame.K_RETURN, pygame.K_z]:
                if self.phase == 'text_appear':
                    self.current_text = self.target_text
                    self.text_index = len(self.target_text)
                    self.phase = 'dialogue_wait'
                elif self.phase == 'dialogue_wait':
                    self.dialogue_index += 1
                    if self.dialogue_index >= len(self.dialogues):
                        self.phase = 'fade_out'
                    else:
                        self.current_text = ""
                        self.text_index = 0
                        self.target_text = ""
                        self.phase = 'text_appear'
                        self.text_appear_timer = 0

class Tower:
    def __init__(self, x, y, tower_type):
        self.x = x * GRID_SIZE + GRID_SIZE // 2
        self.y = y * GRID_SIZE + GRID_SIZE // 2
        self.type = tower_type
        self.config = TOWER_CONFIG[tower_type]
        self.last_attack_time = 0
        self.target = None
        self.attack_effect_timer = 0
        
    def draw(self):
        x, y = self.x, self.y
        size = GRID_SIZE // 2 - 2
        
        pygame.draw.rect(screen, (55, 50, 45), (x - size - 4, y + size // 2, size * 2 + 8, size // 2 + 4))
        pygame.draw.rect(screen, (40, 35, 30), (x - size - 2, y + size // 2 + 2, size * 2 + 4, size // 2))
        
        base_size = size + 4
        pygame.draw.circle(screen, (50, 45, 40), (x, y + size // 3), base_size)
        pygame.draw.circle(screen, (65, 60, 55), (x, y + size // 3), base_size - 3)
        
        color = self.config['color']
        shape = self.config['shape']
        
        if shape == 'triangle':
            pts = [(x, y - size), (x - size, y + size), (x + size, y + size)]
        elif shape == 'hexagon':
            pts = create_polygon_points(x, y, size, 6)
        elif shape == 'diamond':
            pts = [(x, y - size), (x + size, y), (x, y + size), (x - size, y)]
        elif shape == 'star':
            pts = create_star_points(x, y, size)
        elif shape == 'octagon':
            pts = create_polygon_points(x, y, size, 8)
        else:
            pts = [(x, y - size), (x + size, y), (x, y + size), (x - size, y)]
        
        pygame.draw.polygon(screen, color, pts)
        highlight_pts = [(x + (p[0] - x) * 0.8, y + (p[1] - y) * 0.8) for p in pts]
        pygame.draw.polygon(screen, (255, 255, 255, 100), highlight_pts, 2)
        
        if self.attack_effect_timer > 0:
            glow_size = size + (20 - self.attack_effect_timer)
            glow_surf = pygame.Surface((glow_size * 4, glow_size * 4), pygame.SRCALPHA)
            pygame.draw.circle(glow_surf, (*color, 100), (glow_size * 2, glow_size * 2), glow_size)
            screen.blit(glow_surf, (int(x - glow_size * 2), int(y - glow_size * 2)))
            self.attack_effect_timer -= 1
        
        name_text = small_font.render(self.config['name'], True, (220, 200, 180))
        text_rect = name_text.get_rect(center=(x, y + GRID_SIZE // 2 + 16))
        bg_rect = pygame.Rect(text_rect.left - 4, text_rect.top - 2, text_rect.width + 8, text_rect.height + 4)
        pygame.draw.rect(screen, (0, 0, 0, 180), bg_rect)
        screen.blit(name_text, text_rect)
        
    def update(self, enemies, current_time):
        self.target = None
        min_dist = float('inf')
        
        for enemy in enemies:
            dist = math.hypot(self.x - enemy.x, self.y - enemy.y)
            if dist <= self.config['range'] and dist < min_dist:
                min_dist = dist
                self.target = enemy
        
        attack_interval = 1000 / self.config['attack_speed']
        if self.target and current_time - self.last_attack_time >= attack_interval:
            self.last_attack_time = current_time
            self.attack_effect_timer = 15
            return Bullet(self.x, self.y, self.target, self.config)
        return None

class Enemy:
    def __init__(self, enemy_type, path_index=0, wave_num=1):
        self.type = enemy_type
        self.config = ENEMY_CONFIG[enemy_type]
        wave_multiplier = 1 + (wave_num - 1) * 0.12
        
        self.max_health = int(self.config['health'] * wave_multiplier)
        self.health = self.max_health
        self.speed = self.config['speed'] * min(wave_multiplier, 1.8)
        self.reward = int(self.config['reward'] * wave_multiplier)
        self.path_index = path_index
        self.x, self.y = self.get_position()
        self.active = True
        self.wave_num = wave_num
        self.size = int(14 + (wave_num - 1) * 0.4)
        self.size = min(self.size, 28)
        self.anim_time = random.uniform(0, math.pi * 2)
        self.float_offset = 0
        self.ember_particles = ParticleSystem()
        
        base_color = self.config['color']
        darken_factor = min(wave_num * 0.04, 0.35)
        self.color = (
            max(0, int(base_color[0] * (1 - darken_factor))),
            max(0, int(base_color[1] * (1 - darken_factor))),
            max(0, int(base_color[2] * (1 - darken_factor)))
        )
        
    def get_position(self):
        if self.path_index < len(PATH_POINTS):
            x, y = PATH_POINTS[self.path_index]
            return x * GRID_SIZE + GRID_SIZE // 2, y * GRID_SIZE + GRID_SIZE // 2
        return SCREEN_WIDTH, SCREEN_HEIGHT // 2
        
    def update(self, current_time):
        if self.path_index >= len(PATH_POINTS):
            self.active = False
            return True
        
        self.anim_time += 0.1
        self.float_offset = math.sin(self.anim_time * 2) * 3
        
        if random.random() < 0.15:
            self.ember_particles.add_ember(self.x, self.y)
        self.ember_particles.update()
        
        target_x, target_y = PATH_POINTS[self.path_index]
        target_x = target_x * GRID_SIZE + GRID_SIZE // 2
        target_y = target_y * GRID_SIZE + GRID_SIZE // 2
        
        dx = target_x - self.x
        dy = target_y - self.y
        dist = math.hypot(dx, dy)
        
        if dist < 5:
            self.path_index += 1
        else:
            self.x += (dx / dist) * self.speed
            self.y += (dy / dist) * self.speed
        return False
    
    def draw(self):
        self.ember_particles.draw()
        
        x, y = int(self.x), int(self.y + self.float_offset)
        size = self.size
        
        if self.type == 'ash_walker':
            pygame.draw.ellipse(screen, self.color, (x - size, y - size // 2, size * 2, size * 1.5))
            pygame.draw.ellipse(screen, (70, 65, 60), (x - size + 4, y - size // 2 + 4, size * 2 - 8, size * 1.5 - 8))
            pygame.draw.circle(screen, (255, 255, 255), (x - 5, y - 3), 5)
            pygame.draw.circle(screen, (255, 255, 255), (x + 5, y - 3), 5)
            pygame.draw.circle(screen, self.config['eye_color'], (x - 4, y - 2), 3)
            pygame.draw.circle(screen, self.config['eye_color'], (x + 6, y - 2), 3)
            
            for i in range(3):
                leg_x = x - size // 2 + i * size // 2
                pygame.draw.line(screen, (60, 55, 50), (leg_x, y + size), (leg_x - 3, y + size + 8), 3)
                pygame.draw.line(screen, (60, 55, 50), (leg_x, y + size), (leg_x + 3, y + size + 8), 3)
                
        elif 'fusion' in self.type:
            feature = self.config.get('feature', '')
            
            wing_angle = math.sin(pygame.time.get_ticks() * 0.004) * 0.4
            wing1 = [(x, y), (x - size * 2.2, y - size + wing_angle * size), (x - size * 0.8, y)]
            wing2 = [(x, y), (x + size * 2.2, y - size + wing_angle * size), (x + size * 0.8, y)]
            pygame.draw.polygon(screen, self.color, wing1)
            pygame.draw.polygon(screen, self.color, wing2)
            
            pygame.draw.circle(screen, (self.color[0] - 20, self.color[1] - 20, self.color[2] - 20), (x, y), size + 6)
            pygame.draw.circle(screen, self.color, (x, y), size + 3)
            
            if feature == 'goblin':
                pygame.draw.ellipse(screen, (60, 100, 40), (x - size // 2, y - size // 3, size, size // 2))
            elif feature == 'slime':
                pygame.draw.ellipse(screen, (30, 80, 60), (x - size // 2, y - size // 4, size, size // 2))
                for _ in range(2):
                    pygame.draw.circle(screen, (50, 120, 80), 
                                     (x + random.randint(-5, 5), y - size // 4 + random.randint(-5, 5)), 3)
            elif feature == 'spirit':
                tail_pts = [(x, y + size // 2)]
                for i in range(5):
                    tail_pts.append((x + math.sin(i * 0.5 + pygame.time.get_ticks() * 0.003) * 8, 
                                   y + size // 2 + i * 4))
                pygame.draw.lines(screen, (200, 180, 220), False, tail_pts, 2)
            elif feature == 'corrupt':
                pygame.draw.circle(screen, (80, 40, 80), (x - 4, y - 4), 4)
                pygame.draw.circle(screen, (80, 40, 80), (x + 4, y - 4), 4)
                for _ in range(3):
                    pygame.draw.circle(screen, (100, 50, 100), 
                                     (x + random.randint(-size//2, size//2), 
                                      y + random.randint(-size//2, size//2)), 2)
            
            pygame.draw.circle(screen, (255, 255, 255), (x - 6, y - 5), 6)
            pygame.draw.circle(screen, (255, 255, 255), (x + 6, y - 5), 6)
            pygame.draw.circle(screen, self.config['eye_color'], (x - 6, y - 5), 4)
            pygame.draw.circle(screen, self.config['eye_color'], (x + 6, y - 5), 4)
            
            for i in range(4):
                bx = x - size // 2 + i * size // 3
                by = y + size // 3
                pygame.draw.circle(screen, (255, 120, 50), (int(bx), int(by)), 3)
                
        elif self.type == 'boss':
            pygame.draw.polygon(screen, (80, 20, 35), [(x, y - size - 35), (x - size * 2.5, y + size // 2), (x + size * 2.5, y + size // 2)])
            
            for i in range(6):
                angle = i * (math.pi / 3) + pygame.time.get_ticks() * 0.002
                orbit_x = x + math.cos(angle) * (size + 25)
                orbit_y = y - size // 2 + math.sin(angle) * (size + 25)
                pygame.draw.circle(screen, (50, 20, 30), (int(orbit_x), int(orbit_y)), 12)
                pygame.draw.circle(screen, (180, 40, 50), (int(orbit_x), int(orbit_y)), 8)
                pygame.draw.circle(screen, (255, 150, 80), (int(orbit_x), int(orbit_y)), 4)
            
            pygame.draw.circle(screen, (100, 25, 40), (x, y - size // 2), size // 2 + 14)
            pygame.draw.circle(screen, self.color, (x, y - size // 2), size // 2 + 10)
            pygame.draw.circle(screen, (self.color[0] + 30, self.color[1] + 10, self.color[2] + 20), (x, y - size // 2), size // 2 + 5)
            
            pygame.draw.polygon(screen, (90, 35, 55), [(x - size // 2, y - size // 2), (x - size * 2, y - size * 2.5), (x - size // 3, y - size // 3)])
            pygame.draw.polygon(screen, (90, 35, 55), [(x + size // 2, y - size // 2), (x + size * 2, y - size * 2.5), (x + size // 3, y - size // 3)])
            
            pygame.draw.circle(screen, self.config['eye_color'], (x - 10, y - size // 2 - 6), 10)
            pygame.draw.circle(screen, self.config['eye_color'], (x + 10, y - size // 2 - 6), 10)
            pygame.draw.circle(screen, (255, 255, 255), (x - 10, y - size // 2 - 6), 4)
            pygame.draw.circle(screen, (255, 255, 255), (x + 10, y - size // 2 - 6), 4)
            
            for i in range(10):
                angle = i * (math.pi / 5) + pygame.time.get_ticks() * 0.0015
                spike_x = x + math.cos(angle) * (size + 40)
                spike_y = y - size // 2 + math.sin(angle) * (size + 40)
                pygame.draw.line(screen, (120, 30, 50), (x, y - size // 2), (int(spike_x), int(spike_y)), 3)
                pygame.draw.circle(screen, (200, 50, 70), (int(spike_x), int(spike_y)), 4)
            
            mouth_pts = [(x - 8, y - size // 2 + 8), (x, y - size // 2 + 15), (x + 8, y - size // 2 + 8)]
            pygame.draw.polygon(screen, (30, 10, 20), mouth_pts)
        
        bar_width = 44
        bar_height = 6
        bar_y = y - size - 18
        pygame.draw.rect(screen, (20, 15, 15), (x - bar_width // 2, bar_y, bar_width, bar_height))
        health_ratio = max(0, self.health / self.max_health)
        
        if health_ratio > 0.6:
            bar_color = (100, 180, 100)
        elif health_ratio > 0.3:
            bar_color = (180, 180, 80)
        else:
            bar_color = (180, 80, 80)
        
        pygame.draw.rect(screen, bar_color, (x - bar_width // 2, bar_y, bar_width * health_ratio, bar_height))
        pygame.draw.rect(screen, (100, 80, 80), (x - bar_width // 2, bar_y, bar_width, bar_height), 1)
        
    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.active = False

class Bullet:
    def __init__(self, x, y, target, config):
        self.x = x
        self.y = y
        self.target = target
        self.config = config
        self.speed = 12
        self.active = True
        self.color = config.get('bullet_color', config['color'])
        self.trail = []
        
    def update(self, enemies=None):
        if not self.active or not self.target or not self.target.active:
            self.active = False
            return None
        
        self.trail.append((self.x, self.y))
        if len(self.trail) > 5:
            self.trail.pop(0)
        
        dx = self.target.x - self.x
        dy = self.target.y - self.y
        dist = math.hypot(dx, dy)
        
        if dist < 10:
            self.target.take_damage(self.config['damage'])
            self.active = False
            return self.target
        elif dist > 0:
            self.x += (dx / dist) * self.speed
            self.y += (dy / dist) * self.speed
        return None
    
    def draw(self):
        for i, (tx, ty) in enumerate(self.trail):
            alpha = int(100 * (i / len(self.trail)))
            size = 3 + i
            surf = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
            pygame.draw.circle(surf, (*self.color, alpha), (size, size), size)
            screen.blit(surf, (int(tx - size), int(ty - size)))
        
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), 7)
        pygame.draw.circle(screen, (255, 255, 255), (int(self.x), int(self.y)), 4)

class Game:
    def __init__(self):
        self.gold = 800
        self.lives = 30
        self.towers = []
        self.enemies = []
        self.bullets = []
        self.particles = ParticleSystem()
        self.selected_tower_type = None
        self.wave_index = 0
        self.enemy_index = 0
        self.last_spawn_time = 0
        self.game_state = 'intro'
        self.wave_in_progress = False
        self.score = 0
        self.intro = IntroSequence()
        self.background = background
        self.total_waves = 25
        
    def draw_grid(self):
        for x in range(0, SCREEN_WIDTH, GRID_SIZE):
            pygame.draw.line(screen, (90, 85, 80, 40), (x, 0), (x, SCREEN_HEIGHT), 1)
        for y in range(0, SCREEN_HEIGHT, GRID_SIZE):
            pygame.draw.line(screen, (90, 85, 80, 40), (0, y), (SCREEN_WIDTH, y), 1)
    
    def draw_path(self):
        for i in range(len(PATH_POINTS) - 1):
            x1, y1 = PATH_POINTS[i]
            x2, y2 = PATH_POINTS[i + 1]
            pygame.draw.line(screen, (55, 50, 45),
                           (x1 * GRID_SIZE + GRID_SIZE // 2 + 2, y1 * GRID_SIZE + GRID_SIZE // 2 + 2),
                           (x2 * GRID_SIZE + GRID_SIZE // 2 + 2, y2 * GRID_SIZE + GRID_SIZE // 2 + 2), GRID_SIZE)
            pygame.draw.line(screen, (75, 70, 65),
                           (x1 * GRID_SIZE + GRID_SIZE // 2, y1 * GRID_SIZE + GRID_SIZE // 2),
                           (x2 * GRID_SIZE + GRID_SIZE // 2, y2 * GRID_SIZE + GRID_SIZE // 2), GRID_SIZE)
            
            mid_x = (x1 + x2) * GRID_SIZE // 2 + GRID_SIZE // 2
            mid_y = (y1 + y2) * GRID_SIZE // 2 + GRID_SIZE // 2
            angle = math.atan2(y2 - y1, x2 - x1)
            arrow_size = 8
            pygame.draw.polygon(screen, (100, 95, 90), [
                (mid_x + arrow_size * math.cos(angle), mid_y + arrow_size * math.sin(angle)),
                (mid_x + arrow_size * math.cos(angle + 2.5), mid_y + arrow_size * math.sin(angle + 2.5)),
                (mid_x + arrow_size * math.cos(angle - 2.5), mid_y + arrow_size * math.sin(angle - 2.5))
            ])
        
        sx, sy = PATH_POINTS[0]
        ex, ey = PATH_POINTS[-1]
        pygame.draw.circle(screen, (80, 160, 80), (sx * GRID_SIZE + GRID_SIZE // 2, sy * GRID_SIZE + GRID_SIZE // 2), 15)
        pygame.draw.circle(screen, (150, 255, 150), (sx * GRID_SIZE + GRID_SIZE // 2, sy * GRID_SIZE + GRID_SIZE // 2), 15, 3)
        pygame.draw.circle(screen, (140, 30, 50), (ex * GRID_SIZE + GRID_SIZE // 2, ey * GRID_SIZE + GRID_SIZE // 2), 15)
        pygame.draw.circle(screen, (200, 100, 120), (ex * GRID_SIZE + GRID_SIZE // 2, ey * GRID_SIZE + GRID_SIZE // 2), 15, 3)
    
    def can_place_tower(self, grid_x, grid_y):
        for i in range(len(PATH_POINTS) - 1):
            x1, y1 = PATH_POINTS[i]
            x2, y2 = PATH_POINTS[i + 1]
            min_x = min(x1, x2)
            max_x = max(x1, x2)
            min_y = min(y1, y2)
            max_y = max(y1, y2)
            if min_x <= grid_x <= max_x and min_y <= grid_y <= max_y:
                return False
        for tower in self.towers:
            tx = int((tower.x - GRID_SIZE // 2) // GRID_SIZE)
            ty = int((tower.y - GRID_SIZE // 2) // GRID_SIZE)
            if tx == grid_x and ty == grid_y:
                return False
        return True
    
    def spawn_enemy(self, enemy_type='ash_walker'):
        enemy = Enemy(enemy_type, wave_num=self.wave_index + 1)
        self.enemies.append(enemy)
    
    def update_wave(self, current_time):
        if self.game_state != 'playing':
            return
        
        if self.wave_index >= self.total_waves:
            if not self.enemies:
                self.wave_in_progress = False
                self.game_state = 'victory'
            return
        
        base_enemies = 6 + self.wave_index * 2
        delay = max(400, 1200 - self.wave_index * 30)
        
        if not self.wave_in_progress:
            self.wave_in_progress = True
            self.enemy_index = 0
            self.last_spawn_time = current_time
        
        if self.enemy_index < base_enemies:
            if current_time - self.last_spawn_time >= delay:
                if self.wave_index >= self.total_waves * 0.8:
                    enemy_type = random.choice(['fusion_plains', 'fusion_swamp', 'fusion_sky', 'fusion_corrupt'])
                elif self.wave_index >= self.total_waves * 0.5:
                    enemy_type = random.choice(['fusion_plains', 'fusion_swamp'])
                elif self.wave_index >= self.total_waves * 0.3:
                    enemy_type = 'ash_walker'
                else:
                    enemy_type = 'ash_walker'
                
                if self.wave_index == self.total_waves - 1:
                    enemy_type = 'boss'
                elif self.wave_index == self.total_waves - 2:
                    enemy_type = random.choice(['fusion_sky', 'fusion_corrupt'])
                
                self.spawn_enemy(enemy_type)
                self.enemy_index += 1
                self.last_spawn_time = current_time
        else:
            if not self.enemies:
                self.wave_index += 1
                self.wave_in_progress = False
    
    def update(self):
        current_time = pygame.time.get_ticks()
        
        if self.game_state == 'intro':
            intro_complete = self.intro.update()
            if intro_complete:
                self.game_state = 'preparing'
            return
        
        if self.game_state != 'playing':
            return
        
        self.update_wave(current_time)
        
        for enemy in self.enemies[:]:
            reached_end = enemy.update(current_time)
            if reached_end:
                self.lives -= 1
                self.enemies.remove(enemy)
                if self.lives <= 0:
                    self.game_state = 'defeat'
            elif not enemy.active:
                self.gold += enemy.reward
                self.score += enemy.reward * 20
                self.particles.add_ember(enemy.x, enemy.y)
                self.enemies.remove(enemy)
        
        for tower in self.towers:
            result = tower.update(self.enemies, current_time)
            if result:
                self.bullets.append(result)
        
        for bullet in self.bullets[:]:
            bullet.update(self.enemies)
            if not bullet.active:
                self.bullets.remove(bullet)
        
        self.background.update()
    
    def draw(self):
        if self.game_state == 'intro':
            self.intro.draw()
            return
        
        if self.game_state == 'preparing':
            self.background.draw()
            self.draw_grid()
            self.draw_path()
            self.draw_ui()
            
            surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            surf.fill((0, 0, 0, 100))
            screen.blit(surf, (0, 0))
            
            text = large_font.render("终末地", True, (140, 30, 50))
            screen.blit(text, text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 80)))
            text = small_font.render("最后的防线，终极之战", True, (180, 140, 150))
            screen.blit(text, text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 30)))
            btn = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 20, 200, 50)
            pygame.draw.rect(screen, (100, 40, 50), btn)
            pygame.draw.rect(screen, (200, 150, 160), btn, 3)
            text = font.render("开始游戏", True, (220, 200, 180))
            screen.blit(text, text.get_rect(center=btn.center))
            return
        
        self.background.draw()
        self.draw_grid()
        self.draw_path()
        
        for tower in self.towers:
            tower.draw()
        for enemy in self.enemies:
            enemy.draw()
        for bullet in self.bullets:
            bullet.draw()
        
        self.draw_ui()
        
        if self.game_state == 'victory':
            surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            surf.fill((0, 0, 0, 180))
            screen.blit(surf, (0, 0))
            text = large_font.render("胜利！", True, (255, 200, 100))
            screen.blit(text, text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50)))
            text = font.render(f"最终分数: {self.score}", True, (220, 200, 180))
            screen.blit(text, text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 10)))
            text = small_font.render("终末之主已被击败，世界迎来了新的希望...", True, (180, 140, 160))
            screen.blit(text, text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)))
            
        if self.game_state == 'defeat':
            surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            surf.fill((0, 0, 0, 180))
            screen.blit(surf, (0, 0))
            text = large_font.render("失败...", True, (180, 60, 70))
            screen.blit(text, text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 30)))
            text = small_font.render("终末之主仍在废墟中等待...", True, (150, 120, 130))
            screen.blit(text, text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20)))
    
    def draw_ui(self):
        pygame.draw.rect(screen, (45, 40, 38), (0, 0, SCREEN_WIDTH, 50))
        
        pygame.draw.rect(screen, (60, 55, 50), (10, 8, 110, 34))
        text = font.render(f"{self.gold}", True, (255, 215, 0))
        screen.blit(text, text.get_rect(center=(65, 25)))
        
        pygame.draw.rect(screen, (60, 55, 50), (130, 8, 100, 34))
        text = font.render(f"{self.lives}", True, (200, 80, 80))
        screen.blit(text, text.get_rect(center=(180, 25)))
        
        pygame.draw.rect(screen, (60, 55, 50), (240, 8, 120, 34))
        text = font.render(f"{self.wave_index + 1}/{self.total_waves}", True, (220, 200, 180))
        screen.blit(text, text.get_rect(center=(300, 25)))
        
        panel_x = SCREEN_WIDTH - 190
        pygame.draw.rect(screen, (45, 40, 38), (panel_x, 60, 180, 360))
        
        text = small_font.render("防御塔", True, (200, 180, 160))
        screen.blit(text, text.get_rect(center=(panel_x + 90, 80)))
        
        y = 110
        for tower_type, config in TOWER_CONFIG.items():
            color = config['color'] if self.gold >= config['cost'] else (100, 100, 100)
            bg = pygame.Rect(panel_x + 10, y, 160, 62)
            if self.selected_tower_type == tower_type:
                pygame.draw.rect(screen, (70, 65, 60), bg)
                pygame.draw.rect(screen, (140, 30, 50), bg, 2)
            
            text = small_font.render(config['name'], True, (220, 200, 180))
            screen.blit(text, (panel_x + 60, y + 5))
            text = small_font.render(f"{config['cost']}", True, (255, 215, 0))
            screen.blit(text, (panel_x + 60, y + 25))
            text = small_font.render(f"伤害:{config['damage']}", True, (150, 150, 150))
            screen.blit(text, (panel_x + 60, y + 43))
            
            center_x = panel_x + 30
            center_y = y + 31
            shape = config['shape']
            
            if shape == 'triangle':
                pts = [(center_x, center_y - 12), (center_x - 12, center_y + 12), (center_x + 12, center_y + 12)]
                pygame.draw.polygon(screen, color, pts)
            elif shape == 'hexagon':
                pts = create_polygon_points(center_x, center_y, 12, 6)
                pygame.draw.polygon(screen, color, pts)
            elif shape == 'diamond':
                pts = [(center_x, center_y - 12), (center_x + 12, center_y), (center_x, center_y + 12), (center_x - 12, center_y)]
                pygame.draw.polygon(screen, color, pts)
            elif shape == 'star':
                pts = create_star_points(center_x, center_y, 12)
                pygame.draw.polygon(screen, color, pts)
            elif shape == 'octagon':
                pts = create_polygon_points(center_x, center_y, 12, 8)
                pygame.draw.polygon(screen, color, pts)
            
            y += 68

selected_tower_type = None

def main():
    global selected_tower_type
    game = Game()
    running = True
    
    while running:
        mx, my = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if game.game_state == 'intro':
                    game.intro.handle_input(event)
                elif game.game_state == 'preparing':
                    btn = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 20, 200, 50)
                    if btn.collidepoint(mx, my):
                        game.game_state = 'playing'
                elif game.game_state == 'playing':
                    panel_x = SCREEN_WIDTH - 190
                    if panel_x <= mx <= panel_x + 180 and 60 <= my <= 420:
                        y = 110
                        for tower_type in TOWER_CONFIG:
                            if y <= my <= y + 62:
                                if game.gold >= TOWER_CONFIG[tower_type]['cost']:
                                    selected_tower_type = tower_type
                                break
                            y += 68
                    else:
                        gx, gy = mx // GRID_SIZE, my // GRID_SIZE
                        clicked = None
                        for t in game.towers:
                            tx = int((t.x - GRID_SIZE // 2) // GRID_SIZE)
                            ty = int((t.y - GRID_SIZE // 2) // GRID_SIZE)
                            if tx == gx and ty == gy:
                                clicked = t
                                break
                        if clicked:
                            selected_tower_type = None
                        elif selected_tower_type and game.can_place_tower(gx, gy):
                            cfg = TOWER_CONFIG[selected_tower_type]
                            if game.gold >= cfg['cost']:
                                game.gold -= cfg['cost']
                                game.towers.append(Tower(gx, gy, selected_tower_type))
                elif game.game_state in ['victory', 'defeat']:
                    game = Game()
            elif event.type == pygame.KEYDOWN:
                if game.game_state == 'intro':
                    game.intro.handle_input(event)
        
        game.update()
        game.draw()
        pygame.display.flip()
        clock.tick(FPS)
    
    pygame.quit()

if __name__ == "__main__":
    main()
