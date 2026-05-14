# ================================
# 塔防游戏 - 鸿蒙防线
# 第一关：万象平原 - 精细化版本
# ================================

import pygame
import math
import random

pygame.init()

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
GRID_SIZE = 40
FPS = 60

# ================================
# 万象平原主题色配置
# ================================
COLORS = {
    'sky': (135, 206, 235),           # 天空蓝
    'grass_light': (86, 176, 58),     # 浅草地绿
    'grass_main': (68, 140, 46),      # 主草地绿
    'grass_dark': (50, 120, 35),      # 深草地绿
    'grass_accent': (100, 180, 70),   # 草地点缀
    'path_main': (180, 140, 100),      # 路径主色（土路）
    'path_dark': (140, 100, 70),      # 路径阴影
    'path_light': (200, 160, 120),    # 路径高光
    'grid': (60, 130, 50),           # 网格线（柔和绿）
    'water': (64, 164, 223),          # 水体蓝
    'flower_yellow': (255, 220, 80),   # 黄花
    'flower_white': (255, 255, 240),   # 白花
    'flower_pink': (255, 150, 180),    # 粉花
    'tree_dark': (34, 85, 28),        # 深色树
    'tree_light': (60, 130, 50),      # 浅色树
    'stone': (128, 128, 128),         # 石头
    'text': (255, 255, 255),
    'gold': (255, 215, 0),
    'health': (255, 100, 100),
}

# ================================
# 防御塔配置 - 精细化
# ================================
TOWER_CONFIG = {
    'arrow': {
        'name': '箭塔',
        'cost': 100,
        'damage': 15,
        'range': 150,
        'attack_speed': 0.8,
        'color': (70, 130, 180),       # 钢蓝色
        'shape': 'triangle',
    },
    'cannon': {
        'name': '炮塔',
        'cost': 200,
        'damage': 60,
        'range': 120,
        'attack_speed': 0.4,
        'splash_radius': 60,
        'color': (205, 92, 0),         # 橙色
        'shape': 'hexagon',
    },
    'ice': {
        'name': '冰塔',
        'cost': 150,
        'damage': 10,
        'range': 130,
        'attack_speed': 1.0,
        'slow_factor': 0.35,
        'max_stacks': 3,
        'ice_explosion_radius': 80,
        'ice_explosion_damage_pct': 0.05,
        'color': (135, 206, 250),       # 浅蓝色
        'shape': 'diamond',
    },
    'lightning': {
        'name': '电塔',
        'cost': 250,
        'damage': 30,
        'range': 140,
        'attack_speed': 0.5,
        'chain_count': 4,
        'chain_range': 70,
        'color': (255, 215, 0),         # 金色
        'shape': 'star',
    },
    'magic': {
        'name': '魔法塔',
        'cost': 300,
        'damage': 45,
        'range': 150,
        'attack_speed': 0.6,
        'magic_radius': 50,
        'color': (138, 43, 226),        # 蓝紫色
        'shape': 'octagon',
    },
}

# ================================
# 敌人配置 - 精细化怪物建模
# ================================
ENEMY_CONFIG = {
    'normal': {
        'name': '普通敌人',
        'health': 100,
        'speed': 1.5,
        'reward': 20,
        'color': (178, 34, 34),         # 深红色
        'eye_color': (255, 255, 0),     # 黄色眼睛
    },
    'fast': {
        'name': '快速敌人',
        'health': 50,
        'speed': 3.0,
        'reward': 30,
        'color': (255, 165, 0),         # 橙色
        'eye_color': (0, 0, 0),         # 黑色眼睛
    },
    'tank': {
        'name': '坦克敌人',
        'health': 300,
        'speed': 0.8,
        'reward': 50,
        'color': (70, 130, 180),        # 钢蓝色
        'eye_color': (255, 0, 0),       # 红色眼睛
    },
    'boss': {
        'name': 'Boss',
        'health': 1000,
        'speed': 0.5,
        'reward': 200,
        'color': (128, 0, 128),         # 紫色
        'eye_color': (255, 0, 255),     # 品红眼睛
    },
}

# 关卡配置 - 第一关：万象平原
LEVEL_CONFIG = {
    'level_1': {
        'name': '万象平原',
        'waves': 12,
        'start_gold': 500,
        'lives': 20,
        'theme': 'plain',
    },
}

# 第一关路径
PATH_POINTS = [
    (0, 8), (3, 8), (3, 3), (9, 3), (9, 11), (15, 11),
    (15, 5), (20, 5), (20, 13), (26, 13), (26, 7), (31, 7)
]

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("鸿蒙防线 - 万象平原")

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

# ================================
# 万象平原背景生成
# ================================
class PlainBackground:
    def __init__(self):
        self.grass_patches = []
        self.flowers = []
        self.trees = []
        self.stones = []
        self.generate_elements()

    def generate_elements(self):
        """生成平原元素"""
        # 生成草地斑块
        for _ in range(80):
            self.grass_patches.append({
                'x': random.randint(0, SCREEN_WIDTH),
                'y': random.randint(0, SCREEN_HEIGHT),
                'size': random.randint(20, 50),
                'type': random.choice(['light', 'dark', 'accent'])
            })

        # 生成花朵
        for _ in range(150):
            self.flowers.append({
                'x': random.randint(0, SCREEN_WIDTH),
                'y': random.randint(0, SCREEN_HEIGHT),
                'size': random.randint(3, 6),
                'color': random.choice(['yellow', 'white', 'pink']),
                'petals': random.randint(4, 6)
            })

        # 生成树木（主要在边缘）
        for _ in range(25):
            x = random.choice([random.randint(0, 100), random.randint(SCREEN_WIDTH-100, SCREEN_WIDTH)])
            y = random.randint(100, SCREEN_HEIGHT-100)
            self.trees.append({
                'x': x,
                'y': y,
                'size': random.randint(30, 50)
            })

        # 生成石头
        for _ in range(40):
            self.stones.append({
                'x': random.randint(0, SCREEN_WIDTH),
                'y': random.randint(0, SCREEN_HEIGHT),
                'size': random.randint(5, 12)
            })

    def is_on_path(self, x, y):
        """检查是否在路径上"""
        for i in range(len(PATH_POINTS) - 1):
            x1, y1 = PATH_POINTS[i]
            x2, y2 = PATH_POINTS[i + 1]
            min_x, max_x = min(x1, x2) * GRID_SIZE, max(x1, x2) * GRID_SIZE + GRID_SIZE
            min_y, max_y = min(y1, y2) * GRID_SIZE, max(y1, y2) * GRID_SIZE + GRID_SIZE
            if min_x <= x <= max_x and min_y <= y <= max_y:
                return True
        return False

    def draw(self):
        """绘制万象平原背景"""
        # 基础天空渐变（顶部到中部）
        for y in range(SCREEN_HEIGHT):
            ratio = y / SCREEN_HEIGHT
            r = int(135 + (68 - 135) * ratio)
            g = int(206 + (140 - 206) * ratio)
            b = int(235 + (46 - 235) * ratio)
            pygame.draw.line(screen, (r, g, b), (0, y), (SCREEN_WIDTH, y))

        # 绘制草地斑块
        for patch in self.grass_patches:
            if not self.is_on_path(patch['x'], patch['y']):
                if patch['type'] == 'light':
                    color = COLORS['grass_light']
                elif patch['type'] == 'dark':
                    color = COLORS['grass_dark']
                else:
                    color = COLORS['grass_accent']

                # 绘制不规则草地斑块
                points = []
                cx, cy = patch['x'], patch['y']
                size = patch['size']
                for i in range(8):
                    angle = (i / 8) * 2 * math.pi
                    r = size * random.uniform(0.7, 1.0)
                    px = cx + r * math.cos(angle)
                    py = cy + r * math.sin(angle)
                    points.append((px, py))
                if len(points) >= 3:
                    pygame.draw.polygon(screen, color, points)

        # 绘制花朵
        for flower in self.flowers:
            if not self.is_on_path(flower['x'], flower['y']):
                cx, cy = flower['x'], flower['y']
                size = flower['size']
                petals = flower['petals']

                # 绘制花瓣
                if flower['color'] == 'yellow':
                    petal_color = COLORS['flower_yellow']
                elif flower['color'] == 'white':
                    petal_color = COLORS['flower_white']
                else:
                    petal_color = COLORS['flower_pink']

                for i in range(petals):
                    angle = (i / petals) * 2 * math.pi
                    px = cx + size * math.cos(angle)
                    py = cy + size * math.sin(angle)
                    pygame.draw.circle(screen, petal_color, (int(px), int(py)), size // 2)

                # 绘制花心
                pygame.draw.circle(screen, (255, 220, 100), (int(cx), int(cy)), size // 3)

        # 绘制树木
        for tree in self.trees:
            if not self.is_on_path(tree['x'], tree['y']):
                x, y = tree['x'], tree['y']
                size = tree['size']

                # 树干
                trunk_width = size // 4
                trunk_height = size // 2
                pygame.draw.rect(screen, (101, 67, 33), (x - trunk_width//2, y, trunk_width, trunk_height))

                # 树冠（多层圆形）
                pygame.draw.circle(screen, COLORS['tree_dark'], (x, y - size//3), size // 2)
                pygame.draw.circle(screen, COLORS['tree_light'], (x - size//4, y - size//2), size // 3)
                pygame.draw.circle(screen, COLORS['tree_light'], (x + size//4, y - size//2), size // 3)

        # 绘制石头
        for stone in self.stones:
            if not self.is_on_path(stone['x'], stone['y']):
                x, y = stone['x'], stone['y']
                size = stone['size']
                pygame.draw.ellipse(screen, COLORS['stone'], (x - size, y - size//2, size*2, size))
                pygame.draw.ellipse(screen, (100, 100, 100), (x - size + 2, y - size//2 + 2, size - 2, size - 2))

background = PlainBackground()

# ================================
# 防御塔精细化建模
# ================================
class DetailedTower:
    def __init__(self, x, y, tower_type):
        self.x = x * GRID_SIZE + GRID_SIZE // 2
        self.y = y * GRID_SIZE + GRID_SIZE // 2
        self.type = tower_type
        self.config = TOWER_CONFIG[tower_type]
        self.last_attack_time = 0
        self.target = None
        self.animation_frame = 0

    def draw(self):
        """绘制精细化的防御塔"""
        x, y = self.x, self.y
        size = GRID_SIZE // 2 - 2
        base_size = size + 8

        # 塔座（底座）
        pygame.draw.rect(screen, (80, 60, 40), (x - base_size, y + size//2, base_size*2, base_size//2))
        pygame.draw.rect(screen, (100, 80, 60), (x - base_size + 2, y + size//2 + 2, base_size*2 - 4, base_size//2 - 4))

        # 根据塔类型绘制不同造型
        if self.type == 'arrow':
            self.draw_arrow_tower(x, y, size)
        elif self.type == 'cannon':
            self.draw_cannon_tower(x, y, size)
        elif self.type == 'ice':
            self.draw_ice_tower(x, y, size)
        elif self.type == 'lightning':
            self.draw_lightning_tower(x, y, size)
        elif self.type == 'magic':
            self.draw_magic_tower(x, y, size)

        # 塔名称
        name_text = small_font.render(self.config['name'], True, (255, 255, 255))
        text_rect = name_text.get_rect(center=(x, y + GRID_SIZE // 2 + 18))
        pygame.draw.rect(screen, (0, 0, 0, 180), (text_rect.left - 4, text_rect.top - 2, text_rect.width + 8, text_rect.height + 4))
        screen.blit(name_text, text_rect)

    def draw_arrow_tower(self, x, y, size):
        """绘制精细化箭塔"""
        color = self.config['color']

        # 塔身
        pygame.draw.rect(screen, (60, 80, 100), (x - size//2, y - size, size, size*1.5))
        pygame.draw.rect(screen, color, (x - size//2 + 2, y - size + 2, size - 4, size*1.5 - 4))

        # 顶部装饰
        pygame.draw.polygon(screen, color, [(x, y - size - 10), (x - 8, y - size), (x + 8, y - size)])

        # 弓弦细节
        pygame.draw.arc(screen, (139, 90, 43), (x - 6, y - size - 8, 12, 16), math.pi, 2*math.pi, 2)

        # 塔窗/观察口
        pygame.draw.circle(screen, (200, 220, 255), (x, y - size//2), 4)

    def draw_cannon_tower(self, x, y, size):
        """绘制精细化炮塔"""
        color = self.config['color']

        # 炮塔底座
        pygame.draw.circle(screen, (60, 60, 70), (x, y + size//4), size)

        # 炮管
        pygame.draw.rect(screen, (80, 80, 90), (x - 6, y - size - 5, 12, size + 8))
        pygame.draw.rect(screen, (100, 100, 110), (x - 4, y - size - 3, 8, size + 4))

        # 炮口
        pygame.draw.circle(screen, (50, 50, 60), (x, y - size - 5), 6)

        # 装饰环
        pygame.draw.circle(screen, color, (x, y + size//4), size - 3, 2)

    def draw_ice_tower(self, x, y, size):
        """绘制精细化冰塔"""
        color = self.config['color']

        # 水晶底座
        pygame.draw.polygon(screen, (150, 200, 255), [
            (x - size//2, y + size//2),
            (x + size//2, y + size//2),
            (x, y - size//3)
        ])

        # 主冰晶
        points = [
            (x, y - size - 8),      # 顶部
            (x - size//2, y - size//3),  # 左下
            (x + size//2, y - size//3),  # 右下
        ]
        pygame.draw.polygon(screen, color, points)
        pygame.draw.polygon(screen, (200, 240, 255), points, 2)

        # 冰晶装饰
        pygame.draw.line(screen, (255, 255, 255), (x, y - size), (x, y - size - 15), 2)
        pygame.draw.line(screen, (255, 255, 255), (x - 5, y - size - 5), (x + 5, y - size - 5), 2)

    def draw_lightning_tower(self, x, y, size):
        """绘制精细化电塔"""
        color = self.config['color']

        # 能量核心
        pygame.draw.circle(screen, (255, 200, 50), (x, y), size//2)

        # 外圈
        pygame.draw.circle(screen, color, (x, y), size, 3)

        # 闪电装饰
        for i in range(6):
            angle = (i / 6) * 2 * math.pi
            px = x + (size + 5) * math.cos(angle)
            py = y + (size + 5) * math.sin(angle)
            pygame.draw.circle(screen, (255, 255, 100), (int(px), int(py)), 3)

        # 中心闪电符号
        pygame.draw.line(screen, (255, 255, 255), (x - 3, y - 5), (x + 1, y - 1), 2)
        pygame.draw.line(screen, (255, 255, 255), (x + 1, y - 1), (x - 2, y + 2), 2)
        pygame.draw.line(screen, (255, 255, 255), (x - 2, y + 2), (x + 3, y + 5), 2)

    def draw_magic_tower(self, x, y, size):
        """绘制精细化魔法塔"""
        color = self.config['color']

        # 魔法书底座
        pygame.draw.rect(screen, (100, 60, 40), (x - size//2, y + size//4, size, size//2))

        # 悬浮魔法球
        pygame.draw.circle(screen, color, (x, y - size//2), size//2)
        pygame.draw.circle(screen, (220, 180, 255), (x, y - size//2), size//2 - 3)

        # 魔法光环
        for i in range(3):
            offset = (i - 1) * 3
            pygame.draw.circle(screen, (200, 150, 255), (x + offset, y - size//2 - 3), size//3 - i, 1)

        # 魔法粒子
        for _ in range(5):
            angle = random.uniform(0, 2 * math.pi)
            dist = random.uniform(size//2, size)
            px = x + dist * math.cos(angle)
            py = y - size//2 + dist * math.sin(angle) * 0.5
            pygame.draw.circle(screen, (255, 255, 200), (int(px), int(py)), 2)

    def update(self, enemies, current_time):
        """更新防御塔状态"""
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
            return self.create_bullet()

        return None

    def create_bullet(self):
        """创建子弹"""
        return Bullet(self.x, self.y, self.target, self.config)

# ================================
# 精细化敌人类
# ================================
class DetailedEnemy:
    def __init__(self, enemy_type, path_index=0, wave_num=1):
        self.type = enemy_type
        self.config = ENEMY_CONFIG[enemy_type]
        wave_multiplier = 1 + (wave_num - 1) * 0.1

        self.max_health = int(self.config['health'] * wave_multiplier)
        self.health = self.max_health
        self.speed = self.config['speed'] * min(wave_multiplier, 2)
        self.base_speed = self.speed
        self.reward = int(self.config['reward'] * wave_multiplier)
        self.path_index = path_index
        self.x, self.y = self.get_position()
        self.slow_timer = 0
        self.active = True
        self.wave_num = wave_num

        # 敌人大小
        self.size = int(12 + (wave_num - 1) * 0.3)
        self.size = min(self.size, 20)

        # 动画相关
        self.anim_time = 0
        self.bob_offset = 0

        # 颜色变深
        base_color = self.config['color']
        darken_factor = min(wave_num * 0.05, 0.4)
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

        # 动画更新
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
            speed = self.speed
            if self.slow_timer > current_time:
                speed *= 0.5
            self.x += (dx / dist) * speed
            self.y += (dy / dist) * speed

        return False

    def draw(self):
        """绘制精细化的敌人"""
        x, y = int(self.x), int(self.y + self.bob_offset)
        size = self.size

        # 阴影
        pygame.draw.ellipse(screen, (0, 0, 0, 100), (x - size, y + size//2, size*2, size//2))

        # 根据敌人类型绘制不同造型
        if self.type == 'normal':
            self.draw_normal_enemy(x, y, size)
        elif self.type == 'fast':
            self.draw_fast_enemy(x, y, size)
        elif self.type == 'tank':
            self.draw_tank_enemy(x, y, size)
        elif self.type == 'boss':
            self.draw_boss_enemy(x, y, size)

        # 生命值条
        self.draw_health_bar(x, y - size - 8)

    def draw_normal_enemy(self, x, y, size):
        """普通敌人 - 史莱姆造型"""
        color = self.config['color']
        eye_color = self.config['eye_color']

        # 身体（椭圆形）
        pygame.draw.ellipse(screen, color, (x - size, y - size//2, size*2, size*1.5))
        pygame.draw.ellipse(screen, (color[0] + 30, color[1] + 30, color[2] + 30),
                          (x - size + 3, y - size//2 + 3, size*2 - 6, size*1.5 - 6))

        # 眼睛
        pygame.draw.circle(screen, (255, 255, 255), (x - 4, y - 2), 4)
        pygame.draw.circle(screen, (255, 255, 255), (x + 4, y - 2), 4)
        pygame.draw.circle(screen, eye_color, (x - 3, y - 1), 2)
        pygame.draw.circle(screen, eye_color, (x + 5, y - 1), 2)

        # 高光
        pygame.draw.circle(screen, (255, 255, 255, 150), (x - size//2, y - size//2), 2)

    def draw_fast_enemy(self, x, y, size):
        """快速敌人 - 小恶魔造型"""
        color = self.config['color']
        eye_color = self.config['eye_color']

        # 身体
        pygame.draw.circle(screen, color, (x, y), size)

        # 耳朵/角
        pygame.draw.polygon(screen, (color[0] - 30, color[1] - 30, color[2] - 30), [
            (x - size//2, y - size//3),
            (x - size, y - size),
            (x - size//3, y - size//2)
        ])
        pygame.draw.polygon(screen, (color[0] - 30, color[1] - 30, color[2] - 30), [
            (x + size//2, y - size//3),
            (x + size, y - size),
            (x + size//3, y - size//2)
        ])

        # 眼睛（愤怒的表情）
        pygame.draw.circle(screen, (255, 255, 255), (x - 3, y - 2), 3)
        pygame.draw.circle(screen, (255, 255, 255), (x + 3, y - 2), 3)
        pygame.draw.circle(screen, eye_color, (x - 3, y - 2), 2)
        pygame.draw.circle(screen, eye_color, (x + 3, y - 2), 2)

        # 嘴（愤怒线条）
        pygame.draw.line(screen, (50, 50, 50), (x - 4, y + 4), (x + 4, y + 4), 2)

    def draw_tank_enemy(self, x, y, size):
        """坦克敌人 - 石头怪造型"""
        color = self.config['color']

        # 身体（不规则多边形）
        points = [
            (x - size, y),
            (x - size//2, y - size),
            (x + size//2, y - size),
            (x + size, y),
            (x + size//2, y + size//2),
            (x - size//2, y + size//2)
        ]
        pygame.draw.polygon(screen, color, points)
        pygame.draw.polygon(screen, (color[0] + 40, color[1] + 40, color[2] + 40), points, 2)

        # 眼睛
        pygame.draw.circle(screen, (255, 255, 255), (x - 5, y - size//3), 5)
        pygame.draw.circle(screen, (255, 255, 255), (x + 5, y - size//3), 5)
        pygame.draw.circle(screen, self.config['eye_color'], (x - 5, y - size//3), 3)
        pygame.draw.circle(screen, self.config['eye_color'], (x + 5, y - size//3), 3)

        # 裂纹细节
        pygame.draw.line(screen, (30, 30, 30), (x - size//3, y - size//2), (x, y), 1)
        pygame.draw.line(screen, (30, 30, 30), (x + size//3, y - size//3), (x + 2, y + 2), 1)

    def draw_boss_enemy(self, x, y, size):
        """Boss - 魔王造型"""
        color = self.config['color']

        # 斗篷/身体
        points = [
            (x, y - size - 10),
            (x - size, y + size//2),
            (x + size, y + size//2)
        ]
        pygame.draw.polygon(screen, (30, 0, 30), points)
        pygame.draw.polygon(screen, color, [
            (x, y - size - 5),
            (x - size + 5, y + size//2 - 3),
            (x + size - 5, y + size//2 - 3)
        ])

        # 头
        pygame.draw.circle(screen, (60, 0, 60), (x, y - size//2), size//2 + 3)
        pygame.draw.circle(screen, color, (x, y - size//2), size//2)

        # 角
        pygame.draw.polygon(screen, (80, 0, 80), [
            (x - size//2, y - size//2),
            (x - size, y - size),
            (x - size//3, y - size//3)
        ])
        pygame.draw.polygon(screen, (80, 0, 80), [
            (x + size//2, y - size//2),
            (x + size, y - size),
            (x + size//3, y - size//3)
        ])

        # 眼睛（发光）
        pygame.draw.circle(screen, (255, 0, 255), (x - 4, y - size//2 - 2), 4)
        pygame.draw.circle(screen, (255, 0, 255), (x + 4, y - size//2 - 2), 4)
        pygame.draw.circle(screen, (255, 255, 255), (x - 4, y - size//2 - 2), 2)
        pygame.draw.circle(screen, (255, 255, 255), (x + 4, y - size//2 - 2), 2)

        # 光环效果
        for i in range(3):
            pygame.draw.circle(screen, (color[0], 0, color[2]), (x, y - size//2), size + 5 + i*3, 1)

    def draw_health_bar(self, x, y):
        """绘制生命值条"""
        bar_width = 30
        bar_height = 4

        pygame.draw.rect(screen, (50, 50, 50), (x - bar_width//2, y, bar_width, bar_height))
        health_ratio = max(0, self.health / self.max_health)
        bar_color = (0, 255, 0) if health_ratio > 0.5 else (255, 255, 0) if health_ratio > 0.25 else (255, 0, 0)
        pygame.draw.rect(screen, bar_color, (x - bar_width//2, y, bar_width * health_ratio, bar_height))

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.active = False

# ================================
# 子弹类
# ================================
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

# ================================
# 游戏主类
# ================================
class Game:
    def __init__(self):
        self.level = 'level_1'
        self.gold = LEVEL_CONFIG[self.level]['start_gold']
        self.lives = LEVEL_CONFIG[self.level]['lives']
        self.towers = []
        self.enemies = []
        self.bullets = []
        self.selected_tower_type = None
        self.selected_tower = None
        self.wave_index = 0
        self.enemy_index = 0
        self.last_spawn_time = 0
        self.game_state = 'preparing'
        self.wave_in_progress = False
        self.score = 0

    def draw_grid(self):
        for x in range(0, SCREEN_WIDTH, GRID_SIZE):
            pygame.draw.line(screen, COLORS['grid'], (x, 0), (x, SCREEN_HEIGHT), 1)
        for y in range(0, SCREEN_HEIGHT, GRID_SIZE):
            pygame.draw.line(screen, COLORS['grid'], (0, y), (SCREEN_WIDTH, y), 1)

    def draw_path(self):
        for i in range(len(PATH_POINTS) - 1):
            x1, y1 = PATH_POINTS[i]
            x2, y2 = PATH_POINTS[i + 1]

            # 路径阴影
            pygame.draw.line(screen, COLORS['path_dark'],
                           (x1 * GRID_SIZE + GRID_SIZE // 2 + 2, y1 * GRID_SIZE + GRID_SIZE // 2 + 2),
                           (x2 * GRID_SIZE + GRID_SIZE // 2 + 2, y2 * GRID_SIZE + GRID_SIZE // 2 + 2),
                           GRID_SIZE)

            # 路径主体
            pygame.draw.line(screen, COLORS['path_main'],
                           (x1 * GRID_SIZE + GRID_SIZE // 2, y1 * GRID_SIZE + GRID_SIZE // 2),
                           (x2 * GRID_SIZE + GRID_SIZE // 2, y2 * GRID_SIZE + GRID_SIZE // 2),
                           GRID_SIZE)

            # 路径高光
            pygame.draw.line(screen, COLORS['path_light'],
                           (x1 * GRID_SIZE + GRID_SIZE // 2, y1 * GRID_SIZE + GRID_SIZE // 2 - 3),
                           (x2 * GRID_SIZE + GRID_SIZE // 2, y2 * GRID_SIZE + GRID_SIZE // 2 - 3),
                           2)

        # 起点和终点
        sx, sy = PATH_POINTS[0]
        ex, ey = PATH_POINTS[-1]
        pygame.draw.circle(screen, (50, 200, 50), (sx * GRID_SIZE + GRID_SIZE // 2, sy * GRID_SIZE + GRID_SIZE // 2), 15)
        pygame.draw.circle(screen, (0, 255, 0), (sx * GRID_SIZE + GRID_SIZE // 2, sy * GRID_SIZE + GRID_SIZE // 2), 15, 3)
        pygame.draw.circle(screen, (200, 50, 50), (ex * GRID_SIZE + GRID_SIZE // 2, ey * GRID_SIZE + GRID_SIZE // 2), 15)
        pygame.draw.circle(screen, (255, 0, 0), (ex * GRID_SIZE + GRID_SIZE // 2, ey * GRID_SIZE + GRID_SIZE // 2), 15, 3)

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
        enemy = DetailedEnemy(enemy_type, wave_num=self.wave_index + 1)
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
        if self.game_state == 'preparing':
            background.draw()
            self.draw_grid()
            self.draw_path()
            self.draw_ui()

            surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            surf.fill((0, 0, 0, 100))
            screen.blit(surf, (0, 0))

            text = large_font.render("万象平原", True, (255, 215, 0))
            screen.blit(text, text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 80)))
            text = small_font.render("广阔的草原，守护这片土地", True, (200, 200, 200))
            screen.blit(text, text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 30)))
            btn = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 20, 200, 50)
            pygame.draw.rect(screen, (80, 180, 80), btn)
            pygame.draw.rect(screen, (255, 255, 255), btn, 3)
            text = font.render("开始游戏", True, (255, 255, 255))
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
            text = large_font.render("🎉 胜利！", True, (255, 215, 0))
            screen.blit(text, text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50)))
            text = font.render(f"分数: {self.score}", True, (200, 200, 255))
            screen.blit(text, text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)))

        if self.game_state == 'defeat':
            surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            surf.fill((0, 0, 0, 180))
            screen.blit(surf, (0, 0))
            text = large_font.render("💀 失败！", True, (255, 100, 100))
            screen.blit(text, text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 30)))

    def draw_ui(self):
        pygame.draw.rect(screen, (50, 80, 50), (0, 0, SCREEN_WIDTH, 50))

        pygame.draw.rect(screen, (60, 90, 60), (10, 8, 120, 34))
        text = font.render(f"💰 {self.gold}", True, COLORS['gold'])
        screen.blit(text, text.get_rect(center=(70, 25)))

        pygame.draw.rect(screen, (60, 90, 60), (140, 8, 120, 34))
        text = font.render(f"❤️ {self.lives}", True, COLORS['health'])
        screen.blit(text, text.get_rect(center=(200, 25)))

        pygame.draw.rect(screen, (60, 90, 60), (270, 8, 120, 34))
        level = LEVEL_CONFIG[self.level]
        text = font.render(f"🌊 {self.wave_index + 1}/{level['waves']}", True, COLORS['text'])
        screen.blit(text, text.get_rect(center=(330, 25)))

        panel_x = SCREEN_WIDTH - 190
        pygame.draw.rect(screen, (50, 80, 50), (panel_x, 60, 180, 340))

        text = small_font.render("防御塔", True, COLORS['text'])
        screen.blit(text, text.get_rect(center=(panel_x + 90, 80)))

        y = 110
        for tower_type, config in TOWER_CONFIG.items():
            color = config['color'] if self.gold >= config['cost'] else (100, 100, 100)
            bg = pygame.Rect(panel_x + 10, y, 160, 58)
            if self.selected_tower_type == tower_type:
                pygame.draw.rect(screen, (70, 100, 70), bg)
                pygame.draw.rect(screen, (255, 255, 255), bg, 2)

            text = small_font.render(config['name'], True, COLORS['text'])
            screen.blit(text, (panel_x + 60, y + 5))
            text = small_font.render(f"¥{config['cost']}", True, COLORS['gold'])
            screen.blit(text, (panel_x + 60, y + 25))
            text = small_font.render(f"伤害:{config['damage']}", True, (180, 180, 180))
            screen.blit(text, (panel_x + 60, y + 42))

            # 绘制塔图标
            center_x = panel_x + 30
            center_y = y + 29
            if config['shape'] == 'triangle':
                pts = [(center_x, center_y - 12), (center_x - 12, center_y + 12), (center_x + 12, center_y + 12)]
                pygame.draw.polygon(screen, color, pts)
            elif config['shape'] == 'hexagon':
                pts = [(center_x + 12*math.cos(i*60*math.pi/180-90*math.pi/180),
                       center_y + 12*math.sin(i*60*math.pi/180-90*math.pi/180)) for i in range(6)]
                pygame.draw.polygon(screen, color, pts)
            elif config['shape'] == 'diamond':
                pts = [(center_x, center_y - 12), (center_x + 12, center_y), (center_x, center_y + 12), (center_x - 12, center_y)]
                pygame.draw.polygon(screen, color, pts)
            elif config['shape'] == 'star':
                pts = [(center_x + 12*math.cos(i*72*math.pi/180-90*math.pi/180),
                       center_y + 12*math.sin(i*72*math.pi/180-90*math.pi/180)) for i in range(5)]
                pygame.draw.polygon(screen, color, pts)
            elif config['shape'] == 'octagon':
                pts = [(center_x + 12*math.cos(i*45*math.pi/180-22.5*math.pi/180),
                       center_y + 12*math.sin(i*45*math.pi/180-22.5*math.pi/180)) for i in range(8)]
                pygame.draw.polygon(screen, color, pts)

            y += 64

selected_tower_type = None
selected_tower = None

def main():
    global selected_tower_type, selected_tower
    game = Game()
    running = True

    while running:
        mx, my = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if game.game_state == 'preparing':
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
                                    selected_tower = None
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
                            selected_tower = clicked
                            selected_tower_type = None
                        elif selected_tower_type and game.can_place_tower(gx, gy):
                            cfg = TOWER_CONFIG[selected_tower_type]
                            if game.gold >= cfg['cost']:
                                game.gold -= cfg['cost']
                                game.towers.append(DetailedTower(gx, gy, selected_tower_type))
                                selected_tower_type = None
                elif game.game_state in ['victory', 'defeat']:
                    game = Game()

        game.update()
        game.draw()
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
