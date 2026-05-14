# ================================
# 塔防游戏 - 鸿蒙防线
# 第三关：天落殷园
# 主题：天空浮岛、樱花飘落、浮云飘动
# ================================

import pygame
import math
import random

pygame.init()

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
GRID_SIZE = 40
FPS = 60

COLORS = {
    'sky_top': (135, 206, 235),
    'sky_mid': (255, 182, 193),
    'sky_bottom': (255, 160, 122),
    'cloud_white': (255, 255, 255),
    'cloud_shadow': (200, 200, 220),
    'island_grass': (144, 238, 144),
    'island_dirt': (139, 90, 43),
    'island_rock': (128, 128, 128),
    'cherry_pink': (255, 182, 193),
    'cherry_dark': (219, 112, 147),
    'cherry_white': (255, 250, 250),
    'branch_brown': (101, 67, 33),
    'path_stone': (160, 140, 120),
    'path_dark': (120, 100, 80),
    'grid': (255, 255, 255, 40),
    'text': (60, 40, 40),
    'gold': (255, 215, 0),
    'health': (200, 80, 80),
    'undertale_white': (255, 255, 255),
    'undertale_yellow': (255, 255, 0),
}

DIALOGUE_CONFIG = {
    'box_color': (0, 0, 0),
    'border_color': (255, 255, 255),
    'text_color': (255, 255, 255),
    'name_color': (255, 200, 200),
    'heart_color': (255, 150, 150),
    'font_size': 24,
    'box_padding': 20,
    'corner_size': 8,
}

TOWER_CONFIG = {
    'arrow': {'name': '箭塔', 'cost': 100, 'damage': 15, 'range': 150, 'attack_speed': 0.8, 'color': (70, 130, 180), 'shape': 'triangle'},
    'cannon': {'name': '炮塔', 'cost': 200, 'damage': 60, 'range': 120, 'attack_speed': 0.4, 'splash_radius': 60, 'color': (205, 92, 0), 'shape': 'hexagon'},
    'ice': {'name': '冰塔', 'cost': 150, 'damage': 10, 'range': 130, 'attack_speed': 1.0, 'slow_factor': 0.35, 'color': (135, 206, 250), 'shape': 'diamond'},
    'lightning': {'name': '电塔', 'cost': 250, 'damage': 30, 'range': 140, 'attack_speed': 0.5, 'chain_count': 4, 'chain_range': 70, 'color': (255, 215, 0), 'shape': 'star'},
    'magic': {'name': '魔法塔', 'cost': 300, 'damage': 45, 'range': 150, 'attack_speed': 0.6, 'magic_radius': 50, 'color': (138, 43, 226), 'shape': 'octagon'},
}

ENEMY_CONFIG = {
    'spirit': {'name': '樱灵', 'health': 80, 'speed': 2.0, 'reward': 25, 'color': (255, 200, 220), 'eye_color': (255, 100, 150)},
    'bird': {'name': '云雀', 'health': 40, 'speed': 3.5, 'reward': 35, 'color': (180, 180, 220), 'eye_color': (100, 100, 180)},
    'cloud': {'name': '云妖', 'health': 200, 'speed': 1.2, 'reward': 45, 'color': (200, 200, 220), 'eye_color': (80, 80, 120)},
    'boss': {'name': '苍穹之主', 'health': 1200, 'speed': 0.6, 'reward': 300, 'color': (150, 100, 180), 'eye_color': (255, 200, 100)},
}

LEVEL_CONFIG = {
    'level_3': {'name': '天落殷园', 'waves': 18, 'start_gold': 600, 'lives': 25, 'theme': 'sky'},
}

PATH_POINTS = [
    (0, 4), (4, 4), (4, 8), (9, 8), (9, 3), (14, 3),
    (14, 10), (20, 10), (20, 6), (26, 6), (26, 13), (31, 13)
]

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("鸿蒙防线 - 天落殷园")
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

font = get_chinese_font(DIALOGUE_CONFIG['font_size'])
small_font = get_chinese_font(20)
large_font = get_chinese_font(72)

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

class CherryPetalSystem:
    def __init__(self, petal_count=80):
        self.petal_count = petal_count
        self.petals = []
        self.init_petals()

    def init_petals(self):
        for _ in range(self.petal_count):
            self.petals.append({
                'x': random.randint(0, SCREEN_WIDTH),
                'y': random.randint(-50, SCREEN_HEIGHT),
                'size': random.uniform(3, 7),
                'speed_x': random.uniform(-0.5, 0.5),
                'speed_y': random.uniform(0.5, 1.5),
                'rotation': random.uniform(0, 360),
                'rot_speed': random.uniform(-2, 2),
                'sway_phase': random.uniform(0, 2 * math.pi),
                'sway_speed': random.uniform(0.02, 0.05),
                'color': random.choice([COLORS['cherry_pink'], COLORS['cherry_white'], COLORS['cherry_dark']])
            })

    def update(self):
        time = pygame.time.get_ticks() * 0.001
        for petal in self.petals:
            petal['sway_phase'] += petal['sway_speed']
            petal['x'] += petal['speed_x'] + math.sin(petal['sway_phase']) * 0.8
            petal['y'] += petal['speed_y']
            petal['rotation'] += petal['rot_speed']

            if petal['y'] > SCREEN_HEIGHT + 20:
                petal['y'] = random.randint(-50, -10)
                petal['x'] = random.randint(0, SCREEN_WIDTH)

    def draw(self):
        for petal in self.petals:
            size = int(petal['size'])
            surf = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
            color = petal['color']
            pygame.draw.ellipse(surf, (*color, 200), (0, 0, size * 2, size))
            rotated = pygame.transform.rotate(surf, petal['rotation'])
            rect = rotated.get_rect(center=(int(petal['x']), int(petal['y'])))
            screen.blit(rotated, rect)

class FloatingCloud:
    def __init__(self, x=None, y=None):
        self.x = x if x is not None else random.randint(-200, SCREEN_WIDTH)
        self.y = y if y is not None else random.randint(50, SCREEN_HEIGHT // 2)
        self.speed = random.uniform(0.2, 0.8)
        self.size = random.randint(60, 120)
        self.generate_puffs()

    def generate_puffs(self):
        self.puffs = []
        puff_count = random.randint(4, 7)
        for _ in range(puff_count):
            self.puffs.append({
                'offset_x': random.randint(-self.size // 2, self.size // 2),
                'offset_y': random.randint(-self.size // 4, self.size // 4),
                'radius': random.randint(self.size // 4, self.size // 2)
            })

    def update(self):
        self.x += self.speed
        if self.x > SCREEN_WIDTH + 200:
            self.x = -self.size * 2
            self.y = random.randint(50, SCREEN_HEIGHT // 2)

    def draw(self):
        for puff in self.puffs:
            pygame.draw.circle(screen, COLORS['cloud_shadow'],
                            (int(self.x + puff['offset_x']), int(self.y + puff['offset_y'] + 5)),
                            puff['radius'])
        for puff in self.puffs:
            pygame.draw.circle(screen, COLORS['cloud_white'],
                            (int(self.x + puff['offset_x']), int(self.y + puff['offset_y'])),
                            puff['radius'])

class CherryTree:
    def __init__(self):
        self.x = random.randint(100, SCREEN_WIDTH - 100)
        self.y = random.randint(SCREEN_HEIGHT // 2, SCREEN_HEIGHT - 80)
        self.trunk_height = random.randint(60, 100)
        self.trunk_width = random.randint(8, 15)
        self.generate_branches()

    def generate_branches(self):
        self.branches = []
        branch_count = random.randint(3, 5)
        for i in range(branch_count):
            angle = random.uniform(-math.pi * 0.8, -math.pi * 0.2)
            length = random.randint(40, 80)
            sub_count = random.randint(2, 4)
            subs = []
            for j in range(sub_count):
                sub_angle = angle + random.uniform(-0.4, 0.4)
                sub_length = length * random.uniform(0.3, 0.5)
                subs.append({'angle': sub_angle, 'length': sub_length})
            self.branches.append({'angle': angle, 'length': length, 'subs': subs})
        self.blossom_clusters = []
        for _ in range(random.randint(15, 25)):
            self.blossom_clusters.append({
                'x': random.randint(-60, 60),
                'y': random.randint(-80, -20),
                'size': random.randint(8, 15),
                'color': random.choice([COLORS['cherry_pink'], COLORS['cherry_white'], (255, 200, 210)])
            })

    def draw(self):
        pygame.draw.rect(screen, COLORS['branch_brown'],
                        (self.x - self.trunk_width // 2, self.y - self.trunk_height,
                         self.trunk_width, self.trunk_height))

        for branch in self.branches:
            bx = self.x
            by = self.y - self.trunk_height
            ex = bx + math.cos(branch['angle']) * branch['length']
            ey = by + math.sin(branch['angle']) * branch['length']
            pygame.draw.line(screen, COLORS['branch_brown'], (bx, by), (ex, ey), 4)

            for sub in branch['subs']:
                sx = ex + math.cos(sub['angle']) * sub['length']
                sy = ey + math.sin(sub['angle']) * sub['length']
                pygame.draw.line(screen, COLORS['branch_brown'], (ex, ey), (sx, sy), 2)

        for cluster in self.blossom_clusters:
            pygame.draw.circle(screen, cluster['color'],
                             (self.x + cluster['x'], self.y - self.trunk_height + cluster['y']),
                             cluster['size'])
            pygame.draw.circle(screen, (255, 255, 255),
                             (self.x + cluster['x'] - 2, self.y - self.trunk_height + cluster['y'] - 2),
                             cluster['size'] // 3)

class FloatingIsland:
    def __init__(self):
        self.x = random.randint(100, SCREEN_WIDTH - 200)
        self.y = random.randint(SCREEN_HEIGHT // 2 + 50, SCREEN_HEIGHT - 100)
        self.width = random.randint(100, 200)
        self.height = random.randint(30, 50)

    def draw(self):
        pygame.draw.ellipse(screen, COLORS['island_dirt'],
                          (self.x - self.width // 2, self.y, self.width, self.height))
        pygame.draw.ellipse(screen, COLORS['island_grass'],
                          (self.x - self.width // 2, self.y - 10, self.width, 20))

class SkyBackground:
    def __init__(self):
        self.background_surface = None
        self.clouds = []
        self.trees = []
        self.islands = []
        self.petals = CherryPetalSystem(80)
        self.generate_elements()

    def generate_elements(self):
        for _ in range(6):
            self.clouds.append(FloatingCloud())

        for _ in range(4):
            self.trees.append(CherryTree())

        for _ in range(5):
            self.islands.append(FloatingIsland())

        self.create_background_surface()

    def create_background_surface(self):
        self.background_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        for y in range(SCREEN_HEIGHT):
            ratio = y / SCREEN_HEIGHT
            if ratio < 0.3:
                r = int(135 + (255 - 135) * (ratio / 0.3))
                g = int(206 + (182 - 206) * (ratio / 0.3))
                b = int(235 + (193 - 235) * (ratio / 0.3))
            elif ratio < 0.6:
                r = int(255 - (255 - 160) * ((ratio - 0.3) / 0.3))
                g = int(182 - (182 - 100) * ((ratio - 0.3) / 0.3))
                b = int(193 - (193 - 122) * ((ratio - 0.3) / 0.3))
            else:
                r = int(160 + (139 - 160) * ((ratio - 0.6) / 0.4))
                g = int(100 + (90 - 100) * ((ratio - 0.6) / 0.4))
                b = int(122 - (122 - 43) * ((ratio - 0.6) / 0.4))
            pygame.draw.line(self.background_surface, (r, g, b), (0, y), (SCREEN_WIDTH, y))

    def draw(self):
        screen.blit(self.background_surface, (0, 0))

        for cloud in self.clouds:
            cloud.update()
            cloud.draw()

        for island in self.islands:
            if not self.is_on_path(island.x, island.y):
                island.draw()

        self.petals.update()
        self.petals.draw()

        for tree in self.trees:
            if not self.is_on_path(tree.x, tree.y):
                tree.draw()

        fog_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        for y in range(SCREEN_HEIGHT - 100, SCREEN_HEIGHT):
            fog_alpha = int(((y - (SCREEN_HEIGHT - 100)) / 100) * 40)
            fog_surface.fill((255, 250, 250, fog_alpha), (0, y, SCREEN_WIDTH, 1))
        screen.blit(fog_surface, (0, 0))

    def is_on_path(self, x, y):
        for i in range(len(PATH_POINTS) - 1):
            x1, y1 = PATH_POINTS[i]
            x2, y2 = PATH_POINTS[i + 1]
            min_x = min(x1, x2) * GRID_SIZE
            max_x = max(x1, x2) * GRID_SIZE + GRID_SIZE
            min_y = min(y1, y2) * GRID_SIZE
            max_y = max(y1, y2) * GRID_SIZE + GRID_SIZE
            if min_x <= x <= max_x and min_y <= y <= max_y:
                return True
        return False

background = SkyBackground()

class IntroSequence:
    def __init__(self):
        self.phase = 'fade_in'
        self.alpha = 255
        self.dialogue_index = 0
        self.dialogues = []
        self.text_appear_timer = 0
        self.current_text = ""
        self.target_text = ""
        self.text_index = 0
        self.wait_timer = 0
        self.petals = CherryPetalSystem(50)
        self.background_surface = None
        self.fade_surface = None
        self.clouds = [FloatingCloud(y=random.randint(50, 300)) for _ in range(4)]
        self.init_intro()

    def init_intro(self):
        self.dialogues = [
            {"text": "天际传来悠远的钟声...", "speaker": None},
            {"text": "这里是传说中的天落殷园...", "speaker": "向导", "color": (200, 180, 255)},
            {"text": "樱花纷飞的净土，", "speaker": "向导", "color": (200, 180, 255)},
            {"text": "却也隐藏着不为人知的危险...", "speaker": "向导", "color": (200, 180, 255)},
            {"text": "苍穹之主率领天空军团来袭！", "speaker": "哨兵", "color": (255, 180, 180)},
            {"text": "我们必须守护这片最后的净土！", "speaker": "英雄", "color": (180, 255, 200)},
            {"text": "准备好了吗？", "speaker": "向导", "color": (200, 180, 255)},
            {"text": "樱花落尽时，便是决战之日...", "speaker": None},
        ]

        self.create_background_surface()
        self.fade_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.fade_surface.fill((0, 0, 0))

    def create_background_surface(self):
        self.background_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        for y in range(SCREEN_HEIGHT):
            ratio = y / SCREEN_HEIGHT
            r = int(135 + (200 - 135) * ratio)
            g = int(206 + (180 - 206) * ratio)
            b = int(235 + (200 - 235) * ratio)
            pygame.draw.line(self.background_surface, (r, g, b), (0, y), (SCREEN_WIDTH, y))

    def update(self):
        current_time = pygame.time.get_ticks()

        if self.phase == 'fade_in':
            self.alpha = max(0, self.alpha - 2)
            if self.alpha <= 0:
                self.phase = 'text_appear'
            self.petals.update()

        elif self.phase == 'text_appear':
            if self.text_appear_timer == 0:
                self.target_text = self.dialogues[self.dialogue_index]["text"]
                self.text_appear_timer = current_time

            if self.text_index < len(self.target_text):
                if current_time - self.text_appear_timer >= 25:
                    self.current_text += self.target_text[self.text_index]
                    self.text_index += 1
                    self.text_appear_timer = current_time
            else:
                self.phase = 'dialogue_wait'

        elif self.phase == 'dialogue_wait':
            self.wait_timer += 1
            if self.wait_timer > 180:
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
            self.petals.update()

        elif self.phase == 'fade_out':
            self.alpha = min(255, self.alpha + 3)
            if self.alpha >= 255:
                return True

        for cloud in self.clouds:
            cloud.update()

        return False

    def draw(self):
        screen.blit(self.background_surface, (0, 0))

        for cloud in self.clouds:
            cloud.draw()

        self.petals.draw()

        if self.dialogue_index < len(self.dialogues):
            self.draw_intro_text()

        if self.alpha > 0:
            self.fade_surface.set_alpha(self.alpha)
            screen.blit(self.fade_surface, (0, 0))

    def draw_intro_text(self):
        dialogue = self.dialogues[self.dialogue_index]
        speaker = dialogue.get("speaker")
        color = dialogue.get("color", COLORS['undertale_white'])

        box_width = min(SCREEN_WIDTH - 100, 700)
        box_height = 120
        box_x = (SCREEN_WIDTH - box_width) // 2
        box_y = SCREEN_HEIGHT - 180

        pygame.draw.rect(screen, (0, 0, 0), (box_x, box_y, box_width, box_height))
        pygame.draw.rect(screen, COLORS['cherry_pink'], (box_x, box_y, box_width, box_height), 4)

        for i in range(4):
            if i == 0:
                corner_x, corner_y = box_x, box_y
            elif i == 1:
                corner_x, corner_y = box_x + box_width, box_y
            elif i == 2:
                corner_x, corner_y = box_x + box_width, box_y + box_height
            else:
                corner_x, corner_y = box_x, box_y + box_height
            pygame.draw.circle(screen, COLORS['cherry_pink'], (corner_x, corner_y), 8, 4)

        if speaker:
            name_surface = font.render(speaker, True, color)
            name_rect = name_surface.get_rect(center=(box_x + 80, box_y - 15))
            pygame.draw.rect(screen, (0, 0, 0), (name_rect.left - 10, name_rect.top - 2, name_rect.width + 20, name_rect.height + 4))
            screen.blit(name_surface, name_rect)
            pygame.draw.rect(screen, color, (name_rect.left - 10, name_rect.top - 2, name_rect.width + 20, name_rect.height + 4), 2)

        text_x = box_x + 20
        text_y = box_y + 20
        max_width = box_width - 40

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

        for i, line_text in enumerate(lines[:4]):
            if line_text:
                text_surface = font.render(line_text, True, color)
                screen.blit(text_surface, (text_x, text_y + i * 28))

        if self.text_index >= len(self.target_text):
            heart_y = box_y + box_height - 35
            heart_x = box_x + 20
            pygame.draw.polygon(screen, COLORS['cherry_dark'], [
                (heart_x, heart_y - 10),
                (heart_x - 10, heart_y),
                (heart_x, heart_y + 8),
                (heart_x + 10, heart_y)
            ])
            pygame.draw.polygon(screen, COLORS['cherry_dark'], [
                (heart_x - 10, heart_y - 10),
                (heart_x - 20, heart_y),
                (heart_x - 10, heart_y + 8),
                (heart_x, heart_y)
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

    def draw(self):
        x, y = self.x, self.y
        size = GRID_SIZE // 2 - 2

        pygame.draw.rect(screen, COLORS['island_dirt'], (x - size - 4, y + size // 2, size * 2 + 8, size // 2 + 4))
        pygame.draw.rect(screen, COLORS['island_rock'], (x - size - 2, y + size // 2 + 2, size * 2 + 4, size // 2))

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
        pygame.draw.polygon(screen, (255, 255, 255, 150), pts, 2)

        name_text = small_font.render(self.config['name'], True, COLORS['text'])
        text_rect = name_text.get_rect(center=(x, y + GRID_SIZE // 2 + 18))
        pygame.draw.rect(screen, (255, 255, 255, 180), (text_rect.left - 4, text_rect.top - 2, text_rect.width + 8, text_rect.height + 4))
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
            return Bullet(self.x, self.y, self.target, self.config)

        return None

class Enemy:
    def __init__(self, enemy_type, path_index=0, wave_num=1):
        self.type = enemy_type
        self.config = ENEMY_CONFIG[enemy_type]
        wave_multiplier = 1 + (wave_num - 1) * 0.12

        self.max_health = int(self.config['health'] * wave_multiplier)
        self.health = self.max_health
        self.speed = self.config['speed'] * min(wave_multiplier, 2)
        self.reward = int(self.config['reward'] * wave_multiplier)
        self.path_index = path_index
        self.x, self.y = self.get_position()
        self.active = True
        self.wave_num = wave_num
        self.size = int(12 + (wave_num - 1) * 0.3)
        self.size = min(self.size, 22)
        self.anim_time = 0
        self.float_offset = 0
        self.trail_particles = []

        base_color = self.config['color']
        brighten_factor = min(wave_num * 0.03, 0.3)
        self.color = (
            min(255, int(base_color[0] + brighten_factor * 50)),
            min(255, int(base_color[1] + brighten_factor * 50)),
            min(255, int(base_color[2] + brighten_factor * 50)),
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
        self.float_offset = math.sin(self.anim_time * 2) * 4

        if random.random() < 0.1:
            self.trail_particles.append({
                'x': self.x + random.uniform(-5, 5),
                'y': self.y + random.uniform(-5, 5),
                'life': 30,
                'max_life': 30,
                'size': random.uniform(2, 4)
            })

        for p in self.trail_particles[:]:
            p['life'] -= 1
            if p['life'] <= 0:
                self.trail_particles.remove(p)

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
        for p in self.trail_particles:
            alpha = int(255 * (p['life'] / p['max_life']))
            surf = pygame.Surface((int(p['size'] * 2), int(p['size'] * 2)), pygame.SRCALPHA)
            pygame.draw.circle(surf, (*self.color, alpha), (int(p['size']), int(p['size'])), int(p['size']))
            screen.blit(surf, (int(p['x'] - p['size']), int(p['y'] - p['size'] - self.float_offset)))

        x, y = int(self.x), int(self.y + self.float_offset)
        size = self.size

        if self.type == 'spirit':
            wing_flap = math.sin(pygame.time.get_ticks() * 0.008) * 0.3
            points = [
                (x, y - size),
                (x - size * 1.5, y + size * wing_flap),
                (x, y + size // 2),
                (x + size * 1.5, y + size * wing_flap)
            ]
            pygame.draw.polygon(screen, self.color, points)
            pygame.draw.polygon(screen, (255, 255, 255, 150), points, 2)
            pygame.draw.circle(screen, (255, 255, 255), (x - 3, y - 3), 3)
            pygame.draw.circle(screen, (255, 255, 255), (x + 3, y - 3), 3)
            pygame.draw.circle(screen, self.config['eye_color'], (x - 3, y - 3), 2)
            pygame.draw.circle(screen, self.config['eye_color'], (x + 3, y - 3), 2)
        elif self.type == 'bird':
            wing_angle = math.sin(pygame.time.get_ticks() * 0.01) * 0.6
            pygame.draw.ellipse(screen, self.color, (x - size // 2, y - size // 2, size, size))
            wing1 = [(x, y), (x - size * 2, y - size * wing_angle), (x - size, y)]
            wing2 = [(x, y), (x + size * 2, y - size * wing_angle), (x + size, y)]
            pygame.draw.polygon(screen, self.color, wing1)
            pygame.draw.polygon(screen, self.color, wing2)
            pygame.draw.circle(screen, (255, 255, 255), (x - 2, y - 2), 2)
            pygame.draw.circle(screen, (255, 255, 255), (x + 2, y - 2), 2)
            pygame.draw.circle(screen, self.config['eye_color'], (x - 2, y - 2), 1)
            pygame.draw.circle(screen, self.config['eye_color'], (x + 2, y - 2), 1)
        elif self.type == 'cloud':
            puff_count = 5
            for i in range(puff_count):
                angle = i * (2 * math.pi / puff_count)
                px = x + math.cos(angle + pygame.time.get_ticks() * 0.001) * size * 0.5
                py = y + math.sin(angle + pygame.time.get_ticks() * 0.001) * size * 0.3
                pygame.draw.circle(screen, self.color, (int(px), int(py)), size // 2)
            pygame.draw.circle(screen, self.color, (x, y), size // 2)
            pygame.draw.circle(screen, (255, 255, 255), (x - 4, y - 2), 3)
            pygame.draw.circle(screen, (255, 255, 255), (x + 4, y - 2), 3)
            pygame.draw.circle(screen, self.config['eye_color'], (x - 4, y - 2), 2)
            pygame.draw.circle(screen, self.config['eye_color'], (x + 4, y - 2), 2)
        elif self.type == 'boss':
            pygame.draw.polygon(screen, (100, 60, 120), [(x, y - size - 20), (x - size * 1.5, y + size // 2), (x + size * 1.5, y + size // 2)])
            pygame.draw.circle(screen, self.color, (x, y - size // 2), size // 2 + 8)
            pygame.draw.polygon(screen, (120, 80, 140), [(x - size // 2, y - size // 2), (x - size * 1.5, y - size * 1.8), (x - size // 3, y - size // 3)])
            pygame.draw.polygon(screen, (120, 80, 140), [(x + size // 2, y - size // 2), (x + size * 1.5, y - size * 1.8), (x + size // 3, y - size // 3)])
            for i in range(3):
                angle = i * (2 * math.pi / 3) + pygame.time.get_ticks() * 0.002
                orbit_x = x + math.cos(angle) * (size + 10)
                orbit_y = y - size // 2 + math.sin(angle) * (size + 10)
                pygame.draw.circle(screen, (200, 180, 220), (int(orbit_x), int(orbit_y)), 5)
            pygame.draw.circle(screen, self.config['eye_color'], (x - 6, y - size // 2 - 3), 6)
            pygame.draw.circle(screen, self.config['eye_color'], (x + 6, y - size // 2 - 3), 6)
            pygame.draw.circle(screen, (255, 255, 255), (x - 6, y - size // 2 - 3), 2)
            pygame.draw.circle(screen, (255, 255, 255), (x + 6, y - size // 2 - 3), 2)

        bar_width = 30
        bar_height = 4
        pygame.draw.rect(screen, (30, 30, 30), (x - bar_width // 2, y - size - 10, bar_width, bar_height))
        health_ratio = max(0, self.health / self.max_health)
        bar_color = (180, 220, 180) if health_ratio > 0.5 else (220, 220, 120) if health_ratio > 0.25 else (220, 120, 120)
        pygame.draw.rect(screen, bar_color, (x - bar_width // 2, y - size - 10, bar_width * health_ratio, bar_height))

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

    def update(self, enemies=None):
        if not self.active or not self.target or not self.target.active:
            self.active = False
            return None

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
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), 6)
        pygame.draw.circle(screen, (255, 255, 255), (int(self.x), int(self.y)), 3)

class Game:
    def __init__(self):
        self.level = 'level_3'
        self.gold = LEVEL_CONFIG[self.level]['start_gold']
        self.lives = LEVEL_CONFIG[self.level]['lives']
        self.towers = []
        self.enemies = []
        self.bullets = []
        self.selected_tower_type = None
        self.wave_index = 0
        self.enemy_index = 0
        self.last_spawn_time = 0
        self.game_state = 'intro'
        self.wave_in_progress = False
        self.score = 0
        self.intro = IntroSequence()

    def draw_grid(self):
        for x in range(0, SCREEN_WIDTH, GRID_SIZE):
            pygame.draw.line(screen, COLORS['grid'], (x, 0), (x, SCREEN_HEIGHT), 1)
        for y in range(0, SCREEN_HEIGHT, GRID_SIZE):
            pygame.draw.line(screen, COLORS['grid'], (0, y), (SCREEN_WIDTH, y), 1)

    def draw_path(self):
        for i in range(len(PATH_POINTS) - 1):
            x1, y1 = PATH_POINTS[i]
            x2, y2 = PATH_POINTS[i + 1]
            pygame.draw.line(screen, COLORS['path_dark'],
                           (x1 * GRID_SIZE + GRID_SIZE // 2 + 2, y1 * GRID_SIZE + GRID_SIZE // 2 + 2),
                           (x2 * GRID_SIZE + GRID_SIZE // 2 + 2, y2 * GRID_SIZE + GRID_SIZE // 2 + 2), GRID_SIZE)
            pygame.draw.line(screen, COLORS['path_stone'],
                           (x1 * GRID_SIZE + GRID_SIZE // 2, y1 * GRID_SIZE + GRID_SIZE // 2),
                           (x2 * GRID_SIZE + GRID_SIZE // 2, y2 * GRID_SIZE + GRID_SIZE // 2), GRID_SIZE)

        sx, sy = PATH_POINTS[0]
        ex, ey = PATH_POINTS[-1]
        pygame.draw.circle(screen, (144, 238, 144), (sx * GRID_SIZE + GRID_SIZE // 2, sy * GRID_SIZE + GRID_SIZE // 2), 15)
        pygame.draw.circle(screen, (200, 255, 200), (sx * GRID_SIZE + GRID_SIZE // 2, sy * GRID_SIZE + GRID_SIZE // 2), 15, 3)
        pygame.draw.circle(screen, (180, 100, 100), (ex * GRID_SIZE + GRID_SIZE // 2, ey * GRID_SIZE + GRID_SIZE // 2), 15)
        pygame.draw.circle(screen, (255, 150, 150), (ex * GRID_SIZE + GRID_SIZE // 2, ey * GRID_SIZE + GRID_SIZE // 2), 15, 3)

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

    def spawn_enemy(self, enemy_type='spirit'):
        enemy = Enemy(enemy_type, wave_num=self.wave_index + 1)
        self.enemies.append(enemy)

    def update_wave(self, current_time):
        if self.game_state != 'playing':
            return

        level = LEVEL_CONFIG[self.level]
        if self.wave_index >= level['waves']:
            if not self.enemies:
                self.wave_in_progress = False
                self.game_state = 'victory'
            return

        wave = level['waves']
        base_enemies = 6 + self.wave_index * 2
        delay = max(500, 1400 - self.wave_index * 40)

        if not self.wave_in_progress:
            self.wave_in_progress = True
            self.enemy_index = 0
            self.last_spawn_time = current_time

        if self.enemy_index < base_enemies:
            if current_time - self.last_spawn_time >= delay:
                if self.wave_index >= wave * 0.7:
                    enemy_type = 'cloud' if self.wave_index % 3 == 0 else 'bird'
                elif self.wave_index >= wave * 0.4:
                    enemy_type = 'bird' if self.wave_index % 2 == 0 else 'spirit'
                else:
                    enemy_type = 'spirit'

                if self.wave_index == wave - 1:
                    enemy_type = 'boss'

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
                self.score += enemy.reward * 10
                self.enemies.remove(enemy)

        for tower in self.towers:
            result = tower.update(self.enemies, current_time)
            if result:
                self.bullets.append(result)

        for bullet in self.bullets[:]:
            bullet.update(self.enemies)
            if not bullet.active:
                self.bullets.remove(bullet)

    def draw(self):
        if self.game_state == 'intro':
            self.intro.draw()
            return

        if self.game_state == 'preparing':
            background.draw()
            self.draw_grid()
            self.draw_path()
            self.draw_ui()

            surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            surf.fill((0, 0, 0, 80))
            screen.blit(surf, (0, 0))

            text = large_font.render("天落殷园", True, COLORS['cherry_pink'])
            screen.blit(text, text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 80)))
            text = small_font.render("樱花飘落的浮空花园，守护这片净土", True, (200, 180, 200))
            screen.blit(text, text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 30)))
            btn = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 20, 200, 50)
            pygame.draw.rect(screen, (180, 130, 150), btn)
            pygame.draw.rect(screen, COLORS['cherry_white'], btn, 3)
            text = font.render("开始游戏", True, COLORS['text'])
            screen.blit(text, text.get_rect(center=btn.center))
            return

        background.draw()
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
            surf.fill((0, 0, 0, 160))
            screen.blit(surf, (0, 0))
            text = large_font.render("胜利！", True, COLORS['cherry_pink'])
            screen.blit(text, text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50)))
            text = font.render(f"分数: {self.score}", True, COLORS['cherry_white'])
            screen.blit(text, text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)))

        if self.game_state == 'defeat':
            surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            surf.fill((0, 0, 0, 160))
            screen.blit(surf, (0, 0))
            text = large_font.render("失败！", True, (180, 100, 100))
            screen.blit(text, text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 30)))

    def draw_ui(self):
        pygame.draw.rect(screen, (200, 180, 190), (0, 0, SCREEN_WIDTH, 50))

        pygame.draw.rect(screen, (220, 200, 210), (10, 8, 120, 34))
        text = font.render(f"{self.gold}", True, COLORS['gold'])
        screen.blit(text, text.get_rect(center=(70, 25)))

        pygame.draw.rect(screen, (220, 200, 210), (140, 8, 120, 34))
        text = font.render(f"{self.lives}", True, COLORS['health'])
        screen.blit(text, text.get_rect(center=(200, 25)))

        pygame.draw.rect(screen, (220, 200, 210), (270, 8, 120, 34))
        level = LEVEL_CONFIG[self.level]
        text = font.render(f"{self.wave_index + 1}/{level['waves']}", True, COLORS['text'])
        screen.blit(text, text.get_rect(center=(330, 25)))

        panel_x = SCREEN_WIDTH - 190
        pygame.draw.rect(screen, (200, 180, 190), (panel_x, 60, 180, 340))

        text = small_font.render("防御塔", True, COLORS['text'])
        screen.blit(text, text.get_rect(center=(panel_x + 90, 80)))

        y = 110
        for tower_type, config in TOWER_CONFIG.items():
            color = config['color'] if self.gold >= config['cost'] else (120, 120, 120)
            bg = pygame.Rect(panel_x + 10, y, 160, 58)
            if self.selected_tower_type == tower_type:
                pygame.draw.rect(screen, (220, 200, 210), bg)
                pygame.draw.rect(screen, COLORS['cherry_pink'], bg, 3)

            text = small_font.render(config['name'], True, COLORS['text'])
            screen.blit(text, (panel_x + 60, y + 5))
            text = small_font.render(f"{config['cost']}", True, COLORS['gold'])
            screen.blit(text, (panel_x + 60, y + 25))
            text = small_font.render(f"{config['damage']}", True, (120, 120, 120))
            screen.blit(text, (panel_x + 60, y + 42))

            center_x = panel_x + 30
            center_y = y + 29
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

            y += 64

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
                    if panel_x <= mx <= panel_x + 180 and 60 <= my <= 400:
                        y = 110
                        for tower_type in TOWER_CONFIG:
                            if y <= my <= y + 58:
                                if game.gold >= TOWER_CONFIG[tower_type]['cost']:
                                    selected_tower_type = tower_type
                                break
                            y += 64
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
