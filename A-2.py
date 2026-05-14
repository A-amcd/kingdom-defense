# ================================
# 塔防游戏 - 鸿蒙防线 艺术版
# 整合版 - 包含所有关卡与精美UI
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
pygame.display.set_caption("鸿蒙防线 - 艺术版")
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

font = get_chinese_font(36)
small_font = get_chinese_font(20)
large_font = get_chinese_font(72)

TOWER_CONFIG = {
    'arrow': {'name': '箭塔', 'cost': 100, 'damage': 15, 'range': 150, 'attack_speed': 0.8, 'color': (100, 180, 255), 'shape': 'triangle'},
    'cannon': {'name': '炮塔', 'cost': 200, 'damage': 60, 'range': 120, 'attack_speed': 0.4, 'splash_radius': 60, 'color': (255, 150, 100), 'shape': 'hexagon'},
    'ice': {'name': '冰塔', 'cost': 150, 'damage': 10, 'range': 130, 'attack_speed': 1.0, 'slow_factor': 0.35, 'color': (100, 200, 255), 'shape': 'diamond'},
    'lightning': {'name': '电塔', 'cost': 250, 'damage': 30, 'range': 140, 'attack_speed': 0.5, 'chain_count': 4, 'chain_range': 70, 'color': (255, 200, 100), 'shape': 'star'},
    'magic': {'name': '魔法塔', 'cost': 300, 'damage': 45, 'range': 150, 'attack_speed': 0.6, 'magic_radius': 50, 'color': (180, 100, 255), 'shape': 'octagon'},
}

LEVEL_CONFIG = {
    'level_1': {
        'name': '万象平原',
        'waves': 15,
        'start_gold': 500,
        'lives': 20,
        'theme': 'plain',
        'path': [(0, 4), (3, 4), (3, 10), (9, 10), (9, 3), (15, 3), (15, 12), (7, 12), (7, 16), (20, 16), (20, 7), (26, 7), (26, 14), (18, 14), (18, 9), (30, 9), (30, 16), (31, 16)],
        'ui_primary': (40, 100, 60),
        'ui_secondary': (60, 140, 80),
        'ui_accent': (100, 200, 100),
        'ui_border': (80, 180, 80),
        'icon_theme': 'plain',
    },
    'level_2': {
        'name': '恶地沼泽',
        'waves': 15,
        'start_gold': 500,
        'lives': 22,
        'theme': 'swamp',
        'path': [(0, 6), (5, 6), (5, 10), (10, 10), (10, 4), (16, 4), (16, 12), (22, 12), (22, 7), (28, 7), (28, 14), (31, 14)],
        'ui_primary': (30, 50, 60),
        'ui_secondary': (50, 80, 100),
        'ui_accent': (80, 200, 120),
        'ui_border': (60, 150, 100),
        'icon_theme': 'swamp',
    },
    'level_3': {
        'name': '天落殷园',
        'waves': 18,
        'start_gold': 600,
        'lives': 25,
        'theme': 'sky',
        'path': [(0, 4), (4, 4), (4, 8), (9, 8), (9, 3), (14, 3), (14, 10), (20, 10), (20, 6), (26, 6), (26, 13), (31, 13)],
        'ui_primary': (60, 80, 120),
        'ui_secondary': (100, 140, 180),
        'ui_accent': (255, 182, 193),
        'ui_border': (200, 150, 180),
        'icon_theme': 'sky',
    },
    'level_4': {
        'name': '污染花园',
        'waves': 20,
        'start_gold': 650,
        'lives': 28,
        'theme': 'corrupt',
        'path': [(0, 5), (3, 5), (3, 9), (8, 9), (8, 4), (13, 4), (13, 11), (19, 11), (19, 6), (25, 6), (25, 14), (31, 14)],
        'ui_primary': (50, 40, 60),
        'ui_secondary': (80, 60, 90),
        'ui_accent': (150, 100, 160),
        'ui_border': (120, 80, 120),
        'icon_theme': 'corrupt',
    },
}

ENEMY_CONFIG = {
    'plain': {
        'goblin': {'name': '哥布林', 'health': 80, 'speed': 1.2, 'reward': 15, 'color': (100, 180, 80)},
        'skeleton': {'name': '骷髅', 'health': 100, 'speed': 1.0, 'reward': 20, 'color': (180, 180, 180)},
        'orc': {'name': '兽人', 'health': 150, 'speed': 0.8, 'reward': 30, 'color': (80, 150, 60)},
        'boss': {'name': '兽王', 'health': 800, 'speed': 0.5, 'reward': 150, 'color': (60, 100, 50)},
    },
    'swamp': {
        'slime': {'name': '沼泽史莱姆', 'health': 100, 'speed': 1.5, 'reward': 20, 'color': (40, 120, 80)},
        'bat': {'name': '沼泽蝙蝠', 'health': 50, 'speed': 3.0, 'reward': 30, 'color': (80, 70, 80)},
        'troll': {'name': '泥巨人', 'health': 300, 'speed': 0.6, 'reward': 50, 'color': (60, 50, 45)},
        'boss': {'name': '沼泽领主', 'health': 1000, 'speed': 0.4, 'reward': 200, 'color': (30, 80, 50)},
    },
    'sky': {
        'spirit': {'name': '樱灵', 'health': 80, 'speed': 2.0, 'reward': 25, 'color': (255, 200, 220)},
        'bird': {'name': '云雀', 'health': 40, 'speed': 3.5, 'reward': 35, 'color': (180, 180, 220)},
        'cloud': {'name': '云妖', 'health': 200, 'speed': 1.2, 'reward': 45, 'color': (200, 200, 220)},
        'boss': {'name': '苍穹之主', 'health': 1200, 'speed': 0.6, 'reward': 300, 'color': (150, 100, 180)},
    },
    'corrupt': {
        'spirit': {'name': '枯萎灵', 'health': 90, 'speed': 1.8, 'reward': 30, 'color': (120, 100, 120)},
        'beetle': {'name': '腐蚀甲虫', 'health': 60, 'speed': 3.2, 'reward': 35, 'color': (80, 70, 90)},
        'mushroom': {'name': '毒蘑菇', 'health': 150, 'speed': 0.3, 'reward': 25, 'color': (140, 80, 100)},
        'boss': {'name': '污染之主', 'health': 1500, 'speed': 0.5, 'reward': 400, 'color': (80, 60, 80)},
    },
}

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

class FireParticleSystem:
    def __init__(self):
        self.particles = []
        self.time = 0

    def update(self):
        self.time += 0.02
        if len(self.particles) < 100:
            x = random.randint(0, SCREEN_WIDTH)
            y = SCREEN_HEIGHT + 20
            self.particles.append({
                'x': x,
                'y': y,
                'vx': random.uniform(-0.5, 0.5),
                'vy': random.uniform(-3, -1.5),
                'life': random.randint(60, 120),
                'max_life': 120,
                'size': random.uniform(10, 30),
                'hue': random.randint(0, 40),
            })

        for p in self.particles[:]:
            p['x'] += p['vx'] + math.sin(self.time + p['y'] * 0.01) * 0.5
            p['y'] += p['vy']
            p['life'] -= 1
            if p['life'] <= 0 or p['y'] < 0:
                self.particles.remove(p)

    def draw(self):
        for p in self.particles:
            life_ratio = p['life'] / p['max_life']
            size = int(p['size'] * life_ratio)
            if size < 1:
                continue
            alpha = int(255 * life_ratio * 0.6)
            r = min(255, 200 + int((1 - life_ratio) * 55))
            g = min(100, int((1 - life_ratio) * 100))
            b = 0
            surf = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
            for i in range(3):
                s = size * (1 - i * 0.25)
                pygame.draw.circle(surf, (r, g, b, alpha // (i + 1)), (size, size), max(1, int(s)))
            screen.blit(surf, (int(p['x'] - size), int(p['y'] - size)))

class ParticleSystem:
    def __init__(self):
        self.particles = []

    def add_particle(self, x, y, color, count=5):
        for _ in range(count):
            angle = random.uniform(0, math.pi * 2)
            speed = random.uniform(0.5, 2)
            self.particles.append({
                'x': x, 'y': y,
                'vx': math.cos(angle) * speed,
                'vy': math.sin(angle) * speed,
                'life': random.randint(20, 40),
                'max_life': 40,
                'size': random.uniform(1, 3),
                'color': color
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
            surf = pygame.Surface((int(p['size'] * 4), int(p['size'] * 4)), pygame.SRCALPHA)
            pygame.draw.circle(surf, (*p['color'], alpha), (int(p['size'] * 2), int(p['size'] * 2)), int(p['size']))
            screen.blit(surf, (int(p['x'] - p['size'] * 2), int(p['y'] - p['size'] * 2)))

class CherryPetalSystem:
    def __init__(self, count=60):
        self.petals = []
        for _ in range(count):
            self.petals.append({
                'x': random.randint(0, SCREEN_WIDTH),
                'y': random.randint(-50, SCREEN_HEIGHT),
                'size': random.uniform(3, 7),
                'speed_x': random.uniform(-0.5, 0.5),
                'speed_y': random.uniform(0.5, 1.5),
                'rotation': random.uniform(0, 360),
                'rot_speed': random.uniform(-2, 2),
                'sway_phase': random.uniform(0, 2 * math.pi),
                'color': random.choice([(255, 182, 193), (255, 250, 250), (219, 112, 147)])
            })

    def update(self):
        for petal in self.petals:
            petal['sway_phase'] += 0.03
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
            pygame.draw.ellipse(surf, (*petal['color'], 200), (0, 0, size * 2, size))
            rotated = pygame.transform.rotate(surf, petal['rotation'])
            rect = rotated.get_rect(center=(int(petal['x']), int(petal['y'])))
            screen.blit(rotated, rect)

class LevelIconDrawer:
    @staticmethod
    def draw_plain_icon(center_x, center_y, size):
        pygame.draw.circle(screen, (34, 139, 34), (center_x, center_y + 5), size)
        pygame.draw.circle(screen, (50, 205, 50), (center_x, center_y), size)
        pygame.draw.circle(screen, (144, 238, 144), (center_x - 3, center_y - 3), size // 3)
        for i in range(5):
            angle = i * (math.pi * 2 / 5) - math.pi / 2
            px = center_x + math.cos(angle) * (size * 0.6)
            py = center_y + math.sin(angle) * (size * 0.6) - 3
            pygame.draw.circle(screen, (100, 180, 100), (int(px), int(py)), 3)

    @staticmethod
    def draw_swamp_icon(center_x, center_y, size):
        pygame.draw.ellipse(screen, (30, 80, 50), (center_x - size, center_y, size * 2, size * 0.6))
        pygame.draw.ellipse(screen, (50, 150, 80), (center_x - size // 2, center_y - 5, size, size * 0.8))
        for i in range(3):
            pygame.draw.circle(screen, (80, 200, 120), (center_x - size // 3 + i * size // 3, center_y + 3), 4)
        pygame.draw.ellipse(screen, (20, 60, 40), (center_x - size * 0.8, center_y + size * 0.2, size * 1.6, size * 0.3))

    @staticmethod
    def draw_sky_icon(center_x, center_y, size):
        for i in range(4):
            cloud_x = center_x - size // 2 + i * size // 3
            cloud_y = center_y + math.sin(i) * 5
            pygame.draw.circle(screen, (255, 255, 255), (int(cloud_x), int(cloud_y)), size // 3)
        pygame.draw.circle(screen, (255, 200, 210), (center_x - 5, center_y - 5), 6)
        pygame.draw.circle(screen, (255, 200, 210), (center_x + 8, center_y - 8), 5)
        pygame.draw.circle(screen, (255, 200, 210), (center_x + 2, center_y - 2), 4)

    @staticmethod
    def draw_corrupt_icon(center_x, center_y, size):
        pygame.draw.ellipse(screen, (50, 40, 60), (center_x - size, center_y - size // 2, size * 2, size))
        pygame.draw.ellipse(screen, (80, 60, 90), (center_x - size // 2, center_y - size // 2 - 5, size, size // 2))
        pygame.draw.circle(screen, (200, 80, 150), (int(center_x - 5), int(center_y - 8)), 3)
        pygame.draw.circle(screen, (200, 80, 150), (int(center_x + 5), int(center_y - 10)), 3)
        pygame.draw.circle(screen, (100, 200, 100), (int(center_x - 8), int(center_y + 5)), 4)
        pygame.draw.circle(screen, (100, 200, 100), (int(center_x + 10), int(center_y + 8)), 3)

class BackgroundDrawer:
    @staticmethod
    def draw_plain_background():
        for y in range(SCREEN_HEIGHT):
            ratio = y / SCREEN_HEIGHT
            r = int(20 + (30 - 20) * ratio)
            g = int(50 + (80 - 50) * ratio)
            b = int(20 + (40 - 20) * ratio)
            pygame.draw.line(screen, (r, g, b), (0, y), (SCREEN_WIDTH, y))

        for i in range(SCREEN_WIDTH // GRID_SIZE):
            for j in range(SCREEN_HEIGHT // GRID_SIZE):
                if (i * 7 + j * 13 + i * j) % 10 < 3:
                    x = i * GRID_SIZE + random.randint(5, GRID_SIZE - 5)
                    y = j * GRID_SIZE + random.randint(5, GRID_SIZE - 5)
                    pygame.draw.line(screen, (50, 120, 55), (x, y), (x, y - 4), 2)

    @staticmethod
    def draw_swamp_background():
        for y in range(SCREEN_HEIGHT):
            ratio = y / SCREEN_HEIGHT
            r = int(50 + (40 - 50) * ratio)
            g = int(55 + (65 - 55) * ratio)
            b = int(60 + (70 - 60) * ratio)
            pygame.draw.line(screen, (r, g, b), (0, y), (SCREEN_WIDTH, y))

        ground_y = SCREEN_HEIGHT * 0.7
        for y in range(int(ground_y), SCREEN_HEIGHT):
            ratio = (y - ground_y) / (SCREEN_HEIGHT - ground_y)
            r = int(40 + (20 * ratio))
            g = int(60 + (-20 * ratio))
            b = int(45 + (-10 * ratio))
            pygame.draw.line(screen, (r, g, b), (0, y), (SCREEN_WIDTH, y))

        for _ in range(8):
            x = random.randint(50, SCREEN_WIDTH - 50)
            y = random.randint(int(ground_y), SCREEN_HEIGHT - 30)
            pygame.draw.ellipse(screen, (30, 50, 60), (x, y, random.randint(50, 100), random.randint(20, 40)))

    @staticmethod
    def draw_sky_background():
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
            pygame.draw.line(screen, (r, g, b), (0, y), (SCREEN_WIDTH, y))

        for _ in range(6):
            cloud_x = random.randint(0, SCREEN_WIDTH)
            cloud_y = random.randint(50, SCREEN_HEIGHT // 2)
            for i in range(4):
                pygame.draw.circle(screen, (255, 255, 255),
                                (cloud_x + i * 25, cloud_y + random.randint(-10, 10)),
                                random.randint(20, 40))

    @staticmethod
    def draw_corrupt_background():
        for y in range(SCREEN_HEIGHT):
            ratio = y / SCREEN_HEIGHT
            r = int(80 + (60 - 80) * ratio)
            g = int(90 + (50 - 90) * ratio)
            b = int(70 + (40 - 70) * ratio)
            pygame.draw.line(screen, (r, g, b), (0, y), (SCREEN_WIDTH, y))

        ground_y = SCREEN_HEIGHT * 0.65
        for y in range(int(ground_y), SCREEN_HEIGHT):
            ratio = (y - ground_y) / (SCREEN_HEIGHT - ground_y)
            r = int(60 + (40 - 60) * ratio)
            g = int(50 + (35 - 50) * ratio)
            b = int(40 + (30 - 40) * ratio)
            pygame.draw.line(screen, (r, g, b), (0, y), (SCREEN_WIDTH, y))

        for _ in range(5):
            x = random.randint(50, SCREEN_WIDTH - 50)
            y = random.randint(int(ground_y), SCREEN_HEIGHT - 30)
            pygame.draw.ellipse(screen, (50, 180, 50), (x, y, random.randint(60, 120), random.randint(20, 40)))

        for _ in range(25):
            bubble_x = random.randint(0, SCREEN_WIDTH)
            bubble_y = random.randint(int(SCREEN_HEIGHT * 0.5), SCREEN_HEIGHT)
            pygame.draw.circle(screen, (100, 200, 80), (bubble_x, bubble_y), random.randint(2, 5))

class IntroSequence:
    def __init__(self, theme='plain'):
        self.phase = 'fade_in'
        self.alpha = 255
        self.dialogue_index = 0
        self.dialogues = self.get_dialogues(theme)
        self.text_appear_timer = 0
        self.current_text = ""
        self.target_text = ""
        self.text_index = 0
        self.wait_timer = 0
        self.background_surface = None
        self.fade_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.fade_surface.fill((0, 0, 0))
        self.create_background(theme)

    def get_dialogues(self, theme):
        dialogues_map = {
            'plain': [
                {"text": "欢迎来到万象平原...", "speaker": None},
                {"text": "这里是我们的第一道防线。", "speaker": "向导", "color": (100, 200, 100)},
                {"text": "建立防御塔，阻止敌人的进攻！", "speaker": "向导", "color": (100, 200, 100)},
                {"text": "冒险即将开始...", "speaker": None},
            ],
            'swamp': [
                {"text": "又是一片被黑暗侵蚀的土地...", "speaker": None},
                {"text": "这里的空气弥漫着腐烂的气息...", "speaker": "???", "color": (80, 150, 120)},
                {"text": "沼泽领主已经苏醒！", "speaker": "???", "color": (80, 150, 120)},
                {"text": "冒险即将开始...", "speaker": None},
            ],
            'sky': [
                {"text": "天际传来悠远的钟声...", "speaker": None},
                {"text": "这里是传说中的天落殷园...", "speaker": "向导", "color": (255, 200, 220)},
                {"text": "樱花纷飞的净土，隐藏着危险...", "speaker": "向导", "color": (255, 200, 220)},
                {"text": "冒险即将开始...", "speaker": None},
            ],
            'corrupt': [
                {"text": "曾经美丽的花园，如今已是一片死寂...", "speaker": None},
                {"text": "污染的毒素蔓延开来...", "speaker": "向导", "color": (180, 160, 200)},
                {"text": "最后的战斗，即将开始...", "speaker": None},
            ],
        }
        return dialogues_map.get(theme, dialogues_map['plain'])

    def create_background(self, theme):
        self.background_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        if theme == 'swamp':
            for y in range(SCREEN_HEIGHT):
                ratio = y / SCREEN_HEIGHT
                pygame.draw.line(self.background_surface, (50 + int((40-50)*ratio), 55 + int((65-55)*ratio), 60 + int((70-60)*ratio)), (0, y), (SCREEN_WIDTH, y))
        elif theme == 'sky':
            for y in range(SCREEN_HEIGHT):
                ratio = y / SCREEN_HEIGHT
                r = int(135 + (200 - 135) * ratio)
                g = int(206 + (180 - 206) * ratio)
                b = int(235 + (200 - 235) * ratio)
                pygame.draw.line(self.background_surface, (r, g, b), (0, y), (SCREEN_WIDTH, y))
        elif theme == 'corrupt':
            for y in range(SCREEN_HEIGHT):
                ratio = y / SCREEN_HEIGHT
                pygame.draw.line(self.background_surface, (80 + int((60-80)*ratio), 90 + int((50-90)*ratio), 70 + int((40-70)*ratio)), (0, y), (SCREEN_WIDTH, y))
        else:
            for y in range(SCREEN_HEIGHT):
                ratio = y / SCREEN_HEIGHT
                pygame.draw.line(self.background_surface, (20 + int((30-20)*ratio), 50 + int((80-50)*ratio), 20 + int((40-20)*ratio)), (0, y), (SCREEN_WIDTH, y))

    def update(self):
        current_time = pygame.time.get_ticks()
        if self.phase == 'fade_in':
            self.alpha = max(0, self.alpha - 2)
            if self.alpha <= 0:
                self.phase = 'text_appear'
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
        elif self.phase == 'fade_out':
            self.alpha = min(255, self.alpha + 3)
            if self.alpha >= 255:
                return True
        return False

    def draw(self):
        screen.blit(self.background_surface, (0, 0))
        if self.dialogue_index < len(self.dialogues):
            self.draw_intro_text()
        if self.alpha > 0:
            self.fade_surface.set_alpha(self.alpha)
            screen.blit(self.fade_surface, (0, 0))

    def draw_intro_text(self):
        dialogue = self.dialogues[self.dialogue_index]
        speaker = dialogue.get("speaker")
        color = dialogue.get("color", (255, 255, 255))
        box_width = min(SCREEN_WIDTH - 100, 700)
        box_height = 120
        box_x = (SCREEN_WIDTH - box_width) // 2
        box_y = SCREEN_HEIGHT - 180

        pygame.draw.rect(screen, (0, 0, 0), (box_x, box_y, box_width, box_height))
        pygame.draw.rect(screen, color, (box_x, box_y, box_width, box_height), 4)

        for i, (cx, cy) in enumerate([(box_x, box_y), (box_x + box_width, box_y), (box_x + box_width, box_y + box_height), (box_x, box_y + box_height)]):
            pygame.draw.circle(screen, color, (cx, cy), 8, 4)

        if speaker:
            name_surface = font.render(speaker, True, color)
            name_rect = name_surface.get_rect(center=(box_x + 80, box_y - 15))
            pygame.draw.rect(screen, (0, 0, 0), (name_rect.left - 10, name_rect.top - 2, name_rect.width + 20, name_rect.height + 4))
            screen.blit(name_surface, name_rect)
            pygame.draw.rect(screen, color, (name_rect.left - 10, name_rect.top - 2, name_rect.width + 20, name_rect.height + 4), 2)

        text_x, text_y = box_x + 20, box_y + 20
        max_width = box_width - 40
        words = self.current_text.split(' ')
        line, lines = "", []
        for word in words:
            test_line = line + word + " "
            if font.size(test_line)[0] <= max_width:
                line = test_line
            else:
                if line: lines.append(line.strip())
                line = word + " "
        if line: lines.append(line.strip())

        for i, line_text in enumerate(lines[:4]):
            if line_text:
                screen.blit(font.render(line_text, True, color), (text_x, text_y + i * 28))

        if self.text_index >= len(self.target_text):
            heart_x, heart_y = box_x + 20, box_y + box_height - 35
            pygame.draw.polygon(screen, color, [(heart_x, heart_y - 10), (heart_x - 10, heart_y), (heart_x, heart_y + 8), (heart_x + 10, heart_y)])

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
        pygame.draw.rect(screen, (80, 60, 50), (x - size - 4, y + size // 2, size * 2 + 8, size // 2 + 4))
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
        name_text = small_font.render(self.config['name'], True, (255, 255, 255))
        text_rect = name_text.get_rect(center=(x, y + GRID_SIZE // 2 + 18))
        pygame.draw.rect(screen, (0, 0, 0, 180), (text_rect.left - 4, text_rect.top - 2, text_rect.width + 8, text_rect.height + 4))
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
    def __init__(self, enemy_type, path_points, path_index=0, wave_num=1, theme='plain'):
        self.type = enemy_type
        self.path_points = path_points
        self.theme = theme
        enemy_configs = ENEMY_CONFIG.get(theme, ENEMY_CONFIG['plain'])
        self.config = enemy_configs.get(enemy_type, enemy_configs.get(list(enemy_configs.keys())[0]))
        wave_multiplier = 1 + (wave_num - 1) * 0.1

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

        base_color = self.config['color']
        darken_factor = min(wave_num * 0.05, 0.4)
        self.color = (
            max(0, int(base_color[0] * (1 - darken_factor))),
            max(0, int(base_color[1] * (1 - darken_factor))),
            max(0, int(base_color[2] * (1 - darken_factor)))
        )

    def get_position(self):
        if self.path_index < len(self.path_points):
            x, y = self.path_points[self.path_index]
            return x * GRID_SIZE + GRID_SIZE // 2, y * GRID_SIZE + GRID_SIZE // 2
        return SCREEN_WIDTH, SCREEN_HEIGHT // 2

    def update(self, current_time):
        if self.path_index >= len(self.path_points):
            self.active = False
            return True
        self.anim_time += 0.1
        self.float_offset = math.sin(self.anim_time * 2) * 2

        target_x, target_y = self.path_points[self.path_index]
        target_x = target_x * GRID_SIZE + GRID_SIZE // 2
        target_y = target_y * GRID_SIZE + GRID_SIZE // 2
        dx, dy = target_x - self.x, target_y - self.y
        dist = math.hypot(dx, dy)
        if dist < 5:
            self.path_index += 1
        else:
            self.x += (dx / dist) * self.speed
            self.y += (dy / dist) * self.speed
        return False

    def draw(self):
        x, y = int(self.x), int(self.y + self.float_offset)
        size = self.size

        if self.type in ['goblin', 'slime', 'spirit']:
            pygame.draw.ellipse(screen, self.color, (x - size, y - size // 2, size * 2, size * 1.5))
            pygame.draw.circle(screen, (255, 255, 255), (x - 4, y - 2), 4)
            pygame.draw.circle(screen, (255, 255, 255), (x + 4, y - 2), 4)
            pygame.draw.circle(screen, (200, 50, 50), (x - 3, y - 1), 2)
            pygame.draw.circle(screen, (200, 50, 50), (x + 5, y - 1), 2)
        elif self.type in ['skeleton', 'bat', 'beetle']:
            wing_angle = math.sin(pygame.time.get_ticks() * 0.005) * 0.5
            pygame.draw.circle(screen, self.color, (x, y), size // 2)
            wing1 = [(x, y), (x - size * 1.5, y - size + wing_angle * size), (x - size * 0.5, y)]
            wing2 = [(x, y), (x + size * 1.5, y - size + wing_angle * size), (x + size * 0.5, y)]
            pygame.draw.polygon(screen, self.color, wing1)
            pygame.draw.polygon(screen, self.color, wing2)
            pygame.draw.circle(screen, (255, 255, 255), (x - 3, y - 2), 3)
            pygame.draw.circle(screen, (255, 255, 255), (x + 3, y - 2), 3)
            pygame.draw.circle(screen, (200, 50, 50), (x - 3, y - 2), 2)
            pygame.draw.circle(screen, (200, 50, 50), (x + 3, y - 2), 2)
        elif self.type in ['orc', 'troll', 'mushroom', 'cloud']:
            points = [(x - size, y), (x - size // 2, y - size), (x + size // 2, y - size), (x + size, y), (x + size // 2, y + size // 2), (x - size // 2, y + size // 2)]
            pygame.draw.polygon(screen, self.color, points)
            pygame.draw.polygon(screen, (self.color[0] + 30, self.color[1] + 30, self.color[2] + 30), points, 2)
            pygame.draw.circle(screen, (255, 255, 255), (x - 5, y - size // 3), 5)
            pygame.draw.circle(screen, (255, 255, 255), (x + 5, y - size // 3), 5)
            pygame.draw.circle(screen, (200, 50, 50), (x - 5, y - size // 3), 3)
            pygame.draw.circle(screen, (200, 50, 50), (x + 5, y - size // 3), 3)
        elif self.type == 'boss':
            pygame.draw.polygon(screen, (max(0, self.color[0] - 20), max(0, self.color[1] - 20), max(0, self.color[2] - 20)),
                              [(x, y - size - 20), (x - size * 1.5, y + size // 2), (x + size * 1.5, y + size // 2)])
            pygame.draw.circle(screen, self.color, (x, y - size // 2), size // 2 + 8)
            pygame.draw.polygon(screen, (max(0, self.color[0] + 20), max(0, self.color[1] + 20), max(0, self.color[2] + 20)),
                              [(x - size // 2, y - size // 2), (x - size * 1.5, y - size * 1.8), (x - size // 3, y - size // 3)])
            pygame.draw.polygon(screen, (max(0, self.color[0] + 20), max(0, self.color[1] + 20), max(0, self.color[2] + 20)),
                              [(x + size // 2, y - size // 2), (x + size * 1.5, y - size * 1.8), (x + size // 3, y - size // 3)])
            pygame.draw.circle(screen, (255, 200, 50), (x - 6, y - size // 2 - 3), 6)
            pygame.draw.circle(screen, (255, 200, 50), (x + 6, y - size // 2 - 3), 6)
            pygame.draw.circle(screen, (255, 255, 255), (x - 6, y - size // 2 - 3), 2)
            pygame.draw.circle(screen, (255, 255, 255), (x + 6, y - size // 2 - 3), 2)

        bar_width = 30
        bar_height = 4
        pygame.draw.rect(screen, (30, 30, 30), (x - bar_width // 2, y - size - 10, bar_width, bar_height))
        health_ratio = max(0, self.health / self.max_health)
        bar_color = (80, 180, 80) if health_ratio > 0.5 else (200, 200, 80) if health_ratio > 0.25 else (200, 80, 80)
        pygame.draw.rect(screen, bar_color, (x - bar_width // 2, y - size - 10, bar_width * health_ratio, bar_height))

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.active = False

class Bullet:
    def __init__(self, x, y, target, config):
        self.x, self.y = x, y
        self.target = target
        self.config = config
        self.speed = 12
        self.active = True
        self.color = config.get('bullet_color', config['color'])

    def update(self, enemies=None):
        if not self.active or not self.target or not self.target.active:
            self.active = False
            return None
        dx, dy = self.target.x - self.x, self.target.y - self.y
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
        self.level = 'level_1'
        self.gold = 500
        self.lives = 20
        self.towers = []
        self.enemies = []
        self.bullets = []
        self.particles = ParticleSystem()
        self.fire_effect = FireParticleSystem()
        self.selected_tower_type = None
        self.wave_index = 0
        self.enemy_index = 0
        self.last_spawn_time = 0
        self.game_state = 'menu'
        self.wave_in_progress = False
        self.score = 0
        self.intro = None
        self.cherry_petals = CherryPetalSystem(60)

    def get_level_config(self):
        return LEVEL_CONFIG.get(self.level, LEVEL_CONFIG['level_1'])

    def draw_grid(self):
        level_config = self.get_level_config()
        for x in range(0, SCREEN_WIDTH, GRID_SIZE):
            pygame.draw.line(screen, (*level_config['ui_primary'], 30), (x, 0), (x, SCREEN_HEIGHT), 1)
        for y in range(0, SCREEN_HEIGHT, GRID_SIZE):
            pygame.draw.line(screen, (*level_config['ui_primary'], 30), (0, y), (SCREEN_WIDTH, y), 1)

    def draw_path(self):
        level_config = self.get_level_config()
        path_points = level_config['path']
        theme = level_config['theme']
        path_colors = {
            'plain': ((139, 119, 101), (101, 85, 70)),
            'swamp': ((80, 70, 60), (60, 50, 45)),
            'sky': ((160, 140, 120), (120, 100, 80)),
            'corrupt': ((100, 90, 80), (70, 60, 50)),
        }
        path_color, path_edge = path_colors.get(theme, path_colors['plain'])

        for i in range(len(path_points) - 1):
            x1, y1 = path_points[i]
            x2, y2 = path_points[i + 1]
            pygame.draw.line(screen, path_edge,
                           (x1 * GRID_SIZE + GRID_SIZE // 2 + 2, y1 * GRID_SIZE + GRID_SIZE // 2 + 2),
                           (x2 * GRID_SIZE + GRID_SIZE // 2 + 2, y2 * GRID_SIZE + GRID_SIZE // 2 + 2), GRID_SIZE)
            pygame.draw.line(screen, path_color,
                           (x1 * GRID_SIZE + GRID_SIZE // 2, y1 * GRID_SIZE + GRID_SIZE // 2),
                           (x2 * GRID_SIZE + GRID_SIZE // 2, y2 * GRID_SIZE + GRID_SIZE // 2), GRID_SIZE)

        sx, sy = path_points[0]
        ex, ey = path_points[-1]
        pygame.draw.circle(screen, level_config['ui_accent'], (sx * GRID_SIZE + GRID_SIZE // 2, sy * GRID_SIZE + GRID_SIZE // 2), 15)
        pygame.draw.circle(screen, (255, 255, 255), (sx * GRID_SIZE + GRID_SIZE // 2, sy * GRID_SIZE + GRID_SIZE // 2), 15, 3)
        pygame.draw.circle(screen, level_config['ui_border'], (ex * GRID_SIZE + GRID_SIZE // 2, ey * GRID_SIZE + GRID_SIZE // 2), 15)
        pygame.draw.circle(screen, (255, 255, 255), (ex * GRID_SIZE + GRID_SIZE // 2, ey * GRID_SIZE + GRID_SIZE // 2), 15, 3)

    def draw_background(self):
        level_config = self.get_level_config()
        theme = level_config['theme']
        if theme == 'plain':
            BackgroundDrawer.draw_plain_background()
        elif theme == 'swamp':
            BackgroundDrawer.draw_swamp_background()
        elif theme == 'sky':
            BackgroundDrawer.draw_sky_background()
            self.cherry_petals.update()
            self.cherry_petals.draw()
        elif theme == 'corrupt':
            BackgroundDrawer.draw_corrupt_background()
        else:
            BackgroundDrawer.draw_plain_background()

    def can_place_tower(self, grid_x, grid_y):
        level_config = self.get_level_config()
        path_points = level_config['path']
        for i in range(len(path_points) - 1):
            x1, y1 = path_points[i]
            x2, y2 = path_points[i + 1]
            min_x, max_x = min(x1, x2), max(x1, x2)
            min_y, max_y = min(y1, y2), max(y1, y2)
            if min_x <= grid_x <= max_x and min_y <= grid_y <= max_y:
                return False
        for tower in self.towers:
            tx = int((tower.x - GRID_SIZE // 2) // GRID_SIZE)
            ty = int((tower.y - GRID_SIZE // 2) // GRID_SIZE)
            if tx == grid_x and ty == grid_y:
                return False
        return True

    def spawn_enemy(self, enemy_type='goblin'):
        level_config = self.get_level_config()
        path_points = level_config['path']
        theme = level_config['theme']
        enemy = Enemy(enemy_type, path_points, wave_num=self.wave_index + 1, theme=theme)
        self.enemies.append(enemy)

    def update_wave(self, current_time):
        if self.game_state != 'playing':
            return

        level_config = self.get_level_config()
        wave_count = level_config['waves']

        if self.wave_index >= wave_count:
            if not self.enemies:
                self.wave_in_progress = False
                self.game_state = 'victory'
            return

        base_enemies = 5 + self.wave_index * 2
        delay = max(600, 1500 - self.wave_index * 50)

        if not self.wave_in_progress:
            self.wave_in_progress = True
            self.enemy_index = 0
            self.last_spawn_time = current_time

        if self.enemy_index < base_enemies:
            if current_time - self.last_spawn_time >= delay:
                enemy_types = list(ENEMY_CONFIG.get(level_config['theme'], ENEMY_CONFIG['plain']).keys())
                if self.wave_index >= wave_count * 0.7:
                    enemy_type = enemy_types[2] if len(enemy_types) > 2 else enemy_types[-1]
                elif self.wave_index >= wave_count * 0.4:
                    enemy_type = enemy_types[1] if len(enemy_types) > 1 else enemy_types[0]
                else:
                    enemy_type = enemy_types[0]

                if self.wave_index == wave_count - 1:
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
            if self.intro.update():
                self.game_state = 'preparing'
            return

        if self.game_state != 'playing':
            return

        self.update_wave(current_time)
        self.particles.update()

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
                self.particles.add_particle(enemy.x, enemy.y, enemy.color, 10)
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
        if self.game_state == 'menu':
            self.draw_menu()
            return

        if self.game_state == 'level_select':
            self.draw_level_select()
            return

        if self.game_state == 'intro':
            self.intro.draw()
            return

        if self.game_state == 'preparing':
            self.draw_background()
            self.draw_grid()
            self.draw_path()
            self.draw_ui()
            surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            surf.fill((0, 0, 0, 80))
            screen.blit(surf, (0, 0))
            level_config = self.get_level_config()
            text = large_font.render(level_config['name'], True, level_config['ui_accent'])
            screen.blit(text, text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 80)))
            text = small_font.render("准备就绪，点击开始游戏", True, (200, 200, 200))
            screen.blit(text, text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 30)))
            btn = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 20, 200, 50)
            pygame.draw.rect(screen, level_config['ui_secondary'], btn)
            pygame.draw.rect(screen, (255, 255, 255), btn, 3)
            text = font.render("开始游戏", True, (255, 255, 255))
            screen.blit(text, text.get_rect(center=btn.center))
            return

        self.draw_background()
        self.draw_grid()
        self.draw_path()
        self.particles.draw()

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
            text = large_font.render("胜利！", True, (255, 215, 0))
            screen.blit(text, text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50)))
            text = font.render(f"分数: {self.score}", True, (200, 200, 255))
            screen.blit(text, text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)))
            btn = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 60, 200, 50)
            pygame.draw.rect(screen, (80, 100, 180), btn)
            pygame.draw.rect(screen, (255, 255, 255), btn, 3)
            text = font.render("返回选关", True, (255, 255, 255))
            screen.blit(text, text.get_rect(center=btn.center))

        if self.game_state == 'defeat':
            surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            surf.fill((0, 0, 0, 160))
            screen.blit(surf, (0, 0))
            text = large_font.render("失败！", True, (180, 80, 80))
            screen.blit(text, text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 30)))
            btn = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 40, 200, 50)
            pygame.draw.rect(screen, (180, 80, 80), btn)
            pygame.draw.rect(screen, (255, 255, 255), btn, 3)
            text = font.render("重新挑战", True, (255, 255, 255))
            screen.blit(text, text.get_rect(center=btn.center))

    def draw_menu(self):
        screen.fill((5, 5, 8))

        self.fire_effect.update()
        self.fire_effect.draw()

        for y in range(SCREEN_HEIGHT - 150, SCREEN_HEIGHT):
            ratio = (y - (SCREEN_HEIGHT - 150)) / 150
            alpha = int(100 * ratio)
            surf = pygame.Surface((SCREEN_WIDTH, 1), pygame.SRCALPHA)
            surf.fill((100, 30, 0, alpha))
            screen.blit(surf, (0, y))

        title = large_font.render("鸿蒙防线", True, (255, 215, 0))
        screen.blit(title, title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 120)))

        hint = font.render("点击任意处开始游戏", True, (180, 180, 180))
        screen.blit(hint, hint.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 10)))

        btn = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 70, 200, 50)
        pygame.draw.rect(screen, (100, 40, 20), btn)
        pygame.draw.rect(screen, (255, 100, 50), btn, 3)
        text = font.render("查看防御塔", True, (255, 200, 150))
        screen.blit(text, text.get_rect(center=btn.center))

    def draw_level_select(self):
        screen.fill((5, 5, 8))

        self.fire_effect.update()
        self.fire_effect.draw()

        for y in range(SCREEN_HEIGHT - 150, SCREEN_HEIGHT):
            ratio = (y - (SCREEN_HEIGHT - 150)) / 150
            alpha = int(80 * ratio)
            surf = pygame.Surface((SCREEN_WIDTH, 1), pygame.SRCALPHA)
            surf.fill((100, 30, 0, alpha))
            screen.blit(surf, (0, y))

        title = large_font.render("选择关卡", True, (255, 215, 0))
        screen.blit(title, title.get_rect(center=(SCREEN_WIDTH // 2, 80)))

        level_list = list(LEVEL_CONFIG.items())
        start_x = SCREEN_WIDTH // 2 - 600
        y = 180

        icon_drawers = {
            'plain': LevelIconDrawer.draw_plain_icon,
            'swamp': LevelIconDrawer.draw_swamp_icon,
            'sky': LevelIconDrawer.draw_sky_icon,
            'corrupt': LevelIconDrawer.draw_corrupt_icon,
        }

        for i, (level_id, config) in enumerate(level_list):
            col = i % 2
            row = i // 2
            btn_x = start_x + col * 620
            btn_y = y + row * 120

            btn = pygame.Rect(btn_x, btn_y, 280, 80)

            gradient_surf = pygame.Surface((280, 80), pygame.SRCALPHA)
            for gy in range(80):
                alpha = int(60 + 40 * (gy / 80))
                pygame.draw.line(gradient_surf, (*config['ui_primary'], alpha), (0, gy), (280, gy))
            screen.blit(gradient_surf, (btn_x, btn_y))

            pygame.draw.rect(screen, config['ui_accent'], btn, 3)

            icon_theme = config.get('icon_theme', 'plain')
            icon_drawer = icon_drawers.get(icon_theme, icon_drawers['plain'])
            icon_drawer(btn_x + 45, btn_y + 40, 28)

            text = font.render(config['name'], True, config['ui_accent'])
            screen.blit(text, (btn_x + 95, btn_y + 22))

            info = small_font.render(f"波次:{config['waves']} 金:{config['start_gold']} 生命:{config['lives']}", True, (180, 180, 180))
            screen.blit(info, (btn_x + 95, btn_y + 50))

        btn = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - 80, 200, 50)
        pygame.draw.rect(screen, (100, 40, 20), btn)
        pygame.draw.rect(screen, (255, 100, 50), btn, 3)
        text = font.render("返回主菜单", True, (255, 200, 150))
        screen.blit(text, text.get_rect(center=btn.center))

    def draw_ui(self):
        level_config = self.get_level_config()

        pygame.draw.rect(screen, level_config['ui_primary'], (0, 0, SCREEN_WIDTH, 50))

        pygame.draw.rect(screen, level_config['ui_secondary'], (10, 8, 100, 34))
        text = font.render(f"{self.gold}", True, (255, 215, 0))
        screen.blit(text, text.get_rect(center=(60, 25)))

        pygame.draw.rect(screen, level_config['ui_secondary'], (120, 8, 100, 34))
        text = font.render(f"{self.lives}", True, (255, 100, 100))
        screen.blit(text, text.get_rect(center=(170, 25)))

        pygame.draw.rect(screen, level_config['ui_secondary'], (230, 8, 120, 34))
        text = font.render(f"{self.wave_index + 1}/{level_config['waves']}", True, (255, 255, 255))
        screen.blit(text, text.get_rect(center=(290, 25)))

        panel_x = SCREEN_WIDTH - 190
        pygame.draw.rect(screen, level_config['ui_primary'], (panel_x, 60, 180, 340))

        text = small_font.render("防御塔", True, (255, 255, 255))
        screen.blit(text, text.get_rect(center=(panel_x + 90, 80)))

        y = 110
        for tower_type, config in TOWER_CONFIG.items():
            color = config['color'] if self.gold >= config['cost'] else (100, 100, 100)
            bg = pygame.Rect(panel_x + 10, y, 160, 58)
            if self.selected_tower_type == tower_type:
                pygame.draw.rect(screen, level_config['ui_secondary'], bg)
                pygame.draw.rect(screen, (255, 255, 255), bg, 2)

            text = small_font.render(config['name'], True, (255, 255, 255))
            screen.blit(text, (panel_x + 60, y + 5))
            text = small_font.render(f"{config['cost']}", True, (255, 215, 0))
            screen.blit(text, (panel_x + 60, y + 25))
            text = small_font.render(f"{config['damage']}", True, (150, 150, 150))
            screen.blit(text, (panel_x + 60, y + 42))

            center_x = panel_x + 30
            center_y = y + 29
            shape = config['shape']

            if shape == 'triangle':
                pts = [(center_x, center_y - 12), (center_x - 12, center_y + 12), (center_x + 12, center_y + 12)]
            elif shape == 'hexagon':
                pts = create_polygon_points(center_x, center_y, 12, 6)
            elif shape == 'diamond':
                pts = [(center_x, center_y - 12), (center_x + 12, center_y), (center_x, center_y + 12), (center_x - 12, center_y)]
            elif shape == 'star':
                pts = create_star_points(center_x, center_y, 12)
            elif shape == 'octagon':
                pts = create_polygon_points(center_x, center_y, 12, 8)
            pygame.draw.polygon(screen, color, pts)
            y += 64

game = Game()

def main():
    global game
    running = True

    while running:
        mx, my = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if game.game_state == 'menu':
                    if 280 <= mx <= 480 and 420 <= my <= 470:
                        game.game_state = 'tower_intro'
                    else:
                        game.game_state = 'level_select'

                elif game.game_state == 'tower_intro':
                    if 540 <= my <= 590:
                        game.game_state = 'menu'

                elif game.game_state == 'level_select':
                    if 640 <= my <= 690:
                        game.game_state = 'menu'
                    else:
                        level_list = list(LEVEL_CONFIG.items())
                        start_x = SCREEN_WIDTH // 2 - 600
                        y = 180
                        for i, (level_id, config) in enumerate(level_list):
                            col = i % 2
                            row = i // 2
                            btn_x = start_x + col * 620
                            btn_y = y + row * 120
                            if btn_x <= mx <= btn_x + 280 and btn_y <= my <= btn_y + 80:
                                game.level = level_id
                                game.gold = config['start_gold']
                                game.lives = config['lives']
                                game.towers = []
                                game.enemies = []
                                game.bullets = []
                                game.wave_index = 0
                                game.enemy_index = 0
                                game.wave_in_progress = False
                                game.score = 0
                                game.intro = IntroSequence(config['theme'])
                                game.game_state = 'intro'
                                break

                elif game.game_state == 'intro':
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
                                    game.selected_tower_type = tower_type
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
                            game.selected_tower_type = None
                        elif game.selected_tower_type and game.can_place_tower(gx, gy):
                            cfg = TOWER_CONFIG[game.selected_tower_type]
                            if game.gold >= cfg['cost']:
                                game.gold -= cfg['cost']
                                game.towers.append(Tower(gx, gy, game.selected_tower_type))

                elif game.game_state == 'victory':
                    btn = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 60, 200, 50)
                    if btn.collidepoint(mx, my):
                        game.game_state = 'level_select'

                elif game.game_state == 'defeat':
                    btn = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 40, 200, 50)
                    if btn.collidepoint(mx, my):
                        level_config = game.get_level_config()
                        game.gold = level_config['start_gold']
                        game.lives = level_config['lives']
                        game.towers = []
                        game.enemies = []
                        game.bullets = []
                        game.wave_index = 0
                        game.enemy_index = 0
                        game.wave_in_progress = False
                        game.game_state = 'preparing'

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
