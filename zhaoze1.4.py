# ================================
# 塔防游戏 - 鸿蒙防线
# 第二关：恶地沼泽 - 优化版 1.4.1
# 优化：下雨效果性能 + 对话流畅度
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
    'sky_dark': (50, 55, 60),
    'sky_mid': (60, 65, 70),
    'fog': (70, 80, 75),
    'water_dark': (30, 50, 60),
    'water_mid': (45, 70, 85),
    'swamp_green': (40, 60, 45),
    'swamp_dark': (25, 40, 30),
    'mud': (70, 60, 50),
    'mud_dark': (50, 40, 35),
    'path_mud': (80, 70, 60),
    'path_edge': (60, 50, 45),
    'dead_tree': (40, 35, 30),
    'dead_bush': (50, 45, 40),
    'grid': (50, 60, 50),
    'text': (200, 200, 200),
    'gold': (255, 215, 0),
    'health': (200, 80, 80),
    'undertale_white': (255, 255, 255),
    'undertale_yellow': (255, 255, 0),
}

DIALOGUE_CONFIG = {
    'box_color': (0, 0, 0),
    'border_color': (255, 255, 255),
    'text_color': (255, 255, 255),
    'name_color': (255, 255, 0),
    'heart_color': (255, 0, 0),
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
    'normal': {'name': '沼泽史莱姆', 'health': 100, 'speed': 1.5, 'reward': 20, 'color': (40, 80, 60), 'eye_color': (150, 200, 100)},
    'fast': {'name': '沼泽蝙蝠', 'health': 50, 'speed': 3.0, 'reward': 30, 'color': (80, 70, 80), 'eye_color': (200, 50, 50)},
    'tank': {'name': '泥巨人', 'health': 300, 'speed': 0.8, 'reward': 50, 'color': (60, 50, 45), 'eye_color': (100, 150, 80)},
    'boss': {'name': '沼泽领主', 'health': 1000, 'speed': 0.5, 'reward': 200, 'color': (30, 60, 40), 'eye_color': (255, 150, 50)},
}

LEVEL_CONFIG = {
    'level_2': {'name': '恶地沼泽', 'waves': 15, 'start_gold': 500, 'lives': 22, 'theme': 'swamp'},
}

PATH_POINTS = [
    (0, 6), (5, 6), (5, 10), (10, 10), (10, 4), (16, 4),
    (16, 12), (22, 12), (22, 7), (28, 7), (28, 14), (31, 14)
]

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("鸿蒙防线 - 恶地沼泽")
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

class OptimizedRainSystem:
    def __init__(self, particle_count=150):
        self.particle_count = particle_count
        self.rain_surface = None
        self.init_rain()

    def init_rain(self):
        self.rain_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        self.particles = []
        for _ in range(self.particle_count):
            self.particles.append({
                'x': random.randint(0, SCREEN_WIDTH),
                'y': random.randint(-100, SCREEN_HEIGHT),
                'length': random.randint(15, 25),
                'speed': random.randint(10, 16),
            })

    def update(self):
        for p in self.particles:
            p['y'] += p['speed']
            p['x'] += 2
            if p['y'] > SCREEN_HEIGHT:
                p['y'] = random.randint(-50, -10)
                p['x'] = random.randint(0, SCREEN_WIDTH)

    def draw(self):
        self.rain_surface.fill((0, 0, 0, 0))
        for p in self.particles:
            pygame.draw.line(self.rain_surface, (160, 170, 180),
                           (int(p['x']), int(p['y'])),
                           (int(p['x'] + 3), int(p['y'] + p['length'])), 1)
        screen.blit(self.rain_surface, (0, 0))

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
        self.rain = OptimizedRainSystem(100)
        self.background_surface = None
        self.fade_surface = None
        self.init_intro()

    def init_intro(self):
        self.dialogues = [
            {"text": "又是一片被黑暗侵蚀的土地...", "speaker": None},
            {"text": "这里的空气弥漫着腐烂的气息...", "speaker": "???", "color": (100, 100, 150)},
            {"text": "沼泽领主已经苏醒，", "speaker": "???", "color": (100, 100, 150)},
            {"text": "它正召唤着无数怪物...", "speaker": "???", "color": (100, 100, 150)},
            {"text": "我们需要在这里建立防线！", "speaker": "英雄", "color": (100, 200, 100)},
            {"text": "阻止它们前进！", "speaker": "英雄", "color": (100, 200, 100)},
            {"text": "准备好了吗？", "speaker": "???", "color": (100, 100, 150)},
            {"text": "冒险即将开始...", "speaker": None},
        ]

        self.create_background_surface()
        self.fade_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.fade_surface.fill((0, 0, 0))

    def create_background_surface(self):
        self.background_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        for y in range(SCREEN_HEIGHT):
            ratio = y / SCREEN_HEIGHT
            r = int(50 + (40 - 50) * ratio)
            g = int(55 + (65 - 55) * ratio)
            b = int(60 + (70 - 60) * ratio)
            pygame.draw.line(self.background_surface, (r, g, b), (0, y), (SCREEN_WIDTH, y))

        ground_y = SCREEN_HEIGHT * 0.7
        for y in range(int(ground_y), SCREEN_HEIGHT):
            ratio = (y - ground_y) / (SCREEN_HEIGHT - ground_y)
            r = int(40 + (20 * ratio))
            g = int(60 + (-20 * ratio))
            b = int(45 + (-10 * ratio))
            pygame.draw.line(self.background_surface, (r, g, b), (0, y), (SCREEN_WIDTH, y))

    def update(self):
        current_time = pygame.time.get_ticks()

        if self.phase == 'fade_in':
            self.alpha = max(0, self.alpha - 2)
            if self.alpha <= 0:
                self.phase = 'text_appear'
            self.rain.update()

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
            self.rain.update()

        elif self.phase == 'fade_out':
            self.alpha = min(255, self.alpha + 3)
            if self.alpha >= 255:
                return True

        return False

    def draw(self):
        screen.blit(self.background_surface, (0, 0))
        self.rain.draw()
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
        pygame.draw.rect(screen, COLORS['undertale_white'], (box_x, box_y, box_width, box_height), 4)

        for i in range(4):
            if i == 0:
                corner_x, corner_y = box_x, box_y
            elif i == 1:
                corner_x, corner_y = box_x + box_width, box_y
            elif i == 2:
                corner_x, corner_y = box_x + box_width, box_y + box_height
            else:
                corner_x, corner_y = box_x, box_y + box_height
            pygame.draw.circle(screen, COLORS['undertale_white'], (corner_x, corner_y), 8, 4)

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
            pygame.draw.polygon(screen, (255, 0, 0), [
                (heart_x, heart_y - 10),
                (heart_x - 10, heart_y),
                (heart_x, heart_y + 8),
                (heart_x + 10, heart_y)
            ])
            pygame.draw.polygon(screen, (255, 0, 0), [
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

class StaticDeadBush:
    def __init__(self):
        self.x = random.randint(50, SCREEN_WIDTH - 50)
        self.y = random.randint(SCREEN_HEIGHT // 2, SCREEN_HEIGHT - 50)
        self.size = random.randint(25, 50)
        self.branches = []
        self.generate_branches()

    def generate_branches(self):
        branch_count = random.randint(4, 7)
        for i in range(branch_count):
            angle = random.uniform(-math.pi/2 - 0.6, -math.pi/2 + 0.6)
            length = self.size * random.uniform(0.6, 1.2)
            sub_branches = []
            sub_count = random.randint(1, 3)
            for j in range(sub_count):
                sub_angle = angle + random.uniform(-0.5, 0.5)
                sub_length = length * random.uniform(0.3, 0.5)
                sub_branches.append({'angle': sub_angle, 'length': sub_length, 'thickness': random.randint(1, 2)})

            self.branches.append({
                'angle': angle,
                'length': length,
                'thickness': random.randint(2, 4),
                'sub_branches': sub_branches,
                'color_offset': random.randint(-20, 20),
                'droop': random.uniform(0.1, 0.3)
            })

        self.trunk_width = random.randint(4, 8)

    def draw(self):
        pygame.draw.rect(screen, COLORS['dead_tree'], (self.x - self.trunk_width // 2, self.y, self.trunk_width, self.size * 0.3))

        for i, branch in enumerate(self.branches):
            start_x = self.x
            start_y = self.y - self.size * 0.2
            angle = branch['angle']
            droop = branch['droop']

            mid_x = start_x + math.cos(angle) * branch['length'] * 0.5
            mid_y = start_y + math.sin(angle) * branch['length'] * 0.5 + branch['length'] * droop
            end_x = start_x + math.cos(angle) * branch['length']
            end_y = start_y + math.sin(angle) * branch['length'] + branch['length'] * droop * 2

            color_r = max(0, min(255, COLORS['dead_bush'][0] + branch['color_offset']))
            color_g = max(0, min(255, COLORS['dead_bush'][1] + branch['color_offset']))
            color_b = max(0, min(255, COLORS['dead_bush'][2] + branch['color_offset']))
            color = (color_r, color_g, color_b)

            pygame.draw.line(screen, color, (start_x, start_y), (mid_x, mid_y), branch['thickness'])
            pygame.draw.line(screen, color, (mid_x, mid_y), (end_x, end_y), branch['thickness'])

            for sub in branch['sub_branches']:
                sub_end_x = end_x + math.cos(sub['angle']) * sub['length']
                sub_end_y = end_y + math.sin(sub['angle']) * sub['length']
                pygame.draw.line(screen, (color_r - 10, color_g - 10, color_b - 10), (end_x, end_y), (sub_end_x, sub_end_y), sub['thickness'])

            pygame.draw.circle(screen, (color_r - 15, color_g - 15, color_b - 15), (int(end_x), int(end_y)), 3)

class WaterSurface:
    def __init__(self):
        self.puddles = []
        self.shimmers = []
        self.wave_offset = 0
        self.generate_puddles()
        self.generate_shimmers()

    def generate_puddles(self):
        for _ in range(15):
            self.puddles.append({
                'x': random.randint(0, SCREEN_WIDTH),
                'y': random.randint(SCREEN_HEIGHT // 2, SCREEN_HEIGHT),
                'width': random.randint(50, 100),
                'height': random.randint(25, 50),
                'wave_phase': random.uniform(0, 2 * math.pi),
                'wave_speed': random.uniform(0.02, 0.04),
            })

    def generate_shimmers(self):
        for _ in range(60):
            self.shimmers.append({
                'x': random.randint(0, SCREEN_WIDTH),
                'y': random.randint(SCREEN_HEIGHT // 2, SCREEN_HEIGHT),
                'size': random.randint(2, 4),
                'brightness': random.randint(150, 200),
                'phase': random.uniform(0, 2 * math.pi),
                'speed': random.uniform(0.04, 0.07),
                'lifetime': random.randint(60, 120),
                'age': random.randint(0, 120)
            })

    def update(self):
        self.wave_offset += 0.015

        for shimmer in self.shimmers:
            shimmer['age'] += 1
            shimmer['phase'] += shimmer['speed']
            if shimmer['age'] >= shimmer['lifetime']:
                shimmer['x'] = random.randint(0, SCREEN_WIDTH)
                shimmer['y'] = random.randint(SCREEN_HEIGHT // 2, SCREEN_HEIGHT)
                shimmer['age'] = 0
                shimmer['lifetime'] = random.randint(60, 120)

    def draw(self):
        for puddle in self.puddles:
            if not self.is_on_path(puddle['x'], puddle['y']):
                wave_offset = math.sin(self.wave_offset + puddle['wave_phase']) * 2
                pygame.draw.ellipse(screen, COLORS['water_dark'],
                                  (puddle['x'] - puddle['width'] // 2, puddle['y'] - puddle['height'] // 2 + wave_offset, puddle['width'], puddle['height']))

        for shimmer in self.shimmers:
            if not self.is_on_path(shimmer['x'], shimmer['y']):
                age_ratio = shimmer['age'] / shimmer['lifetime']
                if age_ratio < 0.2:
                    alpha_mult = age_ratio / 0.2
                elif age_ratio > 0.8:
                    alpha_mult = (1 - age_ratio) / 0.2
                else:
                    alpha_mult = 1

                brightness = int(shimmer['brightness'] * alpha_mult)
                shimmer_x = shimmer['x'] + math.sin(shimmer['phase']) * 2
                shimmer_y = shimmer['y'] + math.cos(shimmer['phase'] * 0.7) * 2
                color = (min(255, brightness), min(255, brightness + 20), min(255, brightness + 40))
                pygame.draw.circle(screen, color, (int(shimmer_x), int(shimmer_y)), shimmer['size'])

    def is_on_path(self, x, y):
        for i in range(len(PATH_POINTS) - 1):
            x1, y1 = PATH_POINTS[i]
            x2, y2 = PATH_POINTS[i + 1]
            min_x, max_x = min(x1, x2) * GRID_SIZE, max(x1, x2) * GRID_SIZE + GRID_SIZE
            min_y, max_y = min(y1, y2) * GRID_SIZE, max(y1, y2) * GRID_SIZE + GRID_SIZE
            if min_x <= x <= max_x and min_y <= y <= max_y:
                return True
        return False

class SwampBackground:
    def __init__(self):
        self.bushes = []
        self.water = WaterSurface()
        self.reeds = []
        self.dead_trees = []
        self.rain = OptimizedRainSystem(150)
        self.generate_elements()

    def generate_elements(self):
        for _ in range(25):
            bush = StaticDeadBush()
            self.bushes.append(bush)

        for _ in range(40):
            self.reeds.append({
                'x': random.randint(0, SCREEN_WIDTH),
                'y': random.randint(SCREEN_HEIGHT // 2, SCREEN_HEIGHT),
                'height': random.randint(30, 50),
                'sway_offset': random.uniform(0, 2 * math.pi),
                'sway_speed': random.uniform(0.03, 0.05)
            })

        for _ in range(6):
            self.dead_trees.append({
                'x': random.randint(0, SCREEN_WIDTH),
                'y': random.randint(100, SCREEN_HEIGHT - 100),
                'trunk_height': random.randint(60, 90),
                'branch_count': random.randint(3, 5)
            })

    def draw(self):
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

        self.water.update()
        self.water.draw()

        time = pygame.time.get_ticks() * 0.001
        for reed in self.reeds:
            if not self.is_on_path(reed['x'], reed['y']):
                sway = math.sin(time * reed['sway_speed'] + reed['sway_offset']) * 6
                pygame.draw.line(screen, (80, 90, 70), (reed['x'], reed['y']), (reed['x'] + sway, reed['y'] - reed['height']), 2)
                pygame.draw.circle(screen, (90, 100, 80), (int(reed['x'] + sway), int(reed['y'] - reed['height'])), 3)

        for tree in self.dead_trees:
            if not self.is_on_path(tree['x'], tree['y']):
                pygame.draw.rect(screen, COLORS['dead_tree'], (tree['x'] - 6, tree['y'] - tree['trunk_height'], 12, tree['trunk_height']))
                for i in range(tree['branch_count']):
                    angle = (i / tree['branch_count']) * math.pi - math.pi / 2
                    branch_len = 25 + i * 8
                    end_x = tree['x'] + math.cos(angle) * branch_len
                    end_y = tree['y'] - tree['trunk_height'] * 0.5 + math.sin(angle) * branch_len * 0.5
                    pygame.draw.line(screen, COLORS['dead_tree'], (tree['x'], tree['y'] - tree['trunk_height'] * 0.6), (end_x, end_y), 3)

        for bush in self.bushes:
            bush.draw()

        self.rain.update()
        self.rain.draw()

        fog_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        for y in range(SCREEN_HEIGHT):
            fog_alpha = max(0, int((SCREEN_HEIGHT - y) / SCREEN_HEIGHT * 30))
            fog_surface.fill((70, 80, 75, fog_alpha), (0, y, SCREEN_WIDTH, 1))
        screen.blit(fog_surface, (0, 0))

    def is_on_path(self, x, y):
        for i in range(len(PATH_POINTS) - 1):
            x1, y1 = PATH_POINTS[i]
            x2, y2 = PATH_POINTS[i + 1]
            min_x, max_x = min(x1, x2) * GRID_SIZE, max(x1, x2) * GRID_SIZE + GRID_SIZE
            min_y, max_y = min(y1, y2) * GRID_SIZE, max(y1, y2) * GRID_SIZE + GRID_SIZE
            if min_x <= x <= max_x and min_y <= y <= max_y:
                return True
        return False

background = SwampBackground()

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

        pygame.draw.rect(screen, COLORS['mud'], (x - size - 4, y + size // 2, size * 2 + 8, size // 2 + 4))
        pygame.draw.rect(screen, COLORS['mud_dark'], (x - size - 2, y + size // 2 + 2, size * 2 + 4, size // 2))

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
    def __init__(self, enemy_type, path_index=0, wave_num=1):
        self.type = enemy_type
        self.config = ENEMY_CONFIG[enemy_type]
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
        self.size = min(self.size, 20)
        self.anim_time = 0
        self.bob_offset = 0

        base_color = self.config['color']
        darken_factor = min(wave_num * 0.05, 0.4)
        self.color = (
            max(0, int(base_color[0] * (1 - darken_factor))),
            max(0, int(base_color[1] * (1 - darken_factor))),
            max(0, int(base_color[2] * (1 - darken_factor))),
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
        self.bob_offset = math.sin(self.anim_time * 2) * 2

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
        x, y = int(self.x), int(self.y + self.bob_offset)
        size = self.size

        pygame.draw.ellipse(screen, (0, 0, 0, 80), (x - size, y + size // 2, size * 2, size // 2))

        if self.type == 'normal':
            pygame.draw.ellipse(screen, self.color, (x - size, y - size // 2, size * 2, size * 1.5))
            pygame.draw.ellipse(screen, (self.color[0] + 20, self.color[1] + 30, self.color[2] + 20), (x - size + 3, y - size // 2 + 3, size * 2 - 6, size * 1.5 - 6))
            pygame.draw.circle(screen, (200, 220, 180), (x - 4, y - 2), 4)
            pygame.draw.circle(screen, (200, 220, 180), (x + 4, y - 2), 4)
            pygame.draw.circle(screen, self.config['eye_color'], (x - 3, y - 1), 2)
            pygame.draw.circle(screen, self.config['eye_color'], (x + 5, y - 1), 2)
        elif self.type == 'fast':
            wing_angle = math.sin(pygame.time.get_ticks() * 0.005) * 0.5
            pygame.draw.circle(screen, self.color, (x, y), size // 2)
            wing1 = [(x, y), (x - size * 1.5, y - size + wing_angle * size), (x - size * 0.5, y)]
            wing2 = [(x, y), (x + size * 1.5, y - size + wing_angle * size), (x + size * 0.5, y)]
            pygame.draw.polygon(screen, self.color, wing1)
            pygame.draw.polygon(screen, self.color, wing2)
            pygame.draw.circle(screen, (255, 255, 255), (x - 3, y - 2), 3)
            pygame.draw.circle(screen, (255, 255, 255), (x + 3, y - 2), 3)
            pygame.draw.circle(screen, self.config['eye_color'], (x - 3, y - 2), 2)
            pygame.draw.circle(screen, self.config['eye_color'], (x + 3, y - 2), 2)
        elif self.type == 'tank':
            points = [(x - size, y), (x - size // 2, y - size), (x + size // 2, y - size), (x + size, y), (x + size // 2, y + size // 2), (x - size // 2, y + size // 2)]
            pygame.draw.polygon(screen, self.color, points)
            pygame.draw.polygon(screen, (self.color[0] + 30, self.color[1] + 30, self.color[2] + 30), points, 2)
            pygame.draw.circle(screen, (200, 220, 180), (x - 5, y - size // 3), 5)
            pygame.draw.circle(screen, (200, 220, 180), (x + 5, y - size // 3), 5)
            pygame.draw.circle(screen, self.config['eye_color'], (x - 5, y - size // 3), 3)
            pygame.draw.circle(screen, self.config['eye_color'], (x + 5, y - size // 3), 3)
        elif self.type == 'boss':
            pygame.draw.polygon(screen, (25, 35, 25), [(x, y - size - 15), (x - size * 1.2, y + size // 2), (x + size * 1.2, y + size // 2)])
            pygame.draw.circle(screen, self.color, (x, y - size // 2), size // 2 + 5)
            pygame.draw.polygon(screen, (40, 50, 35), [(x - size // 2, y - size // 2), (x - size * 1.2, y - size * 1.5), (x - size // 3, y - size // 3)])
            pygame.draw.polygon(screen, (40, 50, 35), [(x + size // 2, y - size // 2), (x + size * 1.2, y - size * 1.5), (x + size // 3, y - size // 3)])
            pygame.draw.circle(screen, self.config['eye_color'], (x - 5, y - size // 2 - 2), 5)
            pygame.draw.circle(screen, self.config['eye_color'], (x + 5, y - size // 2 - 2), 5)
            pygame.draw.circle(screen, (255, 255, 255), (x - 5, y - size // 2 - 2), 2)
            pygame.draw.circle(screen, (255, 255, 255), (x + 5, y - size // 2 - 2), 2)

        bar_width = 30
        bar_height = 4
        pygame.draw.rect(screen, (30, 30, 30), (x - bar_width // 2, y - size - 8, bar_width, bar_height))
        health_ratio = max(0, self.health / self.max_health)
        bar_color = (80, 180, 80) if health_ratio > 0.5 else (200, 200, 80) if health_ratio > 0.25 else (200, 80, 80)
        pygame.draw.rect(screen, bar_color, (x - bar_width // 2, y - size - 8, bar_width * health_ratio, bar_height))

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
        self.level = 'level_2'
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
            pygame.draw.line(screen, COLORS['path_edge'], (x1 * GRID_SIZE + GRID_SIZE // 2 + 2, y1 * GRID_SIZE + GRID_SIZE // 2 + 2), (x2 * GRID_SIZE + GRID_SIZE // 2 + 2, y2 * GRID_SIZE + GRID_SIZE // 2 + 2), GRID_SIZE)
            pygame.draw.line(screen, COLORS['path_mud'], (x1 * GRID_SIZE + GRID_SIZE // 2, y1 * GRID_SIZE + GRID_SIZE // 2), (x2 * GRID_SIZE + GRID_SIZE // 2, y2 * GRID_SIZE + GRID_SIZE // 2), GRID_SIZE)

        sx, sy = PATH_POINTS[0]
        ex, ey = PATH_POINTS[-1]
        pygame.draw.circle(screen, (40, 120, 40), (sx * GRID_SIZE + GRID_SIZE // 2, sy * GRID_SIZE + GRID_SIZE // 2), 15)
        pygame.draw.circle(screen, (60, 200, 60), (sx * GRID_SIZE + GRID_SIZE // 2, sy * GRID_SIZE + GRID_SIZE // 2), 15, 3)
        pygame.draw.circle(screen, (120, 50, 50), (ex * GRID_SIZE + GRID_SIZE // 2, ey * GRID_SIZE + GRID_SIZE // 2), 15)
        pygame.draw.circle(screen, (200, 80, 80), (ex * GRID_SIZE + GRID_SIZE // 2, ey * GRID_SIZE + GRID_SIZE // 2), 15, 3)

    def can_place_tower(self, grid_x, grid_y):
        for i in range(len(PATH_POINTS) - 1):
            x1, y1 = PATH_POINTS[i]
            x2, y2 = PATH_POINTS[i + 1]
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

    def spawn_enemy(self, enemy_type='normal'):
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
        base_enemies = 5 + self.wave_index * 2
        delay = max(600, 1500 - self.wave_index * 50)

        if not self.wave_in_progress:
            self.wave_in_progress = True
            self.enemy_index = 0
            self.last_spawn_time = current_time

        if self.enemy_index < base_enemies:
            if current_time - self.last_spawn_time >= delay:
                if self.wave_index >= wave * 0.7:
                    enemy_type = 'tank' if self.wave_index % 3 == 0 else 'fast'
                elif self.wave_index >= wave * 0.4:
                    enemy_type = 'fast' if self.wave_index % 2 == 0 else 'normal'
                else:
                    enemy_type = 'normal'

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
            surf.fill((0, 0, 0, 100))
            screen.blit(surf, (0, 0))

            text = large_font.render("恶地沼泽", True, (180, 180, 150))
            screen.blit(text, text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 80)))
            text = small_font.render("险恶的沼泽地带，敌人行动更加隐蔽", True, (150, 150, 150))
            screen.blit(text, text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 30)))
            btn = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 20, 200, 50)
            pygame.draw.rect(screen, (60, 120, 80), btn)
            pygame.draw.rect(screen, (200, 200, 200), btn, 3)
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
            surf.fill((0, 0, 0, 180))
            screen.blit(surf, (0, 0))
            text = large_font.render("胜利！", True, (200, 200, 100))
            screen.blit(text, text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50)))
            text = font.render(f"分数: {self.score}", True, (180, 180, 200))
            screen.blit(text, text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)))

        if self.game_state == 'defeat':
            surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            surf.fill((0, 0, 0, 180))
            screen.blit(surf, (0, 0))
            text = large_font.render("失败！", True, (180, 80, 80))
            screen.blit(text, text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 30)))

    def draw_ui(self):
        pygame.draw.rect(screen, (40, 50, 45), (0, 0, SCREEN_WIDTH, 50))

        pygame.draw.rect(screen, (50, 60, 55), (10, 8, 120, 34))
        text = font.render(f"{self.gold}", True, COLORS['gold'])
        screen.blit(text, text.get_rect(center=(70, 25)))

        pygame.draw.rect(screen, (50, 60, 55), (140, 8, 120, 34))
        text = font.render(f"{self.lives}", True, COLORS['health'])
        screen.blit(text, text.get_rect(center=(200, 25)))

        pygame.draw.rect(screen, (50, 60, 55), (270, 8, 120, 34))
        level = LEVEL_CONFIG[self.level]
        text = font.render(f"{self.wave_index + 1}/{level['waves']}", True, COLORS['text'])
        screen.blit(text, text.get_rect(center=(330, 25)))

        panel_x = SCREEN_WIDTH - 190
        pygame.draw.rect(screen, (40, 50, 45), (panel_x, 60, 180, 340))

        text = small_font.render("防御塔", True, COLORS['text'])
        screen.blit(text, text.get_rect(center=(panel_x + 90, 80)))

        y = 110
        for tower_type, config in TOWER_CONFIG.items():
            color = config['color'] if self.gold >= config['cost'] else (80, 80, 80)
            bg = pygame.Rect(panel_x + 10, y, 160, 58)
            if self.selected_tower_type == tower_type:
                pygame.draw.rect(screen, (60, 70, 65), bg)
                pygame.draw.rect(screen, (200, 200, 200), bg, 3)

            text = small_font.render(config['name'], True, COLORS['text'])
            screen.blit(text, (panel_x + 60, y + 5))
            text = small_font.render(f"{config['cost']}", True, COLORS['gold'])
            screen.blit(text, (panel_x + 60, y + 25))
            text = small_font.render(f"{config['damage']}", True, (150, 150, 150))
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
