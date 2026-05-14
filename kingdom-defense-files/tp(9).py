"""
王国防线 - Kingdom Defense
融合 tab.py 核心玩法与 ty.py 美术设计的塔防游戏
支持中文字体显示
"""

import pygame
import math
import random
import sys
import os
from enum import Enum

try:
    from tp_intro import IntroSequence
    INTRO_AVAILABLE = True
except ImportError:
    INTRO_AVAILABLE = False

pygame.init()

def get_chinese_font(size):
    font_dirs = [
        os.path.join(os.environ.get('WINDIR', 'C:\\Windows'), 'Fonts'),
        os.path.join(os.path.dirname(__file__), 'fonts'),
        '.'
    ]
    font_files = ["msyh.ttc", "simhei.ttf", "simsun.ttc", "msyhbd.ttc", "simkai.ttf", None]
    for font_dir in font_dirs:
        for font_file in font_files[:-1]:
            font_path = os.path.join(font_dir, font_file)
            if os.path.exists(font_path):
                try:
                    return pygame.font.Font(font_path, size)
                except:
                    continue
    return pygame.font.Font(None, size)

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60
GRID_SIZE = 40

COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_GRAY = (128, 128, 128)
COLOR_DARK_GRAY = (64, 64, 64)
COLOR_LIGHT_GRAY = (192, 192, 192)
COLOR_RED = (200, 50, 50)
COLOR_DARK_RED = (139, 0, 0)
COLOR_GREEN = (50, 180, 50)
COLOR_DARK_GREEN = (34, 139, 34)
COLOR_LIGHT_GREEN = (144, 238, 144)
COLOR_BLUE = (70, 130, 180)
COLOR_DARK_BLUE = (25, 25, 112)
COLOR_LIGHT_BLUE = (173, 216, 230)
COLOR_YELLOW = (255, 215, 0)
COLOR_GOLD = (255, 165, 0)
COLOR_ORANGE = (255, 140, 0)
COLOR_PURPLE = (128, 0, 128)
COLOR_DARK_PURPLE = (75, 0, 130)
COLOR_CYAN = (0, 255, 255)
COLOR_BROWN = (139, 69, 19)
COLOR_DARK_BROWN = (101, 67, 33)
COLOR_SKIN = (255, 220, 180)
COLOR_PINK = (255, 182, 193)

MAP_THEME_FOREST = {
    'sky_top': (70, 130, 90), 'sky_bottom': (120, 180, 140),
    'ground': (85, 145, 75), 'ground_alt': (95, 155, 85),
    'path': (160, 140, 110), 'path_border': (120, 100, 80),
    'name': '精灵森林'
}
MAP_THEME_ICE = {
    'sky_top': (135, 206, 235), 'sky_bottom': (200, 230, 250),
    'ground': (200, 220, 240), 'ground_alt': (180, 210, 235),
    'path': (160, 190, 220), 'path_border': (120, 160, 200),
    'name': '冰封山脉'
}
MAP_THEME_CASTLE = {
    'sky_top': (100, 120, 150), 'sky_bottom': (150, 170, 200),
    'ground': (120, 130, 140), 'ground_alt': (110, 120, 130),
    'path': (180, 170, 160), 'path_border': (140, 130, 120),
    'name': '王国城堡'
}
MAP_THEME_DESERT = {
    'sky_top': (255, 180, 80), 'sky_bottom': (255, 220, 150),
    'ground': (210, 180, 120), 'ground_alt': (200, 170, 110),
    'path': (190, 160, 100), 'path_border': (160, 130, 80),
    'name': '灼热沙漠'
}
MAP_THEME_VOLCANO = {
    'sky_top': (80, 30, 30), 'sky_bottom': (140, 60, 40),
    'ground': (60, 50, 45), 'ground_alt': (70, 55, 50),
    'path': (100, 80, 60), 'path_border': (80, 60, 40),
    'name': '火山熔岩'
}
MAP_THEME_SHADOW = {
    'sky_top': (30, 20, 50), 'sky_bottom': (60, 40, 80),
    'ground': (50, 40, 60), 'ground_alt': (45, 35, 55),
    'path': (80, 70, 100), 'path_border': (60, 50, 80),
    'name': '暗影之地'
}
MAP_THEME_CAVE = {
    'sky_top': (20, 20, 25), 'sky_bottom': (30, 30, 40),
    'ground': (60, 55, 50), 'ground_alt': (50, 45, 40),
    'path': (90, 85, 75), 'path_border': (70, 65, 55),
    'name': '幽暗洞穴'
}
MAP_THEME_OCEAN = {
    'sky_top': (30, 80, 130), 'sky_bottom': (50, 120, 180),
    'ground': (40, 100, 160), 'ground_alt': (30, 80, 140),
    'path': (180, 200, 220), 'path_border': (140, 160, 180),
    'name': '深海遗迹'
}
MAP_THEME_SKY = {
    'sky_top': (100, 150, 200), 'sky_bottom': (150, 180, 220),
    'ground': (180, 200, 230), 'ground_alt': (160, 180, 210),
    'path': (200, 210, 220), 'path_border': (160, 170, 180),
    'name': '天空之城'
}
MAP_THEME_SWAMP = {
    'sky_top': (60, 70, 50), 'sky_bottom': (80, 90, 70),
    'ground': (50, 60, 40), 'ground_alt': (40, 50, 30),
    'path': (80, 90, 60), 'path_border': (60, 70, 40),
    'name': '迷雾沼泽'
}
MAP_THEME_JUNGLE = {
    'sky_top': (50, 100, 80), 'sky_bottom': (80, 140, 110),
    'ground': (40, 80, 50), 'ground_alt': (30, 60, 40),
    'path': (100, 120, 80), 'path_border': (80, 100, 60),
    'name': '丛林秘境'
}


class GameState(Enum):
    MENU = 1
    LEVEL_SELECT = 2
    GAME = 3
    PLAYING = 3
    PAUSE = 4
    WAVE_COMPLETE = 5
    GAME_OVER = 6
    VICTORY = 7
    TOWER_INTRO = 8
    ENEMY_INTRO = 9
    TOWER_DETAIL = 10
    ENEMY_DETAIL = 11
    TOWER_ENCYCLOPEDIA = 12
    ENEMY_ENCYCLOPEDIA = 13
    MONSTER_ENCYCLOPEDIA = 14
    BOSS_ENCYCLOPEDIA = 15
    ACHIEVEMENTS = 16


class TowerType(Enum):
    ARCHER = 1
    CANNON = 2
    ICE = 3
    LIGHTNING = 4
    MAGE = 5


class EnemyType(Enum):
    GOBLIN = 1
    SKELETON = 2
    ORC = 3
    SHADOW_WOLF = 4
    TROLL = 5
    OGRE_MAGE = 6
    NECROMANCER = 7
    DARK_KNIGHT = 8
    DEMON = 9
    DRAGON_WHELP = 10
    WIZNAN = 11


class Particle:
    def __init__(self, x, y, vx, vy, color, size, lifetime, gravity=0.0, shape='circle'):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.color = color
        self.size = size
        self.max_lifetime = lifetime
        self.lifetime = lifetime
        self.gravity = gravity
        self.shape = shape
        self.alive = True

    def update(self, dt):
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.vy += self.gravity * dt
        self.lifetime -= dt
        if self.lifetime <= 0:
            self.alive = False

    def draw(self, screen):
        if not self.alive:
            return
        alpha = max(0, self.lifetime / self.max_lifetime)
        sz = max(0.5, self.size * alpha)
        if self.shape == 'circle':
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), int(sz))
        elif self.shape == 'square':
            r = pygame.Rect(int(self.x - sz/2), int(self.y - sz/2), int(sz), int(sz))
            pygame.draw.rect(screen, self.color, r)
        elif self.shape == 'star':
            pts = []
            for i in range(5):
                a = math.pi * 2 * i / 5 - math.pi / 2
                pts.append((self.x + math.cos(a) * sz, self.y + math.sin(a) * sz))
                a += math.pi / 5
                pts.append((self.x + math.cos(a) * sz * 0.4, self.y + math.sin(a) * sz * 0.4))
            pts = [(int(p[0]), int(p[1])) for p in pts]
            pygame.draw.polygon(screen, self.color, pts)
        elif self.shape == 'triangle':
            pts = [
                (self.x, self.y - sz),
                (self.x - sz * 0.866, self.y + sz * 0.5),
                (self.x + sz * 0.866, self.y + sz * 0.5)
            ]


class ParticleSystem:
    def __init__(self):
        self.particles = []

    def add_particle(self, x, y, color, count=10, speed=3):
        for _ in range(count):
            angle = random.uniform(0, math.pi * 2)
            vx = math.cos(angle) * random.uniform(0, speed)
            vy = math.sin(angle) * random.uniform(0, speed)
            self.particles.append(Particle(x, y, vx, vy, color, random.uniform(0.5, 1.5), random.uniform(3, 6)))

    def add_explosion(self, x, y, color=(255, 100, 50), count=20):
        for _ in range(count):
            angle = random.uniform(0, math.pi * 2)
            speed = random.uniform(2, 6)
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed
            self.particles.append(Particle(x, y, vx, vy, color, random.uniform(0.3, 1.0), random.uniform(4, 8)))

    def add_magic_circle(self, x, y, color=(150, 100, 200)):
        for i in range(36):
            angle = i * math.pi * 2 / 36
            vx = math.cos(angle) * 1.5
            vy = math.sin(angle) * 1.5
            self.particles.append(Particle(x, y, vx, vy, color, 2.0, random.uniform(2, 4)))

    def add_trail(self, x, y, color=(255, 200, 100), count=3):
        for _ in range(count):
            self.particles.append(Particle(x, y, random.uniform(-1, 1), random.uniform(-1, 1), color, 0.5, random.uniform(2, 4)))

    def update(self, dt):
        self.particles = [p for p in self.particles if p.alive]
        for p in self.particles:
            p.update(dt)

    def draw(self, screen):
        for p in self.particles:
            p.draw(screen)


class Projectile:
    def __init__(self, x, y, target_x, target_y, damage, type_, splash=False, burn=False, slow=False, chain=False, pierce=False, slow_factor=0.7):
        self.x = x
        self.y = y
        self.target_x = target_x
        self.target_y = target_y
        self.damage = damage
        self.type = type_
        self.splash = splash
        self.burn = burn
        self.slow = slow
        self.chain = chain
        self.pierce = pierce
        self.slow_factor = slow_factor
        self.speed = 8
        self.active = True
        self.anim_timer = 0

        dx = target_x - x
        dy = target_y - y
        dist = math.hypot(dx, dy)
        if dist > 0:
            self.vx = (dx / dist) * self.speed
            self.vy = (dy / dist) * self.speed
        else:
            self.vx = 0
            self.vy = 0

    def update(self, enemies):
        self.x += self.vx
        self.y += self.vy
        self.anim_timer += 0.1

        for enemy in enemies:
            if enemy.alive:
                dist = math.hypot(self.x - enemy.x, self.y - enemy.y)
                if dist < 15:
                    enemy.take_damage(self.damage)
                    if self.slow:
                        enemy.apply_slow(self.slow_factor, 2.0)
                    if self.burn:
                        enemy.apply_burn(self.damage * 0.3, 3.0)
                    self.active = False
                    break

    def draw(self, screen):
        if not self.active:
            return
        x, y = int(self.x), int(self.y)
        pulse = 1 + math.sin(self.anim_timer * 8) * 0.2

        if self.type == "arrow":
            angle = math.atan2(self.vy, self.vx)
            px = x - 8 * math.cos(angle)
            py = y - 8 * math.sin(angle)
            pygame.draw.polygon(screen, (100, 150, 220), 
                              [(x, y), 
                               (px - 4 * math.sin(angle), py + 4 * math.cos(angle)), 
                               (px + 4 * math.sin(angle), py - 4 * math.cos(angle))])
            pygame.draw.polygon(screen, (60, 100, 160), 
                              [(px - 3 * math.sin(angle), py + 3 * math.cos(angle)),
                               (px - 12 * math.cos(angle), py - 12 * math.sin(angle)),
                               (px + 3 * math.sin(angle), py - 3 * math.cos(angle))])
            trail_alpha = max(0, min(255, int(150 * (1 - self.anim_timer * 0.1))))
            for i in range(3):
                tx = x - i * self.vx * 0.8
                ty = y - i * self.vy * 0.8
                pygame.draw.circle(screen, (150, 200, 255, trail_alpha), (int(tx), int(ty)), 3 - i)

        elif self.type == "cannonball":
            pygame.draw.circle(screen, (120, 60, 30), (x, y), 12)
            pygame.draw.circle(screen, (180, 100, 60), (x, y), 8)
            pygame.draw.circle(screen, (220, 140, 100), (x, y), 4)
            
            smoke_offset = int(3 * math.sin(self.anim_timer * 10))
            pygame.draw.circle(screen, (100, 100, 100, 80), (x - 8 + smoke_offset, y), 6)
            pygame.draw.circle(screen, (150, 150, 150, 60), (x - 14 + smoke_offset, y - 2), 4)

        elif self.type == "magic":
            glow_pulse = 1 + math.sin(self.anim_timer * 10) * 0.3
            pygame.draw.circle(screen, (180, 100, 255), (x, y), int(8 * glow_pulse))
            pygame.draw.circle(screen, (220, 150, 255), (x, y), int(5 * glow_pulse))
            pygame.draw.circle(screen, (255, 200, 255), (x, y), int(3 * glow_pulse))
            
            for i in range(6):
                ring_angle = i * 60 + self.anim_timer * 50
                ring_radius = 12 + i * 3
                rx = x + int(ring_radius * math.cos(math.radians(ring_angle)))
                ry = y + int(ring_radius * math.sin(math.radians(ring_angle)))
                pygame.draw.circle(screen, (200, 150, 255, 100), (rx, ry), 2)

        elif self.type == "flame":
            fire_pulse = 1 + math.sin(self.anim_timer * 12) * 0.4
            pygame.draw.circle(screen, COLOR_RED, (x, y), int(10 * fire_pulse))
            pygame.draw.circle(screen, COLOR_ORANGE, (x, y), int(7 * fire_pulse))
            pygame.draw.circle(screen, COLOR_YELLOW, (x, y), int(4 * fire_pulse))
            
            for i in range(5):
                flame_angle = i * 72 + self.anim_timer * 80
                flame_length = 12 + int(4 * math.sin(self.anim_timer * 10 + i))
                fx = x + int(flame_length * math.cos(math.radians(flame_angle)))
                fy = y + int(flame_length * math.sin(math.radians(flame_angle)))
                pygame.draw.line(screen, (255, 150, 50, 100), (x, y), (fx, fy), 3)

        elif self.type == "ice":
            ice_glow = 1 + math.sin(self.anim_timer * 8) * 0.2
            pygame.draw.circle(screen, (80, 180, 230), (x, y), int(8 * ice_glow))
            pygame.draw.circle(screen, (120, 220, 255), (x, y), int(5 * ice_glow))
            pygame.draw.circle(screen, COLOR_WHITE, (x, y), int(3 * ice_glow))
            
            for i in range(4):
                spike_angle = i * 90 + self.anim_timer * 60
                spike_length = 8 + int(3 * math.sin(self.anim_timer * 12))
                sx = x + int(spike_length * math.cos(math.radians(spike_angle)))
                sy = y + int(spike_length * math.sin(math.radians(spike_angle)))
                pygame.draw.line(screen, (150, 230, 255), (x, y), (sx, sy), 2)

        elif self.type == "lightning":
            branch_count = 3
            for i in range(branch_count):
                branch_offset = (i - 1) * 0.3
                start_x = x - self.vx * branch_offset
                start_y = y - self.vy * branch_offset
                end_x = start_x - self.vx * (1 - branch_offset)
                end_y = start_y - self.vy * (1 - branch_offset)
                
                zig_zag_count = 5
                points = [(start_x, start_y)]
                current_x, current_y = start_x, start_y
                segment_length = math.hypot(end_x - start_x, end_y - start_y) / zig_zag_count
                angle = math.atan2(end_y - start_y, end_x - start_x)
                
                for j in range(zig_zag_count):
                    current_x += math.cos(angle) * segment_length
                    current_y += math.sin(angle) * segment_length
                    current_x += (random.random() - 0.5) * 8
                    current_y += (random.random() - 0.5) * 8
                    points.append((current_x, current_y))
                
                points.append((end_x, end_y))
                pygame.draw.lines(screen, COLOR_YELLOW, False, points, 3)
                pygame.draw.lines(screen, COLOR_WHITE, False, points, 1)

        elif self.type == "slow":
            pygame.draw.circle(screen, (100, 100, 120), (x, y), 8)
            pygame.draw.circle(screen, (150, 150, 180), (x, y), 5)
            pygame.draw.circle(screen, COLOR_WHITE, (x, y), 8, 2)
            
            for i in range(8):
                orb_angle = i * 45 + self.anim_timer * 30
                orb_radius = 10 + int(3 * math.sin(self.anim_timer * 6))
                ox = x + int(orb_radius * math.cos(math.radians(orb_angle)))
                oy = y + int(orb_radius * math.sin(math.radians(orb_angle)))
                pygame.draw.circle(screen, (150, 150, 200, 80), (ox, oy), 2)

        elif self.type == "sniper":
            scope_angle = math.atan2(self.vy, self.vx)
            scope_length = 50
            
            pygame.draw.line(screen, (200, 200, 200, 50), 
                           (x - scope_length * math.cos(scope_angle), 
                            y - scope_length * math.sin(scope_angle)),
                           (x + scope_length * math.cos(scope_angle), 
                            y + scope_length * math.sin(scope_angle)), 1)
            
            for i in range(3):
                cross_dist = 15 + i * 12
                cx1 = x - cross_dist * math.cos(scope_angle) - 5 * math.sin(scope_angle)
                cy1 = y - cross_dist * math.sin(scope_angle) + 5 * math.cos(scope_angle)
                cx2 = x - cross_dist * math.cos(scope_angle) + 5 * math.sin(scope_angle)
                cy2 = y - cross_dist * math.sin(scope_angle) - 5 * math.cos(scope_angle)
                pygame.draw.line(screen, (150, 150, 150, 80), (cx1, cy1), (cx2, cy2), 1)
            
            pygame.draw.circle(screen, (100, 150, 200), (x, y), 6)
            pygame.draw.circle(screen, COLOR_WHITE, (x, y), 3)

        elif self.type == "archer":
            arrow_angle = math.atan2(self.vy, self.vx)
            arrow_length = 15
            
            pygame.draw.line(screen, (80, 140, 220), (x, y), 
                           (x - arrow_length * math.cos(arrow_angle), 
                            y - arrow_length * math.sin(arrow_angle)), 3)
            
            tail_length = 8
            pygame.draw.polygon(screen, (60, 100, 180), 
                              [(x, y),
                               (x + tail_length * math.cos(arrow_angle) - 4 * math.sin(arrow_angle),
                                y + tail_length * math.sin(arrow_angle) + 4 * math.cos(arrow_angle)),
                               (x + tail_length * math.cos(arrow_angle) + 4 * math.sin(arrow_angle),
                                y + tail_length * math.sin(arrow_angle) - 4 * math.cos(arrow_angle))])
            
            for i in range(4):
                spark_x = x - i * self.vx * 1.5
                spark_y = y - i * self.vy * 1.5
                pygame.draw.circle(screen, (150, 200, 255, 100), (int(spark_x), int(spark_y)), 2)

        elif self.type == "cannon":
            pygame.draw.circle(screen, (150, 80, 40), (x, y), 12)
            pygame.draw.circle(screen, (200, 120, 70), (x, y), 8)
            pygame.draw.circle(screen, (230, 150, 100), (x, y), 4)
            
            for i in range(3):
                smoke_x = x - (i + 1) * 8 + int(3 * math.sin(self.anim_timer * 8 + i))
                smoke_y = y + int(2 * math.sin(self.anim_timer * 10 + i))
                pygame.draw.circle(screen, (100, 100, 100, 60 - i * 15), (smoke_x, smoke_y), 4 + i)

        elif self.type == "mage":
            magic_pulse = 1 + math.sin(self.anim_timer * 8) * 0.25
            pygame.draw.circle(screen, (150, 80, 200), (x, y), int(10 * magic_pulse))
            pygame.draw.circle(screen, (180, 120, 230), (x, y), int(6 * magic_pulse))
            pygame.draw.circle(screen, (220, 180, 255), (x, y), int(3 * magic_pulse))
            
            rune_count = 6
            for i in range(rune_count):
                rune_angle = i * 60 + self.anim_timer * 30
                rune_radius = 15 + int(5 * math.sin(self.anim_timer * 4))
                rune_x = x + int(rune_radius * math.cos(math.radians(rune_angle)))
                rune_y = y + int(rune_radius * math.sin(math.radians(rune_angle)))
                pygame.draw.polygon(screen, (200, 150, 255, 80), 
                                  [(rune_x, rune_y - 4), 
                                   (rune_x - 3, rune_y + 2), 
                                   (rune_x + 3, rune_y + 2)])

        else:
            pygame.draw.circle(screen, COLOR_WHITE, (x, y), 5)
            pygame.draw.circle(screen, COLOR_GRAY, (x, y), 3)


class HomingProjectile(Projectile):
    def __init__(self, x, y, target, damage, type_):
        super().__init__(x, y, target.x, target.y, damage, type_)
        self.target = target
        self.speed = 12
        self.homing_strength = 0.15
        
        dx = target.x - x
        dy = target.y - y
        dist = math.hypot(dx, dy)
        if dist > 0:
            self.vx = (dx / dist) * self.speed
            self.vy = (dy / dist) * self.speed
        else:
            self.vx = 0
            self.vy = 0

    def update(self, enemies):
        if self.target and self.target.alive:
            dx = self.target.x - self.x
            dy = self.target.y - self.y
            dist = math.hypot(dx, dy)
            if dist > 0:
                desired_vx = (dx / dist) * self.speed
                desired_vy = (dy / dist) * self.speed
                self.vx += (desired_vx - self.vx) * self.homing_strength
                self.vy += (desired_vy - self.vy) * self.homing_strength
                
                current_speed = math.hypot(self.vx, self.vy)
                if current_speed > 0:
                    self.vx = (self.vx / current_speed) * self.speed
                    self.vy = (self.vy / current_speed) * self.speed
        
        self.x += self.vx
        self.y += self.vy
        self.anim_timer += 0.1
        
        for enemy in enemies:
            if enemy.alive:
                dist = math.hypot(self.x - enemy.x, self.y - enemy.y)
                if dist < 12:
                    enemy.take_damage(self.damage)
                    self.active = False
                    break


class SpreadProjectile(Projectile):
    def __init__(self, x, y, target_x, target_y, damage, spread_count, spread_angle):
        super().__init__(x, y, target_x, target_y, damage, 'spread')
        self.spread_count = spread_count
        self.spread_angle = spread_angle
        self.speed = 10
        self.active_projectiles = []
        
        base_angle = math.atan2(target_y - y, target_x - x)
        for i in range(spread_count):
            angle_offset = (i - (spread_count - 1) / 2) * spread_angle
            angle = base_angle + angle_offset
            proj = Projectile(x, y, 
                            x + math.cos(angle) * 1000,
                            y + math.sin(angle) * 1000,
                            damage, 'arrow')
            proj.vx = math.cos(angle) * self.speed
            proj.vy = math.sin(angle) * self.speed
            self.active_projectiles.append(proj)

    def update(self, enemies):
        all_inactive = True
        for proj in self.active_projectiles:
            if proj.active:
                proj.update(enemies)
                all_inactive = False
        if all_inactive:
            self.active = False

    def draw(self, screen):
        for proj in self.active_projectiles:
            proj.draw(screen)


class CircularProjectile(Projectile):
    def __init__(self, x, y, damage, radius, speed, count):
        super().__init__(x, y, x + 1, y, damage, 'circular')
        self.radius = radius
        self.speed = speed
        self.count = count
        self.active_projectiles = []
        self.angle = 0
        
        for i in range(count):
            angle = i * (360 / count)
            proj = Projectile(x, y,
                            x + math.cos(math.radians(angle)) * 500,
                            y + math.sin(math.radians(angle)) * 500,
                            damage, 'energy')
            proj.vx = math.cos(math.radians(angle)) * speed
            proj.vy = math.sin(math.radians(angle)) * speed
            self.active_projectiles.append(proj)

    def update(self, enemies):
        self.angle += self.speed * 0.1
        
        all_inactive = True
        for i, proj in enumerate(self.active_projectiles):
            if proj.active:
                proj.update(enemies)
                all_inactive = False
        if all_inactive:
            self.active = False

    def draw(self, screen):
        for proj in self.active_projectiles:
            proj.draw(screen)


class SpiralProjectile(Projectile):
    def __init__(self, x, y, damage, speed, count):
        super().__init__(x, y, x + 1, y, damage, 'spiral')
        self.speed = speed
        self.count = count
        self.active_projectiles = []
        self.angle = 0
        self.angle_increment = 360 / count
        self.spawn_timer = 0
        self.spawn_interval = 0.1

    def update(self, enemies):
        self.spawn_timer += 0.016
        
        if self.spawn_timer >= self.spawn_interval and len(self.active_projectiles) < self.count:
            angle = math.radians(self.angle)
            proj = Projectile(self.x, self.y,
                            self.x + math.cos(angle) * 500,
                            self.y + math.sin(angle) * 500,
                            self.damage, 'magic')
            proj.vx = math.cos(angle) * self.speed
            proj.vy = math.sin(angle) * self.speed
            self.active_projectiles.append(proj)
            self.angle += self.angle_increment
            self.spawn_timer = 0
        
        all_inactive = True
        for proj in self.active_projectiles:
            if proj.active:
                proj.update(enemies)
                all_inactive = False
        if all_inactive and len(self.active_projectiles) >= self.count:
            self.active = False

    def draw(self, screen):
        for proj in self.active_projectiles:
            proj.draw(screen)


class WaveProjectile(Projectile):
    def __init__(self, x, y, target_x, target_y, damage, amplitude, frequency):
        super().__init__(x, y, target_x, target_y, damage, 'wave')
        self.amplitude = amplitude
        self.frequency = frequency
        self.speed = 8
        self.progress = 0
        
        dx = target_x - x
        dy = target_y - y
        dist = math.hypot(dx, dy)
        if dist > 0:
            self.base_vx = (dx / dist) * self.speed
            self.base_vy = (dy / dist) * self.speed
            self.perp_x = -self.base_vy / self.speed * self.amplitude
            self.perp_y = self.base_vx / self.speed * self.amplitude
        else:
            self.base_vx = 0
            self.base_vy = 0
            self.perp_x = 0
            self.perp_y = 0

    def update(self, enemies):
        self.progress += 0.1
        
        wave_offset = math.sin(self.progress * self.frequency)
        self.x += self.base_vx
        self.y += self.base_vy
        self.x += self.perp_x * wave_offset * 0.5
        self.y += self.perp_y * wave_offset * 0.5
        
        for enemy in enemies:
            if enemy.alive:
                dist = math.hypot(self.x - enemy.x, self.y - enemy.y)
                if dist < 15:
                    enemy.take_damage(self.damage)
                    self.active = False
                    break

    def draw(self, screen):
        if not self.active:
            return
        x, y = int(self.x), int(self.y)
        
        wave_pulse = 1 + math.sin(self.anim_timer * 8) * 0.2
        pygame.draw.circle(screen, (100, 200, 255), (x, y), int(6 * wave_pulse))
        pygame.draw.circle(screen, COLOR_CYAN, (x, y), int(4 * wave_pulse))
        
        for i in range(3):
            trail_x = x - i * self.base_vx * 1.2
            trail_y = y - i * self.base_vy * 1.2
            trail_offset = math.sin((self.progress - i * 0.1) * self.frequency)
            trail_x += self.perp_x * trail_offset * 0.3
            trail_y += self.perp_y * trail_offset * 0.3
            pygame.draw.circle(screen, (150, 220, 255, 100), (int(trail_x), int(trail_y)), 3 - i)


class LaserProjectile(Projectile):
    def __init__(self, x, y, target_x, target_y, damage, duration):
        super().__init__(x, y, target_x, target_y, damage, 'laser')
        self.duration = duration
        self.lifetime = 0
        self.target_x = target_x
        self.target_y = target_y

    def update(self, enemies):
        self.lifetime += 16
        
        if self.lifetime >= self.duration:
            self.active = False
            return
        
        for enemy in enemies:
            if enemy.alive:
                if self.is_point_on_line(self.x, self.y, self.target_x, self.target_y, enemy.x, enemy.y, 20):
                    enemy.take_damage(self.damage * 0.1)

    def is_point_on_line(self, x1, y1, x2, y2, px, py, tolerance):
        dist = abs((y2 - y1) * px - (x2 - x1) * py + x2 * y1 - y2 * x1) / math.hypot(y2 - y1, x2 - x1)
        return dist < tolerance

    def draw(self, screen):
        if not self.active:
            return
        
        alpha = int(255 * (1 - self.lifetime / self.duration))
        pulse = 1 + math.sin(self.lifetime * 0.05) * 0.3
        
        temp_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        pygame.draw.line(temp_surface, (255, 100, 200, alpha), (self.x, self.y), (self.target_x, self.target_y), int(4 * pulse))
        pygame.draw.line(temp_surface, (255, 200, 255, alpha), (self.x, self.y), (self.target_x, self.target_y), int(2 * pulse))
        
        for i in range(5):
            spark_x = self.x + (self.target_x - self.x) * (0.2 + i * 0.15)
            spark_y = self.y + (self.target_y - self.y) * (0.2 + i * 0.15)
            spark_size = 3 + int(2 * math.sin(self.lifetime * 0.1 + i))
            pygame.draw.circle(temp_surface, (255, 255, 255, alpha), (int(spark_x), int(spark_y)), spark_size)
        
        screen.blit(temp_surface, (0, 0))


class CannonballProjectile(Projectile):
    def __init__(self, x, y, target_x, target_y, damage, splash_radius):
        super().__init__(x, y, target_x, target_y, damage, 'cannonball')
        self.speed = 5
        self.splash_radius = splash_radius
        self.hit = False
        self.explosion_frame = 0
        
        dx = target_x - x
        dy = target_y - y
        dist = math.hypot(dx, dy)
        if dist > 0:
            self.vx = (dx / dist) * self.speed
            self.vy = (dy / dist) * self.speed
        else:
            self.vx = 0
            self.vy = 0

    def update(self, enemies):
        if not self.hit:
            self.x += self.vx
            self.y += self.vy
            
            for enemy in enemies:
                if enemy.alive:
                    dist = math.hypot(self.x - enemy.x, self.y - enemy.y)
                    if dist < 20:
                        self.hit = True
                        break
        else:
            self.explosion_frame += 1
            if self.explosion_frame > 30:
                for enemy in enemies:
                    if enemy.alive:
                        dist = math.hypot(self.x - enemy.x, self.y - enemy.y)
                        if dist <= self.splash_radius:
                            enemy.take_damage(self.damage * (1 - dist / self.splash_radius * 0.5))
                self.active = False

    def draw(self, screen):
        if not self.active:
            return
        x, y = int(self.x), int(self.y)
        
        if self.hit:
            explosion_pulse = 1 + self.explosion_frame * 0.1
            pygame.draw.circle(screen, (255, 100, 50), (x, y), int(self.splash_radius * explosion_pulse * 0.5), 2)
            pygame.draw.circle(screen, (255, 150, 100), (x, y), int(self.splash_radius * explosion_pulse * 0.3), 1)
            
            for i in range(8):
                spark_angle = i * 45 + self.explosion_frame * 10
                spark_distance = 20 + self.explosion_frame * 2
                spark_x = x + int(spark_distance * math.cos(math.radians(spark_angle)))
                spark_y = y + int(spark_distance * math.sin(math.radians(spark_angle)))
                pygame.draw.circle(screen, (255, 200, 100), (spark_x, spark_y), 3)
        else:
            pygame.draw.circle(screen, (120, 60, 30), (x, y), 12)
            pygame.draw.circle(screen, (180, 100, 60), (x, y), 8)
            pygame.draw.circle(screen, (220, 140, 100), (x, y), 4)
            
            smoke_offset = int(3 * math.sin(self.anim_timer * 10))
            pygame.draw.circle(screen, (100, 100, 100, 80), (x - 8 + smoke_offset, y), 6)
            pygame.draw.circle(screen, (150, 150, 150, 60), (x - 14 + smoke_offset, y - 2), 4)


class HomingMissileProjectile(HomingProjectile):
    def __init__(self, x, y, target, damage, splash_radius):
        super().__init__(x, y, target, damage, 'missile')
        self.splash_radius = splash_radius
        self.hit = False

    def update(self, enemies):
        if not self.hit:
            super().update([])
            
            for enemy in enemies:
                if enemy.alive:
                    dist = math.hypot(self.x - enemy.x, self.y - enemy.y)
                    if dist < 15:
                        self.hit = True
                        break
        else:
            for enemy in enemies:
                if enemy.alive:
                    dist = math.hypot(self.x - enemy.x, self.y - enemy.y)
                    if dist <= self.splash_radius:
                        enemy.take_damage(self.damage * (1 - dist / self.splash_radius * 0.3))
            self.active = False

    def draw(self, screen):
        if not self.active:
            return
        x, y = int(self.x), int(self.y)
        
        if self.hit:
            pygame.draw.circle(screen, (255, 100, 50), (x, y), int(self.splash_radius), 2)
        else:
            missile_angle = math.atan2(self.vy, self.vx)
            pygame.draw.rect(screen, (80, 80, 100), 
                           (x - 5, y - 15, 10, 22), 2)
            pygame.draw.polygon(screen, (120, 120, 140), 
                              [(x, y + 7), (x - 4, y - 3), (x + 4, y - 3)])
            
            flame_length = 8 + int(4 * math.sin(self.anim_timer * 15))
            fx = x - flame_length * math.cos(missile_angle)
            fy = y - flame_length * math.sin(missile_angle)
            pygame.draw.polygon(screen, COLOR_ORANGE, 
                              [(x - 3 * math.cos(missile_angle), y - 3 * math.sin(missile_angle)),
                               (fx - 2 * math.sin(missile_angle), fy + 2 * math.cos(missile_angle)),
                               (fx, fy),
                               (fx + 2 * math.sin(missile_angle), fy - 2 * math.cos(missile_angle))])


class BouncingProjectile(Projectile):
    def __init__(self, x, y, target_x, target_y, damage, bounce_count):
        super().__init__(x, y, target_x, target_y, damage, 'bounce')
        self.speed = 12
        self.bounce_count = bounce_count
        self.bounces_remaining = bounce_count
        self.last_target = None
        
        dx = target_x - x
        dy = target_y - y
        dist = math.hypot(dx, dy)
        if dist > 0:
            self.vx = (dx / dist) * self.speed
            self.vy = (dy / dist) * self.speed
        else:
            self.vx = 0
            self.vy = 0

    def update(self, enemies):
        self.x += self.vx
        self.y += self.vy
        self.anim_timer += 0.1
        
        if self.bounces_remaining <= 0:
            self.active = False
            return
        
        for enemy in enemies:
            if enemy.alive and enemy != self.last_target:
                dist = math.hypot(self.x - enemy.x, self.y - enemy.y)
                if dist < 15:
                    enemy.take_damage(self.damage)
                    self.last_target = enemy
                    self.bounces_remaining -= 1
                    
                    if self.bounces_remaining > 0:
                        closest_enemy = None
                        closest_dist = float('inf')
                        for other_enemy in enemies:
                            if other_enemy.alive and other_enemy != enemy:
                                d = math.hypot(enemy.x - other_enemy.x, enemy.y - other_enemy.y)
                                if d < closest_dist:
                                    closest_dist = d
                                    closest_enemy = other_enemy
                        
                        if closest_enemy:
                            dx = closest_enemy.x - self.x
                            dy = closest_enemy.y - self.y
                            dist = math.hypot(dx, dy)
                            if dist > 0:
                                self.vx = (dx / dist) * self.speed
                                self.vy = (dy / dist) * self.speed
                    break

    def draw(self, screen):
        if not self.active:
            return
        x, y = int(self.x), int(self.y)
        
        bounce_pulse = 1 + math.sin(self.anim_timer * 12) * 0.2
        pygame.draw.circle(screen, (200, 150, 255), (x, y), int(7 * bounce_pulse))
        pygame.draw.circle(screen, (230, 180, 255), (x, y), int(4 * bounce_pulse))
        
        for i in range(3):
            trail_x = x - i * self.vx * 0.6
            trail_y = y - i * self.vy * 0.6
            pygame.draw.circle(screen, (180, 120, 255, 80), (int(trail_x), int(trail_y)), 3 - i)


class SplitProjectile(Projectile):
    def __init__(self, x, y, target_x, target_y, damage, split_count, split_angle):
        super().__init__(x, y, target_x, target_y, damage, 'split')
        self.split_count = split_count
        self.split_angle = split_angle
        self.speed = 10
        self.split_done = False
        self.split_distance = 100
        self.traveled = 0
        
        dx = target_x - x
        dy = target_y - y
        dist = math.hypot(dx, dy)
        if dist > 0:
            self.vx = (dx / dist) * self.speed
            self.vy = (dy / dist) * self.speed
        else:
            self.vx = 0
            self.vy = 0
        
        self.base_angle = math.atan2(dy, dx)

    def update(self, enemies):
        if not self.split_done:
            self.x += self.vx
            self.y += self.vy
            self.traveled += self.speed
            
            if self.traveled >= self.split_distance:
                self.split_done = True
                
                for enemy in enemies:
                    if enemy.alive:
                        dist = math.hypot(self.x - enemy.x, self.y - enemy.y)
                        if dist < 15:
                            enemy.take_damage(self.damage)
        else:
            self.active = False

    def draw(self, screen):
        if not self.active:
            return
        x, y = int(self.x), int(self.y)
        
        if not self.split_done:
            pygame.draw.circle(screen, (150, 200, 255), (x, y), 6)
            pygame.draw.circle(screen, COLOR_CYAN, (x, y), 3)
        else:
            for i in range(self.split_count):
                angle_offset = (i - (self.split_count - 1) / 2) * self.split_angle
                angle = self.base_angle + angle_offset
                for j in range(10):
                    px = x + j * 5 * math.cos(angle)
                    py = y + j * 5 * math.sin(angle)
                    alpha = int(255 * (1 - j / 10))
                    pygame.draw.circle(screen, (100, 200, 255, alpha), (int(px), int(py)), 4 - j // 3)


class FireballProjectile(CannonballProjectile):
    def __init__(self, x, y, target_x, target_y, damage, splash_radius):
        super().__init__(x, y, target_x, target_y, damage, splash_radius)
        self.burn_damage = damage * 0.2
        self.burn_duration = 2.0
        self.trail_particles = []

    def update(self, enemies):
        if not self.hit:
            self.x += self.vx
            self.y += self.vy
            
            self.trail_particles.append((self.x, self.y, self.anim_timer))
            if len(self.trail_particles) > 10:
                self.trail_particles.pop(0)
            
            for enemy in enemies:
                if enemy.alive:
                    dist = math.hypot(self.x - enemy.x, self.y - enemy.y)
                    if dist < 20:
                        self.hit = True
                        break
        else:
            for enemy in enemies:
                if enemy.alive:
                    dist = math.hypot(self.x - enemy.x, self.y - enemy.y)
                    if dist <= self.splash_radius:
                        enemy.take_damage(self.damage * (1 - dist / self.splash_radius * 0.4))
                        enemy.apply_burn(self.burn_damage, self.burn_duration)
            self.active = False

    def draw(self, screen):
        if not self.active:
            return
        x, y = int(self.x), int(self.y)
        
        if self.hit:
            explosion_pulse = 1 + self.anim_timer * 0.5
            pygame.draw.circle(screen, (255, 50, 0), (x, y), int(self.splash_radius * explosion_pulse * 0.8), 2)
            pygame.draw.circle(screen, (255, 100, 0), (x, y), int(self.splash_radius * explosion_pulse * 0.5), 1)
            pygame.draw.circle(screen, (255, 150, 50), (x, y), int(self.splash_radius * explosion_pulse * 0.3))
            
            for i in range(12):
                spark_angle = i * 30 + self.anim_timer * 100
                spark_distance = 15 + int(20 * math.sin(self.anim_timer * 20 + i))
                spark_x = x + int(spark_distance * math.cos(math.radians(spark_angle)))
                spark_y = y + int(spark_distance * math.sin(math.radians(spark_angle)))
                pygame.draw.circle(screen, (255, 200, 100), (spark_x, spark_y), 3)
        else:
            flicker = int(3 * math.sin(self.anim_timer * 10))
            pygame.draw.circle(screen, (255, 80, 0), (x, y), 10 + flicker)
            pygame.draw.circle(screen, (255, 150, 50), (x, y), 6 + flicker)
            pygame.draw.circle(screen, (255, 200, 100), (x, y), 3)
            
            for i, (tx, ty, t) in enumerate(self.trail_particles):
                alpha = int(100 * (i / len(self.trail_particles)))
                size = 4 - i // 3
                pygame.draw.circle(screen, (255, 100, 50, alpha), (int(tx), int(ty)), size)


class IceProjectile(Projectile):
    def __init__(self, x, y, target_x, target_y, damage, slow_factor, slow_duration):
        super().__init__(x, y, target_x, target_y, damage, 'ice')
        self.speed = 9
        self.slow_factor = slow_factor
        self.slow_duration = slow_duration
        self.slow_stack = 0
        
        dx = target_x - x
        dy = target_y - y
        dist = math.hypot(dx, dy)
        if dist > 0:
            self.vx = (dx / dist) * self.speed
            self.vy = (dy / dist) * self.speed
        else:
            self.vx = 0
            self.vy = 0

    def update(self, enemies):
        self.x += self.vx
        self.y += self.vy
        self.anim_timer += 0.1
        
        for enemy in enemies:
            if enemy.alive:
                dist = math.hypot(self.x - enemy.x, self.y - enemy.y)
                if dist < 12:
                    enemy.take_damage(self.damage)
                    enemy.apply_slow(self.slow_factor, self.slow_duration, stackable=True)
                    self.active = False
                    break

    def draw(self, screen):
        if not self.active:
            return
        x, y = int(self.x), int(self.y)
        
        pygame.draw.circle(screen, (100, 200, 255), (x, y), 6)
        pygame.draw.circle(screen, COLOR_WHITE, (x, y), 3)
        pygame.draw.circle(screen, (150, 230, 255), (x, y), 8, 1)


class BigIceballProjectile(Projectile):
    def __init__(self, x, y, target_x, target_y, damage, splash_radius, freeze_duration, slow_factor):
        super().__init__(x, y, target_x, target_y, damage, 'ice')
        self.speed = 6
        self.splash_radius = splash_radius
        self.freeze_duration = freeze_duration
        self.slow_factor = slow_factor
        self.hit = False
        
        dx = target_x - x
        dy = target_y - y
        dist = math.hypot(dx, dy)
        if dist > 0:
            self.vx = (dx / dist) * self.speed
            self.vy = (dy / dist) * self.speed
        else:
            self.vx = 0
            self.vy = 0

    def update(self, enemies):
        if not self.hit:
            self.x += self.vx
            self.y += self.vy
            
            for enemy in enemies:
                if enemy.alive:
                    dist = math.hypot(self.x - enemy.x, self.y - enemy.y)
                    if dist < 25:
                        self.hit = True
                        break
        else:
            for enemy in enemies:
                if enemy.alive:
                    dist = math.hypot(self.x - enemy.x, self.y - enemy.y)
                    if dist <= self.splash_radius * 0.6:
                        enemy.take_damage(self.damage)
                        enemy.freeze(self.freeze_duration)
                    elif dist <= self.splash_radius:
                        enemy.apply_slow(self.slow_factor, self.freeze_duration * 0.8)
            self.active = False

    def draw(self, screen):
        if not self.active:
            return
        x, y = int(self.x), int(self.y)
        
        if self.hit:
            pygame.draw.circle(screen, (100, 180, 255), (x, y), int(self.splash_radius), 3)
            pygame.draw.circle(screen, (150, 220, 255), (x, y), int(self.splash_radius * 0.6), 2)
            pygame.draw.circle(screen, COLOR_WHITE, (x, y), int(self.splash_radius * 0.3))
        else:
            size = 12 + int(3 * math.sin(self.anim_timer * 5))
            pygame.draw.circle(screen, (100, 200, 255), (x, y), size)
            pygame.draw.circle(screen, (150, 230, 255), (x, y), size - 4)
            pygame.draw.circle(screen, COLOR_WHITE, (x, y), size - 7)


class ChainLightningProjectile(Projectile):
    def __init__(self, x, y, first_target, damage, enemies, chain_count, chain_range):
        super().__init__(x, y, first_target.x, first_target.y, damage, 'lightning')
        self.speed = 15
        self.enemies = enemies
        self.chain_count = chain_count
        self.chain_range = chain_range
        self.current_target = first_target
        self.chained_enemies = []
        self.chain_index = 0
        self.hit = False
        
        dx = first_target.x - x
        dy = first_target.y - y
        dist = math.hypot(dx, dy)
        if dist > 0:
            self.vx = (dx / dist) * self.speed
            self.vy = (dy / dist) * self.speed
        else:
            self.vx = 0
            self.vy = 0

    def update(self, enemies):
        if self.current_target and self.current_target.alive:
            dx = self.current_target.x - self.x
            dy = self.current_target.y - self.y
            dist = math.hypot(dx, dy)
            
            if dist < 15:
                damage = self.damage * (0.7 ** self.chain_index)
                self.current_target.take_damage(damage)
                self.chained_enemies.append(self.current_target)
                self.chain_index += 1
                
                if self.chain_index < self.chain_count:
                    next_target = self.find_next_target()
                    if next_target:
                        self.current_target = next_target
                        dx = next_target.x - self.x
                        dy = next_target.y - self.y
                        dist = math.hypot(dx, dy)
                        if dist > 0:
                            self.vx = (dx / dist) * self.speed
                            self.vy = (dy / dist) * self.speed
                    else:
                        self.active = False
                else:
                    self.active = False
            else:
                self.x += self.vx
                self.y += self.vy
        else:
            self.active = False
        
        self.anim_timer += 0.1

    def find_next_target(self):
        closest = None
        closest_dist = float('inf')
        for enemy in self.enemies:
            if enemy.alive and enemy not in self.chained_enemies:
                dist = math.hypot(self.current_target.x - enemy.x, self.current_target.y - enemy.y)
                if dist <= self.chain_range and dist < closest_dist:
                    closest = enemy
                    closest_dist = dist
        return closest

    def draw(self, screen):
        if not self.active:
            return
        x, y = int(self.x), int(self.y)
        
        if self.current_target and self.current_target.alive:
            tx, ty = int(self.current_target.x), int(self.current_target.y)
            pygame.draw.line(screen, COLOR_YELLOW, (x, y), (tx, ty), 2)
            pygame.draw.line(screen, COLOR_WHITE, (x, y), (tx, ty), 1)
        
        pygame.draw.circle(screen, COLOR_WHITE, (x, y), 5)
        pygame.draw.circle(screen, COLOR_YELLOW, (x, y), 3)


class SkillChainLightning(ChainLightningProjectile):
    def __init__(self, x, y, first_target, damage, enemies, chain_count, chain_range):
        super().__init__(x, y, first_target, damage, enemies, chain_count, chain_range)
        self.speed = 20


class LightningBeamProjectile(Projectile):
    def __init__(self, x, y, first_target, damage, enemies, chain_count, chain_range, duration):
        super().__init__(x, y, first_target.x, first_target.y, damage, 'lightning')
        self.enemies = enemies
        self.chain_count = chain_count
        self.chain_range = chain_range
        self.duration = duration
        self.lifetime = 0
        self.active = True
        
        self.targets = []
        self.find_targets(first_target)

    def find_targets(self, first_target):
        if not first_target or not first_target.alive:
            return
        
        self.targets = [first_target]
        current_target = first_target
        
        for _ in range(self.chain_count - 1):
            closest = None
            closest_dist = float('inf')
            
            for enemy in self.enemies:
                if enemy.alive and enemy not in self.targets:
                    dist = math.hypot(current_target.x - enemy.x, current_target.y - enemy.y)
                    if dist <= self.chain_range and dist < closest_dist:
                        closest = enemy
                        closest_dist = dist
            
            if closest:
                self.targets.append(closest)
                current_target = closest
            else:
                break

    def update(self, enemies):
        self.lifetime += 16
        
        if self.lifetime >= self.duration:
            self.active = False
            return
        
        self.find_targets(self.targets[0] if self.targets else None)
        
        damage_interval = 50
        if self.lifetime % damage_interval < 16:
            for i, target in enumerate(self.targets):
                if target and target.alive:
                    damage = self.damage * (0.8 ** i)
                    target.take_damage(damage)

    def draw(self, screen):
        if not self.active or not self.targets:
            return
        
        x, y = int(self.x), int(self.y)
        
        for i in range(len(self.targets) - 1):
            target1 = self.targets[i]
            target2 = self.targets[i + 1]
            
            if target1 and target1.alive and target2 and target2.alive:
                tx1, ty1 = int(target1.x), int(target1.y)
                tx2, ty2 = int(target2.x), int(target2.y)
                
                flicker = 1 + math.sin(self.lifetime * 0.05) * 0.3
                width = int(3 * flicker)
                
                pygame.draw.line(screen, COLOR_YELLOW, (tx1, ty1), (tx2, ty2), width)
                pygame.draw.line(screen, COLOR_WHITE, (tx1, ty1), (tx2, ty2), int(width * 0.5))
        
        if self.targets[0] and self.targets[0].alive:
            tx, ty = int(self.targets[0].x), int(self.targets[0].y)
            pygame.draw.line(screen, COLOR_YELLOW, (x, y), (tx, ty), 4)
            pygame.draw.line(screen, COLOR_WHITE, (x, y), (tx, ty), 2)
        
        for target in self.targets:
            if target and target.alive:
                px, py = int(target.x), int(target.y)
                pygame.draw.circle(screen, COLOR_WHITE, (px, py), 8)
                pygame.draw.circle(screen, COLOR_YELLOW, (px, py), 4)


class MagicProjectile(Projectile):
    def __init__(self, x, y, target_x, target_y, damage):
        super().__init__(x, y, target_x, target_y, damage, 'magic')
        self.speed = 7
        self.has_buff = True
        
        dx = target_x - x
        dy = target_y - y
        dist = math.hypot(dx, dy)
        if dist > 0:
            self.vx = (dx / dist) * self.speed
            self.vy = (dy / dist) * self.speed
        else:
            self.vx = 0
            self.vy = 0

    def update(self, enemies):
        self.x += self.vx
        self.y += self.vy
        self.anim_timer += 0.1
        
        for enemy in enemies:
            if enemy.alive:
                dist = math.hypot(self.x - enemy.x, self.y - enemy.y)
                if dist < 12:
                    enemy.take_damage(self.damage)
                    enemy.apply_magic_buff()
                    self.active = False
                    break

    def draw(self, screen):
        if not self.active:
            return
        x, y = int(self.x), int(self.y)
        
        pulse = 1 + math.sin(self.anim_timer * 8) * 0.3
        pygame.draw.circle(screen, (150, 100, 200), (x, y), int(8 * pulse))
        pygame.draw.circle(screen, (200, 150, 255), (x, y), int(5 * pulse))
        pygame.draw.circle(screen, (220, 200, 255), (x, y), int(8 * pulse), 1)


class MagicCircleProjectile(Projectile):
    def __init__(self, x, y, damage, radius, slow_factor, slow_duration):
        super().__init__(x, y, x, y, damage, 'magic')
        self.radius = radius
        self.slow_factor = slow_factor
        self.slow_duration = slow_duration
        self.duration = 4.0
        self.lifetime = 0
        self.active = True

    def update(self, enemies):
        self.lifetime += 0.016
        if self.lifetime >= self.duration:
            self.active = False
            return
        
        for enemy in enemies:
            if enemy.alive:
                dist = math.hypot(self.x - enemy.x, self.y - enemy.y)
                if dist <= self.radius:
                    enemy.take_damage(self.damage * 0.1)
                    enemy.apply_slow(self.slow_factor, self.slow_duration)

    def draw(self, screen):
        if not self.active:
            return
        x, y = int(self.x), int(self.y)
        
        alpha = int(255 * (1 - self.lifetime / self.duration))
        pulse = 1 + math.sin(self.lifetime * 10) * 0.1
        
        temp_surface = pygame.Surface((int(self.radius * 2.5), int(self.radius * 2.5)), pygame.SRCALPHA)
        temp_x = int(self.radius * 1.25)
        temp_y = int(self.radius * 1.25)
        
        pygame.draw.circle(temp_surface, (180, 100, 255, alpha // 4), (temp_x, temp_y), int(self.radius * pulse))
        pygame.draw.circle(temp_surface, (200, 150, 255, alpha // 2), (temp_x, temp_y), int(self.radius * 0.7 * pulse), 2)
        pygame.draw.circle(temp_surface, (220, 200, 255, alpha), (temp_x, temp_y), int(self.radius * 0.4 * pulse))
        
        for i in range(8):
            angle = i * 45
            px = temp_x + int(self.radius * 0.8 * pulse * math.cos(math.radians(angle)))
            py = temp_y + int(self.radius * 0.8 * pulse * math.sin(math.radians(angle)))
            pygame.draw.circle(temp_surface, (255, 255, 255, alpha), (px, py), 3)
        
        screen.blit(temp_surface, (x - int(self.radius * 1.25), y - int(self.radius * 1.25)))


class Level:
    def __init__(self, name, theme, path_points, tower_positions, waves, gold_reward):
        self.name = name
        self.theme = theme
        self.path_points = path_points
        self.tower_positions = tower_positions
        self.waves = waves
        self.gold_reward = gold_reward
        self.unlocked = False
        self.completed = False
        self.high_score = 0
        self.stars = 0


class LevelTheme(Enum):
    FOREST = "forest"
    ICE = "ice"
    CASTLE = "castle"
    DESERT = "desert"
    VOLCANO = "volcano"
    SHADOW = "shadow"
    CAVE = "cave"
    OCEAN = "ocean"
    SKY = "sky"
    SWAMP = "swamp"
    JUNGLE = "jungle"


class LevelData:
    FOREST_PATH = [
        (50, 350), (150, 350), (150, 200), (300, 200), (300, 350),
        (450, 350), (450, 150), (600, 150), (600, 350), (750, 350),
        (750, 250), (900, 250), (900, 400), (1050, 400), (1050, 300),
        (1150, 300), (1150, 350), (1230, 350)
    ]
    FOREST_TOWERS = [
        (100, 275), (225, 275), (225, 425), (375, 425), (375, 100),
        (525, 100), (525, 275), (675, 275), (675, 425), (825, 200),
        (825, 425), (975, 325), (975, 475), (1100, 225)
    ]
    FOREST_WAVES = [
        {"enemies": [EnemyType.GOBLIN] * 5, "delay": 0.8},
        {"enemies": [EnemyType.GOBLIN] * 8 + [EnemyType.SKELETON] * 2, "delay": 0.7},
        {"enemies": [EnemyType.SKELETON] * 6 + [EnemyType.ORC] * 3, "delay": 0.6},
        {"enemies": [EnemyType.ORC] * 6 + [EnemyType.TROLL] * 2, "delay": 0.6},
        {"enemies": [EnemyType.GOBLIN] * 12 + [EnemyType.ORC] * 4 + [EnemyType.OGRE_MAGE] * 1, "delay": 0.5},
        {"enemies": [EnemyType.SKELETON] * 10 + [EnemyType.TROLL] * 3 + [EnemyType.OGRE_MAGE] * 2, "delay": 0.45},
        {"enemies": [EnemyType.TROLL] * 6 + [EnemyType.OGRE_MAGE] * 3 + [EnemyType.NECROMANCER] * 1, "delay": 0.4},
        {"enemies": [EnemyType.ORC] * 12 + [EnemyType.NECROMANCER] * 3 + [EnemyType.DARK_KNIGHT] * 2, "delay": 0.35},
        {"enemies": [EnemyType.TROLL] * 10 + [EnemyType.DARK_KNIGHT] * 3 + [EnemyType.DEMON] * 1, "delay": 0.3},
        {"enemies": [EnemyType.DEMON] * 5 + [EnemyType.DRAGON_WHELP] * 1, "delay": 0.25}
    ]

    ICE_PATH = [
        (50, 360), (200, 360), (200, 180), (350, 180), (350, 400),
        (500, 400), (500, 250), (650, 250), (650, 420), (800, 420),
        (800, 200), (950, 200), (950, 350), (1100, 350), (1100, 280),
        (1230, 280)
    ]
    ICE_TOWERS = [
        (125, 270), (275, 270), (275, 470), (425, 320), (425, 130),
        (575, 330), (575, 170), (725, 330), (725, 470), (875, 130),
        (875, 400), (1025, 270), (1025, 420)
    ]
    ICE_WAVES = [
        {"enemies": [EnemyType.SHADOW_WOLF] * 6, "delay": 0.7},
        {"enemies": [EnemyType.SHADOW_WOLF] * 10 + [EnemyType.GOBLIN] * 4, "delay": 0.6},
        {"enemies": [EnemyType.GOBLIN] * 8 + [EnemyType.SKELETON] * 4, "delay": 0.6},
        {"enemies": [EnemyType.SKELETON] * 8 + [EnemyType.TROLL] * 3, "delay": 0.5},
        {"enemies": [EnemyType.SHADOW_WOLF] * 15 + [EnemyType.TROLL] * 4 + [EnemyType.OGRE_MAGE] * 1, "delay": 0.5},
        {"enemies": [EnemyType.TROLL] * 8 + [EnemyType.OGRE_MAGE] * 3, "delay": 0.45},
        {"enemies": [EnemyType.SKELETON] * 15 + [EnemyType.NECROMANCER] * 4, "delay": 0.4},
        {"enemies": [EnemyType.TROLL] * 10 + [EnemyType.NECROMANCER] * 3 + [EnemyType.DARK_KNIGHT] * 2, "delay": 0.35},
        {"enemies": [EnemyType.SHADOW_WOLF] * 20 + [EnemyType.DARK_KNIGHT] * 4 + [EnemyType.DEMON] * 2, "delay": 0.3},
        {"enemies": [EnemyType.TROLL] * 12 + [EnemyType.DEMON] * 4 + [EnemyType.DRAGON_WHELP] * 1, "delay": 0.25}
    ]

    CASTLE_PATH = [
        (50, 350), (150, 350), (150, 250), (250, 250), (250, 400),
        (350, 400), (350, 180), (450, 180), (450, 350), (550, 350),
        (550, 200), (650, 200), (650, 420), (750, 420), (750, 250),
        (850, 250), (850, 380), (950, 380), (950, 220), (1050, 220),
        (1050, 350), (1150, 350), (1150, 300), (1230, 300)
    ]
    CASTLE_TOWERS = [
        (100, 300), (200, 325), (200, 470), (300, 275), (300, 130),
        (400, 315), (400, 130), (500, 275), (500, 470), (600, 275),
        (600, 150), (700, 335), (700, 470), (800, 315), (800, 180),
        (900, 315), (900, 430), (1000, 280), (1000, 430), (1100, 280)
    ]
    CASTLE_WAVES = [
        {"enemies": [EnemyType.GOBLIN] * 6, "delay": 0.7},
        {"enemies": [EnemyType.GOBLIN] * 10 + [EnemyType.SKELETON] * 3, "delay": 0.6},
        {"enemies": [EnemyType.SKELETON] * 8 + [EnemyType.ORC] * 4, "delay": 0.6},
        {"enemies": [EnemyType.ORC] * 8 + [EnemyType.TROLL] * 3, "delay": 0.5},
        {"enemies": [EnemyType.GOBLIN] * 15 + [EnemyType.ORC] * 6 + [EnemyType.OGRE_MAGE] * 2, "delay": 0.5},
        {"enemies": [EnemyType.TROLL] * 8 + [EnemyType.OGRE_MAGE] * 4, "delay": 0.4},
        {"enemies": [EnemyType.SKELETON] * 20 + [EnemyType.NECROMANCER] * 5, "delay": 0.4},
        {"enemies": [EnemyType.TROLL] * 10 + [EnemyType.NECROMANCER] * 4 + [EnemyType.DARK_KNIGHT] * 3, "delay": 0.35},
        {"enemies": [EnemyType.ORC] * 15 + [EnemyType.DARK_KNIGHT] * 5 + [EnemyType.DEMON] * 2, "delay": 0.3},
        {"enemies": [EnemyType.TROLL] * 12 + [EnemyType.DARK_KNIGHT] * 6 + [EnemyType.DEMON] * 4 + [EnemyType.DRAGON_WHELP] * 1, "delay": 0.25}
    ]

    DESERT_PATH = [
        (50, 360), (180, 360), (180, 150), (310, 150), (310, 400),
        (440, 400), (440, 200), (570, 200), (570, 420), (700, 420),
        (700, 180), (830, 180), (830, 350), (960, 350), (960, 220),
        (1090, 220), (1090, 380), (1230, 380)
    ]
    DESERT_TOWERS = [
        (115, 255), (245, 255), (245, 470), (375, 300), (375, 100),
        (505, 310), (505, 140), (635, 310), (635, 470), (765, 130),
        (765, 265), (895, 285), (895, 430), (1025, 300), (1025, 430)
    ]
    DESERT_WAVES = [
        {"enemies": [EnemyType.GOBLIN] * 8, "delay": 0.6},
        {"enemies": [EnemyType.GOBLIN] * 12 + [EnemyType.SHADOW_WOLF] * 4, "delay": 0.5},
        {"enemies": [EnemyType.SHADOW_WOLF] * 10 + [EnemyType.ORC] * 5, "delay": 0.5},
        {"enemies": [EnemyType.ORC] * 10 + [EnemyType.TROLL] * 4, "delay": 0.45},
        {"enemies": [EnemyType.GOBLIN] * 15 + [EnemyType.TROLL] * 6 + [EnemyType.OGRE_MAGE] * 2, "delay": 0.4},
        {"enemies": [EnemyType.SHADOW_WOLF] * 20 + [EnemyType.OGRE_MAGE] * 4, "delay": 0.4},
        {"enemies": [EnemyType.TROLL] * 10 + [EnemyType.NECROMANCER] * 5 + [EnemyType.DARK_KNIGHT] * 2, "delay": 0.35},
        {"enemies": [EnemyType.ORC] * 15 + [EnemyType.DARK_KNIGHT] * 4 + [EnemyType.DEMON] * 2, "delay": 0.3},
        {"enemies": [EnemyType.TROLL] * 12 + [EnemyType.DARK_KNIGHT] * 6 + [EnemyType.DEMON] * 4, "delay": 0.25},
        {"enemies": [EnemyType.SHADOW_WOLF] * 25 + [EnemyType.DEMON] * 6 + [EnemyType.DRAGON_WHELP] * 2 + [EnemyType.WIZNAN] * 1, "delay": 0.2}
    ]

    VOLCANO_PATH = [
        (50, 350), (150, 350), (150, 200), (250, 200), (250, 420),
        (350, 420), (350, 150), (450, 150), (450, 380), (550, 380),
        (550, 180), (650, 180), (650, 400), (750, 400), (750, 220),
        (850, 220), (850, 350), (950, 350), (950, 180), (1050, 180),
        (1050, 380), (1150, 380), (1150, 300), (1230, 300)
    ]
    VOLCANO_TOWERS = [
        (100, 275), (200, 260), (200, 470), (300, 280), (300, 100),
        (400, 265), (400, 100), (500, 280), (500, 470), (600, 290),
        (600, 130), (700, 260), (700, 470), (800, 275), (800, 130),
        (900, 265), (900, 420), (1000, 275), (1000, 430), (1100, 240)
    ]
    VOLCANO_WAVES = [
        {"enemies": [EnemyType.GOBLIN] * 10, "delay": 0.5},
        {"enemies": [EnemyType.GOBLIN] * 15 + [EnemyType.ORC] * 5, "delay": 0.45},
        {"enemies": [EnemyType.ORC] * 12 + [EnemyType.TROLL] * 5, "delay": 0.4},
        {"enemies": [EnemyType.TROLL] * 10 + [EnemyType.OGRE_MAGE] * 4, "delay": 0.4},
        {"enemies": [EnemyType.GOBLIN] * 20 + [EnemyType.OGRE_MAGE] * 6 + [EnemyType.NECROMANCER] * 2, "delay": 0.35},
        {"enemies": [EnemyType.TROLL] * 12 + [EnemyType.NECROMANCER] * 5 + [EnemyType.DARK_KNIGHT] * 3, "delay": 0.35},
        {"enemies": [EnemyType.OGRE_MAGE] * 8 + [EnemyType.DARK_KNIGHT] * 5 + [EnemyType.DEMON] * 2, "delay": 0.3},
        {"enemies": [EnemyType.NECROMANCER] * 10 + [EnemyType.DEMON] * 5 + [EnemyType.DRAGON_WHELP] * 1, "delay": 0.25},
        {"enemies": [EnemyType.DARK_KNIGHT] * 8 + [EnemyType.DEMON] * 8 + [EnemyType.DRAGON_WHELP] * 2, "delay": 0.25},
        {"enemies": [EnemyType.DEMON] * 10 + [EnemyType.DRAGON_WHELP] * 4 + [EnemyType.WIZNAN] * 1, "delay": 0.2}
    ]

    SHADOW_PATH = [
        (50, 360), (150, 360), (150, 200), (250, 200), (250, 400),
        (350, 400), (350, 150), (450, 150), (450, 350), (550, 350),
        (550, 180), (650, 180), (650, 420), (750, 420), (750, 220),
        (850, 220), (850, 380), (950, 380), (950, 180), (1050, 180),
        (1050, 400), (1150, 400), (1150, 280), (1230, 280)
    ]
    SHADOW_TOWERS = [
        (100, 280), (200, 280), (200, 470), (300, 275), (300, 100),
        (400, 250), (400, 100), (500, 265), (500, 470), (600, 250),
        (600, 130), (700, 320), (700, 470), (800, 300), (800, 130),
        (900, 280), (900, 430), (1000, 275), (1000, 450), (1100, 230)
    ]
    SHADOW_WAVES = [
        {"enemies": [EnemyType.SHADOW_WOLF] * 10, "delay": 0.4},
        {"enemies": [EnemyType.SHADOW_WOLF] * 15 + [EnemyType.SKELETON] * 5, "delay": 0.35},
        {"enemies": [EnemyType.SKELETON] * 15 + [EnemyType.TROLL] * 6, "delay": 0.35},
        {"enemies": [EnemyType.TROLL] * 12 + [EnemyType.NECROMANCER] * 4, "delay": 0.3},
        {"enemies": [EnemyType.SHADOW_WOLF] * 20 + [EnemyType.NECROMANCER] * 6 + [EnemyType.DARK_KNIGHT] * 2, "delay": 0.3},
        {"enemies": [EnemyType.NECROMANCER] * 10 + [EnemyType.DARK_KNIGHT] * 5 + [EnemyType.DEMON] * 3, "delay": 0.25},
        {"enemies": [EnemyType.DARK_KNIGHT] * 8 + [EnemyType.DEMON] * 6 + [EnemyType.DRAGON_WHELP] * 2, "delay": 0.25},
        {"enemies": [EnemyType.TROLL] * 15 + [EnemyType.DEMON] * 8 + [EnemyType.DRAGON_WHELP] * 3, "delay": 0.2},
        {"enemies": [EnemyType.DARK_KNIGHT] * 10 + [EnemyType.DEMON] * 10 + [EnemyType.DRAGON_WHELP] * 4, "delay": 0.2},
        {"enemies": [EnemyType.DEMON] * 15 + [EnemyType.DRAGON_WHELP] * 6 + [EnemyType.WIZNAN] * 2, "delay": 0.15}
    ]

    CAVE_PATH = [
        (50, 350), (120, 350), (120, 420), (200, 420), (200, 280),
        (280, 280), (280, 400), (360, 400), (360, 200), (440, 200),
        (440, 350), (520, 350), (520, 180), (600, 180), (600, 420),
        (680, 420), (680, 220), (760, 220), (760, 380), (840, 380),
        (840, 200), (920, 200), (920, 350), (1000, 350), (1000, 250),
        (1080, 250), (1080, 320), (1160, 320), (1160, 350), (1230, 350)
    ]
    CAVE_TOWERS = [
        (85, 275), (160, 350), (160, 470), (240, 200), (240, 470),
        (320, 340), (320, 150), (400, 290), (400, 470), (480, 130),
        (480, 300), (560, 280), (560, 470), (640, 150), (640, 320),
        (720, 270), (720, 470), (800, 150), (800, 330), (880, 260),
        (880, 430), (960, 280), (960, 420), (1040, 200), (1040, 400)
    ]
    CAVE_WAVES = [
        {"enemies": [EnemyType.GOBLIN] * 8, "delay": 0.7},
        {"enemies": [EnemyType.GOBLIN] * 12 + [EnemyType.SHADOW_WOLF] * 4, "delay": 0.6},
        {"enemies": [EnemyType.SHADOW_WOLF] * 10 + [EnemyType.SKELETON] * 5, "delay": 0.55},
        {"enemies": [EnemyType.SKELETON] * 10 + [EnemyType.ORC] * 5, "delay": 0.5},
        {"enemies": [EnemyType.ORC] * 8 + [EnemyType.TROLL] * 4 + [EnemyType.GOBLIN] * 8, "delay": 0.45},
        {"enemies": [EnemyType.TROLL] * 6 + [EnemyType.OGRE_MAGE] * 3 + [EnemyType.SKELETON] * 6, "delay": 0.4},
        {"enemies": [EnemyType.OGRE_MAGE] * 5 + [EnemyType.NECROMANCER] * 3 + [EnemyType.ORC] * 6, "delay": 0.35},
        {"enemies": [EnemyType.NECROMANCER] * 4 + [EnemyType.DARK_KNIGHT] * 3 + [EnemyType.TROLL] * 4, "delay": 0.3},
        {"enemies": [EnemyType.DARK_KNIGHT] * 5 + [EnemyType.DEMON] * 4 + [EnemyType.NECROMANCER] * 3, "delay": 0.25},
        {"enemies": [EnemyType.DEMON] * 6 + [EnemyType.DRAGON_WHELP] * 2 + [EnemyType.WIZNAN] * 1, "delay": 0.2}
    ]

    OCEAN_PATH = [
        (50, 360), (150, 360), (150, 250), (250, 250), (250, 400),
        (350, 400), (350, 180), (450, 180), (450, 320), (550, 320),
        (550, 200), (650, 200), (650, 380), (750, 380), (750, 220),
        (850, 220), (850, 350), (950, 350), (950, 180), (1050, 180),
        (1050, 300), (1150, 300), (1150, 360), (1230, 360)
    ]
    OCEAN_TOWERS = [
        (100, 305), (200, 325), (200, 470), (300, 290), (300, 130),
        (400, 250), (400, 130), (500, 250), (500, 470), (600, 260),
        (600, 150), (700, 300), (700, 470), (800, 270), (800, 130),
        (900, 265), (900, 430), (1000, 240), (1000, 420), (1100, 240)
    ]
    OCEAN_WAVES = [
        {"enemies": [EnemyType.SHADOW_WOLF] * 8, "delay": 0.65},
        {"enemies": [EnemyType.SHADOW_WOLF] * 12 + [EnemyType.GOBLIN] * 6, "delay": 0.55},
        {"enemies": [EnemyType.GOBLIN] * 10 + [EnemyType.SKELETON] * 5, "delay": 0.5},
        {"enemies": [EnemyType.SKELETON] * 8 + [EnemyType.ORC] * 4, "delay": 0.45},
        {"enemies": [EnemyType.ORC] * 6 + [EnemyType.TROLL] * 3 + [EnemyType.SHADOW_WOLF] * 8, "delay": 0.4},
        {"enemies": [EnemyType.TROLL] * 5 + [EnemyType.OGRE_MAGE] * 2 + [EnemyType.ORC] * 6, "delay": 0.35},
        {"enemies": [EnemyType.OGRE_MAGE] * 4 + [EnemyType.NECROMANCER] * 2 + [EnemyType.TROLL] * 4, "delay": 0.3},
        {"enemies": [EnemyType.NECROMANCER] * 3 + [EnemyType.DARK_KNIGHT] * 2 + [EnemyType.OGRE_MAGE] * 3, "delay": 0.25},
        {"enemies": [EnemyType.DARK_KNIGHT] * 4 + [EnemyType.DEMON] * 3 + [EnemyType.NECROMANCER] * 2, "delay": 0.2},
        {"enemies": [EnemyType.DEMON] * 5 + [EnemyType.DRAGON_WHELP] * 2 + [EnemyType.WIZNAN] * 1, "delay": 0.15}
    ]

    SKY_PATH = [
        (50, 350), (100, 350), (100, 280), (180, 280), (180, 380),
        (260, 380), (260, 220), (340, 220), (340, 350), (420, 350),
        (420, 180), (500, 180), (500, 320), (580, 320), (580, 200),
        (660, 200), (660, 380), (740, 380), (740, 180), (820, 180),
        (820, 300), (900, 300), (900, 220), (980, 220), (980, 350),
        (1060, 350), (1060, 280), (1140, 280), (1140, 350), (1230, 350)
    ]
    SKY_TOWERS = [
        (75, 315), (140, 330), (140, 430), (220, 250), (220, 430),
        (300, 300), (300, 160), (380, 280), (380, 430), (460, 130),
        (460, 250), (540, 260), (540, 430), (620, 150), (620, 300),
        (700, 240), (700, 430), (780, 130), (780, 260), (860, 260),
        (860, 380), (940, 160), (940, 330), (1020, 290), (1020, 420),
        (1100, 240), (1100, 410)
    ]
    SKY_WAVES = [
        {"enemies": [EnemyType.GOBLIN] * 6, "delay": 0.75},
        {"enemies": [EnemyType.GOBLIN] * 10 + [EnemyType.SKELETON] * 3, "delay": 0.65},
        {"enemies": [EnemyType.SKELETON] * 8 + [EnemyType.SHADOW_WOLF] * 4, "delay": 0.55},
        {"enemies": [EnemyType.SHADOW_WOLF] * 10 + [EnemyType.ORC] * 4, "delay": 0.5},
        {"enemies": [EnemyType.ORC] * 7 + [EnemyType.TROLL] * 3 + [EnemyType.GOBLIN] * 6, "delay": 0.45},
        {"enemies": [EnemyType.TROLL] * 5 + [EnemyType.OGRE_MAGE] * 2 + [EnemyType.ORC] * 5, "delay": 0.4},
        {"enemies": [EnemyType.OGRE_MAGE] * 4 + [EnemyType.NECROMANCER] * 2 + [EnemyType.TROLL] * 3, "delay": 0.35},
        {"enemies": [EnemyType.NECROMANCER] * 3 + [EnemyType.DARK_KNIGHT] * 2 + [EnemyType.OGRE_MAGE] * 2, "delay": 0.3},
        {"enemies": [EnemyType.DARK_KNIGHT] * 4 + [EnemyType.DEMON] * 3 + [EnemyType.NECROMANCER] * 2, "delay": 0.25},
        {"enemies": [EnemyType.DEMON] * 5 + [EnemyType.DRAGON_WHELP] * 3 + [EnemyType.WIZNAN] * 1, "delay": 0.2}
    ]

    SWAMP_PATH = [
        (50, 360), (130, 360), (130, 280), (210, 280), (210, 400),
        (290, 400), (290, 200), (370, 200), (370, 350), (450, 350),
        (450, 180), (530, 180), (530, 380), (610, 380), (610, 220),
        (690, 220), (690, 320), (770, 320), (770, 200), (850, 200),
        (850, 360), (930, 360), (930, 250), (1010, 250), (1010, 380),
        (1090, 380), (1090, 300), (1170, 300), (1170, 360), (1230, 360)
    ]
    SWAMP_TOWERS = [
        (90, 320), (170, 340), (170, 460), (250, 240), (250, 460),
        (330, 280), (330, 150), (410, 270), (410, 460), (490, 130),
        (490, 290), (570, 300), (570, 460), (650, 150), (650, 280),
        (730, 260), (730, 460), (810, 130), (810, 280), (890, 280),
        (890, 430), (970, 200), (970, 420), (1050, 310), (1050, 450),
        (1130, 230), (1130, 440)
    ]
    SWAMP_WAVES = [
        {"enemies": [EnemyType.SHADOW_WOLF] * 10, "delay": 0.6},
        {"enemies": [EnemyType.SHADOW_WOLF] * 15 + [EnemyType.GOBLIN] * 5, "delay": 0.5},
        {"enemies": [EnemyType.GOBLIN] * 12 + [EnemyType.SKELETON] * 6, "delay": 0.45},
        {"enemies": [EnemyType.SKELETON] * 10 + [EnemyType.ORC] * 5, "delay": 0.4},
        {"enemies": [EnemyType.ORC] * 8 + [EnemyType.TROLL] * 4 + [EnemyType.SHADOW_WOLF] * 8, "delay": 0.35},
        {"enemies": [EnemyType.TROLL] * 6 + [EnemyType.OGRE_MAGE] * 3 + [EnemyType.ORC] * 6, "delay": 0.3},
        {"enemies": [EnemyType.OGRE_MAGE] * 5 + [EnemyType.NECROMANCER] * 3 + [EnemyType.TROLL] * 4, "delay": 0.25},
        {"enemies": [EnemyType.NECROMANCER] * 4 + [EnemyType.DARK_KNIGHT] * 3 + [EnemyType.OGRE_MAGE] * 3, "delay": 0.2},
        {"enemies": [EnemyType.DARK_KNIGHT] * 5 + [EnemyType.DEMON] * 4 + [EnemyType.NECROMANCER] * 3, "delay": 0.18},
        {"enemies": [EnemyType.DEMON] * 7 + [EnemyType.DRAGON_WHELP] * 3 + [EnemyType.WIZNAN] * 2, "delay": 0.15}
    ]

    JUNGLE_PATH = [
        (50, 350), (120, 350), (120, 220), (200, 220), (200, 380),
        (280, 380), (280, 180), (360, 180), (360, 320), (440, 320),
        (440, 200), (520, 200), (520, 360), (600, 360), (600, 220),
        (680, 220), (680, 340), (760, 340), (760, 180), (840, 180),
        (840, 300), (920, 300), (920, 200), (1000, 200), (1000, 350),
        (1080, 350), (1080, 260), (1160, 260), (1160, 350), (1230, 350)
    ]
    JUNGLE_TOWERS = [
        (85, 285), (160, 300), (160, 450), (240, 200), (240, 450),
        (320, 250), (320, 130), (400, 260), (400, 450), (480, 130),
        (480, 290), (560, 290), (560, 450), (640, 160), (640, 280),
        (720, 280), (720, 450), (800, 130), (800, 240), (880, 250),
        (880, 420), (960, 160), (960, 320), (1040, 280), (1040, 420),
        (1120, 210), (1120, 410)
    ]
    JUNGLE_WAVES = [
        {"enemies": [EnemyType.GOBLIN] * 8, "delay": 0.7},
        {"enemies": [EnemyType.GOBLIN] * 12 + [EnemyType.SHADOW_WOLF] * 4, "delay": 0.6},
        {"enemies": [EnemyType.SHADOW_WOLF] * 10 + [EnemyType.SKELETON] * 5, "delay": 0.5},
        {"enemies": [EnemyType.SKELETON] * 9 + [EnemyType.ORC] * 4, "delay": 0.45},
        {"enemies": [EnemyType.ORC] * 7 + [EnemyType.TROLL] * 3 + [EnemyType.GOBLIN] * 8, "delay": 0.4},
        {"enemies": [EnemyType.TROLL] * 5 + [EnemyType.OGRE_MAGE] * 2 + [EnemyType.ORC] * 5, "delay": 0.35},
        {"enemies": [EnemyType.OGRE_MAGE] * 4 + [EnemyType.NECROMANCER] * 2 + [EnemyType.TROLL] * 4, "delay": 0.3},
        {"enemies": [EnemyType.NECROMANCER] * 3 + [EnemyType.DARK_KNIGHT] * 2 + [EnemyType.OGRE_MAGE] * 3, "delay": 0.25},
        {"enemies": [EnemyType.DARK_KNIGHT] * 4 + [EnemyType.DEMON] * 3 + [EnemyType.NECROMANCER] * 2, "delay": 0.2},
        {"enemies": [EnemyType.DEMON] * 5 + [EnemyType.DRAGON_WHELP] * 2 + [EnemyType.WIZNAN] * 1, "delay": 0.15}
    ]

    @staticmethod
    def get_levels():
        return [
            Level("精灵森林", LevelTheme.FOREST, LevelData.FOREST_PATH, LevelData.FOREST_TOWERS, LevelData.FOREST_WAVES, 100),
            Level("冰封峡谷", LevelTheme.ICE, LevelData.ICE_PATH, LevelData.ICE_TOWERS, LevelData.ICE_WAVES, 150),
            Level("城堡废墟", LevelTheme.CASTLE, LevelData.CASTLE_PATH, LevelData.CASTLE_TOWERS, LevelData.CASTLE_WAVES, 200),
            Level("沙漠绿洲", LevelTheme.DESERT, LevelData.DESERT_PATH, LevelData.DESERT_TOWERS, LevelData.DESERT_WAVES, 250),
            Level("火山深渊", LevelTheme.VOLCANO, LevelData.VOLCANO_PATH, LevelData.VOLCANO_TOWERS, LevelData.VOLCANO_WAVES, 300),
            Level("暗影要塞", LevelTheme.SHADOW, LevelData.SHADOW_PATH, LevelData.SHADOW_TOWERS, LevelData.SHADOW_WAVES, 500)
        ]


class Enemy:
    def __init__(self, x, y, path, wave_num=1):
        self.x = x
        self.y = y
        self.path = path
        self.path_index = 0
        self.max_hp = 100
        self.hp = self.max_hp
        self.speed = 1.0
        self.base_speed = 1.0
        self.reward = 10
        self.alive = True
        self.slow_timer = 0
        self.burn_timer = 0
        self.burn_damage = 0
        self.anim_timer = 0
        self.type = "enemy"
        self.wave_num = wave_num
        self.damage_modifier = 1.0 + (wave_num - 1) * 0.1
        self.reached_end = False
        
        self.frozen = False
        self.frozen_timer = 0
        self.poisoned = False
        self.poison_timer = 0
        self.poison_damage = 0
        self.stunned = False
        self.stun_timer = 0
        self.buff_timer = 0
        self.has_shield = False
        self.shield_timer = 0
        self.shield_amount = 0
        
        self.walk_anim_timer = 0
        self.hit_flash = False
        self.hit_flash_timer = 0
        
        self.particles = []
        self.emitter_active = False
        self.emitter_timer = 0

    def update(self, dt):
        if not self.alive:
            return

        self.anim_timer += dt
        self.walk_anim_timer += dt * self.speed
        
        if self.hit_flash:
            self.hit_flash_timer -= dt
            if self.hit_flash_timer <= 0:
                self.hit_flash = False

        if self.stunned:
            self.stun_timer -= dt
            if self.stun_timer <= 0:
                self.stunned = False
            return

        if self.frozen:
            self.frozen_timer -= dt
            if self.frozen_timer <= 0:
                self.frozen = False
                self.speed = self.base_speed
            return

        if self.slow_timer > 0:
            self.slow_timer -= dt
            if self.slow_timer <= 0:
                self.speed = self.base_speed

        if self.burn_timer > 0:
            self.burn_timer -= dt
            self.hp -= self.burn_damage * dt
            if self.hp <= 0:
                self.alive = False

        if self.poisoned and self.poison_timer > 0:
            self.poison_timer -= dt
            self.hp -= self.poison_damage * dt
            if self.poison_timer <= 0:
                self.poisoned = False

        if self.buff_timer > 0:
            self.buff_timer -= dt
            if self.buff_timer <= 0:
                self.speed = self.base_speed

        if self.hp <= 0:
            self.alive = False

        if self.path_index < len(self.path) - 1:
            target_x, target_y = self.path[self.path_index + 1]
            dx = target_x - self.x
            dy = target_y - self.y
            dist = math.hypot(dx, dy)
            if dist > 5:
                self.x += (dx / dist) * self.speed * 60 * dt
                self.y += (dy / dist) * self.speed * 60 * dt
            else:
                self.path_index += 1
        else:
            self.reached_end = True

        for particle in list(self.particles):
            particle.update(dt)
            if not particle.alive:
                self.particles.remove(particle)

    def take_damage(self, damage):
        if self.has_shield and self.shield_amount > 0:
            absorbed = min(damage, self.shield_amount)
            self.shield_amount -= absorbed
            damage -= absorbed
            if self.shield_amount <= 0:
                self.has_shield = False
        
        self.hp -= damage * self.damage_modifier
        self.hit_flash = True
        self.hit_flash_timer = 0.15
        
        if self.hp <= 0:
            self.alive = False

    def apply_slow(self, factor, duration, stackable=False):
        if stackable:
            current_factor = self.speed / self.base_speed
            new_factor = max(0.1, current_factor * factor)
            self.speed = self.base_speed * new_factor
            self.slow_timer = max(self.slow_timer, duration)
        else:
            self.speed = self.base_speed * factor
            self.slow_timer = duration

    def apply_burn(self, damage, duration):
        self.burn_damage = damage
        self.burn_timer = duration
        self.poisoned = False

    def apply_poison(self, damage, duration):
        self.poison_damage = damage
        self.poison_timer = duration
        self.poisoned = True

    def freeze(self, duration):
        self.frozen = True
        self.frozen_timer = duration
        self.speed = 0

    def stun(self, duration):
        self.stunned = True
        self.stun_timer = duration

    def apply_buff(self, speed_multiplier, duration):
        self.speed = self.base_speed * speed_multiplier
        self.buff_timer = duration

    def add_shield(self, amount, duration):
        self.has_shield = True
        self.shield_amount += amount
        self.shield_timer = duration

    def apply_magic_buff(self):
        self.has_magic_buff = True
        self.magic_buff_timer = 5.0

    def add_particle(self, x, y, vx, vy, color, size, lifetime):
        self.particles.append(Particle(x, y, vx, vy, color, size, lifetime))

    def draw(self, screen, font):
        if not self.alive:
            return

        x, y = int(self.x), int(self.y)

        for particle in self.particles:
            particle.draw(screen)

        if self.frozen:
            frost_color = (150, 220, 255)
            frost_radius = 8 + int(3 * math.sin(self.anim_timer * 8))
            pygame.draw.circle(screen, frost_color, (x, y), frost_radius, 2)
            pygame.draw.circle(screen, (200, 240, 255), (x, y), frost_radius // 2)

        if self.has_shield:
            shield_alpha = int(100 + 50 * math.sin(self.anim_timer * 6))
            shield_surface = pygame.Surface((30, 30), pygame.SRCALPHA)
            pygame.draw.circle(shield_surface, (100, 150, 255, shield_alpha), (15, 15), 15)
            screen.blit(shield_surface, (x - 15, y - 15))

        health_bar_width = 40
        health_bar_height = 6
        health_bar_y = y - 25
        health_percent = self.hp / self.max_hp
        
        pygame.draw.rect(screen, COLOR_DARK_RED, (x - health_bar_width // 2, health_bar_y, health_bar_width, health_bar_height), border_radius=3)
        
        health_color = COLOR_GREEN
        if health_percent < 0.3:
            health_color = COLOR_RED
        elif health_percent < 0.6:
            health_color = COLOR_ORANGE
        
        pygame.draw.rect(screen, health_color, (x - health_bar_width // 2, health_bar_y, int(health_bar_width * health_percent), health_bar_height), border_radius=3)
        
        health_border = pygame.Rect(x - health_bar_width // 2, health_bar_y, health_bar_width, health_bar_height)
        pygame.draw.rect(screen, COLOR_WHITE, health_border, 1, border_radius=3)

        if self.burn_timer > 0:
            fire_pulse = int(3 * math.sin(self.anim_timer * 10))
            pygame.draw.circle(screen, COLOR_ORANGE, (x, y + 15), 6 + fire_pulse, 2)

        if self.poisoned:
            poison_pulse = int(2 * math.sin(self.anim_timer * 8))
            pygame.draw.circle(screen, COLOR_GREEN, (x - 15, y), 4 + poison_pulse)

        if self.hit_flash:
            flash_surface = pygame.Surface((30, 30), pygame.SRCALPHA)
            flash_surface.fill((255, 255, 255, int(200 * (self.hit_flash_timer / 0.15))))
            screen.blit(flash_surface, (x - 15, y - 15))

    def draw_health_bar(self, screen, font):
        pass


class Goblin(Enemy):
    def __init__(self, x, y, path, wave_num=1):
        super().__init__(x, y, path, wave_num)
        self.max_hp = 80 + wave_num * 10
        self.hp = self.max_hp
        self.speed = 1.2
        self.base_speed = 1.2
        self.reward = 15
        self.type = "goblin"
        self.eye_color = (255, 200, 50)

    def draw(self, screen, font):
        super().draw(screen, font)
        x, y = int(self.x), int(self.y)
        
        walk_offset = int(3 * math.sin(self.walk_anim_timer * 8))
        
        body_color = (100, 180, 80)
        body_light = (130, 210, 110)
        
        pygame.draw.ellipse(screen, body_color, (x-12, y-8 + walk_offset, 24, 20))
        
        pygame.draw.circle(screen, body_light, (x, y-5 + walk_offset), 11)
        
        pygame.draw.polygon(screen, body_color, [(x-10, y-3 + walk_offset), (x-5, y+5 + walk_offset), (x-10, y+5 + walk_offset)])
        pygame.draw.polygon(screen, body_color, [(x+10, y-3 + walk_offset), (x+5, y+5 + walk_offset), (x+10, y+5 + walk_offset)])
        
        pygame.draw.circle(screen, COLOR_BLACK, (x-4, y-7 + walk_offset), 3)
        pygame.draw.circle(screen, self.eye_color, (x-4, y-7 + walk_offset), 1)
        pygame.draw.circle(screen, COLOR_BLACK, (x+4, y-7 + walk_offset), 3)
        pygame.draw.circle(screen, self.eye_color, (x+4, y-7 + walk_offset), 1)
        
        pygame.draw.polygon(screen, COLOR_GREEN, [(x-8, y-2 + walk_offset), (x-3, y+3 + walk_offset), (x-8, y+3 + walk_offset)])
        
        leg_offset = int(2 * math.sin(self.walk_anim_timer * 6 + 1))
        pygame.draw.line(screen, body_color, (x-4, y+12 + walk_offset), (x-6, y+18 + walk_offset + leg_offset), 4)
        pygame.draw.line(screen, body_color, (x+4, y+12 + walk_offset), (x+6, y+18 + walk_offset - leg_offset), 4)

    def draw_health_bar(self, screen, font):
        pass


class Skeleton(Enemy):
    def __init__(self, x, y, path, wave_num=1):
        super().__init__(x, y, path, wave_num)
        self.max_hp = 100 + wave_num * 15
        self.hp = self.max_hp
        self.speed = 1.0
        self.base_speed = 1.0
        self.reward = 20
        self.type = "skeleton"
        self.has_sword = True

    def draw(self, screen, font):
        super().draw(screen, font)
        x, y = int(self.x), int(self.y)
        
        walk_offset = int(2 * math.sin(self.walk_anim_timer * 5))
        
        bone_color = (200, 200, 200)
        bone_dark = (150, 150, 150)
        
        pygame.draw.circle(screen, bone_color, (x, y-6 + walk_offset), 10)
        pygame.draw.circle(screen, COLOR_BLACK, (x-3, y-8 + walk_offset), 3)
        pygame.draw.circle(screen, COLOR_BLACK, (x+3, y-8 + walk_offset), 3)
        pygame.draw.line(screen, bone_dark, (x, y-1), (x, y-5), 2)
        
        pygame.draw.line(screen, bone_color, (x, y+4 + walk_offset), (x, y+18 + walk_offset), 5)
        
        arm_swing = int(5 * math.sin(self.walk_anim_timer * 8))
        pygame.draw.line(screen, bone_color, (x, y+6 + walk_offset), (x-12 + arm_swing, y+2 + walk_offset), 4)
        pygame.draw.line(screen, bone_color, (x, y+6 + walk_offset), (x+12 - arm_swing, y+2 + walk_offset), 4)
        
        leg_swing = int(4 * math.sin(self.walk_anim_timer * 5 + math.pi))
        pygame.draw.line(screen, bone_color, (x, y+18 + walk_offset), (x-8 + leg_swing, y+28 + walk_offset), 4)
        pygame.draw.line(screen, bone_color, (x, y+18 + walk_offset), (x+8 - leg_swing, y+28 + walk_offset), 4)
        
        if self.has_sword:
            sword_angle = math.sin(self.walk_anim_timer * 6) * 0.3
            sword_x = x - 15 + arm_swing
            sword_y = y + 2 + walk_offset
            pygame.draw.line(screen, COLOR_GRAY, (sword_x, sword_y), 
                           (sword_x + int(15 * math.cos(sword_angle)), sword_y + int(15 * math.sin(sword_angle))), 3)
            pygame.draw.circle(screen, COLOR_GOLD, 
                             (sword_x + int(15 * math.cos(sword_angle)), sword_y + int(15 * math.sin(sword_angle))), 4)

    def draw_health_bar(self, screen, font):
        pass


class Orc(Enemy):
    def __init__(self, x, y, path, wave_num=1):
        super().__init__(x, y, path, wave_num)
        self.max_hp = 150 + wave_num * 20
        self.hp = self.max_hp
        self.speed = 0.8
        self.base_speed = 0.8
        self.reward = 30
        self.type = "orc"
        self.has_axe = True

    def draw(self, screen, font):
        super().draw(screen, font)
        x, y = int(self.x), int(self.y)
        
        walk_offset = int(2 * math.sin(self.walk_anim_timer * 3))
        
        skin_color = (80, 150, 60)
        skin_light = (100, 170, 80)
        
        pygame.draw.ellipse(screen, skin_color, (x-16, y-10 + walk_offset, 32, 28))
        
        pygame.draw.circle(screen, skin_light, (x, y-5 + walk_offset), 14)
        
        pygame.draw.polygon(screen, skin_color, [(x-12, y-3 + walk_offset), (x-6, y+5 + walk_offset), (x-12, y+5 + walk_offset)])
        pygame.draw.polygon(screen, skin_color, [(x+12, y-3 + walk_offset), (x+6, y+5 + walk_offset), (x+12, y+5 + walk_offset)])
        
        pygame.draw.circle(screen, COLOR_BLACK, (x-5, y-7 + walk_offset), 4)
        pygame.draw.circle(screen, COLOR_WHITE, (x-4, y-8 + walk_offset), 1)
        pygame.draw.circle(screen, COLOR_BLACK, (x+5, y-7 + walk_offset), 4)
        pygame.draw.circle(screen, COLOR_WHITE, (x+4, y-8 + walk_offset), 1)
        
        pygame.draw.polygon(screen, (40, 80, 30), [(x, y+2 + walk_offset), (x-4, y+8 + walk_offset), (x+4, y+8 + walk_offset)])
        
        arm_swing = int(4 * math.sin(self.walk_anim_timer * 4))
        pygame.draw.line(screen, skin_color, (x-8, y-2 + walk_offset), (x-20 + arm_swing, y-8 + walk_offset), 8)
        pygame.draw.line(screen, skin_color, (x+8, y-2 + walk_offset), (x+20 - arm_swing, y-8 + walk_offset), 8)
        
        leg_swing = int(3 * math.sin(self.walk_anim_timer * 3 + math.pi))
        pygame.draw.line(screen, skin_color, (x-6, y+18 + walk_offset), (x-12 + leg_swing, y+28 + walk_offset), 8)
        pygame.draw.line(screen, skin_color, (x+6, y+18 + walk_offset), (x+12 - leg_swing, y+28 + walk_offset), 8)
        
        if self.has_axe:
            axe_x = x - 25 + arm_swing
            axe_y = y - 12 + walk_offset
            pygame.draw.line(screen, COLOR_GRAY, (axe_x, axe_y), (axe_x - 15, axe_y + 10), 5)
            pygame.draw.polygon(screen, (80, 80, 80), [(axe_x - 15, axe_y + 10), (axe_x - 25, axe_y + 5), (axe_x - 20, axe_y + 18)])

    def draw_health_bar(self, screen, font):
        pass


class ShadowWolf(Enemy):
    def __init__(self, x, y, path, wave_num=1):
        super().__init__(x, y, path, wave_num)
        self.max_hp = 60 + wave_num * 8
        self.hp = self.max_hp
        self.speed = 1.5
        self.base_speed = 1.5
        self.reward = 12
        self.type = "shadow_wolf"
        self.glow_color = (150, 100, 200)

    def draw(self, screen, font):
        super().draw(screen, font)
        x, y = int(self.x), int(self.y)
        
        bob = int(4 * math.sin(self.walk_anim_timer * 10))
        shadow_offset = int(3 * math.sin(self.anim_timer * 4))
        
        body_color = (80, 80, 120)
        body_dark = (50, 50, 80)
        
        pygame.draw.ellipse(screen, body_dark, (x-15 + shadow_offset, y-3 + bob + 5, 30, 16))
        
        pygame.draw.ellipse(screen, body_color, (x-14, y-4 + bob, 28, 14))
        
        pygame.draw.circle(screen, body_color, (x-10, y-8 + bob), 8)
        pygame.draw.circle(screen, COLOR_WHITE, (x-12, y-10 + bob), 3)
        pygame.draw.circle(screen, COLOR_BLACK, (x-11, y-10 + bob), 1)
        pygame.draw.circle(screen, COLOR_WHITE, (x-7, y-10 + bob), 3)
        pygame.draw.circle(screen, COLOR_BLACK, (x-6, y-10 + bob), 1)
        
        ear_tilt = int(2 * math.sin(self.walk_anim_timer * 8))
        pygame.draw.polygon(screen, body_color, [(x-16, y-14 + bob), (x-12, y-20 + bob + ear_tilt), (x-10, y-14 + bob)])
        pygame.draw.polygon(screen, body_color, [(x-5, y-14 + bob), (x-3, y-20 + bob - ear_tilt), (x-1, y-14 + bob)])
        
        pygame.draw.polygon(screen, body_color, [(x+15, y-1 + bob), (x+22, y-3 + bob), (x+18, y+2 + bob)])
        
        leg_swing = int(3 * math.sin(self.walk_anim_timer * 8 + math.pi))
        pygame.draw.line(screen, body_color, (x-8, y+10 + bob), (x-10 + leg_swing, y+16 + bob), 3)
        pygame.draw.line(screen, body_color, (x-2, y+10 + bob), (x-1 - leg_swing, y+16 + bob), 3)
        pygame.draw.line(screen, body_color, (x+2, y+10 + bob), (x+3 + leg_swing, y+16 + bob), 3)
        pygame.draw.line(screen, body_color, (x+8, y+10 + bob), (x+9 - leg_swing, y+16 + bob), 3)
        
        glow_pulse = int(5 * math.sin(self.anim_timer * 6))
        glow_surface = pygame.Surface((40, 30), pygame.SRCALPHA)
        pygame.draw.ellipse(glow_surface, (self.glow_color[0], self.glow_color[1], self.glow_color[2], 30 + glow_pulse), 
                          (5, 5, 30, 20))
        screen.blit(glow_surface, (x - 20, y - 15 + bob))

    def draw_health_bar(self, screen, font):
        pass


class Troll(Enemy):
    def __init__(self, x, y, path, wave_num=1):
        super().__init__(x, y, path, wave_num)
        self.max_hp = 300 + wave_num * 40
        self.hp = self.max_hp
        self.speed = 0.5
        self.base_speed = 0.5
        self.reward = 50
        self.type = "troll"
        self.has_club = True
        self.enraged = False

    def draw(self, screen, font):
        super().draw(screen, font)
        x, y = int(self.x), int(self.y)
        
        walk_offset = int(2 * math.sin(self.walk_anim_timer * 2))
        
        skin_color = (100, 80, 60)
        skin_light = (130, 100, 80)
        
        body_width = 36
        body_height = 40
        
        pygame.draw.rect(screen, skin_color, (x - body_width//2, y - 5 + walk_offset, body_width, body_height))
        
        pygame.draw.circle(screen, skin_light, (x, y - 8 + walk_offset), 18)
        
        brow_offset = int(3 * math.sin(self.anim_timer * 3))
        pygame.draw.line(screen, COLOR_BLACK, (x-10, y-12 + walk_offset), (x-5, y-10 + walk_offset + brow_offset), 3)
        pygame.draw.line(screen, COLOR_BLACK, (x+10, y-12 + walk_offset), (x+5, y-10 + walk_offset + brow_offset), 3)
        
        pygame.draw.circle(screen, COLOR_BLACK, (x-7, y-8 + walk_offset), 5)
        pygame.draw.circle(screen, COLOR_WHITE, (x-6, y-9 + walk_offset), 2)
        pygame.draw.circle(screen, COLOR_BLACK, (x+7, y-8 + walk_offset), 5)
        pygame.draw.circle(screen, COLOR_WHITE, (x+6, y-9 + walk_offset), 2)
        
        nose_size = 8 + int(2 * math.sin(self.anim_timer * 2))
        pygame.draw.circle(screen, COLOR_GRAY, (x, y-1 + walk_offset), nose_size)
        
        pygame.draw.polygon(screen, skin_color, [(x-15, y-5 + walk_offset), (x-8, y+3 + walk_offset), (x-15, y+3 + walk_offset)])
        pygame.draw.polygon(screen, skin_color, [(x+15, y-5 + walk_offset), (x+8, y+3 + walk_offset), (x+15, y+3 + walk_offset)])
        
        arm_swing = int(5 * math.sin(self.walk_anim_timer * 2))
        pygame.draw.line(screen, skin_color, (x-18, y+5 + walk_offset), (x-35 + arm_swing, y+10 + walk_offset), 12)
        pygame.draw.line(screen, skin_color, (x+18, y+5 + walk_offset), (x+35 - arm_swing, y+10 + walk_offset), 12)
        
        leg_swing = int(4 * math.sin(self.walk_anim_timer * 2 + math.pi))
        pygame.draw.line(screen, skin_color, (x-10, y+35 + walk_offset), (x-15 + leg_swing, y+50 + walk_offset), 14)
        pygame.draw.line(screen, skin_color, (x+10, y+35 + walk_offset), (x+15 - leg_swing, y+50 + walk_offset), 14)
        
        if self.has_club:
            club_x = x - 45 + arm_swing
            club_y = y + 15 + walk_offset
            pygame.draw.rect(screen, COLOR_BROWN, (club_x - 8, club_y - 25, 16, 35))
            pygame.draw.circle(screen, COLOR_DARK_BROWN, (club_x, club_y - 25), 12)
        
        if self.enraged:
            rage_pulse = int(5 * math.sin(self.anim_timer * 8))
            pygame.draw.circle(screen, (255, 100, 50, 50 + rage_pulse), (x, y), 30 + rage_pulse)

    def draw_health_bar(self, screen, font):
        pass


class OgreMage(Enemy):
    def __init__(self, x, y, path, wave_num=1):
        super().__init__(x, y, path, wave_num)
        self.max_hp = 200 + wave_num * 30
        self.hp = self.max_hp
        self.speed = 0.7
        self.base_speed = 0.7
        self.reward = 60
        self.type = "ogre_mage"
        self.has_staff = True
        self.magic_glow = True

    def draw(self, screen, font):
        super().draw(screen, font)
        x, y = int(self.x), int(self.y)
        
        walk_offset = int(2 * math.sin(self.walk_anim_timer * 3))
        
        skin_color = (130, 60, 130)
        skin_light = (160, 90, 160)
        
        pygame.draw.ellipse(screen, skin_color, (x-18, y-10 + walk_offset, 36, 32))
        
        pygame.draw.circle(screen, skin_light, (x, y-8 + walk_offset), 16)
        
        hat_tilt = int(2 * math.sin(self.walk_anim_timer * 4))
        pygame.draw.polygon(screen, COLOR_PURPLE, [(x-12, y-20 + walk_offset), (x, y-35 + walk_offset + hat_tilt), (x+12, y-20 + walk_offset)])
        pygame.draw.circle(screen, COLOR_GOLD, (x, y-28 + walk_offset + hat_tilt), 4)
        
        pygame.draw.circle(screen, COLOR_RED, (x-5, y-8 + walk_offset), 4)
        pygame.draw.circle(screen, COLOR_WHITE, (x-4, y-9 + walk_offset), 1)
        pygame.draw.circle(screen, COLOR_RED, (x+5, y-8 + walk_offset), 4)
        pygame.draw.circle(screen, COLOR_WHITE, (x+4, y-9 + walk_offset), 1)
        
        pygame.draw.polygon(screen, COLOR_PURPLE, [(x-14, y-3 + walk_offset), (x-8, y+5 + walk_offset), (x-14, y+5 + walk_offset)])
        pygame.draw.polygon(screen, COLOR_PURPLE, [(x+14, y-3 + walk_offset), (x+8, y+5 + walk_offset), (x+14, y+5 + walk_offset)])
        
        arm_swing = int(4 * math.sin(self.walk_anim_timer * 3))
        pygame.draw.line(screen, skin_color, (x-10, y+2 + walk_offset), (x-20 + arm_swing, y-2 + walk_offset), 7)
        pygame.draw.line(screen, skin_color, (x+10, y+2 + walk_offset), (x+20 - arm_swing, y-2 + walk_offset), 7)
        
        leg_swing = int(3 * math.sin(self.walk_anim_timer * 3 + math.pi))
        pygame.draw.line(screen, skin_color, (x-8, y+22 + walk_offset), (x-12 + leg_swing, y+32 + walk_offset), 10)
        pygame.draw.line(screen, skin_color, (x+8, y+22 + walk_offset), (x+12 - leg_swing, y+32 + walk_offset), 10)
        
        if self.has_staff:
            staff_x = x + 25 - arm_swing
            staff_y = y + 5 + walk_offset
            pygame.draw.line(screen, COLOR_BROWN, (staff_x, staff_y), (staff_x, staff_y + 25), 5)
            pygame.draw.circle(screen, COLOR_PURPLE, (staff_x, staff_y), 8)
            
            magic_pulse = int(4 * math.sin(self.anim_timer * 6))
            pygame.draw.circle(screen, (200, 150, 255), (staff_x, staff_y - 5), 5 + magic_pulse)
            pygame.draw.circle(screen, (255, 200, 255), (staff_x, staff_y - 5), 3 + magic_pulse // 2)
        
        if self.magic_glow:
            glow_pulse = int(3 * math.sin(self.anim_timer * 5))
            glow_surface = pygame.Surface((40, 40), pygame.SRCALPHA)
            pygame.draw.circle(glow_surface, (150, 100, 200, 30 + glow_pulse), (20, 20), 15 + glow_pulse)
            screen.blit(glow_surface, (x - 20, y - 20 + walk_offset))

    def draw_health_bar(self, screen, font):
        pass


class EnemyNecromancer(Enemy):
    def __init__(self, x, y, path, wave_num=1):
        super().__init__(x, y, path, wave_num)
        self.max_hp = 180 + wave_num * 25
        self.hp = self.max_hp
        self.speed = 0.6
        self.base_speed = 0.6
        self.reward = 70
        self.type = "necromancer"
        self.has_scythe = True
        self.death_aura = True

    def draw(self, screen, font):
        super().draw(screen, font)
        x, y = int(self.x), int(self.y)
        
        walk_offset = int(2 * math.sin(self.walk_anim_timer * 2.5))
        
        robe_color = (40, 40, 60)
        skin_color = (200, 180, 180)
        
        pygame.draw.ellipse(screen, robe_color, (x-16, y-8 + walk_offset, 32, 30))
        
        pygame.draw.circle(screen, skin_color, (x, y-8 + walk_offset), 10)
        
        pygame.draw.polygon(screen, COLOR_BLACK, [(x-8, y-16 + walk_offset), (x-5, y-8 + walk_offset), (x-8, y-8 + walk_offset)])
        pygame.draw.polygon(screen, COLOR_BLACK, [(x+8, y-16 + walk_offset), (x+5, y-8 + walk_offset), (x+8, y-8 + walk_offset)])
        
        pygame.draw.circle(screen, COLOR_BLACK, (x-3, y-9 + walk_offset), 3)
        pygame.draw.circle(screen, COLOR_RED, (x-2, y-10 + walk_offset), 1)
        pygame.draw.circle(screen, COLOR_BLACK, (x+3, y-9 + walk_offset), 3)
        pygame.draw.circle(screen, COLOR_RED, (x+2, y-10 + walk_offset), 1)
        
        hood_points = [(x-12, y-5 + walk_offset), (x-5, y-20 + walk_offset), (x+5, y-20 + walk_offset), (x+12, y-5 + walk_offset)]
        pygame.draw.polygon(screen, COLOR_BLACK, hood_points)
        pygame.draw.polygon(screen, robe_color, [(x-10, y-3 + walk_offset), (x-4, y-18 + walk_offset), (x+4, y-18 + walk_offset), (x+10, y-3 + walk_offset)])
        
        arm_swing = int(3 * math.sin(self.walk_anim_timer * 2.5))
        pygame.draw.line(screen, robe_color, (x-10, y+2 + walk_offset), (x-18 + arm_swing, y-2 + walk_offset), 6)
        pygame.draw.line(screen, robe_color, (x+10, y+2 + walk_offset), (x+18 - arm_swing, y-2 + walk_offset), 6)
        
        leg_swing = int(3 * math.sin(self.walk_anim_timer * 2.5 + math.pi))
        pygame.draw.line(screen, COLOR_BLACK, (x-6, y+22 + walk_offset), (x-9 + leg_swing, y+30 + walk_offset), 6)
        pygame.draw.line(screen, COLOR_BLACK, (x+6, y+22 + walk_offset), (x+9 - leg_swing, y+30 + walk_offset), 6)
        
        if self.has_scythe:
            scythe_angle = math.sin(self.walk_anim_timer * 3) * 0.2
            scythe_x = x - 22 + arm_swing
            scythe_y = y - 5 + walk_offset
            pygame.draw.line(screen, COLOR_GRAY, (scythe_x, scythe_y), 
                           (scythe_x + int(25 * math.cos(scythe_angle)), scythe_y + int(25 * math.sin(scythe_angle))), 4)
            pygame.draw.arc(screen, COLOR_GRAY, 
                          (scythe_x + int(20 * math.cos(scythe_angle)) - 15, 
                           scythe_y + int(20 * math.sin(scythe_angle)) - 15, 
                           30, 30), 
                          scythe_angle - math.pi/2, scythe_angle + math.pi/2, 4)
        
        if self.death_aura:
            aura_pulse = int(4 * math.sin(self.anim_timer * 4))
            aura_surface = pygame.Surface((50, 50), pygame.SRCALPHA)
            pygame.draw.circle(aura_surface, (80, 50, 80, 20 + aura_pulse), (25, 25), 20 + aura_pulse)
            screen.blit(aura_surface, (x - 25, y - 25 + walk_offset))

    def draw_health_bar(self, screen, font):
        pass


class DarkKnight(Enemy):
    def __init__(self, x, y, path, wave_num=1):
        super().__init__(x, y, path, wave_num)
        self.max_hp = 400 + wave_num * 50
        self.hp = self.max_hp
        self.speed = 0.6
        self.base_speed = 0.6
        self.reward = 100
        self.type = "dark_knight"
        self.has_sword = True
        self.has_shield = True
        self.armor_color = (120, 120, 140)

    def draw(self, screen, font):
        super().draw(screen, font)
        x, y = int(self.x), int(self.y)
        
        walk_offset = int(2 * math.sin(self.walk_anim_timer * 2.5))
        
        armor_color = (120, 120, 140)
        armor_light = (150, 150, 170)
        dark_color = (40, 40, 60)
        
        pygame.draw.ellipse(screen, dark_color, (x-18, y-5 + walk_offset, 36, 35))
        
        pygame.draw.polygon(screen, armor_color, [(x-18, y-8 + walk_offset), (x-8, y-30 + walk_offset), 
                                                 (x+8, y-30 + walk_offset), (x+18, y-8 + walk_offset)])
        pygame.draw.line(screen, armor_light, (x, y-30 + walk_offset), (x, y-5 + walk_offset), 3)
        
        visor_offset = int(2 * math.sin(self.walk_anim_timer * 3))
        pygame.draw.polygon(screen, COLOR_BLACK, [(x-8, y-12 + walk_offset), (x-4, y-22 + walk_offset + visor_offset), 
                                                  (x+4, y-22 + walk_offset + visor_offset), (x+8, y-12 + walk_offset)])
        
        pygame.draw.rect(screen, armor_color, (x-15, y+5 + walk_offset, 30, 22))
        pygame.draw.line(screen, armor_light, (x, y+5 + walk_offset), (x, y+27 + walk_offset), 2)
        pygame.draw.line(screen, armor_light, (x-10, y+12 + walk_offset), (x+10, y+12 + walk_offset), 2)
        pygame.draw.line(screen, armor_light, (x-10, y+20 + walk_offset), (x+10, y+20 + walk_offset), 2)
        
        arm_swing = int(4 * math.sin(self.walk_anim_timer * 2.5))
        pygame.draw.line(screen, armor_color, (x-15, y+8 + walk_offset), (x-30 + arm_swing, y+3 + walk_offset), 10)
        pygame.draw.line(screen, armor_color, (x+15, y+8 + walk_offset), (x+30 - arm_swing, y+3 + walk_offset), 10)
        
        leg_swing = int(3 * math.sin(self.walk_anim_timer * 2.5 + math.pi))
        pygame.draw.line(screen, armor_color, (x-10, y+27 + walk_offset), (x-14 + leg_swing, y+40 + walk_offset), 10)
        pygame.draw.line(screen, armor_color, (x+10, y+27 + walk_offset), (x+14 - leg_swing, y+40 + walk_offset), 10)
        
        if self.has_shield:
            shield_x = x + 35 - arm_swing
            shield_y = y + 10 + walk_offset
            pygame.draw.circle(screen, armor_color, (shield_x, shield_y), 14)
            pygame.draw.circle(screen, armor_light, (shield_x, shield_y), 10)
            pygame.draw.polygon(screen, COLOR_RED, [(shield_x-3, shield_y-5), (shield_x, shield_y), (shield_x+3, shield_y-5), (shield_x, shield_y+5)])
        
        if self.has_sword:
            sword_angle = math.sin(self.walk_anim_timer * 3) * 0.15
            sword_x = x - 35 + arm_swing
            sword_y = y + 5 + walk_offset
            pygame.draw.line(screen, COLOR_GRAY, (sword_x, sword_y), 
                           (sword_x + int(30 * math.cos(sword_angle)), sword_y + int(30 * math.sin(sword_angle))), 5)
            pygame.draw.polygon(screen, COLOR_GOLD, 
                             [(sword_x + int(28 * math.cos(sword_angle)), sword_y + int(28 * math.sin(sword_angle))),
                              (sword_x + int(35 * math.cos(sword_angle)), sword_y + int(35 * math.sin(sword_angle))),
                              (sword_x + int(26 * math.cos(sword_angle) + 3 * math.sin(sword_angle)), 
                               sword_y + int(26 * math.sin(sword_angle) - 3 * math.cos(sword_angle)))])

    def draw_health_bar(self, screen, font):
        pass


class Demon(Enemy):
    def __init__(self, x, y, path, wave_num=1):
        super().__init__(x, y, path, wave_num)
        self.max_hp = 500 + wave_num * 60
        self.hp = self.max_hp
        self.speed = 0.7
        self.base_speed = 0.7
        self.reward = 150
        self.type = "demon"
        self.has_wings = True
        self.has_tail = True
        self.fire_aura = True

    def draw(self, screen, font):
        super().draw(screen, font)
        x, y = int(self.x), int(self.y)
        
        walk_offset = int(2 * math.sin(self.walk_anim_timer * 3))
        
        skin_color = (180, 60, 40)
        skin_dark = (140, 40, 30)
        fire_color = (255, 100, 30)
        
        if self.has_wings:
            wing_flap = int(5 * math.sin(self.walk_anim_timer * 6))
            pygame.draw.polygon(screen, skin_dark, [(x-20, y-10 + walk_offset), 
                                                   (x-40 + wing_flap, y-30 + walk_offset), 
                                                   (x-15, y+5 + walk_offset)])
            pygame.draw.polygon(screen, skin_dark, [(x+20, y-10 + walk_offset), 
                                                   (x+40 - wing_flap, y-30 + walk_offset), 
                                                   (x+15, y+5 + walk_offset)])
        
        pygame.draw.ellipse(screen, skin_color, (x-18, y-5 + walk_offset, 36, 32))
        
        pygame.draw.circle(screen, skin_color, (x, y-8 + walk_offset), 15)
        
        horn_tilt = int(2 * math.sin(self.walk_anim_timer * 4))
        pygame.draw.polygon(screen, COLOR_ORANGE, [(x-8, y-12 + walk_offset), 
                                                  (x-12, y-28 + walk_offset + horn_tilt), 
                                                  (x-4, y-18 + walk_offset)])
        pygame.draw.polygon(screen, COLOR_ORANGE, [(x+8, y-12 + walk_offset), 
                                                  (x+12, y-28 + walk_offset - horn_tilt), 
                                                  (x+4, y-18 + walk_offset)])
        
        pygame.draw.circle(screen, COLOR_RED, (x-5, y-10 + walk_offset), 4)
        pygame.draw.circle(screen, COLOR_YELLOW, (x-4, y-11 + walk_offset), 2)
        pygame.draw.circle(screen, COLOR_RED, (x+5, y-10 + walk_offset), 4)
        pygame.draw.circle(screen, COLOR_YELLOW, (x+4, y-11 + walk_offset), 2)
        
        pygame.draw.line(screen, COLOR_BLACK, (x-4, y-3 + walk_offset), (x-6, y+2 + walk_offset), 2)
        pygame.draw.line(screen, COLOR_BLACK, (x+4, y-3 + walk_offset), (x+6, y+2 + walk_offset), 2)
        
        arm_swing = int(4 * math.sin(self.walk_anim_timer * 3))
        pygame.draw.line(screen, skin_color, (x-12, y+2 + walk_offset), (x-25 + arm_swing, y-2 + walk_offset), 9)
        pygame.draw.line(screen, skin_color, (x+12, y+2 + walk_offset), (x+25 - arm_swing, y-2 + walk_offset), 9)
        
        leg_swing = int(4 * math.sin(self.walk_anim_timer * 3 + math.pi))
        pygame.draw.line(screen, skin_color, (x-10, y+27 + walk_offset), (x-15 + leg_swing, y+40 + walk_offset), 10)
        pygame.draw.line(screen, skin_color, (x+10, y+27 + walk_offset), (x+15 - leg_swing, y+40 + walk_offset), 10)
        
        if self.has_tail:
            tail_wag = int(5 * math.sin(self.walk_anim_timer * 5))
            pygame.draw.line(screen, skin_color, (x+15, y+15 + walk_offset), 
                           (x+25 + tail_wag, y+25 + walk_offset), 6)
            pygame.draw.circle(screen, COLOR_ORANGE, (x+28 + tail_wag, y+28 + walk_offset), 5)
        
        if self.fire_aura:
            fire_pulse = int(5 * math.sin(self.anim_timer * 6))
            fire_surface = pygame.Surface((50, 50), pygame.SRCALPHA)
            pygame.draw.circle(fire_surface, (255, 100, 50, 30 + fire_pulse), (25, 25), 20 + fire_pulse)
            screen.blit(fire_surface, (x - 25, y - 25 + walk_offset))

    def draw_health_bar(self, screen, font):
        pass


class DragonWhelp(Enemy):
    def __init__(self, x, y, path, wave_num=1):
        super().__init__(x, y, path, wave_num)
        self.max_hp = 600 + wave_num * 80
        self.hp = self.max_hp
        self.speed = 0.8
        self.base_speed = 0.8
        self.reward = 200
        self.type = "dragon_whelp"
        self.has_wings = True
        self.has_fire_breath = True
        self.scale_color = COLOR_RED

    def draw(self, screen, font):
        super().draw(screen, font)
        x, y = int(self.x), int(self.y)
        
        bob = int(3 * math.sin(self.walk_anim_timer * 4))
        
        body_color = (180, 60, 60)
        body_light = (220, 100, 100)
        belly_color = (255, 150, 100)
        
        if self.has_wings:
            wing_flap = int(6 * math.sin(self.walk_anim_timer * 5))
            pygame.draw.polygon(screen, body_color, [(x-5, y-15 + bob), 
                                                   (x-30 + wing_flap, y-35 + bob), 
                                                   (x+5, y-5 + bob)])
            pygame.draw.polygon(screen, belly_color, [(x-5, y-12 + bob), 
                                                    (x-25 + wing_flap, y-30 + bob), 
                                                    (x+5, y-3 + bob)])
        
        pygame.draw.ellipse(screen, body_color, (x-22, y-5 + bob, 44, 26))
        
        pygame.draw.ellipse(screen, belly_color, (x-18, y+5 + bob, 36, 14))
        
        pygame.draw.circle(screen, body_color, (x-18, y-10 + bob), 12)
        
        eye_offset = int(2 * math.sin(self.walk_anim_timer * 6))
        pygame.draw.circle(screen, COLOR_YELLOW, (x-22, y-12 + bob + eye_offset), 4)
        pygame.draw.circle(screen, COLOR_BLACK, (x-21, y-12 + bob + eye_offset), 2)
        
        horn_angle = int(2 * math.sin(self.walk_anim_timer * 4))
        pygame.draw.polygon(screen, COLOR_ORANGE, [(x-22, y-18 + bob), 
                                                  (x-24, y-28 + bob + horn_angle), 
                                                  (x-18, y-20 + bob)])
        pygame.draw.polygon(screen, COLOR_ORANGE, [(x-14, y-18 + bob), 
                                                  (x-12, y-28 + bob - horn_angle), 
                                                  (x-16, y-20 + bob)])
        
        leg_swing = int(4 * math.sin(self.walk_anim_timer * 4 + math.pi))
        pygame.draw.line(screen, body_color, (x-10, y+18 + bob), (x-14 + leg_swing, y+28 + bob), 6)
        pygame.draw.line(screen, body_color, (x+2, y+18 + bob), (x+6 - leg_swing, y+28 + bob), 6)
        pygame.draw.line(screen, body_color, (x+14, y+15 + bob), (x+18 + leg_swing, y+25 + bob), 5)
        
        tail_wag = int(5 * math.sin(self.walk_anim_timer * 6))
        tail_points = [(x+22, y), (x+45 + tail_wag, y-5), (x+55 + tail_wag, y+5)]
        pygame.draw.polygon(screen, body_color, tail_points)
        pygame.draw.circle(screen, COLOR_ORANGE, (x+55 + tail_wag, y+5), 6)
        
        if self.has_fire_breath:
            fire_pulse = int(8 * math.sin(self.anim_timer * 10))
            fire_surface = pygame.Surface((40, 20), pygame.SRCALPHA)
            pygame.draw.polygon(fire_surface, (255, 200, 50, 100), 
                              [(0, 10), (25 + fire_pulse, 5), (30 + fire_pulse, 10), (25 + fire_pulse, 15)])
            pygame.draw.polygon(fire_surface, (255, 100, 30, 80), 
                              [(0, 10), (15 + fire_pulse, 7), (20 + fire_pulse, 10), (15 + fire_pulse, 13)])
            screen.blit(fire_surface, (x - 35, y - 10 + bob))

    def draw_health_bar(self, screen, font):
        pass


class Wiznan(Enemy):
    def __init__(self, x, y, path, wave_num=1):
        super().__init__(x, y, path, wave_num)
        self.max_hp = 1000 + wave_num * 100
        self.hp = self.max_hp
        self.speed = 0.4
        self.base_speed = 0.4
        self.reward = 500
        self.type = "wiznan"
        self.has_crown = True
        self.has_staff = True
        self.magic_orb = True
        self.phase = 1

    def draw(self, screen, font):
        super().draw(screen, font)
        x, y = int(self.x), int(self.y)
        
        walk_offset = int(2 * math.sin(self.walk_anim_timer * 2))
        
        robe_color = (60, 20, 80)
        skin_color = (220, 200, 240)
        
        magic_glow = int(150 + 50 * math.sin(self.anim_timer * 3))
        
        if self.has_crown:
            crown_tilt = int(2 * math.sin(self.walk_anim_timer * 3))
            pygame.draw.polygon(screen, COLOR_GOLD, [(x-15, y-15 + walk_offset), 
                                                    (x-10, y-30 + walk_offset + crown_tilt), 
                                                    (x, y-25 + walk_offset + crown_tilt), 
                                                    (x+10, y-30 + walk_offset + crown_tilt), 
                                                    (x+15, y-15 + walk_offset)])
            pygame.draw.circle(screen, COLOR_GOLD, (x, y-28 + walk_offset + crown_tilt), 5)
        
        pygame.draw.ellipse(screen, robe_color, (x-20, y-5 + walk_offset, 40, 35))
        
        pygame.draw.circle(screen, skin_color, (x, y-8 + walk_offset), 16)
        
        eye_glow = (255, 100, 255) if self.phase >= 2 else (200, 150, 255)
        pygame.draw.circle(screen, eye_glow, (x-5, y-10 + walk_offset), 5)
        pygame.draw.circle(screen, COLOR_WHITE, (x-4, y-11 + walk_offset), 2)
        pygame.draw.circle(screen, eye_glow, (x+5, y-10 + walk_offset), 5)
        pygame.draw.circle(screen, COLOR_WHITE, (x+4, y-11 + walk_offset), 2)
        
        pygame.draw.line(screen, COLOR_BLACK, (x-3, y-2 + walk_offset), (x-6, y+4 + walk_offset), 2)
        pygame.draw.line(screen, COLOR_BLACK, (x+3, y-2 + walk_offset), (x+6, y+4 + walk_offset), 2)
        
        hood_points = [(x-18, y-5 + walk_offset), (x-8, y-20 + walk_offset), (x+8, y-20 + walk_offset), (x+18, y-5 + walk_offset)]
        pygame.draw.polygon(screen, robe_color, hood_points)
        
        arm_swing = int(3 * math.sin(self.walk_anim_timer * 2))
        pygame.draw.line(screen, robe_color, (x-12, y+2 + walk_offset), (x-25 + arm_swing, y-3 + walk_offset), 8)
        pygame.draw.line(screen, robe_color, (x+12, y+2 + walk_offset), (x+25 - arm_swing, y-3 + walk_offset), 8)
        
        leg_swing = int(3 * math.sin(self.walk_anim_timer * 2 + math.pi))
        pygame.draw.line(screen, COLOR_BLACK, (x-8, y+30 + walk_offset), (x-12 + leg_swing, y+42 + walk_offset), 10)
        pygame.draw.line(screen, COLOR_BLACK, (x+8, y+30 + walk_offset), (x+12 - leg_swing, y+42 + walk_offset), 10)
        
        if self.has_staff:
            staff_x = x - 30 + arm_swing
            staff_y = y + 5 + walk_offset
            pygame.draw.line(screen, COLOR_BROWN, (staff_x, staff_y), (staff_x, staff_y + 30), 6)
            pygame.draw.circle(screen, COLOR_GOLD, (staff_x, staff_y), 8)
            
            orb_pulse = int(5 * math.sin(self.anim_timer * 8))
            pygame.draw.circle(screen, (200, 100, 255), (staff_x, staff_y - 8), 8 + orb_pulse)
            pygame.draw.circle(screen, (255, 150, 255), (staff_x, staff_y - 8), 5 + orb_pulse // 2)
        
        magic_aura_pulse = int(8 * math.sin(self.anim_timer * 4))
        aura_surface = pygame.Surface((60, 60), pygame.SRCALPHA)
        pygame.draw.circle(aura_surface, (150, 80, 200, 40 + magic_aura_pulse), (30, 30), 25 + magic_aura_pulse)
        screen.blit(aura_surface, (x - 30, y - 30 + walk_offset))
        
        if self.phase >= 2:
            lightning_pulse = int(3 * math.sin(self.anim_timer * 10))
            for i in range(3):
                lx = x + (i - 1) * 15
                ly = y - 15 + walk_offset
                pygame.draw.line(screen, (200 + lightning_pulse, 200 + lightning_pulse, 255), 
                               (lx, ly), (lx + lightning_pulse, ly + 10), 2)

    def draw_health_bar(self, screen, font):
        pass


class EnemyFactory:
    @staticmethod
    def create_enemy(enemy_type, x, y, path, wave_num=1):
        if enemy_type == EnemyType.GOBLIN:
            return Goblin(x, y, path, wave_num)
        elif enemy_type == EnemyType.SKELETON:
            return Skeleton(x, y, path, wave_num)
        elif enemy_type == EnemyType.ORC:
            return Orc(x, y, path, wave_num)
        elif enemy_type == EnemyType.SHADOW_WOLF:
            return ShadowWolf(x, y, path, wave_num)
        elif enemy_type == EnemyType.TROLL:
            return Troll(x, y, path, wave_num)
        elif enemy_type == EnemyType.OGRE_MAGE:
            return OgreMage(x, y, path, wave_num)
        elif enemy_type == EnemyType.NECROMANCER:
            return EnemyNecromancer(x, y, path, wave_num)
        elif enemy_type == EnemyType.DARK_KNIGHT:
            return DarkKnight(x, y, path, wave_num)
        elif enemy_type == EnemyType.DEMON:
            return Demon(x, y, path, wave_num)
        elif enemy_type == EnemyType.DRAGON_WHELP:
            return DragonWhelp(x, y, path, wave_num)
        elif enemy_type == EnemyType.WIZNAN:
            return Wiznan(x, y, path, wave_num)
        return Goblin(x, y, path, wave_num)


class Tower:
    def __init__(self, x, y, tower_type):
        self.x = x
        self.y = y
        self.tower_type = tower_type
        self.level = 1
        self.damage = 10
        self.range = 100
        self.attack_speed = 1.0
        self.target = None
        self.last_attack_time = 0
        self.cost = 100
        self.sell_value = 75
        self.upgrade_cost = 50
        self.anim_timer = 0
        self.max_hp = 100
        self.hp = self.max_hp
        self.alive = True
        self.skill_cooldown = 30000
        self.last_skill_time = 0
        self.skill_ready = True
        self.skill_name = ""
        self.particles = []
        self.skill_cooldown_timer = 0

    def update(self, enemies, current_time_ms, projectiles):
        self.anim_timer += 0.05
        time_since_last_attack = current_time_ms - self.last_attack_time
        attack_interval = 1000 / self.attack_speed
        
        for particle in list(self.particles):
            particle.update(0.05)
            if not particle.alive:
                self.particles.remove(particle)
        
        self.update_skill_cooldown(current_time_ms)
        
        self.find_target(enemies)
        
        if time_since_last_attack >= attack_interval:
            if self.target and self.target.alive:
                self.attack(enemies, current_time_ms, projectiles)
    
    def try_use_skill(self, enemies, projectiles):
        if not self.skill_ready:
            return False
        
        has_enemy_in_range = False
        for enemy in enemies:
            if enemy.alive:
                dist = math.hypot(self.x - enemy.x, self.y - enemy.y)
                if dist <= self.range:
                    has_enemy_in_range = True
                    break
        
        if not has_enemy_in_range:
            return False
        
        if hasattr(self, 'use_skill') and callable(getattr(self, 'use_skill')):
            self.use_skill(enemies, projectiles)
            self.skill_ready = False
            self.last_skill_time = pygame.time.get_ticks()
            return True
        return False
    
    def update_skill_cooldown(self, current_time_ms):
        if not self.skill_ready:
            time_since_skill = current_time_ms - self.last_skill_time
            if time_since_skill >= self.skill_cooldown:
                self.skill_ready = True

    def find_target(self, enemies):
        best_target = None
        best_score = -float('inf')
        
        for enemy in enemies:
            if enemy.alive:
                dist = math.hypot(self.x - enemy.x, self.y - enemy.y)
                if dist <= self.range:
                    hp_ratio = 1 - (enemy.hp / enemy.max_hp)
                    path_progress = enemy.path_index / max(len(enemy.path) - 1, 1)
                    
                    score = hp_ratio * 0.6 + path_progress * 0.4
                    
                    if score > best_score:
                        best_score = score
                        best_target = enemy
        
        self.target = best_target

    def attack(self, enemies, current_time_ms, projectiles):
        self.last_attack_time = current_time_ms
        if self.target and self.target.alive:
            dx = self.target.x - self.x
            dy = self.target.y - self.y
            dist = math.hypot(dx, dy)
            if dist > 0:
                angle = math.atan2(dy, dx)
                
                tower_type_name = self.tower_type.name.lower()
                if tower_type_name == "archer":
                    projectile_type = "arrow"
                elif tower_type_name == "cannon":
                    projectile_type = "cannonball"
                elif tower_type_name == "mage":
                    projectile_type = "magic"
                elif tower_type_name == "ice":
                    projectile_type = "ice"
                elif tower_type_name == "lightning":
                    projectile_type = "lightning"
                else:
                    projectile_type = tower_type_name
                
                for i in range(-1, 2):
                    spread_angle = angle + math.radians(i * 8)
                    projectile = Projectile(self.x, self.y, 
                                           self.x + math.cos(spread_angle) * 500,
                                           self.y + math.sin(spread_angle) * 500,
                                           self.damage, projectile_type)
                    projectiles.append(projectile)
                
                for i in range(8):
                    angle_particle = angle + math.radians((i - 3) * 20)
                    vx = math.cos(angle_particle) * 4
                    vy = math.sin(angle_particle) * 4
                    self.particles.append(Particle(self.x, self.y, vx, vy, (255, 200, 100), 4, 0.5))

    def upgrade(self):
        if self.level < 3:
            self.level += 1
            self.damage *= 1.5
            self.range *= 1.1
            self.attack_speed *= 1.2
            self.upgrade_cost = int(self.upgrade_cost * 1.5)
            self.sell_value = int(self.cost * 0.75)
            return True
        return False

    def get_upgrade_cost(self):
        return self.upgrade_cost

    def get_sell_value(self):
        return self.sell_value
    
    def take_damage(self, damage):
        self.hp -= damage
        if self.hp <= 0:
            self.hp = 0
            self.alive = False

    def draw(self, screen, font):
        for particle in self.particles:
            if particle.alive:
                alpha = int(255 * (particle.lifetime / particle.max_lifetime))
                sz = max(1, int(particle.size * (particle.lifetime / particle.max_lifetime)))
                temp_surface = pygame.Surface((sz * 2, sz * 2), pygame.SRCALPHA)
                temp_color = (particle.color[0], particle.color[1], particle.color[2], alpha)
                pygame.draw.circle(temp_surface, temp_color, (sz, sz), sz)
                screen.blit(temp_surface, (int(particle.x) - sz, int(particle.y) - sz))


class ArcherTower(Tower):
    def __init__(self, x, y):
        super().__init__(x, y, TowerType.ARCHER)
        self.damage = 3
        self.range = 150
        self.attack_speed = 2.5
        self.cost = 100
        self.upgrade_cost = 50
        self.color = (100, 180, 255)
        self.shape = 'triangle'

    def update(self, enemies, current_time_ms, projectiles):
        super().update(enemies, current_time_ms, projectiles)

    def attack(self, enemies, current_time_ms, projectiles):
        self.last_attack_time = current_time_ms
        if self.target and self.target.alive:
            dx = self.target.x - self.x
            dy = self.target.y - self.y
            dist = math.hypot(dx, dy)
            if dist > 0:
                angle = math.atan2(dy, dx)
                
                for i in range(6):
                    spread_angle = angle + math.radians((i - 3) * 5)
                    projectile = Projectile(self.x, self.y, 
                                           self.x + math.cos(spread_angle) * 500,
                                           self.y + math.sin(spread_angle) * 500,
                                           self.damage, 'arrow')
                    projectiles.append(projectile)
                
                for i in range(6):
                    angle_particle = angle + math.radians((i - 2) * 25)
                    vx = math.cos(angle_particle) * 3
                    vy = math.sin(angle_particle) * 3
                    self.particles.append(Particle(self.x, self.y, vx, vy, (200, 220, 255), 3, 0.4))

    def draw(self, screen, font):
        super().draw(screen, font)
        
        x, y = self.x, self.y
        pygame.draw.polygon(screen, self.color, [(x, y-20), (x-15, y+15), (x+15, y+15)])
        pygame.draw.polygon(screen, (80, 150, 220), [(x, y-15), (x-10, y+5), (x+10, y+5)])
        
        self.draw_health_bar(screen, font)

    def draw_health_bar(self, screen, font):
        pass


class CannonTower(Tower):
    def __init__(self, x, y):
        super().__init__(x, y, TowerType.CANNON)
        self.damage = 120
        self.range = 120
        self.attack_speed = 0.2
        self.cost = 200
        self.upgrade_cost = 100
        self.splash_radius = 80
        self.color = (255, 150, 100)
        self.shape = 'hexagon'
        self.skill_cooldown = 15000
        self.skill_name = "燃烧弹"
        self.skill_active = False
        self.skill_charge = 0
        self.skill_duration = 2000

    def update(self, enemies, current_time_ms, projectiles):
        super().update(enemies, current_time_ms, projectiles)
        
        if self.skill_active:
            self.skill_charge -= 1
            if self.skill_charge <= 0:
                self.skill_active = False
                if hasattr(self, 'base_attack_speed'):
                    self.attack_speed = self.base_attack_speed

    def attack(self, enemies, current_time_ms, projectiles):
        self.last_attack_time = current_time_ms
        if self.target and self.target.alive:
            dx = self.target.x - self.x
            dy = self.target.y - self.y
            dist = math.hypot(dx, dy)
            if dist > 0:
                angle = math.atan2(dy, dx)
                
                projectile = CannonballProjectile(self.x, self.y, 
                                                 self.target.x, self.target.y,
                                                 self.damage, self.splash_radius)
                projectiles.append(projectile)
                
                for i in range(10):
                    angle_particle = angle + math.radians((i - 4) * 30)
                    speed = 3 + random.random() * 2
                    vx = math.cos(angle_particle) * speed
                    vy = math.sin(angle_particle) * speed
                    self.particles.append(Particle(self.x, self.y, vx, vy, (255, 150, 80), 5, 0.6))

    def draw(self, screen, font):
        super().draw(screen, font)
        
        x, y = self.x, self.y
        points = []
        for i in range(6):
            angle = i * 60
            px = x + 15 * math.cos(math.radians(angle))
            py = y + 15 * math.sin(math.radians(angle))
            points.append((px, py))
        pygame.draw.polygon(screen, self.color, points)
        pygame.draw.circle(screen, (200, 100, 50), (x, y), 8)
        
        if self.skill_active:
            rr = 22 + int(6 * math.sin(self.anim_timer * 8))
            pygame.draw.circle(screen, (255, 100, 50), (x, y), rr, 3)
            pygame.draw.circle(screen, (255, 150, 100), (x, y), rr-6, 2)
        
        self.draw_health_bar(screen, font)

    def draw_health_bar(self, screen, font):
        pass
    
    def use_skill(self, enemies, projectiles, current_time_ms=None):
        if current_time_ms is None:
            current_time_ms = pygame.time.get_ticks()
        
        time_since_last_skill = current_time_ms - self.last_skill_time
        if time_since_last_skill < self.skill_cooldown:
            return
        
        if not self.target or not self.target.alive:
            return
        
        self.last_skill_time = current_time_ms
        self.skill_active = True
        self.skill_charge = 50
        
        projectile = FireballProjectile(self.x, self.y, self.target.x, self.target.y,
                                       self.damage * 2, self.splash_radius * 1.5)
        projectiles.append(projectile)

        for i in range(15):
            angle = i * 24
            speed = 2.5 + random.random() * 2.5
            px = self.x + 25 * math.cos(math.radians(angle))
            py = self.y + 25 * math.sin(math.radians(angle))
            vx = math.cos(math.radians(angle)) * speed
            vy = math.sin(math.radians(angle)) * speed
            self.particles.append(Particle(px, py, vx, vy, (255, 100, 50), 5, 1.8))


class MagicTower(Tower):
    def __init__(self, x, y):
        super().__init__(x, y, TowerType.MAGE)
        self.damage = 45
        self.range = 150
        self.attack_speed = 0.6
        self.cost = 300
        self.upgrade_cost = 150
        self.magic_radius = 50
        self.color = (180, 100, 255)
        self.shape = 'octagon'
        self.skill_cooldown = 30000
        self.skill_name = "魔法阵"
        self.magic_damage = 8
        self.slow_factor = 0.5
        self.slow_duration = 1.0
        self.skill_duration = 2500

    def attack(self, enemies, current_time_ms, projectiles):
        self.last_attack_time = current_time_ms
        if self.target and self.target.alive:
            dx = self.target.x - self.x
            dy = self.target.y - self.y
            dist = math.hypot(dx, dy)
            if dist > 0:
                angle = math.atan2(dy, dx)
                
                projectile = MagicProjectile(self.x, self.y, 
                                           self.target.x, self.target.y,
                                           self.damage)
                projectiles.append(projectile)
                
                for i in range(6):
                    angle_particle = angle + math.radians((i - 2.5) * 30)
                    vx = math.cos(angle_particle) * 2
                    vy = math.sin(angle_particle) * 2
                    self.particles.append(Particle(self.x, self.y, vx, vy, (180, 100, 255), 3, 0.5))

    def draw(self, screen, font):
        super().draw(screen, font)
        
        x, y = self.x, self.y
        points = []
        for i in range(8):
            angle = i * 45 - 22.5
            px = x + 15 * math.cos(math.radians(angle))
            py = y + 15 * math.sin(math.radians(angle))
            points.append((px, py))
        pygame.draw.polygon(screen, self.color, points)
        pygame.draw.circle(screen, (150, 80, 220), (x, y), 8)
        rr = 18 + int(4 * math.sin(self.anim_timer * 3))
        pygame.draw.circle(screen, self.color, (x, y), rr, 2)
        
        self.draw_health_bar(screen, font)

    def draw_health_bar(self, screen, font):
        pass
    
    def use_skill(self, enemies, projectiles):
        if not self.target or not self.target.alive:
            return
        
        projectile = MagicCircleProjectile(self.target.x, self.target.y,
                                         self.magic_damage, self.magic_radius,
                                         self.slow_factor, self.slow_duration)
        projectiles.append(projectile)
        
        for i in range(20):
            angle = i * 18
            px = self.target.x + 35 * math.cos(math.radians(angle))
            py = self.target.y + 35 * math.sin(math.radians(angle))
            vx = math.cos(math.radians(angle)) * 2
            vy = math.sin(math.radians(angle)) * 2
            self.particles.append(Particle(px, py, vx, vy, (180, 100, 255), 4, 1.5))


class IceTower(Tower):
    def __init__(self, x, y):
        super().__init__(x, y, TowerType.ICE)
        self.damage = 12
        self.range = 130
        self.attack_speed = 1.0
        self.cost = 150
        self.upgrade_cost = 75
        self.slow_factor = 0.35
        self.slow_duration = 2.0
        self.color = (100, 200, 255)
        self.shape = 'diamond'
        self.skill_cooldown = 30000
        self.skill_name = "冰冻球"
        self.frozen_duration = 3.0
        self.skill_duration = 2000

    def attack(self, enemies, current_time_ms, projectiles):
        self.last_attack_time = current_time_ms
        if self.target and self.target.alive:
            dx = self.target.x - self.x
            dy = self.target.y - self.y
            dist = math.hypot(dx, dy)
            if dist > 0:
                angle = math.atan2(dy, dx)
                
                projectile = IceProjectile(self.x, self.y, 
                                          self.target.x, self.target.y,
                                          self.damage, self.slow_factor, self.slow_duration)
                projectiles.append(projectile)
                
                for i in range(4):
                    angle_particle = angle + math.radians((i - 1.5) * 30)
                    vx = math.cos(angle_particle) * 2.5
                    vy = math.sin(angle_particle) * 2.5
                    self.particles.append(Particle(self.x, self.y, vx, vy, (100, 200, 255), 3, 0.4))

    def draw(self, screen, font):
        super().draw(screen, font)
        
        x, y = self.x, self.y
        pygame.draw.polygon(screen, self.color, [(x, y-18), (x+18, y), (x, y+18), (x-18, y)])
        pygame.draw.polygon(screen, (80, 180, 230), [(x, y-12), (x+12, y), (x, y+12), (x-12, y)])
        pygame.draw.polygon(screen, COLOR_WHITE, [(x, y-20), (x-6, y-8), (x+6, y-8)])
        
        self.draw_health_bar(screen, font)

    def draw_health_bar(self, screen, font):
        pass
    
    def use_skill(self, enemies, projectiles):
        if not self.target or not self.target.alive:
            return
        
        projectile = BigIceballProjectile(self.x, self.y, 
                                         self.target.x, self.target.y,
                                         self.damage * 4, self.range * 0.5,
                                         self.frozen_duration, self.slow_factor)
        projectiles.append(projectile)
        
        for i in range(20):
            angle = i * 18
            px = self.x + 30 * math.cos(math.radians(angle))
            py = self.y + 30 * math.sin(math.radians(angle))
            vx = math.cos(math.radians(angle)) * 2.5
            vy = math.sin(math.radians(angle)) * 2.5
            self.particles.append(Particle(px, py, vx, vy, (100, 200, 255), 5, 1.5))


class LightningTower(Tower):
    def __init__(self, x, y):
        super().__init__(x, y, TowerType.LIGHTNING)
        self.damage = 35
        self.range = 140
        self.attack_speed = 0.5
        self.cost = 250
        self.upgrade_cost = 125
        self.chain_count = 3
        self.chain_range = 80
        self.color = (255, 200, 100)
        self.shape = 'star'
        self.skill_cooldown = 30000
        self.skill_name = "闪电光束"
        self.skill_chain_count = 5
        self.skill_duration = 3000

    def attack(self, enemies, current_time_ms, projectiles):
        self.last_attack_time = current_time_ms
        if self.target and self.target.alive:
            projectile = ChainLightningProjectile(self.x, self.y, self.target, 
                                                self.damage, enemies, 
                                                self.chain_count, self.chain_range)
            projectiles.append(projectile)
            
            for i in range(6):
                angle = i * 60
                px = self.x + 20 * math.cos(math.radians(angle))
                py = self.y + 20 * math.sin(math.radians(angle))
                vx = math.cos(math.radians(angle)) * 3
                vy = math.sin(math.radians(angle)) * 3
                self.particles.append(Particle(px, py, vx, vy, (255, 255, 200), 3, 0.4))

    def draw(self, screen, font):
        super().draw(screen, font)
        
        x, y = self.x, self.y
        points = []
        for i in range(5):
            angle = i * 72
            px = x + 15 * math.cos(math.radians(angle - 90))
            py = y + 15 * math.sin(math.radians(angle - 90))
            points.append((px, py))
            inner_px = x + 7 * math.cos(math.radians(angle - 90 + 36))
            inner_py = y + 7 * math.sin(math.radians(angle - 90 + 36))
            points.append((inner_px, inner_py))
        pygame.draw.polygon(screen, self.color, points)
        bob = int(3 * math.sin(self.anim_timer * 4))
        pygame.draw.circle(screen, COLOR_WHITE, (x + bob, y - 15), 6)
        
        self.draw_health_bar(screen, font)

    def draw_health_bar(self, screen, font):
        pass
    
    def use_skill(self, enemies, projectiles):
        if not self.target or not self.target.alive:
            return
        
        projectile = LightningBeamProjectile(self.x, self.y, self.target, 
                                           self.damage * 0.5, enemies,
                                           self.skill_chain_count, self.chain_range,
                                           self.skill_duration)
        projectiles.append(projectile)
        
        for i in range(25):
            angle = i * 14.4
            px = self.x + 35 * math.cos(math.radians(angle))
            py = self.y + 35 * math.sin(math.radians(angle))
            vx = math.cos(math.radians(angle)) * 3
            vy = math.sin(math.radians(angle)) * 3
            self.particles.append(Particle(px, py, vx, vy, (255, 255, 200), 4, 1.2))


class TowerFactory:
    @staticmethod
    def create_tower(tower_type, x, y):
        if tower_type == TowerType.ARCHER:
            return ArcherTower(x, y)
        elif tower_type == TowerType.CANNON:
            return CannonTower(x, y)
        elif tower_type == TowerType.ICE:
            return IceTower(x, y)
        elif tower_type == TowerType.LIGHTNING:
            return LightningTower(x, y)
        elif tower_type == TowerType.MAGE:
            return MagicTower(x, y)
        return ArcherTower(x, y)


class Game:
    def __init__(self):
        pygame.init()
        
        flags = pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.SCALED
        pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), flags)
        pygame.display.set_caption("王国防线 - Kingdom Defense")
        
        self.screen = pygame.display.get_surface()
        self.screen.set_alpha(None)
        
        pygame.display.set_icon(pygame.Surface((32, 32)))
        
        pygame.mouse.set_visible(True)
        
        self.clock = pygame.time.Clock()
        
        self.scale_factor = min(SCREEN_WIDTH / 1280, SCREEN_HEIGHT / 720)
        self.font = get_chinese_font(int(20 * self.scale_factor))
        self.font_large = get_chinese_font(int(36 * self.scale_factor))
        self.font_small = get_chinese_font(int(16 * self.scale_factor))
        self.font_title = get_chinese_font(int(48 * self.scale_factor))
        
        self.game_state = GameState.MENU
        self.selected_level = None
        self.current_level = None
        self.wave_index = 0
        self.gold = 150
        self.lives = 20
        self.score = 0
        self.damage_taken = 0
        self.wave_in_progress = False
        self.spawn_queue = []
        
        self.animation_timer = 0
        self.title_bob_offset = 0
        self.menu_particles = []
        self.init_menu_particles()
        
        self.gold_animation = 0
        self.lives_animation = 0
        self.score_animation = 0
        
        self.selected_button = None
        
        self.level_unlock_animations = []
        self.spawn_timer = 0
        self.particles = ParticleSystem()
        
        self.developer_mode = False
        self.dev_panel_active = False
        self.dev_panel_x = SCREEN_WIDTH - 380
        self.dev_panel_y = 100
        self.dev_panel_dragging = False
        self.dev_panel_drag_offset = (0, 0)
        self.dev_selected_tab = 0
        self.achievement_manager = AchievementManager()
        
        self.cheat_password = "244466666"
        self.show_cheat_password_dialog = False
        self.cheat_password_input = ""
        self.show_cheat_unlock_notification = False
        
        self.load_cheat_unlock_status()
        
        self.show_locked_level_dialog = False
        self.locked_level_index = -1
        self.achievement_notification = None
        self.towers = []
        self.enemies = []
        
        self.showing_intro = INTRO_AVAILABLE
        self.intro_sequence = None
        if self.showing_intro:
            self.intro_sequence = IntroSequence(self.screen, self.font, self.font_large, self.font_small)
    
    def init_menu_particles(self):
        self.menu_particles = []
        for _ in range(50):
            self.menu_particles.append({
                'x': random.randint(0, SCREEN_WIDTH),
                'y': random.randint(0, SCREEN_HEIGHT),
                'vx': (random.random() - 0.5) * 0.5,
                'vy': (random.random() - 0.5) * 0.5,
                'radius': random.randint(2, 5),
                'color': (random.randint(100, 200), random.randint(100, 200), random.randint(150, 255)),
                'alpha': random.randint(50, 150)
            })
    
    def update_menu_particles(self):
        for p in self.menu_particles:
            p['x'] += p['vx']
            p['y'] += p['vy']
            
            if p['x'] < 0 or p['x'] > SCREEN_WIDTH:
                p['vx'] *= -1
            if p['y'] < 0 or p['y'] > SCREEN_HEIGHT:
                p['vy'] *= -1
    
    def draw_menu_particles(self):
        for p in self.menu_particles:
            pygame.draw.circle(self.screen, p['color'], (int(p['x']), int(p['y'])), p['radius'], 0)
        self.projectiles = []
        self.selected_tower_type = None
        self.selected_tower = None
        self.levels = LevelData.get_levels()
        self.load_game_progress()
        
        self.theme_colors = {
            LevelTheme.FOREST: {
                'sky_top': (70, 130, 90), 'sky_bottom': (120, 180, 140),
                'ground': (85, 145, 75), 'ground_alt': (95, 155, 85),
                'path': (160, 140, 110), 'path_border': (120, 100, 80)
            },
            LevelTheme.ICE: {
                'sky_top': (80, 150, 200), 'sky_bottom': (150, 200, 230),
                'ground': (200, 220, 255), 'ground_alt': (180, 200, 240),
                'path': (220, 220, 220), 'path_border': (180, 180, 200)
            },
            LevelTheme.CASTLE: {
                'sky_top': (100, 120, 160), 'sky_bottom': (150, 170, 200),
                'ground': (120, 120, 120), 'ground_alt': (140, 140, 140),
                'path': (180, 180, 180), 'path_border': (140, 140, 140)
            },
            LevelTheme.DESERT: {
                'sky_top': (255, 200, 100), 'sky_bottom': (255, 150, 80),
                'ground': (240, 200, 120), 'ground_alt': (220, 180, 100),
                'path': (180, 160, 120), 'path_border': (140, 120, 80)
            },
            LevelTheme.VOLCANO: {
                'sky_top': (180, 50, 50), 'sky_bottom': (255, 100, 50),
                'ground': (100, 50, 30), 'ground_alt': (120, 60, 40),
                'path': (160, 80, 40), 'path_border': (120, 60, 30)
            },
            LevelTheme.SHADOW: {
                'sky_top': (30, 20, 50), 'sky_bottom': (50, 30, 80),
                'ground': (40, 30, 50), 'ground_alt': (50, 40, 60),
                'path': (80, 60, 90), 'path_border': (50, 40, 60)
            },
            LevelTheme.CAVE: {
                'sky_top': (20, 20, 25), 'sky_bottom': (30, 30, 40),
                'ground': (60, 55, 50), 'ground_alt': (50, 45, 40),
                'path': (90, 85, 75), 'path_border': (70, 65, 55)
            },
            LevelTheme.OCEAN: {
                'sky_top': (30, 80, 130), 'sky_bottom': (50, 120, 180),
                'ground': (40, 100, 160), 'ground_alt': (30, 80, 140),
                'path': (180, 200, 220), 'path_border': (140, 160, 180)
            },
            LevelTheme.SKY: {
                'sky_top': (100, 150, 200), 'sky_bottom': (150, 180, 220),
                'ground': (180, 200, 230), 'ground_alt': (160, 180, 210),
                'path': (200, 210, 220), 'path_border': (160, 170, 180)
            },
            LevelTheme.SWAMP: {
                'sky_top': (60, 70, 50), 'sky_bottom': (80, 90, 70),
                'ground': (50, 60, 40), 'ground_alt': (40, 50, 30),
                'path': (80, 90, 60), 'path_border': (60, 70, 40)
            },
            LevelTheme.JUNGLE: {
                'sky_top': (50, 100, 80), 'sky_bottom': (80, 140, 110),
                'ground': (40, 80, 50), 'ground_alt': (30, 60, 40),
                'path': (100, 120, 80), 'path_border': (80, 100, 60)
            }
        }

        self.tower_info = {
            TowerType.ARCHER: {"name": "箭塔", "desc": "远程攻击，攻速快", "cost": 100, "damage": 15, "range": 150, "speed": 0.8},
            TowerType.CANNON: {"name": "炮塔", "desc": "高伤害范围攻击", "cost": 200, "damage": 60, "range": 120, "speed": 0.4},
            TowerType.ICE: {"name": "冰塔", "desc": "减缓敌人移动速度", "cost": 150, "damage": 10, "range": 130, "speed": 1.0},
            TowerType.LIGHTNING: {"name": "电塔", "desc": "高伤害连锁攻击", "cost": 250, "damage": 30, "range": 140, "speed": 0.5},
            TowerType.MAGE: {"name": "魔法塔", "desc": "释放魔法攻击敌人", "cost": 300, "damage": 45, "range": 150, "speed": 0.6}
        }

        self.enemy_info = {
            EnemyType.GOBLIN: {"name": "哥布林", "desc": "弱小但数量众多", "type": "normal", "hp": 40, "speed": 50, "reward": 10, "stars": 1, "skill": "无", "is_ranged": False, "attack_range": 0},
            EnemyType.SKELETON: {"name": "骷髅兵", "desc": "不死族的先锋", "type": "normal", "hp": 60, "speed": 45, "reward": 15, "stars": 1, "skill": "无", "is_ranged": False, "attack_range": 0},
            EnemyType.ORC: {"name": "兽人", "desc": "强壮的近战单位", "type": "normal", "hp": 50, "speed": 40, "reward": 20, "stars": 2, "skill": "重击", "is_ranged": False, "attack_range": 0},
            EnemyType.SHADOW_WOLF: {"name": "暗影狼", "desc": "敏捷的暗影生物", "type": "normal", "hp": 35, "speed": 80, "reward": 12, "stars": 2, "skill": "暗影冲刺", "is_ranged": False, "attack_range": 0},
            EnemyType.TROLL: {"name": "巨魔", "desc": "高血量的精英敌人", "type": "elite", "hp": 80, "speed": 30, "reward": 35, "stars": 3, "skill": "狂暴", "is_ranged": False, "attack_range": 0},
            EnemyType.OGRE_MAGE: {"name": "食人魔法师", "desc": "会施法的精英敌人", "type": "elite", "hp": 100, "speed": 35, "reward": 45, "stars": 3, "skill": "火球术", "is_ranged": True, "attack_range": 100},
            EnemyType.NECROMANCER: {"name": "死灵法师", "desc": "召唤亡灵的法师", "type": "elite", "hp": 70, "speed": 40, "reward": 40, "stars": 4, "skill": "召唤骷髅", "is_ranged": True, "attack_range": 120},
            EnemyType.DARK_KNIGHT: {"name": "黑暗骑士", "desc": "身披铠甲的精英", "type": "elite", "hp": 150, "speed": 45, "reward": 60, "stars": 4, "skill": "暗影斩", "is_ranged": False, "attack_range": 0},
            EnemyType.DEMON: {"name": "恶魔", "desc": "来自深渊的强大敌人", "type": "boss", "hp": 200, "speed": 50, "reward": 80, "stars": 5, "skill": "地狱火", "is_ranged": True, "attack_range": 150},
            EnemyType.DRAGON_WHELP: {"name": "幼龙", "desc": "龙族的幼崽", "type": "boss", "hp": 250, "speed": 60, "reward": 100, "stars": 5, "skill": "龙息", "is_ranged": True, "attack_range": 180},
            EnemyType.WIZNAN: {"name": "维兹南", "desc": "最终BOSS", "type": "boss", "hp": 800, "speed": 35, "reward": 200, "stars": 5, "skill": "时空裂隙", "is_ranged": True, "attack_range": 200}
        }
    
    def draw_star(self, screen, x, y, size=10, color=(255, 215, 0), filled=True):
        points = []
        for i in range(5):
            outer_angle = i * 72 - 90
            outer_px = x + size * math.cos(math.radians(outer_angle))
            outer_py = y + size * math.sin(math.radians(outer_angle))
            points.append((outer_px, outer_py))
            
            inner_angle = outer_angle + 36
            inner_px = x + (size * 0.4) * math.cos(math.radians(inner_angle))
            inner_py = y + (size * 0.4) * math.sin(math.radians(inner_angle))
            points.append((inner_px, inner_py))
        
        if filled:
            pygame.draw.polygon(screen, color, points)
        else:
            pygame.draw.polygon(screen, color, points, 1)
    
    def draw_skull(self, screen, x, y, size=12, color=(200, 200, 200), filled=True):
        pygame.draw.circle(screen, color, (x, y), size)
        
        pygame.draw.circle(screen, (30, 30, 60), (x - size // 3, y - 2), size // 3)
        pygame.draw.circle(screen, (30, 30, 60), (x + size // 3, y - 2), size // 3)
        
        pygame.draw.polygon(screen, (30, 30, 60), [
            (x - size // 4, y + 2),
            (x, y + size // 2),
            (x + size // 4, y + 2)
        ])

    def draw_background(self, theme):
        colors = self.theme_colors.get(theme, self.theme_colors[LevelTheme.FOREST])
        sky_top = colors['sky_top']
        sky_bottom = colors['sky_bottom']
        
        for y in range(SCREEN_HEIGHT):
            ratio = y / SCREEN_HEIGHT
            r = int(sky_top[0] * (1 - ratio) + sky_bottom[0] * ratio)
            g = int(sky_top[1] * (1 - ratio) + sky_bottom[1] * ratio)
            b = int(sky_top[2] * (1 - ratio) + sky_bottom[2] * ratio)
            pygame.draw.line(self.screen, (r, g, b), (0, y), (SCREEN_WIDTH, y))

        self.draw_theme_decorations(theme)

        ground_color = colors['ground']
        ground_alt_color = colors['ground_alt']
        
        for y in range(380, SCREEN_HEIGHT):
            pattern_y = (y - 380) % 40
            if pattern_y < 20:
                pygame.draw.line(self.screen, ground_color, (0, y), (SCREEN_WIDTH, y))
            else:
                pygame.draw.line(self.screen, ground_alt_color, (0, y), (SCREEN_WIDTH, y))

        if self.current_level:
            self.draw_path(colors)
            self.draw_tower_positions()

    def draw_theme_decorations(self, theme):
        anim = self.animation_timer
        
        if theme == LevelTheme.FOREST:
            self.draw_forest_decorations(anim)
        elif theme == LevelTheme.ICE:
            self.draw_ice_decorations(anim)
        elif theme == LevelTheme.CASTLE:
            self.draw_castle_decorations(anim)
        elif theme == LevelTheme.DESERT:
            self.draw_desert_decorations(anim)
        elif theme == LevelTheme.VOLCANO:
            self.draw_volcano_decorations(anim)
        elif theme == LevelTheme.SHADOW:
            self.draw_shadow_decorations(anim)
        elif theme == LevelTheme.CAVE:
            self.draw_cave_decorations(anim)
        elif theme == LevelTheme.OCEAN:
            self.draw_ocean_decorations(anim)
        elif theme == LevelTheme.SKY:
            self.draw_sky_decorations(anim)
        elif theme == LevelTheme.SWAMP:
            self.draw_swamp_decorations(anim)
        elif theme == LevelTheme.JUNGLE:
            self.draw_jungle_decorations(anim)

    def draw_forest_decorations(self, anim):
        trees = [
            (50, 450), (180, 440), (320, 450), (450, 430), (580, 450),
            (720, 440), (850, 450), (980, 430), (1110, 450), (1200, 440)
        ]
        for i, (x, y) in enumerate(trees):
            sway = math.sin(anim * 0.5 + i) * 3
            self.draw_tree(x + sway, y, i % 3)
        
        bushes = [
            (120, 470), (250, 480), (380, 470), (510, 480), (640, 470),
            (770, 480), (900, 470), (1030, 480), (1160, 470)
        ]
        for x, y in bushes:
            pygame.draw.circle(self.screen, (60, 140, 60), (x, y), 15)
            pygame.draw.circle(self.screen, (80, 160, 80), (x + 5, y - 5), 12)
        
        for i in range(6):
            bird_x = 100 + i * 220 + math.sin(anim * 2 + i) * 30
            bird_y = 80 + i * 20 + math.sin(anim * 3 + i) * 15
            pygame.draw.circle(self.screen, (180, 160, 140), (int(bird_x), int(bird_y)), 6)
            wing_angle = math.sin(anim * 8 + i) * 0.3
            pygame.draw.line(self.screen, (180, 160, 140), 
                           (int(bird_x), int(bird_y)),
                           (int(bird_x - 8 * math.cos(wing_angle)), int(bird_y - 6 * math.sin(wing_angle))), 3)

    def draw_tree(self, x, y, style):
        trunk_height = 30 + style * 10
        pygame.draw.rect(self.screen, (80, 50, 30), (x - 8, y - trunk_height, 16, trunk_height))
        
        if style == 0:
            pygame.draw.polygon(self.screen, (40, 100, 40), [(x, y - trunk_height - 25), (x - 20, y - trunk_height), (x + 20, y - trunk_height)])
            pygame.draw.polygon(self.screen, (50, 120, 50), [(x, y - trunk_height - 40), (x - 15, y - trunk_height - 15), (x + 15, y - trunk_height - 15)])
            pygame.draw.polygon(self.screen, (60, 140, 60), [(x, y - trunk_height - 50), (x - 12, y - trunk_height - 30), (x + 12, y - trunk_height - 30)])
        elif style == 1:
            pygame.draw.circle(self.screen, (40, 100, 40), (x, y - trunk_height - 20), 20)
            pygame.draw.circle(self.screen, (50, 120, 50), (x, y - trunk_height - 35), 15)
            pygame.draw.circle(self.screen, (60, 140, 60), (x, y - trunk_height - 45), 10)
        else:
            pygame.draw.polygon(self.screen, (40, 100, 40), [(x, y - trunk_height - 30), (x - 25, y - trunk_height), (x + 5, y - trunk_height)])
            pygame.draw.polygon(self.screen, (50, 120, 50), [(x + 10, y - trunk_height - 25), (x - 10, y - trunk_height), (x + 30, y - trunk_height)])

    def draw_ice_decorations(self, anim):
        ice_spikes = [
            (30, 450), (160, 440), (290, 450), (420, 430), (550, 450),
            (680, 440), (810, 450), (940, 430), (1070, 450), (1200, 440)
        ]
        for i, (x, y) in enumerate(ice_spikes):
            spike_height = 30 + (i % 3) * 15
            pygame.draw.polygon(self.screen, (150, 200, 255), [(x, y), (x - 8, y - spike_height), (x + 8, y)])
            pygame.draw.polygon(self.screen, (180, 220, 255), [(x - 3, y), (x, y - spike_height + 5), (x + 3, y)])
        
        for i in range(20):
            snowflake_x = (i * 70 + anim * 20) % SCREEN_WIDTH
            snowflake_y = (i * 40 + anim * 15 * (i % 2 + 1)) % SCREEN_HEIGHT
            snowflake_size = 2 + (i % 3)
            self.draw_snowflake(int(snowflake_x), int(snowflake_y), snowflake_size)
        
        for i in range(3):
            ice_block_x = 200 + i * 400
            ice_block_y = 460
            pygame.draw.rect(self.screen, (150, 200, 255), (ice_block_x, ice_block_y, 60, 40))
            pygame.draw.line(self.screen, (180, 220, 255), (ice_block_x + 15, ice_block_y), (ice_block_x + 15, ice_block_y + 40))
            pygame.draw.line(self.screen, (180, 220, 255), (ice_block_x + 45, ice_block_y), (ice_block_x + 45, ice_block_y + 40))

    def draw_snowflake(self, x, y, size):
        for i in range(6):
            angle = i * 60
            px = x + size * math.cos(math.radians(angle))
            py = y + size * math.sin(math.radians(angle))
            pygame.draw.line(self.screen, (255, 255, 255), (x, y), (int(px), int(py)), 1)

    def draw_castle_decorations(self, anim):
        castle_walls = [
            (100, 380), (300, 380), (500, 380), (700, 380), (900, 380), (1100, 380)
        ]
        for i, (x, y) in enumerate(castle_walls):
            wall_height = 60 + (i % 2) * 20
            pygame.draw.rect(self.screen, (100, 100, 100), (x, y - wall_height, 80, wall_height))
            pygame.draw.rect(self.screen, (130, 130, 130), (x + 10, y - wall_height + 10, 60, wall_height - 20))
            pygame.draw.polygon(self.screen, (100, 100, 100), [(x + 40, y - wall_height - 20), (x + 20, y - wall_height), (x + 60, y - wall_height)])
        
        for i in range(4):
            pillar_x = 150 + i * 350
            pygame.draw.rect(self.screen, (80, 80, 80), (pillar_x, 350, 20, 50))
            pygame.draw.polygon(self.screen, (100, 100, 100), [(pillar_x - 5, 350), (pillar_x + 10, 330), (pillar_x + 25, 350)])
        
        flag_y = 100 + math.sin(anim * 2) * 10
        pygame.draw.line(self.screen, COLOR_BROWN, (640, 120), (640, 60))
        pygame.draw.polygon(self.screen, COLOR_RED, [(640, 60), (680, flag_y), (640, flag_y)])

    def draw_desert_decorations(self, anim):
        sand_dunes = [
            (0, 420), (150, 400), (300, 430), (450, 390), (600, 420),
            (750, 400), (900, 430), (1050, 390), (1200, 420)
        ]
        for i in range(len(sand_dunes) - 1):
            x1, y1 = sand_dunes[i]
            x2, y2 = sand_dunes[i + 1]
            pygame.draw.line(self.screen, (240, 200, 120), (x1, y1), (x2, y2), 30)
        
        sun_glow = int((math.sin(anim * 0.5) + 1) * 30)
        pygame.draw.circle(self.screen, (255, 180 + sun_glow, 80), (1150, 80), 50)
        pygame.draw.circle(self.screen, (255, 220, 150), (1150, 80), 35)
        pygame.draw.circle(self.screen, (255, 240, 200), (1150, 80), 20)
        
        palm_trees = [(80, 450), (350, 450), (650, 450), (950, 450)]
        for x, y in palm_trees:
            pygame.draw.rect(self.screen, (130, 80, 40), (x - 5, y - 50, 10, 50))
            for i in range(5):
                frond_angle = (i - 2) * 25
                frond_x = x + 30 * math.cos(math.radians(frond_angle))
                frond_y = y - 50 + 30 * math.sin(math.radians(frond_angle))
                pygame.draw.line(self.screen, (30, 120, 30), (x, y - 50), (int(frond_x), int(frond_y)), 6)
        
        for i in range(5):
            cactus_x = 200 + i * 250
            cactus_height = 30 + (i % 2) * 20
            pygame.draw.rect(self.screen, (50, 150, 50), (cactus_x, 480 - cactus_height, 15, cactus_height))
            if cactus_height > 30:
                pygame.draw.rect(self.screen, (50, 150, 50), (cactus_x - 12, 480 - cactus_height + 15, 10, 20))
                pygame.draw.rect(self.screen, (50, 150, 50), (cactus_x + 17, 480 - cactus_height + 25, 10, 15))

    def draw_volcano_decorations(self, anim):
        lava_rivers = [
            [(50, 400), (80, 450), (120, 480)],
            [(1180, 400), (1150, 450), (1100, 480)]
        ]
        for river in lava_rivers:
            for i in range(len(river) - 1):
                x1, y1 = river[i]
                x2, y2 = river[i + 1]
                lava_color = (255, 80 + int(math.sin(anim * 3) * 20), 0)
                pygame.draw.line(self.screen, lava_color, (x1, y1), (x2, y2), 15)
        
        smoke_particles = []
        for i in range(8):
            smoke_x = 640 + (i - 3.5) * 40
            smoke_y = 200 + math.sin(anim * 0.3 + i) * 30 + anim * 10 * ((i % 2) * 2 - 1)
            smoke_size = 15 + i * 3
            smoke_alpha = max(50, 150 - int(smoke_y / 4))
            pygame.draw.circle(self.screen, (80, 80, 80, smoke_alpha), (int(smoke_x), int(smoke_y)), smoke_size)
        
        flame_height = 40 + int(math.sin(anim * 5) * 15)
        pygame.draw.polygon(self.screen, (255, 50, 0), [(620, 220), (640, 220 - flame_height), (660, 220)])
        pygame.draw.polygon(self.screen, (255, 100, 0), [(625, 220), (640, 220 - flame_height + 10), (655, 220)])
        pygame.draw.polygon(self.screen, (255, 150, 0), [(630, 220), (640, 220 - flame_height + 20), (650, 220)])
        
        rocks = [(100, 470), (250, 480), (400, 470), (550, 480), (700, 470), 
                 (850, 480), (1000, 470), (1150, 480)]
        for x, y in rocks:
            rock_size = 15 + random.randint(5, 10)
            pygame.draw.circle(self.screen, (60, 50, 50), (x, y), rock_size)
            pygame.draw.circle(self.screen, (80, 70, 70), (x - 3, y - 3), rock_size // 2)

    def draw_shadow_decorations(self, anim):
        moon_phase = int((anim * 0.2) % 8)
        moon_x, moon_y = 1100, 80
        pygame.draw.circle(self.screen, (180, 180, 200), (moon_x, moon_y), 30)
        if moon_phase > 0:
            shadow_offset = moon_phase * 5
            pygame.draw.circle(self.screen, (20, 15, 35), (moon_x + shadow_offset, moon_y), 28)
        
        for i in range(30):
            star_x = (i * 43 + anim * 5) % SCREEN_WIDTH
            star_y = (i * 25 + anim * 3) % 350
            star_alpha = int((math.sin(anim * 3 + i) + 1) * 127)
            star_size = 1 + (i % 3)
            pygame.draw.circle(self.screen, (255, 255, 255, star_alpha), (int(star_x), int(star_y)), star_size)
        
        dark_trees = [
            (60, 450), (200, 440), (350, 450), (500, 430), (650, 450),
            (800, 440), (950, 450), (1100, 430), (1200, 450)
        ]
        for x, y in dark_trees:
            pygame.draw.rect(self.screen, (30, 20, 40), (x - 5, y - 40, 10, 40))
            pygame.draw.polygon(self.screen, (25, 15, 35), [(x, y - 45), (x - 15, y - 30), (x + 15, y - 30)])
            pygame.draw.polygon(self.screen, (20, 12, 30), [(x, y - 55), (x - 12, y - 40), (x + 12, y - 40)])
        
        fog_particles = []
        for i in range(15):
            fog_x = (i * 90 + anim * 8) % SCREEN_WIDTH
            fog_y = 400 + (i % 3) * 30
            fog_alpha = 30 + int(math.sin(anim * 2 + i) * 20)
            pygame.draw.circle(self.screen, (60, 50, 80, fog_alpha), (int(fog_x), int(fog_y)), 25)

    def draw_cave_decorations(self, anim):
        stalactites = [
            (50, 100), (150, 80), (250, 120), (350, 90), (450, 110),
            (550, 85), (650, 105), (750, 95), (850, 115), (950, 80),
            (1050, 100), (1150, 90)
        ]
        for i, (x, y) in enumerate(stalactites):
            stal_height = 25 + (i % 4) * 15
            pygame.draw.polygon(screen, (80, 75, 70), [(x, y), (x - 8, y + stal_height), (x + 8, y + stal_height)])
            pygame.draw.polygon(screen, (100, 95, 90), [(x - 3, y + 5), (x, y + stal_height), (x + 3, y + 5)])
        
        stalagmites = [
            (100, 450), (200, 460), (300, 450), (400, 465), (500, 450),
            (600, 455), (700, 460), (800, 450), (900, 455), (1000, 460),
            (1100, 450), (1200, 455)
        ]
        for i, (x, y) in enumerate(stalagmites):
            stal_height = 20 + (i % 3) * 12
            pygame.draw.polygon(screen, (70, 65, 60), [(x, y), (x - 6, y - stal_height), (x + 6, y - stal_height)])
        
        gems = [
            (120, 280), (320, 350), (520, 220), (720, 380), (920, 250), (1120, 320)
        ]
        for i, (x, y) in enumerate(gems):
            gem_color = [(255, 100, 100), (100, 255, 100), (100, 100, 255), (255, 255, 100), (255, 100, 255), (100, 255, 255)][i % 6]
            gem_pulse = int(10 * math.sin(anim * 3 + i))
            pygame.draw.polygon(screen, gem_color, [(x, y - 10 + gem_pulse), (x - 8, y), (x, y + 10 + gem_pulse), (x + 8, y)])
        
        bats = []
        for i in range(5):
            bat_x = 150 + i * 250 + math.sin(anim * 2 + i) * 20
            bat_y = 150 + math.sin(anim * 3 + i) * 15
            wing_flap = math.sin(anim * 6 + i) * 0.5
            pygame.draw.polygon(screen, (20, 20, 25), [
                (bat_x, bat_y),
                (bat_x - 15 * math.cos(wing_flap), bat_y - 10 * math.sin(wing_flap)),
                (bat_x - 5, bat_y + 5),
                (bat_x - 15 * math.cos(wing_flap), bat_y + 10 * math.sin(wing_flap)),
                (bat_x, bat_y),
                (bat_x + 15 * math.cos(wing_flap), bat_y + 10 * math.sin(wing_flap)),
                (bat_x + 5, bat_y + 5),
                (bat_x + 15 * math.cos(wing_flap), bat_y - 10 * math.sin(wing_flap))
            ])

    def draw_ocean_decorations(self, anim):
        for i in range(10):
            wave_y = 400 + math.sin(anim * 2 + i * 0.5) * 5
            pygame.draw.line(screen, (80, 150, 220), (i * 130, wave_y), ((i + 1) * 130, wave_y), 3)
        
        bubbles = []
        for i in range(20):
            bubble_x = (i * 65 + anim * 10) % SCREEN_WIDTH
            bubble_y = SCREEN_HEIGHT - (anim * 5 + i * 25) % SCREEN_HEIGHT
            bubble_size = 3 + (i % 4)
            bubble_alpha = max(30, 100 - int(bubble_y / 5))
            pygame.draw.circle(screen, (150, 200, 255, bubble_alpha), (int(bubble_x), int(bubble_y)), bubble_size)
        
        seaweed = [
            (60, 460), (200, 470), (350, 460), (500, 470), (650, 460),
            (800, 470), (950, 460), (1100, 470), (1200, 460)
        ]
        for i, (x, y) in enumerate(seaweed):
            sway = math.sin(anim * 1.5 + i) * 8
            pygame.draw.line(screen, (30, 120, 80), (x, y), (x + sway, y - 30), 4)
            pygame.draw.line(screen, (40, 140, 90), (x, y - 10), (x + sway * 0.7, y - 40), 3)
            pygame.draw.line(screen, (30, 120, 80), (x, y - 20), (x + sway * 0.5, y - 45), 2)
        
        fish = []
        for i in range(4):
            fish_x = (i * 350 + anim * 30) % (SCREEN_WIDTH + 50) - 25
            fish_y = 200 + i * 80 + math.sin(anim * 2 + i) * 20
            fish_size = 15 + (i % 2) * 5
            pygame.draw.ellipse(screen, (100, 180, 220), (fish_x, fish_y, fish_size, fish_size // 2))
            pygame.draw.circle(screen, COLOR_WHITE, (fish_x + fish_size - 3, fish_y + fish_size // 4), 2)
        
        anchors = [(400, 450), (900, 460)]
        for x, y in anchors:
            pygame.draw.line(screen, (80, 80, 80), (x, y), (x, y - 30), 4)
            pygame.draw.line(screen, (80, 80, 80), (x - 15, y - 10), (x + 15, y - 10), 4)
            pygame.draw.polygon(screen, (60, 60, 60), [(x - 15, y - 10), (x - 25, y), (x - 5, y)])
            pygame.draw.polygon(screen, (60, 60, 60), [(x + 15, y - 10), (x + 25, y), (x + 5, y)])

    def draw_sky_decorations(self, anim):
        clouds = [
            (100, 80), (350, 100), (600, 70), (850, 90), (1100, 80)
        ]
        for i, (x, y) in enumerate(clouds):
            cloud_offset = math.sin(anim * 0.3 + i) * 5
            pygame.draw.ellipse(screen, (220, 230, 240), (x + cloud_offset, y, 60, 25))
            pygame.draw.ellipse(screen, (230, 240, 250), (x + 20 + cloud_offset, y - 5, 50, 20))
            pygame.draw.ellipse(screen, (240, 245, 250), (x + 35 + cloud_offset, y, 40, 18))
        
        sun_rays = []
        sun_x, sun_y = 1150, 70
        for i in range(12):
            angle = i * 30 + anim * 5
            ray_length = 60 + int(math.sin(anim * 2 + i) * 10)
            ray_x = sun_x + ray_length * math.cos(math.radians(angle))
            ray_y = sun_y + ray_length * math.sin(math.radians(angle))
            pygame.draw.line(screen, (255, 230, 150, 80), (sun_x, sun_y), (int(ray_x), int(ray_y)), 2)
        
        pygame.draw.circle(screen, (255, 220, 100), (sun_x, sun_y), 35)
        pygame.draw.circle(screen, (255, 240, 150), (sun_x, sun_y), 25)
        pygame.draw.circle(screen, (255, 255, 200), (sun_x, sun_y), 15)
        
        floating_islands = [
            (200, 350), (500, 280), (800, 320), (1100, 290)
        ]
        for i, (x, y) in enumerate(floating_islands):
            island_wobble = math.sin(anim * 0.5 + i) * 3
            pygame.draw.ellipse(screen, (80, 140, 80), (x - 40, y + island_wobble, 80, 20))
            pygame.draw.ellipse(screen, (60, 120, 60), (x - 35, y + island_wobble, 70, 15))
            
            tree_x = x + (-20 + (i % 3) * 20)
            pygame.draw.rect(screen, (60, 40, 20), (tree_x - 4, y + island_wobble - 25, 8, 25))
            pygame.draw.circle(screen, (40, 100, 40), (tree_x, y + island_wobble - 35), 12)
        
        birds = []
        for i in range(6):
            bird_x = (i * 220 + anim * 15) % SCREEN_WIDTH
            bird_y = 150 + math.sin(anim * 2 + i) * 30
            wing_flap = math.sin(anim * 8 + i) * 0.4
            pygame.draw.line(screen, (100, 100, 100), (bird_x, bird_y),
                           (bird_x - 10 * math.cos(wing_flap), bird_y - 8 * math.sin(wing_flap)), 2)
            pygame.draw.line(screen, (100, 100, 100), (bird_x, bird_y),
                           (bird_x + 10 * math.cos(wing_flap), bird_y - 8 * math.sin(wing_flap)), 2)

    def draw_swamp_decorations(self, anim):
        swamp_gas = []
        for i in range(12):
            gas_x = (i * 110 + anim * 8) % SCREEN_WIDTH
            gas_y = 380 + (i % 3) * 40 + math.sin(anim * 1.5 + i) * 10
            gas_size = 20 + int(math.sin(anim * 2 + i) * 5)
            gas_alpha = 40 + int(math.sin(anim * 3 + i) * 20)
            pygame.draw.circle(screen, (80, 100, 70, gas_alpha), (int(gas_x), int(gas_y)), gas_size)
        
        lily_pads = [
            (80, 460), (220, 450), (360, 460), (500, 450), (640, 460),
            (780, 450), (920, 460), (1060, 450), (1200, 460)
        ]
        for i, (x, y) in enumerate(lily_pads):
            pad_size = 15 + (i % 3) * 5
            pygame.draw.circle(screen, (40, 80, 40), (x, y), pad_size)
            pygame.draw.circle(screen, (50, 100, 50), (x, y), pad_size, 2)
            if i % 2 == 0:
                pygame.draw.circle(screen, COLOR_PINK, (x + 5, y - 3), 4)
        
        dead_trees = [
            (100, 420), (300, 430), (500, 420), (700, 430), (900, 420), (1100, 430)
        ]
        for x, y in dead_trees:
            pygame.draw.line(screen, (60, 50, 40), (x, y), (x, y - 50), 8)
            pygame.draw.line(screen, (50, 40, 30), (x, y - 20), (x - 25, y - 35), 5)
            pygame.draw.line(screen, (50, 40, 30), (x, y - 35), (x + 20, y - 50), 4)
        
        frogs = []
        for i in range(3):
            frog_x = 300 + i * 350 + math.sin(anim * 2 + i) * 10
            frog_y = 470
            frog_size = 12
            pygame.draw.ellipse(screen, (50, 150, 50), (frog_x - frog_size, frog_y - frog_size // 2, frog_size * 2, frog_size))
            pygame.draw.circle(screen, COLOR_WHITE, (frog_x - 5, frog_y - 3), 3)
            pygame.draw.circle(screen, COLOR_BLACK, (frog_x - 5, frog_y - 3), 1)
            pygame.draw.circle(screen, COLOR_WHITE, (frog_x + 5, frog_y - 3), 3)
            pygame.draw.circle(screen, COLOR_BLACK, (frog_x + 5, frog_y - 3), 1)
        
        vines = [
            (150, 150), (450, 180), (750, 160), (1050, 170)
        ]
        for i, (x, y) in enumerate(vines):
            vine_sway = math.sin(anim * 1.5 + i) * 15
            pygame.draw.line(screen, (60, 100, 60), (x, y), (x + vine_sway, y + 80), 3)
            for j in range(3):
                leaf_x = x + vine_sway * (j + 1) / 3
                leaf_y = y + 30 + j * 20
                pygame.draw.polygon(screen, (50, 90, 50), [(leaf_x, leaf_y), (leaf_x - 8, leaf_y + 5), (leaf_x + 8, leaf_y + 5)])

    def draw_jungle_decorations(self, anim):
        jungle_trees = [
            (60, 450), (200, 440), (350, 450), (500, 430), (650, 450),
            (800, 440), (950, 450), (1100, 430), (1200, 450)
        ]
        for i, (x, y) in enumerate(jungle_trees):
            trunk_height = 60 + (i % 3) * 20
            pygame.draw.rect(screen, (80, 60, 30), (x - 10, y - trunk_height, 20, trunk_height))
            
            canopy_size = 40 + (i % 2) * 15
            pygame.draw.circle(screen, (30, 100, 50), (x - 15, y - trunk_height - 10), canopy_size)
            pygame.draw.circle(screen, (40, 120, 60), (x + 15, y - trunk_height - 15), canopy_size)
            pygame.draw.circle(screen, (50, 140, 70), (x, y - trunk_height - 25), canopy_size - 5)
        
        vines = [
            (120, 100), (280, 120), (440, 90), (600, 110), (760, 100),
            (920, 120), (1080, 90), (1180, 110)
        ]
        for i, (x, y) in enumerate(vines):
            vine_sway = math.sin(anim * 1.2 + i) * 20
            pygame.draw.line(screen, (40, 90, 50), (x, y), (x + vine_sway, y + 150), 4)
            for j in range(5):
                leaf_x = x + vine_sway * (j + 1) / 5
                leaf_y = y + 30 + j * 25
                leaf_angle = math.sin(anim * 2 + i + j) * 0.3
                pygame.draw.polygon(screen, (30, 80, 40), [
                    (leaf_x, leaf_y),
                    (leaf_x - 10 * math.cos(leaf_angle), leaf_y + 8 * math.sin(leaf_angle)),
                    (leaf_x + 10 * math.cos(leaf_angle), leaf_y + 8 * math.sin(leaf_angle))
                ])
        
        flowers = [
            (150, 470), (300, 475), (450, 470), (600, 475), (750, 470),
            (900, 475), (1050, 470), (1200, 475)
        ]
        flower_colors = [(255, 100, 150), (255, 200, 100), (150, 100, 255), (100, 200, 255)]
        for i, (x, y) in enumerate(flowers):
            color = flower_colors[i % 4]
            pygame.draw.circle(screen, color, (x, y), 8)
            pygame.draw.circle(screen, COLOR_YELLOW, (x, y), 4)
        
        parrots = []
        for i in range(3):
            parrot_x = 250 + i * 400 + math.sin(anim * 1.5 + i) * 15
            parrot_y = 180 + math.sin(anim * 2 + i) * 10
            wing_flap = math.sin(anim * 6 + i) * 0.4
            
            pygame.draw.ellipse(screen, (255, 50, 50), (parrot_x - 10, parrot_y - 8, 20, 16))
            pygame.draw.line(screen, (255, 150, 50), (parrot_x - 10, parrot_y),
                           (parrot_x - 20 * math.cos(wing_flap), parrot_y - 15 * math.sin(wing_flap)), 3)
            pygame.draw.line(screen, (255, 150, 50), (parrot_x + 10, parrot_y),
                           (parrot_x + 20 * math.cos(wing_flap), parrot_y - 15 * math.sin(wing_flap)), 3)
            pygame.draw.circle(screen, COLOR_YELLOW, (parrot_x + 8, parrot_y - 3), 4)
        
        bananas = [
            (320, 280), (680, 250), (1020, 270)
        ]
        for x, y in bananas:
            for j in range(3):
                banana_x = x + (j - 1) * 8
                banana_y = y + j * 5
                pygame.draw.ellipse(screen, (255, 200, 50), (banana_x - 10, banana_y, 20, 8), 0, 4)
                pygame.draw.line(screen, (200, 150, 30), (banana_x, banana_y), (banana_x - 2, banana_y - 8), 2)

    def draw_path(self, colors):
        path_color = colors['path']
        border_color = colors['path_border']
        
        for i in range(len(self.current_level.path_points) - 1):
            x1, y1 = self.current_level.path_points[i]
            x2, y2 = self.current_level.path_points[i + 1]
            
            pygame.draw.line(self.screen, border_color, (x1 - 5, y1), (x2 - 5, y2), 25)
            pygame.draw.line(self.screen, border_color, (x1 + 5, y1), (x2 + 5, y2), 25)
            pygame.draw.line(self.screen, path_color, (x1, y1), (x2, y2), 20)

        start_x, start_y = self.current_level.path_points[0]
        end_x, end_y = self.current_level.path_points[-1]
        
        start_glow = pygame.Surface((40, 40), pygame.SRCALPHA)
        pygame.draw.circle(start_glow, (0, 255, 0, 50), (20, 20), 20)
        self.screen.blit(start_glow, (start_x - 20, start_y - 20))
        pygame.draw.circle(self.screen, COLOR_GREEN, (start_x, start_y), 15)
        pygame.draw.circle(self.screen, COLOR_DARK_GREEN, (start_x, start_y), 15, 3)
        pygame.draw.polygon(self.screen, COLOR_WHITE, [(start_x, start_y - 8), (start_x - 4, start_y + 2), (start_x + 4, start_y + 2)])
        
        end_glow = pygame.Surface((40, 40), pygame.SRCALPHA)
        pygame.draw.circle(end_glow, (255, 0, 0, 50), (20, 20), 20)
        self.screen.blit(end_glow, (end_x - 20, end_y - 20))
        pygame.draw.circle(self.screen, COLOR_RED, (end_x, end_y), 15)
        pygame.draw.circle(self.screen, COLOR_DARK_RED, (end_x, end_y), 15, 3)
        pygame.draw.polygon(self.screen, COLOR_WHITE, [(end_x - 6, end_y - 6), (end_x + 6, end_y - 6), (end_x, end_y + 4)])

    def draw_tower_positions(self):
        for pos in self.current_level.tower_positions:
            occupied = False
            for tower in self.towers:
                if math.hypot(tower.x - pos[0], tower.y - pos[1]) < 30:
                    occupied = True
                    break
            
            if not occupied:
                tile_glow = pygame.Surface((50, 50), pygame.SRCALPHA)
                pygame.draw.circle(tile_glow, (100, 150, 100, 30), (25, 25), 22)
                self.screen.blit(tile_glow, (pos[0] - 25, pos[1] - 25))
                
                pygame.draw.circle(self.screen, COLOR_GRAY, pos, 22)
                pygame.draw.circle(self.screen, COLOR_DARK_GRAY, pos, 22, 2)
                pygame.draw.circle(self.screen, COLOR_GREEN, pos, 5)

    def draw_menu(self):
        gradient_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        for y in range(SCREEN_HEIGHT):
            ratio = y / SCREEN_HEIGHT
            r = int(30 + ratio * 20)
            g = int(30 + ratio * 20)
            b = int(60 + ratio * 40)
            pygame.draw.line(gradient_surface, (r, g, b), (0, y), (SCREEN_WIDTH, y))
        self.screen.blit(gradient_surface, (0, 0))
        
        self.update_menu_particles()
        self.draw_menu_particles()
        
        self.title_bob_offset = math.sin(self.animation_timer * 2) * 10
        
        mouse_pos = pygame.mouse.get_pos()
        
        if self.developer_mode:
            dev_panel_button = pygame.Rect(SCREEN_WIDTH // 2 - 90, 80, 180, 30)
            is_dev_hovered = dev_panel_button.collidepoint(mouse_pos)
            
            if is_dev_hovered:
                pygame.draw.rect(self.screen, COLOR_GOLD, dev_panel_button, border_radius=4)
                dev_text = self.font_small.render("开发者面板", True, COLOR_BLACK)
            else:
                pygame.draw.rect(self.screen, COLOR_GREEN, dev_panel_button, border_radius=4)
                pygame.draw.rect(self.screen, COLOR_WHITE, dev_panel_button, 2, border_radius=4)
                dev_text = self.font_small.render("开发者面板", True, COLOR_WHITE)
            
            dev_rect = dev_text.get_rect(center=dev_panel_button.center)
            self.screen.blit(dev_text, dev_rect)
        
        title_text = self.font_title.render("王国防线", True, COLOR_GOLD)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 150 + self.title_bob_offset))
        
        title_glow = pygame.Surface((title_rect.width + 20, title_rect.height + 20), pygame.SRCALPHA)
        pygame.draw.rect(title_glow, (255, 215, 0, 50), (0, 0, title_rect.width + 20, title_rect.height + 20), border_radius=10)
        self.screen.blit(title_glow, (title_rect.x - 10, title_rect.y - 10))
        
        self.screen.blit(title_text, title_rect)
        
        subtitle_text = self.font_large.render("Kingdom Defense", True, (200, 200, 255))
        subtitle_rect = subtitle_text.get_rect(center=(SCREEN_WIDTH // 2, 220 + self.title_bob_offset * 0.5))
        self.screen.blit(subtitle_text, subtitle_rect)
        
        buttons = [
            {"text": "开始游戏", "action": "level_select", "y": 300},
            {"text": "塔图鉴", "action": "tower_encyclopedia", "y": 360},
            {"text": "敌人图鉴", "action": "enemy_encyclopedia", "y": 420},
            {"text": "成就系统", "action": "achievements", "y": 480},
            {"text": "作弊模式", "action": "developer_mode", "y": 540, "enabled": self.cheat_unlocked},
            {"text": "退出游戏", "action": "quit", "y": 600}
        ]

        for btn in buttons:
            button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 120, btn["y"], 240, 50)
            is_hovered = button_rect.collidepoint(mouse_pos)
            
            enabled = btn.get("enabled", True)
            
            if enabled:
                if is_hovered:
                    scale = 1.05
                    offset_y = -5
                    color = (80, 100, 130)
                    border_color = COLOR_GOLD
                    text_color = COLOR_GOLD
                else:
                    scale = 1.0
                    offset_y = 0
                    color = COLOR_GRAY
                    border_color = COLOR_WHITE
                    text_color = COLOR_WHITE
            else:
                scale = 1.0
                offset_y = 0
                color = COLOR_DARK_GRAY
                border_color = COLOR_GRAY
                text_color = COLOR_GRAY
            
            scaled_rect = pygame.Rect(
                button_rect.x + (button_rect.width * (1 - scale)) / 2,
                button_rect.y + offset_y + (button_rect.height * (1 - scale)) / 2,
                button_rect.width * scale,
                button_rect.height * scale
            )
            
            pygame.draw.rect(self.screen, color, scaled_rect, border_radius=8)
            pygame.draw.rect(self.screen, border_color, scaled_rect, 3, border_radius=8)
            
            if enabled and is_hovered:
                glow_surface = pygame.Surface((scaled_rect.width, scaled_rect.height), pygame.SRCALPHA)
                pygame.draw.rect(glow_surface, (255, 215, 0, 30), glow_surface.get_rect(), border_radius=8)
                self.screen.blit(glow_surface, scaled_rect.topleft)
            
            if enabled:
                text = self.font.render(btn["text"], True, text_color)
            else:
                text = self.font.render(f"🔒 {btn['text']}", True, text_color)
            text_rect = text.get_rect(center=scaled_rect.center)
            self.screen.blit(text, text_rect)
            
            if self.developer_mode:
                dev_text = self.font.render("✅ 作弊模式已开启", True, COLOR_GREEN)
                dev_rect = dev_text.get_rect(bottomright=(SCREEN_WIDTH - 20, SCREEN_HEIGHT - 20))
                self.screen.blit(dev_text, dev_rect)
            
            cheat_toggle_button = pygame.Rect(20, SCREEN_HEIGHT - 60, 120, 40)
            if self.cheat_unlocked:
                pygame.draw.rect(self.screen, COLOR_RED, cheat_toggle_button, border_radius=6)
                pygame.draw.rect(self.screen, COLOR_WHITE, cheat_toggle_button, 2, border_radius=6)
                toggle_text = self.font_small.render("🔒 锁上作弊", True, COLOR_WHITE)
            else:
                pygame.draw.rect(self.screen, COLOR_GREEN, cheat_toggle_button, border_radius=6)
                pygame.draw.rect(self.screen, COLOR_WHITE, cheat_toggle_button, 2, border_radius=6)
                toggle_text = self.font_small.render("🔓 解锁作弊", True, COLOR_WHITE)
            toggle_rect = toggle_text.get_rect(center=cheat_toggle_button.center)
            self.screen.blit(toggle_text, toggle_rect)

    def draw_level_select(self):
        self.screen.fill((25, 25, 50))
        
        title_text = self.font_large.render("选择关卡", True, COLOR_GOLD)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 60))
        self.screen.blit(title_text, title_rect)

        back_button = pygame.Rect(50, 50, 100, 40)
        pygame.draw.rect(self.screen, COLOR_GRAY, back_button)
        pygame.draw.rect(self.screen, COLOR_WHITE, back_button, 2)
        back_text = self.font.render("返回", True, COLOR_WHITE)
        back_rect = back_text.get_rect(center=back_button.center)
        self.screen.blit(back_text, back_rect)

        for i, level in enumerate(self.levels):
            x = 100 + (i % 3) * 250
            y = 150 + (i // 3) * 200
            
            level_rect = pygame.Rect(x, y, 200, 150)
            
            if level.unlocked:
                self.draw_level_cover(x, y, level, i)
                
                overlay = pygame.Surface((200, 150), pygame.SRCALPHA)
                overlay.fill((0, 0, 0, 100))
                self.screen.blit(overlay, (x, y))
                
                pygame.draw.rect(self.screen, COLOR_WHITE, level_rect, 2)
                
                name_text = self.font.render(level.name, True, COLOR_WHITE)
                name_rect = name_text.get_rect(center=(x + 100, y + 35))
                self.screen.blit(name_text, name_rect)
                
                reward_text = self.font_small.render(f"{level.gold_reward} 金币", True, COLOR_GOLD)
                reward_rect = reward_text.get_rect(center=(x + 100, y + 65))
                self.screen.blit(reward_text, reward_rect)
                
                stars = "★" * min(i + 1, 3) + "☆" * (3 - min(i + 1, 3))
                stars_text = self.font.render(stars, True, COLOR_YELLOW)
                stars_rect = stars_text.get_rect(center=(x + 100, y + 95))
                self.screen.blit(stars_text, stars_rect)
                
                if level.completed:
                    completed_text = self.font_small.render("已通关", True, COLOR_GREEN)
                    completed_rect = completed_text.get_rect(center=(x + 100, y + 125))
                    self.screen.blit(completed_text, completed_rect)
            else:
                self.draw_locked_level_cover(x, y, level, i)
                
                overlay = pygame.Surface((200, 150), pygame.SRCALPHA)
                overlay.fill((0, 0, 0, 150))
                self.screen.blit(overlay, (x, y))
                
                pygame.draw.rect(self.screen, COLOR_GRAY, level_rect, 2)
                
                lock_text = self.font_large.render("🔒", True, COLOR_GRAY)
                lock_rect = lock_text.get_rect(center=(x + 100, y + 75))
                self.screen.blit(lock_text, lock_rect)
                
                hint_text = self.font_small.render("完成前一关解锁", True, COLOR_GRAY)
                hint_rect = hint_text.get_rect(center=(x + 100, y + 120))
                self.screen.blit(hint_text, hint_rect)
    
    def draw_level_cover(self, x, y, level, index):
        theme = level.theme
        
        if theme == LevelTheme.FOREST:
            pygame.draw.rect(self.screen, (30, 70, 30), (x, y, 200, 150))
            for i in range(5):
                tree_x = x + 20 + i * 40
                pygame.draw.polygon(self.screen, (25, 55, 25), [(tree_x - 12, y + 150), (tree_x, y + 90), (tree_x + 12, y + 150)])
                pygame.draw.rect(self.screen, (20, 45, 20), (tree_x - 4, y + 130, 8, 20))
            pygame.draw.circle(self.screen, (255, 230, 150), (x + 160, y + 35), 20)
            for i in range(3):
                bird_y = y + 40 + i * 20 + math.sin(self.animation_timer * 2 + index) * 3
                pygame.draw.circle(self.screen, (200, 180, 160), (x + 150 + i * 15, bird_y), 4)
        
        elif theme == LevelTheme.ICE:
            pygame.draw.rect(self.screen, (60, 100, 150), (x, y, 200, 150))
            for i in range(6):
                snow_x = x + 15 + i * 35
                snow_y = y + 100 + (i % 2) * 25
                pygame.draw.polygon(self.screen, (180, 200, 255), [(snow_x, snow_y), (snow_x - 8, snow_y + 15), (snow_x + 8, snow_y + 15)])
            for i in range(4):
                flake_y = (y + 25 + i * 30 + self.animation_timer * 0.5) % 150
                pygame.draw.circle(self.screen, (255, 255, 255), (x + 20 + i * 50, flake_y), 2)
            pygame.draw.polygon(self.screen, (220, 230, 255), [(x + 100, y + 20), (x + 90, y + 50), (x + 110, y + 50)])
        
        elif theme == LevelTheme.CASTLE:
            pygame.draw.rect(self.screen, (60, 60, 80), (x, y, 200, 150))
            pygame.draw.rect(self.screen, (100, 100, 100), (x + 60, y + 50, 80, 100))
            pygame.draw.polygon(self.screen, (120, 120, 120), [(x + 50, y + 70), (x + 60, y + 30), (x + 70, y + 70)])
            pygame.draw.polygon(self.screen, (120, 120, 120), [(x + 130, y + 70), (x + 140, y + 30), (x + 150, y + 70)])
            pygame.draw.line(self.screen, COLOR_BROWN, (x + 100, y + 45), (x + 100, y + 20))
            flag_y = y + 30 + math.sin(self.animation_timer * 2 + index) * 5
            pygame.draw.polygon(self.screen, COLOR_RED, [(x + 100, y + 20), (x + 115, flag_y), (x + 100, flag_y)])
        
        elif theme == LevelTheme.DESERT:
            pygame.draw.rect(self.screen, (160, 120, 60), (x, y, 200, 150))
            for i in range(4):
                sand_x = x + 20 + i * 55
                pygame.draw.polygon(self.screen, (180, 140, 80), [(sand_x, y + 150), (sand_x - 15, y + 110), (sand_x + 15, y + 150)])
            sun_glow = int((math.sin(self.animation_timer + index) + 1) * 15)
            pygame.draw.circle(self.screen, (255, 180 + sun_glow, 80), (x + 165, y + 30), 22)
            pygame.draw.circle(self.screen, (255, 220, 150), (x + 165, y + 30), 12)
        
        elif theme == LevelTheme.VOLCANO:
            pygame.draw.rect(self.screen, (100, 30, 30), (x, y, 200, 150))
            for i in range(4):
                flame_x = x + 30 + i * 50
                flame_height = 25 + (i % 2) * 15 + math.sin(self.animation_timer * 3 + i) * 5
                pygame.draw.polygon(self.screen, (255, 80, 0), [(flame_x, y + 150), (flame_x - 8, y + 150 - flame_height), (flame_x + 8, y + 150)])
            pygame.draw.polygon(self.screen, (80, 25, 25), [(x + 100, y + 150), (x + 50, y + 80), (x + 150, y + 80)])
            smoke_y = y + 60 + math.sin(self.animation_timer * 0.5 + index) * 10
            pygame.draw.circle(self.screen, (70, 70, 70), (x + 100, smoke_y), 8)
            pygame.draw.circle(self.screen, (90, 90, 90), (x + 108, smoke_y + 5), 6)
        
        elif theme == LevelTheme.SHADOW:
            pygame.draw.rect(self.screen, (25, 15, 40), (x, y, 200, 150))
            for i in range(5):
                shadow_x = x + 25 + i * 35
                pygame.draw.circle(self.screen, (35, 25, 55), (shadow_x, y + 130), 12 + (i % 3) * 3)
            moon_phase = int((self.animation_timer * 0.3 + index) % 4)
            pygame.draw.circle(self.screen, (160, 160, 180), (x + 160, y + 35), 18)
            if moon_phase > 0:
                pygame.draw.circle(self.screen, (25, 15, 40), (x + 160 + moon_phase * 4, y + 35), 14)
            for i in range(5):
                sparkle_x = x + 30 + i * 30
                sparkle_y = y + 40 + (i % 2) * 30
                sparkle_alpha = int((math.sin(self.animation_timer * 3 + i) + 1) * 127)
                sparkle = pygame.Surface((4, 4), pygame.SRCALPHA)
                sparkle.fill((255, 255, 255, sparkle_alpha))
                self.screen.blit(sparkle, (sparkle_x, sparkle_y))
        
        elif theme == LevelTheme.CAVE:
            pygame.draw.rect(self.screen, (25, 25, 30), (x, y, 200, 150))
            for i in range(6):
                stal_x = x + 15 + i * 30
                stal_height = 15 + (i % 3) * 10
                pygame.draw.polygon(self.screen, (60, 55, 50), [(stal_x, y), (stal_x - 6, y + stal_height), (stal_x + 6, y + stal_height)])
            for i in range(3):
                gem_x = x + 50 + i * 50
                gem_y = y + 100 + (i % 2) * 20
                pygame.draw.circle(self.screen, (150, 100, 200), (gem_x, gem_y), 8)
                pygame.draw.circle(self.screen, (180, 130, 230), (gem_x, gem_y), 4)
        
        elif theme == LevelTheme.OCEAN:
            pygame.draw.rect(self.screen, (20, 60, 100), (x, y, 200, 150))
            for i in range(5):
                wave_y = y + 110 + math.sin(self.animation_timer * 2 + i) * 5
                pygame.draw.arc(self.screen, (80, 150, 200), (x + 10 + i * 40, wave_y, 30, 20), math.pi, 0, 2)
            for i in range(3):
                fish_x = (x + 20 + i * 60 + self.animation_timer * 20) % 220
                fish_y = y + 60 + (i % 2) * 30
                pygame.draw.ellipse(self.screen, (100, 200, 150), (fish_x, fish_y, 15, 8))
                pygame.draw.polygon(self.screen, (100, 200, 150), [(fish_x + 15, fish_y + 4), (fish_x + 20, fish_y), (fish_x + 20, fish_y + 8)])
        
        elif theme == LevelTheme.SKY:
            pygame.draw.rect(self.screen, (100, 150, 200), (x, y, 200, 150))
            for i in range(4):
                cloud_y = y + 30 + i * 25 + math.sin(self.animation_timer * 0.5 + i) * 5
                pygame.draw.ellipse(self.screen, (255, 255, 255), (x + 20 + i * 45, cloud_y, 35, 15))
                pygame.draw.ellipse(self.screen, (255, 255, 255), (x + 30 + i * 45, cloud_y - 5, 25, 12))
            for i in range(2):
                island_x = x + 50 + i * 80
                pygame.draw.ellipse(self.screen, (80, 150, 80), (island_x, y + 110, 40, 20))
                pygame.draw.polygon(self.screen, (60, 120, 60), [(island_x + 20, y + 90), (island_x + 10, y + 110), (island_x + 30, y + 110)])
        
        elif theme == LevelTheme.SWAMP:
            pygame.draw.rect(self.screen, (30, 40, 25), (x, y, 200, 150))
            for i in range(4):
                lily_x = x + 30 + i * 45
                lily_y = y + 100 + (i % 2) * 25
                pygame.draw.circle(self.screen, (60, 80, 50), (lily_x, lily_y), 12)
                pygame.draw.circle(self.screen, (80, 100, 70), (lily_x, lily_y), 8)
                pygame.draw.polygon(self.screen, (100, 150, 100), [(lily_x, lily_y - 8), (lily_x - 6, lily_y - 2), (lily_x + 6, lily_y - 2)])
            fog_alpha = int((math.sin(self.animation_timer + index) + 1) * 50)
            fog = pygame.Surface((200, 40), pygame.SRCALPHA)
            fog.fill((80, 90, 70, fog_alpha))
            self.screen.blit(fog, (x, y + 50))
        
        elif theme == LevelTheme.JUNGLE:
            pygame.draw.rect(self.screen, (20, 60, 40), (x, y, 200, 150))
            for i in range(3):
                vine_x = x + 30 + i * 60
                for j in range(5):
                    vine_y = y + j * 30 + math.sin(self.animation_timer * 2 + i + j) * 3
                    pygame.draw.circle(self.screen, (30, 80, 50), (vine_x, vine_y), 3)
            for i in range(2):
                parrot_x = x + 50 + i * 80
                parrot_y = y + 50 + math.sin(self.animation_timer * 2 + i) * 5
                pygame.draw.ellipse(self.screen, (255, 100, 100), (parrot_x, parrot_y, 12, 8))
                pygame.draw.polygon(self.screen, (255, 200, 100), [(parrot_x + 12, parrot_y + 4), (parrot_x + 18, parrot_y), (parrot_x + 18, parrot_y + 8)])
    
    def draw_locked_level_cover(self, x, y, level, index):
        theme = level.theme
        
        if theme == LevelTheme.FOREST:
            pygame.draw.rect(self.screen, (20, 40, 20), (x, y, 200, 150))
            for i in range(5):
                tree_x = x + 20 + i * 40
                pygame.draw.polygon(self.screen, (15, 30, 15), [(tree_x - 10, y + 150), (tree_x, y + 100), (tree_x + 10, y + 150)])
        
        elif theme == LevelTheme.ICE:
            pygame.draw.rect(self.screen, (30, 50, 80), (x, y, 200, 150))
            for i in range(4):
                snow_x = x + 25 + i * 45
                pygame.draw.polygon(self.screen, (60, 80, 120), [(snow_x, y + 110), (snow_x - 6, y + 125), (snow_x + 6, y + 125)])
        
        elif theme == LevelTheme.CASTLE:
            pygame.draw.rect(self.screen, (30, 30, 40), (x, y, 200, 150))
            pygame.draw.rect(self.screen, (50, 50, 50), (x + 70, y + 60, 60, 90))
        
        elif theme == LevelTheme.DESERT:
            pygame.draw.rect(self.screen, (80, 60, 30), (x, y, 200, 150))
            for i in range(3):
                sand_x = x + 30 + i * 55
                pygame.draw.polygon(self.screen, (90, 70, 40), [(sand_x, y + 150), (sand_x - 12, y + 120), (sand_x + 12, y + 150)])
        
        elif theme == LevelTheme.VOLCANO:
            pygame.draw.rect(self.screen, (50, 15, 15), (x, y, 200, 150))
            pygame.draw.polygon(self.screen, (40, 12, 12), [(x + 100, y + 150), (x + 60, y + 90), (x + 140, y + 90)])
        
        elif theme == LevelTheme.SHADOW:
            pygame.draw.rect(self.screen, (15, 10, 25), (x, y, 200, 150))
            for i in range(4):
                shadow_x = x + 30 + i * 40
                pygame.draw.circle(self.screen, (20, 15, 30), (shadow_x, y + 130), 10)
        
        elif theme == LevelTheme.CAVE:
            pygame.draw.rect(self.screen, (15, 15, 20), (x, y, 200, 150))
            for i in range(5):
                stal_x = x + 20 + i * 35
                pygame.draw.polygon(self.screen, (30, 30, 35), [(stal_x, y), (stal_x - 5, y + 12), (stal_x + 5, y + 12)])
        
        elif theme == LevelTheme.OCEAN:
            pygame.draw.rect(self.screen, (10, 30, 60), (x, y, 200, 150))
            for i in range(4):
                wave_y = y + 120
                pygame.draw.arc(self.screen, (30, 60, 100), (x + 15 + i * 45, wave_y, 25, 15), math.pi, 0, 1)
        
        elif theme == LevelTheme.SKY:
            pygame.draw.rect(self.screen, (60, 100, 140), (x, y, 200, 150))
            for i in range(3):
                pygame.draw.ellipse(self.screen, (100, 130, 160), (x + 25 + i * 50, y + 30 + i * 10, 30, 12))
        
        elif theme == LevelTheme.SWAMP:
            pygame.draw.rect(self.screen, (20, 25, 15), (x, y, 200, 150))
            for i in range(3):
                lily_x = x + 40 + i * 50
                pygame.draw.circle(self.screen, (30, 40, 25), (lily_x, y + 110), 10)
        
        elif theme == LevelTheme.JUNGLE:
            pygame.draw.rect(self.screen, (10, 35, 20), (x, y, 200, 150))
            for i in range(3):
                vine_x = x + 40 + i * 50
                for j in range(4):
                    pygame.draw.circle(self.screen, (15, 50, 30), (vine_x, y + 30 + j * 30), 2)
    
    def draw_dev_panel(self):
        panel_x = self.dev_panel_x
        panel_y = self.dev_panel_y
        panel_width = 360
        panel_height = SCREEN_HEIGHT - 80
        
        panel_rect = pygame.Rect(panel_x, panel_y, panel_width, panel_height)
        pygame.draw.rect(self.screen, (25, 25, 45), panel_rect, border_radius=12)
        pygame.draw.rect(self.screen, COLOR_GOLD, panel_rect, 2, border_radius=12)
        
        drag_bar_rect = pygame.Rect(panel_x + 10, panel_y + 8, panel_width - 55, 27)
        if self.dev_panel_dragging:
            pygame.draw.rect(self.screen, COLOR_GOLD, drag_bar_rect, border_radius=6)
        else:
            pygame.draw.rect(self.screen, (40, 40, 60), drag_bar_rect, border_radius=6)
        
        title_text = self.font.render("🎮 作弊面板", True, COLOR_GOLD)
        title_rect = title_text.get_rect(center=(panel_x + panel_width // 2, panel_y + 25))
        self.screen.blit(title_text, title_rect)
        
        close_button = pygame.Rect(panel_x + panel_width - 35, panel_y + 8, 27, 27)
        pygame.draw.rect(self.screen, COLOR_RED, close_button, border_radius=6)
        close_text = self.font_small.render("✕", True, COLOR_WHITE)
        close_rect = close_text.get_rect(center=close_button.center)
        self.screen.blit(close_text, close_rect)
        
        content_y = panel_y + 50
        
        self.draw_dev_game_panel(panel_x, panel_width, content_y)
    
    def draw_dev_game_panel(self, panel_x, panel_width, content_y):
        button_width = panel_width - 20
        button_height = 48
        gap = 10
        y = content_y
        
        buttons = [
            {"icon": "$", "text": f"增加金币 +100 (当前: {self.gold})", "color": COLOR_GREEN, "icon_color": (255, 215, 0)},
            {"icon": "♥", "text": f"增加生命 +5 (当前: {self.lives})", "color": COLOR_RED, "icon_color": (255, 100, 100)},
            {"icon": "#", "text": "解锁所有关卡", "color": COLOR_BLUE, "icon_color": (200, 200, 200)},
            {"icon": "X", "text": "清除所有敌人", "color": COLOR_GRAY, "icon_color": (200, 200, 200)},
            {"icon": ">", "text": f"开始下一波 ({self.wave_index + 1}/{len(self.current_level.waves) if self.current_level else 0})", "color": COLOR_PURPLE, "icon_color": (200, 150, 255)},
            {"icon": "*", "text": "跳转到关卡", "color": (128, 0, 128), "icon_color": (200, 100, 200)},
            {"icon": "🗑️", "text": "清除游戏记录", "color": (139, 0, 0), "icon_color": (255, 100, 100)},
        ]
        
        icon_font = pygame.font.Font(None, 28)
        
        for i, btn in enumerate(buttons):
            button_rect = pygame.Rect(panel_x + 10, y, button_width, button_height)
            pygame.draw.rect(self.screen, btn["color"], button_rect, border_radius=8)
            
            icon_text = icon_font.render(btn["icon"], True, btn["icon_color"])
            icon_x = panel_x + 20
            icon_y = y + (button_height - icon_text.get_height()) // 2
            self.screen.blit(icon_text, (icon_x, icon_y))
            
            button_text = self.font_small.render(btn["text"], True, COLOR_WHITE)
            text_x = panel_x + 50
            text_y = y + (button_height - button_text.get_height()) // 2
            self.screen.blit(button_text, (text_x, text_y))
            
            y += button_height + gap
            if y > SCREEN_HEIGHT - 30:
                break
    
    def handle_dev_panel_click(self, pos):
        panel_x = self.dev_panel_x
        panel_y = self.dev_panel_y
        panel_width = 360
        
        close_button = pygame.Rect(panel_x + panel_width - 35, panel_y + 8, 27, 27)
        if close_button.collidepoint(pos):
            self.dev_panel_active = False
            return
        
        drag_bar_rect = pygame.Rect(panel_x + 10, panel_y + 8, panel_width - 55, 27)
        if drag_bar_rect.collidepoint(pos):
            self.dev_panel_dragging = True
            self.dev_panel_drag_offset = (pos[0] - panel_x, pos[1] - panel_y)
            return
        
        button_width = panel_width - 20
        button_height = 48
        gap = 10
        y = panel_y + 50
        
        if pygame.Rect(panel_x + 10, y, button_width, button_height).collidepoint(pos):
            self.gold += 100
            return
        
        y += button_height + gap
        if pygame.Rect(panel_x + 10, y, button_width, button_height).collidepoint(pos):
            self.lives += 5
            return
        
        y += button_height + gap
        if pygame.Rect(panel_x + 10, y, button_width, button_height).collidepoint(pos):
            for level in self.levels:
                level.unlocked = True
            return
        
        y += button_height + gap
        if pygame.Rect(panel_x + 10, y, button_width, button_height).collidepoint(pos):
            self.enemies = []
            return
        
        y += button_height + gap
        if pygame.Rect(panel_x + 10, y, button_width, button_height).collidepoint(pos) and self.current_level:
            if self.wave_index < len(self.current_level.waves) - 1:
                self.wave_index += 1
                self.start_wave()
            return
        
        y += button_height + gap
        if pygame.Rect(panel_x + 10, y, button_width, button_height).collidepoint(pos):
            self.show_level_jump_dialog = True
            return
        
        y += button_height + gap
        if pygame.Rect(panel_x + 10, y, button_width, button_height).collidepoint(pos):
            self.clear_game_progress()
            return
    
    def get_scroll_offset(self):
        mouse_y = pygame.mouse.get_pos()[1]
        scroll_range = max(0, len(self.levels) * 220 - SCREEN_HEIGHT + 200)
        return (mouse_y / SCREEN_HEIGHT) * scroll_range if scroll_range > 0 else 0
    
    def draw_level_card(self, index, level, scroll_offset):
        card_y = 120 + index * 220 - scroll_offset
        card_x = (SCREEN_WIDTH - 600) // 2
        
        if card_y < -200 or card_y > SCREEN_HEIGHT + 100:
            return
        
        card_rect = pygame.Rect(card_x, card_y, 600, 180)
        mouse_pos = pygame.mouse.get_pos()
        is_hovered = card_rect.collidepoint(mouse_pos) and level.unlocked
        
        self.draw_level_background(card_x, card_y, level.theme)
        
        self.draw_level_decorations(card_x, card_y, level.theme, index)
        
        overlay = pygame.Surface((600, 180), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 120))
        self.screen.blit(overlay, (card_x, card_y))
        
        if level.unlocked:
            border_color = COLOR_GOLD if is_hovered else COLOR_WHITE
            border_width = 3 if is_hovered else 2
            pygame.draw.rect(self.screen, border_color, card_rect, border_width, border_radius=15)
            
            if is_hovered:
                glow_surface = pygame.Surface((600, 180), pygame.SRCALPHA)
                pygame.draw.rect(glow_surface, (255, 215, 0, 30), glow_surface.get_rect(), border_radius=15)
                self.screen.blit(glow_surface, (card_x, card_y))
            
            title_text = self.font_large.render(level.name, True, COLOR_GOLD)
            title_rect = title_text.get_rect(left=card_x + 30, top=card_y + 20)
            self.screen.blit(title_text, title_rect)
            
            desc_text = self.font.render(self.get_level_description(level.theme), True, COLOR_WHITE)
            desc_rect = desc_text.get_rect(left=card_x + 30, top=card_y + 65)
            self.screen.blit(desc_text, desc_rect)
            
            difficulty = self.get_level_difficulty(index)
            difficulty_text = self.font.render(f"难度: {'★' * difficulty}{'☆' * (5 - difficulty)}", True, (255, 200, 0))
            difficulty_rect = difficulty_text.get_rect(left=card_x + 30, top=card_y + 100)
            self.screen.blit(difficulty_text, difficulty_rect)
            
            reward_text = self.font.render(f"奖励: {level.gold_reward} 金币", True, COLOR_GREEN)
            reward_rect = reward_text.get_rect(right=card_x + 570, top=card_y + 20)
            self.screen.blit(reward_text, reward_rect)
            
            wave_count = len(level.waves)
            wave_text = self.font.render(f"波次: {wave_count}", True, COLOR_CYAN)
            wave_rect = wave_text.get_rect(right=card_x + 570, top=card_y + 65)
            self.screen.blit(wave_text, wave_rect)
            
            self.draw_path_preview(card_x + 350, card_y + 100, level.theme, index)
        else:
            pygame.draw.rect(self.screen, COLOR_GRAY, card_rect, border_radius=15)
            pygame.draw.rect(self.screen, COLOR_DARK_GRAY, card_rect, 2, border_radius=15)
            
            lock_text = self.font_large.render("🔒", True, COLOR_GRAY)
            lock_rect = lock_text.get_rect(center=(card_x + 300, card_y + 90))
            self.screen.blit(lock_text, lock_rect)
            
            locked_text = self.font.render("完成前一关解锁", True, COLOR_GRAY)
            locked_rect = locked_text.get_rect(center=(card_x + 300, card_y + 130))
            self.screen.blit(locked_text, locked_rect)
    
    def draw_level_background(self, x, y, theme):
        bg_surface = pygame.Surface((600, 180))
        
        if theme == LevelTheme.FOREST:
            bg_surface.fill((40, 80, 40))
            for i in range(10):
                tree_x = x + 50 + i * 60
                pygame.draw.polygon(bg_surface, (30, 60, 30), [(tree_x - 15, y + 180), (tree_x, y + 120), (tree_x + 15, y + 180)])
                pygame.draw.rect(bg_surface, (20, 50, 20), (tree_x - 5, y + 160, 10, 20))
        elif theme == LevelTheme.ICE:
            bg_surface.fill((80, 120, 180))
            for i in range(8):
                snow_x = x + 30 + i * 75
                snow_y = y + 100 + (i % 3) * 20
                pygame.draw.polygon(bg_surface, (200, 220, 255), [(snow_x, snow_y), (snow_x - 10, snow_y + 20), (snow_x + 10, snow_y + 20)])
        elif theme == LevelTheme.CASTLE:
            bg_surface.fill((80, 80, 100))
            pygame.draw.rect(bg_surface, (120, 120, 120), (x + 250, y + 40, 100, 140))
            pygame.draw.polygon(bg_surface, (140, 140, 140), [(x + 230, y + 80), (x + 250, y + 40), (x + 270, y + 80)])
            pygame.draw.polygon(bg_surface, (140, 140, 140), [(x + 330, y + 80), (x + 350, y + 40), (x + 370, y + 80)])
        elif theme == LevelTheme.DESERT:
            bg_surface.fill((180, 140, 80))
            for i in range(6):
                sand_x = x + 50 + i * 100
                pygame.draw.polygon(bg_surface, (200, 160, 100), [(sand_x, y + 180), (sand_x - 20, y + 140), (sand_x + 20, y + 180)])
        elif theme == LevelTheme.VOLCANO:
            bg_surface.fill((120, 40, 40))
            for i in range(5):
                flame_x = x + 80 + i * 110
                flame_height = 30 + (i % 2) * 20
                pygame.draw.polygon(bg_surface, (255, 100, 0), [(flame_x, y + 180), (flame_x - 10, y + 180 - flame_height), (flame_x + 10, y + 180)])
        elif theme == LevelTheme.SHADOW:
            bg_surface.fill((30, 20, 50))
            for i in range(8):
                shadow_x = x + 40 + i * 70
                pygame.draw.circle(bg_surface, (50, 40, 70), (shadow_x, y + 160), 15 + (i % 3) * 5)
        
        self.screen.blit(bg_surface, (x, y))
    
    def draw_level_decorations(self, x, y, theme, index):
        anim_offset = math.sin(self.animation_timer * 2 + index) * 5
        
        if theme == LevelTheme.FOREST:
            for i in range(3):
                bird_y = y + 30 + i * 25 + anim_offset
                pygame.draw.circle(self.screen, (200, 180, 160), (x + 550 + i * 20, bird_y), 5)
        elif theme == LevelTheme.ICE:
            for i in range(4):
                snowflake_y = (y + 20 + i * 35 + anim_offset * 0.5) % 180
                pygame.draw.circle(self.screen, (255, 255, 255), (x + 540 + i * 15, y + snowflake_y), 3)
        elif theme == LevelTheme.CASTLE:
            flag_y = y + 50 + anim_offset
            pygame.draw.line(self.screen, COLOR_BROWN, (x + 300, y + 50), (x + 300, y + 20))
            pygame.draw.polygon(self.screen, COLOR_RED, [(x + 300, y + 20), (x + 320, flag_y), (x + 300, flag_y)])
        elif theme == LevelTheme.DESERT:
            sun_glow = int((math.sin(self.animation_timer + index) + 1) * 20)
            pygame.draw.circle(self.screen, (255, 200 + sun_glow, 100), (x + 550, y + 40), 25)
        elif theme == LevelTheme.VOLCANO:
            smoke_y = y + 20 + anim_offset * 0.3
            pygame.draw.circle(self.screen, (80, 80, 80), (x + 550, smoke_y), 10)
            pygame.draw.circle(self.screen, (100, 100, 100), (x + 560, smoke_y + 5), 8)
        elif theme == LevelTheme.SHADOW:
            moon_phase = int((self.animation_timer * 0.5 + index) % 4)
            if moon_phase == 0:
                pygame.draw.circle(self.screen, (180, 180, 200), (x + 550, y + 40), 15)
            else:
                pygame.draw.circle(self.screen, (180, 180, 200), (x + 550, y + 40), 15)
                pygame.draw.circle(self.screen, (30, 20, 50), (x + 550 + moon_phase * 3, y + 40), 12)
    
    def draw_path_preview(self, x, y, theme, index):
        path_points = self.get_path_preview_points(index)
        
        if len(path_points) < 2:
            return
        
        path_color = self.get_theme_path_color(theme)
        
        for i in range(len(path_points) - 1):
            start_x = x + path_points[i][0]
            start_y = y + path_points[i][1]
            end_x = x + path_points[i + 1][0]
            end_y = y + path_points[i + 1][1]
            pygame.draw.line(self.screen, path_color, (start_x, start_y), (end_x, end_y), 3)
        
        for point in path_points:
            pygame.draw.circle(self.screen, (255, 255, 255), (x + point[0], y + point[1]), 4)
        
        start_icon = pygame.Surface((16, 16))
        start_icon.fill((0, 255, 0))
        self.screen.blit(start_icon, (x + path_points[0][0] - 8, y + path_points[0][1] - 8))
        
        end_icon = pygame.Surface((16, 16))
        end_icon.fill((255, 0, 0))
        self.screen.blit(end_icon, (x + path_points[-1][0] - 8, y + path_points[-1][1] - 8))
    
    def get_path_preview_points(self, index):
        path_patterns = [
            [(0, 40), (50, 40), (50, 0), (100, 0), (100, 40), (150, 40)],
            [(0, 0), (40, 0), (40, 40), (80, 40), (80, 20), (120, 20), (120, 40), (160, 40)],
            [(0, 20), (30, 20), (30, 0), (60, 0), (60, 40), (90, 40), (90, 10), (120, 10), (120, 40), (150, 40)],
            [(0, 40), (40, 40), (40, 10), (80, 10), (80, 40), (120, 40), (120, 20), (160, 20)],
            [(0, 30), (30, 30), (30, 0), (60, 0), (60, 30), (90, 30), (90, 10), (120, 10), (120, 30), (150, 30), (150, 0), (180, 0)],
            [(0, 40), (50, 40), (50, 10), (100, 10), (100, 40), (150, 40), (150, 20), (200, 20)]
        ]
        return path_patterns[index % len(path_patterns)]
    
    def get_theme_path_color(self, theme):
        colors = {
            LevelTheme.FOREST: (160, 140, 100),
            LevelTheme.ICE: (220, 220, 240),
            LevelTheme.CASTLE: (180, 180, 180),
            LevelTheme.DESERT: (160, 140, 100),
            LevelTheme.VOLCANO: (140, 80, 40),
            LevelTheme.SHADOW: (80, 60, 100)
        }
        return colors.get(theme, COLOR_GRAY)
    
    def get_level_description(self, theme):
        descriptions = {
            LevelTheme.FOREST: "茂密的森林中隐藏着哥布林的踪迹...",
            LevelTheme.ICE: "冰封的峡谷中，暗影狼正在徘徊...",
            LevelTheme.CASTLE: "古老的城堡废墟中，亡灵军团苏醒了...",
            LevelTheme.DESERT: "灼热的沙漠中，危险潜伏在沙丘之后...",
            LevelTheme.VOLCANO: "炽热的火山深处，恶魔正在聚集...",
            LevelTheme.SHADOW: "暗影要塞中，最终的挑战等待着你..."
        }
        return descriptions.get(theme, "")
    
    def get_level_difficulty(self, index):
        return min(5, index + 1)
    
    def draw_level_select_ui(self):
        title_text = self.font_large.render("选择关卡", True, COLOR_GOLD)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 50))
        
        title_glow = pygame.Surface((title_rect.width + 20, title_rect.height + 16), pygame.SRCALPHA)
        pygame.draw.rect(title_glow, (255, 215, 0, 50), (0, 0, title_rect.width + 20, title_rect.height + 16), border_radius=10)
        self.screen.blit(title_glow, (title_rect.x - 10, title_rect.y - 8))
        self.screen.blit(title_text, title_rect)
        
        mouse_pos = pygame.mouse.get_pos()
        back_button = pygame.Rect(30, 30, 100, 40)
        is_back_hovered = back_button.collidepoint(mouse_pos)
        
        if is_back_hovered:
            back_color = (80, 100, 130)
            back_border = COLOR_GOLD
            back_text_color = COLOR_GOLD
        else:
            back_color = COLOR_GRAY
            back_border = COLOR_WHITE
            back_text_color = COLOR_WHITE
        
        pygame.draw.rect(self.screen, back_color, back_button, border_radius=6)
        pygame.draw.rect(self.screen, back_border, back_button, 2, border_radius=6)
        back_text = self.font.render("返回", True, back_text_color)
        back_rect = back_text.get_rect(center=back_button.center)
        self.screen.blit(back_text, back_rect)
    
    def draw_scroll_indicators(self):
        mouse_y = pygame.mouse.get_pos()[1]
        scroll_progress = mouse_y / SCREEN_HEIGHT
        
        indicator_y = 60 + scroll_progress * (SCREEN_HEIGHT - 120)
        
        pygame.draw.rect(self.screen, COLOR_DARK_GRAY, (SCREEN_WIDTH - 15, 60, 10, SCREEN_HEIGHT - 120), border_radius=5)
        pygame.draw.rect(self.screen, COLOR_GOLD, (SCREEN_WIDTH - 15, indicator_y - 20, 10, 40), border_radius=5)
                
    def draw_locked_level_dialog(self):
        dialog_width = 400
        dialog_height = 220
        dialog_x = (SCREEN_WIDTH - dialog_width) // 2
        dialog_y = (SCREEN_HEIGHT - dialog_height) // 2
        
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))
        
        pygame.draw.rect(self.screen, COLOR_DARK_GRAY, (dialog_x, dialog_y, dialog_width, dialog_height), border_radius=15)
        pygame.draw.rect(self.screen, COLOR_GOLD, (dialog_x, dialog_y, dialog_width, dialog_height), 3, border_radius=15)
        
        title_text = self.font_large.render("关卡未解锁", True, COLOR_RED)
        title_rect = title_text.get_rect(center=(dialog_x + dialog_width // 2, dialog_y + 45))
        self.screen.blit(title_text, title_rect)
        
        level_name = self.levels[self.locked_level_index].name if 0 <= self.locked_level_index < len(self.levels) else "该关卡"
        message_lines = [
            f"确定开启{level_name}吗？",
            "开启需要满足上一关卡通关",
            ""
        ]
        
        y_offset = 85
        for line in message_lines:
            text = self.font.render(line, True, COLOR_WHITE)
            text_rect = text.get_rect(center=(dialog_x + dialog_width // 2, dialog_y + y_offset))
            self.screen.blit(text, text_rect)
            y_offset += 30
        
        button_width = 150
        button_height = 45
        button_gap = 30
        
        ok_button = pygame.Rect(dialog_x + dialog_width // 2 - button_width - button_gap // 2, dialog_y + dialog_height - 65, button_width, button_height)
        cancel_button = pygame.Rect(dialog_x + dialog_width // 2 + button_gap // 2, dialog_y + dialog_height - 65, button_width, button_height)
        
        pygame.draw.rect(self.screen, COLOR_GREEN, ok_button, border_radius=8)
        pygame.draw.rect(self.screen, COLOR_WHITE, ok_button, 2, border_radius=8)
        ok_text = self.font.render("确定", True, COLOR_WHITE)
        ok_rect = ok_text.get_rect(center=ok_button.center)
        self.screen.blit(ok_text, ok_rect)
        
        pygame.draw.rect(self.screen, COLOR_RED, cancel_button, border_radius=8)
        pygame.draw.rect(self.screen, COLOR_WHITE, cancel_button, 2, border_radius=8)
        cancel_text = self.font.render("取消", True, COLOR_WHITE)
        cancel_rect = cancel_text.get_rect(center=cancel_button.center)
        self.screen.blit(cancel_text, cancel_rect)

    def handle_locked_level_dialog_click(self, pos):
        dialog_width = 400
        dialog_height = 220
        dialog_x = (SCREEN_WIDTH - dialog_width) // 2
        dialog_y = (SCREEN_HEIGHT - dialog_height) // 2
        
        button_width = 150
        button_height = 45
        button_gap = 30
        
        ok_button = pygame.Rect(dialog_x + dialog_width // 2 - button_width - button_gap // 2, dialog_y + dialog_height - 65, button_width, button_height)
        cancel_button = pygame.Rect(dialog_x + dialog_width // 2 + button_gap // 2, dialog_y + dialog_height - 65, button_width, button_height)
        
        if ok_button.collidepoint(pos):
            prev_level_index = self.locked_level_index - 1
            if prev_level_index >= 0 and self.levels[prev_level_index].completed:
                self.levels[self.locked_level_index].unlocked = True
                self.save_game_progress()
            self.show_locked_level_dialog = False
        elif cancel_button.collidepoint(pos):
            self.show_locked_level_dialog = False

    def draw_game_ui(self):
        ui_gradient = pygame.Surface((SCREEN_WIDTH, 60))
        for y in range(60):
            ratio = y / 60
            r = int(20 + ratio * 10)
            g = int(20 + ratio * 10)
            b = int(30 + ratio * 15)
            pygame.draw.line(ui_gradient, (r, g, b), (0, y), (SCREEN_WIDTH, y))
        self.screen.blit(ui_gradient, (0, 0))
        
        pygame.draw.rect(self.screen, (255, 255, 255, 20), (0, 0, SCREEN_WIDTH, 60))
        
        gold_pulse = (math.sin(self.animation_timer * 3) + 1) * 0.2
        gold_color = (
            int(255),
            int(215 + gold_pulse * 40),
            int(0 + gold_pulse * 30)
        )
        gold_text = self.font.render(f"金币: {self.gold}", True, gold_color)
        self.screen.blit(gold_text, (20, 15))
        
        lives_pulse = (math.sin(self.animation_timer * 4) + 1) * 0.3
        if self.lives <= 5:
            lives_color = (
                int(255),
                int(100 + lives_pulse * 50),
                int(100 + lives_pulse * 50)
            )
        else:
            lives_color = COLOR_RED
        lives_text = self.font.render(f"生命: {self.lives}", True, lives_color)
        self.screen.blit(lives_text, (20, 40))
        
        score_pulse = (math.sin(self.animation_timer * 2) + 1) * 0.1
        score_color = (
            int(255 - score_pulse * 50),
            int(255 - score_pulse * 50),
            int(255)
        )
        score_text = self.font.render(f"得分: {self.score}", True, score_color)
        score_rect = score_text.get_rect(right=SCREEN_WIDTH - 20, top=15)
        self.screen.blit(score_text, score_rect)
        
        wave_progress = (self.wave_index) / len(self.current_level.waves)
        total_waves = len(self.current_level.waves)
        remaining_enemies = self.current_wave_total_enemies - self.current_wave_killed_enemies
        
        wave_bar_bg_width = 180
        wave_bar_bg_height = 28
        wave_bar_bg_x = 130
        wave_bar_bg_y = 15
        
        pygame.draw.rect(self.screen, (30, 30, 40), (wave_bar_bg_x, wave_bar_bg_y, wave_bar_bg_width, wave_bar_bg_height), border_radius=8)
        
        border_color = (80, 80, 100)
        pygame.draw.rect(self.screen, border_color, (wave_bar_bg_x, wave_bar_bg_y, wave_bar_bg_width, wave_bar_bg_height), width=2, border_radius=8)
        
        wave_bar_width = wave_bar_bg_width - 6
        wave_bar_height = 8
        wave_bar_x = wave_bar_bg_x + 3
        wave_bar_y = wave_bar_bg_y + 17
        
        pygame.draw.rect(self.screen, (40, 40, 50), (wave_bar_x, wave_bar_y, wave_bar_width, wave_bar_height), border_radius=4)
        
        fill_width = wave_bar_width * wave_progress
        if fill_width > 0:
            fill_surface = pygame.Surface((fill_width, wave_bar_height))
            fill_surface.fill((50, 200, 50))
            fill_surface.set_alpha(255)
            self.screen.blit(fill_surface, (wave_bar_x, wave_bar_y))
            
            highlight_surface = pygame.Surface((fill_width, wave_bar_height // 2))
            highlight_surface.fill((100, 255, 100))
            highlight_surface.set_alpha(100)
            self.screen.blit(highlight_surface, (wave_bar_x, wave_bar_y))
        
        wave_text = self.font.render(f"波次 {self.wave_index + 1}/{total_waves}", True, (255, 215, 0))
        wave_text_rect = wave_text.get_rect(centerx=wave_bar_bg_x + wave_bar_bg_width // 2, top=wave_bar_bg_y + 3)
        self.screen.blit(wave_text, wave_text_rect)
        
        enemy_bg_y = wave_bar_bg_y + wave_bar_bg_height + 3
        pygame.draw.rect(self.screen, (30, 30, 40), (wave_bar_bg_x, enemy_bg_y, wave_bar_bg_width, 24), border_radius=6)
        pygame.draw.rect(self.screen, border_color, (wave_bar_bg_x, enemy_bg_y, wave_bar_bg_width, 24), width=2, border_radius=6)
        
        enemy_icon = "👹"
        enemy_text = self.font_small.render(f"{enemy_icon} 当前波次剩余: {remaining_enemies}个敌人", True, (255, 200, 100))
        enemy_text_rect = enemy_text.get_rect(centerx=wave_bar_bg_x + wave_bar_bg_width // 2, top=enemy_bg_y + 4)
        self.screen.blit(enemy_text, enemy_text_rect)

        mouse_pos = pygame.mouse.get_pos()
        
        if self.developer_mode:
            dev_panel_button = pygame.Rect(SCREEN_WIDTH // 2 - 90, 15, 180, 30)
            is_dev_hovered = dev_panel_button.collidepoint(mouse_pos)
            
            if is_dev_hovered:
                dev_color = COLOR_GOLD
                dev_text_color = COLOR_BLACK
            else:
                dev_color = COLOR_GREEN
                dev_text_color = COLOR_WHITE
            
            pygame.draw.rect(self.screen, dev_color, dev_panel_button, border_radius=4)
            pygame.draw.rect(self.screen, COLOR_WHITE, dev_panel_button, 2, border_radius=4)
            dev_text = self.font_small.render("开发者面板", True, dev_text_color)
            dev_rect = dev_text.get_rect(center=dev_panel_button.center)
            self.screen.blit(dev_text, dev_rect)

        pause_button = pygame.Rect(SCREEN_WIDTH - 100, 15, 80, 30)
        is_pause_hovered = pause_button.collidepoint(mouse_pos)
        
        if is_pause_hovered:
            pause_color = (80, 100, 130)
            pause_border = COLOR_GOLD
            pause_text_color = COLOR_GOLD
        else:
            pause_color = COLOR_GRAY
            pause_border = COLOR_WHITE
            pause_text_color = COLOR_WHITE
        
        pygame.draw.rect(self.screen, pause_color, pause_button, border_radius=4)
        pygame.draw.rect(self.screen, pause_border, pause_button, 2, border_radius=4)
        pause_text = self.font_small.render("暂停", True, pause_text_color)
        pause_rect = pause_text.get_rect(center=pause_button.center)
        self.screen.blit(pause_text, pause_rect)
        
        if self.selected_tower_type:
            self.draw_tower_selection_ui()
        elif self.selected_tower:
            self.draw_selected_tower_ui()
        else:
            self.draw_tower_buttons()
    
    def draw_cheat_password_dialog(self):
        if not self.show_cheat_password_dialog:
            return
        
        dialog_width = 350
        dialog_height = 220
        dialog_x = (SCREEN_WIDTH - dialog_width) // 2
        dialog_y = (SCREEN_HEIGHT - dialog_height) // 2
        
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))
        
        pygame.draw.rect(self.screen, COLOR_DARK_GRAY, (dialog_x, dialog_y, dialog_width, dialog_height), border_radius=15)
        pygame.draw.rect(self.screen, COLOR_GOLD, (dialog_x, dialog_y, dialog_width, dialog_height), 3, border_radius=15)
        
        title_text = self.font_large.render("🔒 输入密码", True, COLOR_RED)
        title_rect = title_text.get_rect(center=(dialog_x + dialog_width // 2, dialog_y + 40))
        self.screen.blit(title_text, title_rect)
        
        input_box = pygame.Rect(dialog_x + 30, dialog_y + 90, dialog_width - 60, 45)
        pygame.draw.rect(self.screen, (30, 30, 40), input_box, border_radius=8)
        pygame.draw.rect(self.screen, COLOR_GOLD if self.cheat_password_input else COLOR_GRAY, input_box, 2, border_radius=8)
        
        input_text = self.font_large.render("*" * len(self.cheat_password_input), True, COLOR_WHITE)
        input_rect = input_text.get_rect(center=input_box.center)
        self.screen.blit(input_text, input_rect)
        
        button_width = 130
        button_height = 40
        button_gap = 30
        
        ok_button = pygame.Rect(dialog_x + dialog_width // 2 - button_width - button_gap // 2, dialog_y + 150, button_width, button_height)
        cancel_button = pygame.Rect(dialog_x + dialog_width // 2 + button_gap // 2, dialog_y + 150, button_width, button_height)
        
        pygame.draw.rect(self.screen, COLOR_GREEN, ok_button, border_radius=8)
        pygame.draw.rect(self.screen, COLOR_WHITE, ok_button, 2, border_radius=8)
        ok_text = self.font.render("确定", True, COLOR_WHITE)
        ok_rect = ok_text.get_rect(center=ok_button.center)
        self.screen.blit(ok_text, ok_rect)
        
        pygame.draw.rect(self.screen, COLOR_RED, cancel_button, border_radius=8)
        pygame.draw.rect(self.screen, COLOR_WHITE, cancel_button, 2, border_radius=8)
        cancel_text = self.font.render("取消", True, COLOR_WHITE)
        cancel_rect = cancel_text.get_rect(center=cancel_button.center)
        self.screen.blit(cancel_text, cancel_rect)

    def handle_cheat_password_dialog_click(self, pos):
        dialog_width = 350
        dialog_height = 220
        dialog_x = (SCREEN_WIDTH - dialog_width) // 2
        dialog_y = (SCREEN_HEIGHT - dialog_height) // 2
        
        button_width = 130
        button_height = 40
        button_gap = 30
        
        ok_button = pygame.Rect(dialog_x + dialog_width // 2 - button_width - button_gap // 2, dialog_y + 150, button_width, button_height)
        cancel_button = pygame.Rect(dialog_x + dialog_width // 2 + button_gap // 2, dialog_y + 150, button_width, button_height)
        
        if ok_button.collidepoint(pos):
            if self.cheat_password_input == self.cheat_password:
                self.cheat_unlocked = True
                self.save_cheat_unlock_status()
            self.show_cheat_password_dialog = False
            self.cheat_password_input = ""
        elif cancel_button.collidepoint(pos):
            self.show_cheat_password_dialog = False
            self.cheat_password_input = ""

    def draw_cheat_unlock_notification(self):
        if not self.show_cheat_unlock_notification:
            return
        
        dialog_width = 400
        dialog_height = 150
        dialog_x = (SCREEN_WIDTH - dialog_width) // 2
        dialog_y = (SCREEN_HEIGHT - dialog_height) // 2
        
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        self.screen.blit(overlay, (0, 0))
        
        pygame.draw.rect(self.screen, (30, 60, 30), (dialog_x, dialog_y, dialog_width, dialog_height), border_radius=15)
        pygame.draw.rect(self.screen, COLOR_GREEN, (dialog_x, dialog_y, dialog_width, dialog_height), 3, border_radius=15)
        
        title_text = self.font_large.render("🎉 恭喜！", True, COLOR_GREEN)
        title_rect = title_text.get_rect(center=(dialog_x + dialog_width // 2, dialog_y + 45))
        self.screen.blit(title_text, title_rect)
        
        name_text = self.font.render("已解锁作弊模式", True, COLOR_WHITE)
        name_rect = name_text.get_rect(center=(dialog_x + dialog_width // 2, dialog_y + 85))
        self.screen.blit(name_text, name_rect)
        
        close_button = pygame.Rect(dialog_x + dialog_width // 2 - 60, dialog_y + 110, 120, 35)
        pygame.draw.rect(self.screen, COLOR_GREEN, close_button, border_radius=6)
        pygame.draw.rect(self.screen, COLOR_WHITE, close_button, 2, border_radius=6)
        close_text = self.font_small.render("确定", True, COLOR_WHITE)
        close_rect = close_text.get_rect(center=close_button.center)
        self.screen.blit(close_text, close_rect)
        
        return close_button

    def save_cheat_unlock_status(self):
        import json
        try:
            with open('cheat_status.json', 'w', encoding='utf-8') as f:
                json.dump({'cheat_unlocked': self.cheat_unlocked}, f)
        except Exception as e:
            print(f"保存作弊状态失败: {e}")

    def load_cheat_unlock_status(self):
        import json
        try:
            with open('cheat_status.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.cheat_unlocked = data.get('cheat_unlocked', False)
        except FileNotFoundError:
            self.cheat_unlocked = False
        except Exception as e:
            print(f"加载作弊状态失败: {e}")
            self.cheat_unlocked = False

    def draw_achievement_notification(self):
        if self.achievement_notification is None:
            return
        
        current_time = pygame.time.get_ticks()
        elapsed = current_time - self.achievement_notification['time']
        
        if elapsed > 3000:
            self.achievement_notification = None
            return
        
        notification = self.achievement_notification
        achievement = notification['achievement']
        
        if elapsed < 500:
            notification['alpha'] = min(255, notification['alpha'] + 5)
            notification['y_offset'] = min(0, notification['y_offset'] + 2)
        elif elapsed > 2500:
            notification['alpha'] = max(0, notification['alpha'] - 5)
            notification['y_offset'] = max(-50, notification['y_offset'] - 2)
        
        dialog_width = 400
        dialog_height = 120
        dialog_x = (SCREEN_WIDTH - dialog_width) // 2
        dialog_y = 100 + notification['y_offset']
        
        overlay = pygame.Surface((dialog_width, dialog_height), pygame.SRCALPHA)
        overlay.fill((30, 30, 50, notification['alpha']))
        self.screen.blit(overlay, (dialog_x, dialog_y))
        
        pygame.draw.rect(self.screen, (255, 215, 0), (dialog_x, dialog_y, dialog_width, dialog_height), 3, border_radius=15)
        
        icon_text = self.font_large.render(achievement.icon, True, (255, 215, 0))
        icon_rect = icon_text.get_rect(center=(dialog_x + 50, dialog_y + dialog_height // 2))
        self.screen.blit(icon_text, icon_rect)
        
        title_text = self.font_large.render(f"🎉 成就达成！", True, COLOR_WHITE)
        title_rect = title_text.get_rect(center=(dialog_x + dialog_width // 2, dialog_y + 35))
        self.screen.blit(title_text, title_rect)
        
        name_text = self.font.render(f"您已完成「{achievement.name}」成就", True, (255, 215, 0))
        name_rect = name_text.get_rect(center=(dialog_x + dialog_width // 2, dialog_y + 75))
        self.screen.blit(name_text, name_rect)

    def draw_tower_buttons(self):
        x = 20
        y = SCREEN_HEIGHT - 80
        
        for tower_type in TowerType:
            info = self.tower_info[tower_type]
            button_rect = pygame.Rect(x, y, 80, 70)
            
            if self.gold >= info["cost"]:
                pygame.draw.rect(self.screen, COLOR_GRAY, button_rect)
                pygame.draw.rect(self.screen, COLOR_WHITE, button_rect, 2)
                
                name_text = self.font_small.render(info["name"], True, COLOR_WHITE)
                name_rect = name_text.get_rect(center=(x + 40, y + 15))
                self.screen.blit(name_text, name_rect)
                
                cost_text = self.font_small.render(f"{info['cost']}金", True, COLOR_GOLD)
                cost_rect = cost_text.get_rect(center=(x + 40, y + 40))
                self.screen.blit(cost_text, cost_rect)
            else:
                pygame.draw.rect(self.screen, COLOR_DARK_GRAY, button_rect)
                pygame.draw.rect(self.screen, COLOR_GRAY, button_rect, 2)
                
                name_text = self.font_small.render(info["name"], True, COLOR_GRAY)
                name_rect = name_text.get_rect(center=(x + 40, y + 15))
                self.screen.blit(name_text, name_rect)
                
                cost_text = self.font_small.render(f"{info['cost']}金", True, COLOR_RED)
                cost_rect = cost_text.get_rect(center=(x + 40, y + 40))
                self.screen.blit(cost_text, cost_rect)
            
            x += 90

    def draw_tower_selection_ui(self):
        pygame.draw.rect(self.screen, COLOR_BLACK, (0, SCREEN_HEIGHT - 80, SCREEN_WIDTH, 80))
        
        info = self.tower_info[self.selected_tower_type]
        
        cancel_button = pygame.Rect(20, SCREEN_HEIGHT - 60, 80, 40)
        pygame.draw.rect(self.screen, COLOR_RED, cancel_button)
        pygame.draw.rect(self.screen, COLOR_WHITE, cancel_button, 2)
        cancel_text = self.font_small.render("取消", True, COLOR_WHITE)
        cancel_rect = cancel_text.get_rect(center=cancel_button.center)
        self.screen.blit(cancel_text, cancel_rect)
        
        info_text = self.font.render(f"{info['name']}: {info['desc']}", True, COLOR_WHITE)
        info_rect = info_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
        self.screen.blit(info_text, info_rect)

    def draw_selected_tower_ui(self):
        ui_height = 140
        pygame.draw.rect(self.screen, COLOR_BLACK, (0, SCREEN_HEIGHT - ui_height, SCREEN_WIDTH, ui_height))
        
        tower = self.selected_tower
        info = self.tower_info[tower.tower_type]
        
        info_text = self.font.render(f"{info['name']} Lv.{tower.level}", True, COLOR_WHITE)
        info_rect = info_text.get_rect(left=20, top=SCREEN_HEIGHT - ui_height + 15)
        self.screen.blit(info_text, info_rect)
        
        stats_text = self.font_small.render(f"伤害: {int(tower.damage)} 范围: {int(tower.range)}", True, COLOR_GREEN)
        stats_rect = stats_text.get_rect(left=20, top=SCREEN_HEIGHT - ui_height + 45)
        self.screen.blit(stats_text, stats_rect)

        if tower.level < 3:
            upgrade_button = pygame.Rect(SCREEN_WIDTH - 200, SCREEN_HEIGHT - ui_height + 20, 100, 40)
            upgrade_cost = tower.get_upgrade_cost()
            
            if self.gold >= upgrade_cost:
                pygame.draw.rect(self.screen, COLOR_GREEN, upgrade_button)
                pygame.draw.rect(self.screen, COLOR_WHITE, upgrade_button, 2)
                upgrade_text = self.font_small.render(f"升级 {upgrade_cost}金", True, COLOR_WHITE)
                upgrade_rect = upgrade_text.get_rect(center=upgrade_button.center)
                self.screen.blit(upgrade_text, upgrade_rect)
            else:
                pygame.draw.rect(self.screen, COLOR_DARK_GRAY, upgrade_button)
                pygame.draw.rect(self.screen, COLOR_GRAY, upgrade_button, 2)
                upgrade_text = self.font_small.render(f"升级 {upgrade_cost}金", True, COLOR_RED)
                upgrade_rect = upgrade_text.get_rect(center=upgrade_button.center)
                self.screen.blit(upgrade_text, upgrade_rect)
        
        sell_button = pygame.Rect(SCREEN_WIDTH - 80, SCREEN_HEIGHT - ui_height + 20, 60, 40)
        pygame.draw.rect(self.screen, COLOR_ORANGE, sell_button)
        pygame.draw.rect(self.screen, COLOR_WHITE, sell_button, 2)
        sell_value = tower.get_sell_value()
        sell_text = self.font_small.render(f"卖 {sell_value}", True, COLOR_WHITE)
        sell_rect = sell_text.get_rect(center=sell_button.center)
        self.screen.blit(sell_text, sell_rect)

        skill_button = pygame.Rect(SCREEN_WIDTH - 140, SCREEN_HEIGHT - ui_height + 70, 120, 40)
        if tower.skill_ready:
            pygame.draw.rect(self.screen, COLOR_PURPLE, skill_button)
            pygame.draw.rect(self.screen, COLOR_WHITE, skill_button, 2)
            skill_text = self.font_small.render(f"技能: {tower.skill_name}", True, COLOR_WHITE)
        else:
            time_since_skill = pygame.time.get_ticks() - tower.last_skill_time
            remaining_cooldown = max(0, tower.skill_cooldown - time_since_skill)
            cooldown_seconds = int(remaining_cooldown / 1000)
            pygame.draw.rect(self.screen, COLOR_DARK_GRAY, skill_button)
            pygame.draw.rect(self.screen, COLOR_GRAY, skill_button, 2)
            cooldown_text = self.font_small.render(f"冷却: {cooldown_seconds}s", True, COLOR_RED)
            skill_text = cooldown_text
        skill_rect = skill_text.get_rect(center=skill_button.center)
        self.screen.blit(skill_text, skill_rect)

    def draw_tower_encyclopedia(self):
        self.screen.fill((30, 30, 60))
        
        title_text = self.font_large.render("塔图鉴", True, COLOR_GOLD)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 50))
        self.screen.blit(title_text, title_rect)

        back_button = pygame.Rect(50, 50, 100, 40)
        pygame.draw.rect(self.screen, COLOR_GRAY, back_button)
        pygame.draw.rect(self.screen, COLOR_WHITE, back_button, 2)
        back_text = self.font.render("返回", True, COLOR_WHITE)
        back_rect = back_text.get_rect(center=back_button.center)
        self.screen.blit(back_text, back_rect)

        card_width = 280
        card_height = 180
        padding_x = 40
        padding_y = 20
        start_x = padding_x
        start_y = 100
        cols = 2
        
        tower_types = list(TowerType)
        max_towers = len(tower_types)
        
        for i, tower_type in enumerate(tower_types):
            col = i % cols
            row = i // cols
            
            x = start_x + col * (card_width + padding_x)
            y = start_y + row * (card_height + padding_y)
            
            if y + card_height > SCREEN_HEIGHT - padding_y:
                break
            
            info = self.tower_info.get(tower_type)
            if not info:
                continue
            
            card_rect = pygame.Rect(x, y, card_width, card_height)
            pygame.draw.rect(self.screen, (50, 50, 80), card_rect)
            pygame.draw.rect(self.screen, COLOR_WHITE, card_rect, 2)
            
            name_text = self.font_large.render(info["name"], True, COLOR_GOLD)
            name_rect = name_text.get_rect(center=(x + card_width // 2, y + 25))
            self.screen.blit(name_text, name_rect)
            
            desc_text = self.font_small.render(info["desc"], True, COLOR_WHITE)
            desc_rect = desc_text.get_rect(center=(x + card_width // 2, y + 60))
            self.screen.blit(desc_text, desc_rect)
            
            stats = [
                f"费用: {info['cost']} 金币",
                f"伤害: {info['damage']}",
                f"范围: {info['range']}",
                f"攻速: {info['speed']}/秒"
            ]
            
            for j, stat in enumerate(stats):
                stat_text = self.font_small.render(stat, True, COLOR_GREEN)
                self.screen.blit(stat_text, (x + 20, y + 90 + j * 22))

            tower_center_x = x + card_width // 2
            tower_center_y = y + card_height - 25
            temp_tower = TowerFactory.create_tower(tower_type, tower_center_x, tower_center_y)
            temp_tower.draw(self.screen, self.font_small)

    def draw_enemy_encyclopedia(self):
        self.screen.fill((30, 30, 60))
        
        title_text = self.font_large.render("敌人图鉴", True, COLOR_GOLD)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 50))
        self.screen.blit(title_text, title_rect)

        back_button = pygame.Rect(50, 50, 100, 40)
        pygame.draw.rect(self.screen, COLOR_GRAY, back_button)
        pygame.draw.rect(self.screen, COLOR_WHITE, back_button, 2)
        back_text = self.font.render("返回", True, COLOR_WHITE)
        back_rect = back_text.get_rect(center=back_button.center)
        self.screen.blit(back_text, back_rect)

        monster_button = pygame.Rect(SCREEN_WIDTH // 2 - 150, 200, 300, 80)
        pygame.draw.rect(self.screen, COLOR_GREEN, monster_button)
        pygame.draw.rect(self.screen, COLOR_WHITE, monster_button, 3)
        monster_text = self.font_large.render("怪物图鉴", True, COLOR_WHITE)
        monster_rect = monster_text.get_rect(center=monster_button.center)
        self.screen.blit(monster_text, monster_rect)

        boss_button = pygame.Rect(SCREEN_WIDTH // 2 - 150, 320, 300, 80)
        pygame.draw.rect(self.screen, COLOR_RED, boss_button)
        pygame.draw.rect(self.screen, COLOR_WHITE, boss_button, 3)
        boss_text = self.font_large.render("BOSS图鉴", True, COLOR_WHITE)
        boss_rect = boss_text.get_rect(center=boss_button.center)
        self.screen.blit(boss_text, boss_rect)

    def draw_monster_encyclopedia(self):
        self.screen.fill((30, 30, 60))
        
        title_text = self.font_large.render("怪物图鉴", True, COLOR_GOLD)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 50))
        self.screen.blit(title_text, title_rect)

        back_button = pygame.Rect(50, 50, 100, 40)
        pygame.draw.rect(self.screen, COLOR_GRAY, back_button)
        pygame.draw.rect(self.screen, COLOR_WHITE, back_button, 2)
        back_text = self.font.render("返回", True, COLOR_WHITE)
        back_rect = back_text.get_rect(center=back_button.center)
        self.screen.blit(back_text, back_rect)

        card_width = 240
        card_height = 130
        padding_x = 25
        padding_y = 15
        cols = 4
        start_x = padding_x
        y = 100
        
        normal_enemies = []
        for enemy_type in EnemyType:
            info = self.enemy_info.get(enemy_type)
            if info and info["type"] != "boss":
                normal_enemies.append((enemy_type, info))
        
        for i, (enemy_type, info) in enumerate(normal_enemies):
            col = i % cols
            row = i // cols
            
            x = start_x + col * (card_width + padding_x)
            card_y = y + row * (card_height + padding_y)
            
            stars = info.get("stars", 1)
            if stars == 1:
                border_color = (80, 80, 80)
            elif stars == 2:
                border_color = COLOR_GREEN
            elif stars == 3:
                border_color = COLOR_BLUE
            elif stars == 4:
                border_color = COLOR_PURPLE
            else:
                border_color = COLOR_YELLOW
            
            card_rect = pygame.Rect(x, card_y, card_width, card_height)
            pygame.draw.rect(self.screen, (50, 50, 80), card_rect)
            pygame.draw.rect(self.screen, border_color, card_rect, 3)
            
            name_text = self.font.render(info["name"], True, COLOR_WHITE)
            self.screen.blit(name_text, (x + 15, card_y + 12))
            
            stars = info.get("stars", 1)
            star_size = 10
            star_spacing = 14
            stars_x = x + card_width - 15 - stars * star_spacing
            stars_y = card_y + 12
            
            for j in range(stars):
                star_x = stars_x + j * star_spacing
                self.draw_star(self.screen, star_x, stars_y, star_size, COLOR_YELLOW, filled=True)
            
            stats = [
                f"生命: {info['hp']}",
                f"速度: {info['speed']}",
                f"奖励: {info['reward']}金"
            ]
            
            for j, stat in enumerate(stats):
                stat_text = self.font_small.render(stat, True, COLOR_GREEN)
                self.screen.blit(stat_text, (x + 15, card_y + 40 + j * 16))
            
            skill = info.get("skill", "无")
            skill_text = self.font_small.render(f"技能: {skill}", True, COLOR_CYAN)
            self.screen.blit(skill_text, (x + 15, card_y + 88))
            
            desc_lines = self.wrap_text(info["desc"], 20)
            for j, line in enumerate(desc_lines[:1]):
                desc_text = self.font_small.render(line, True, (180, 180, 180))
                self.screen.blit(desc_text, (x + 15, card_y + 110 + j * 14))
    
    def draw_boss_encyclopedia(self):
        self.screen.fill((30, 30, 60))
        
        title_text = self.font_large.render("BOSS图鉴", True, COLOR_RED)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 50))
        self.screen.blit(title_text, title_rect)

        back_button = pygame.Rect(50, 50, 100, 40)
        pygame.draw.rect(self.screen, COLOR_GRAY, back_button)
        pygame.draw.rect(self.screen, COLOR_WHITE, back_button, 2)
        back_text = self.font.render("返回", True, COLOR_WHITE)
        back_rect = back_text.get_rect(center=back_button.center)
        self.screen.blit(back_text, back_rect)

        card_width = 300
        card_height = 180
        padding_x = 30
        padding_y = 20
        cols = 3
        start_x = padding_x
        y = 100
        
        boss_enemies = []
        for enemy_type in EnemyType:
            info = self.enemy_info.get(enemy_type)
            if info and info["type"] == "boss":
                boss_enemies.append((enemy_type, info))
        
        for i, (enemy_type, info) in enumerate(boss_enemies):
            col = i % cols
            row = i // cols
            
            x = start_x + col * (card_width + padding_x)
            card_y = y + row * (card_height + padding_y)
            
            border_color = COLOR_RED
            
            card_rect = pygame.Rect(x, card_y, card_width, card_height)
            pygame.draw.rect(self.screen, (80, 30, 30), card_rect)
            pygame.draw.rect(self.screen, border_color, card_rect, 2)
            
            name_text = self.font_large.render(info["name"], True, COLOR_WHITE)
            self.screen.blit(name_text, (x + 15, card_y + 15))
            
            stars = info.get("stars", 5)
            star_size = 12
            star_spacing = 16
            stars_x = x + card_width - 15 - stars * star_spacing
            stars_y = card_y + 15
            
            for j in range(stars):
                star_x = stars_x + j * star_spacing
                self.draw_star(self.screen, star_x, stars_y, star_size, COLOR_YELLOW, filled=True)
            
            stats = [
                f"生命: {info['hp']}",
                f"速度: {info['speed']}",
                f"奖励: {info['reward']}金"
            ]
            
            for j, stat in enumerate(stats):
                stat_text = self.font_small.render(stat, True, COLOR_GREEN)
                self.screen.blit(stat_text, (x + 15, card_y + 50 + j * 20))
            
            skill = info.get("skill", "无")
            skill_text = self.font.render(f"技能: {skill}", True, COLOR_CYAN)
            self.screen.blit(skill_text, (x + 15, card_y + 115))
            
            desc_lines = self.wrap_text(info["desc"], 25)
            for j, line in enumerate(desc_lines[:2]):
                desc_text = self.font_small.render(line, True, (180, 180, 180))
                self.screen.blit(desc_text, (x + 15, card_y + 145 + j * 16))
        
        y += ((len(boss_enemies) + cols - 1) // cols) * (card_height + padding_y)

    def wrap_text(self, text, max_chars):
        words = text
        lines = []
        current_line = ""
        
        for char in words:
            if len(current_line) >= max_chars:
                lines.append(current_line)
                current_line = char
            else:
                current_line += char
        
        if current_line:
            lines.append(current_line)
        
        return lines

    def draw_pause(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill(COLOR_BLACK)
        self.screen.blit(overlay, (0, 0))
        
        pause_text = self.font_title.render("游戏暂停", True, COLOR_WHITE)
        pause_rect = pause_text.get_rect(center=(SCREEN_WIDTH // 2, 200))
        self.screen.blit(pause_text, pause_rect)

        buttons = [
            {"text": "继续游戏", "action": "continue", "y": 300},
            {"text": "返回主菜单", "action": "menu", "y": 370},
            {"text": "重新开始", "action": "restart", "y": 440}
        ]

        for btn in buttons:
            button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 120, btn["y"], 240, 50)
            pygame.draw.rect(self.screen, COLOR_GRAY, button_rect)
            pygame.draw.rect(self.screen, COLOR_WHITE, button_rect, 3)
            
            text = self.font.render(btn["text"], True, COLOR_WHITE)
            text_rect = text.get_rect(center=button_rect.center)
            self.screen.blit(text, text_rect)

    def draw_game_over(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill(COLOR_BLACK)
        self.screen.blit(overlay, (0, 0))
        
        game_over_text = self.font_title.render("游戏结束", True, COLOR_RED)
        game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, 200))
        self.screen.blit(game_over_text, game_over_rect)
        
        score_text = self.font_large.render(f"最终得分: {self.score}", True, COLOR_GOLD)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, 300))
        self.screen.blit(score_text, score_rect)

        buttons = [
            {"text": "重新开始", "action": "restart", "y": 380},
            {"text": "返回主菜单", "action": "menu", "y": 450}
        ]

        for btn in buttons:
            button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 120, btn["y"], 240, 50)
            pygame.draw.rect(self.screen, COLOR_GRAY, button_rect)
            pygame.draw.rect(self.screen, COLOR_WHITE, button_rect, 3)
            
            text = self.font.render(btn["text"], True, COLOR_WHITE)
            text_rect = text.get_rect(center=button_rect.center)
            self.screen.blit(text, text_rect)

    def draw_victory(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill(COLOR_BLACK)
        self.screen.blit(overlay, (0, 0))
        
        victory_text = self.font_title.render("胜利!", True, COLOR_GOLD)
        victory_rect = victory_text.get_rect(center=(SCREEN_WIDTH // 2, 200))
        self.screen.blit(victory_text, victory_rect)
        
        score_text = self.font_large.render(f"得分: {self.score}", True, COLOR_WHITE)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, 300))
        self.screen.blit(score_text, score_rect)
        
        reward_text = self.font_large.render(f"奖励: {self.current_level.gold_reward} 金币", True, COLOR_GREEN)
        reward_rect = reward_text.get_rect(center=(SCREEN_WIDTH // 2, 350))
        self.screen.blit(reward_text, reward_rect)

        buttons = [
            {"text": "下一关", "action": "next_level", "y": 420},
            {"text": "返回主菜单", "action": "menu", "y": 490}
        ]

        for btn in buttons:
            button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 120, btn["y"], 240, 50)
            pygame.draw.rect(self.screen, COLOR_GRAY, button_rect)
            pygame.draw.rect(self.screen, COLOR_WHITE, button_rect, 3)
            
            text = self.font.render(btn["text"], True, COLOR_WHITE)
            text_rect = text.get_rect(center=button_rect.center)
            self.screen.blit(text, text_rect)

    def handle_menu_click(self, pos):
        cheat_toggle_button = pygame.Rect(20, SCREEN_HEIGHT - 60, 120, 40)
        if cheat_toggle_button.collidepoint(pos):
            if self.cheat_unlocked:
                self.cheat_unlocked = False
                self.save_cheat_unlock_status()
                self.developer_mode = False
                self.dev_panel_active = False
            else:
                self.show_cheat_password_dialog = True
            return
        
        if self.developer_mode:
            dev_panel_button = pygame.Rect(SCREEN_WIDTH // 2 - 90, 80, 180, 30)
            if dev_panel_button.collidepoint(pos):
                self.dev_panel_active = not self.dev_panel_active
                return
        
        buttons = [
            {"rect": pygame.Rect(SCREEN_WIDTH // 2 - 120, 300, 240, 50), "action": "level_select"},
            {"rect": pygame.Rect(SCREEN_WIDTH // 2 - 120, 360, 240, 50), "action": "tower_encyclopedia"},
            {"rect": pygame.Rect(SCREEN_WIDTH // 2 - 120, 420, 240, 50), "action": "enemy_encyclopedia"},
            {"rect": pygame.Rect(SCREEN_WIDTH // 2 - 120, 480, 240, 50), "action": "achievements"},
            {"rect": pygame.Rect(SCREEN_WIDTH // 2 - 120, 540, 240, 50), "action": "developer_mode"},
            {"rect": pygame.Rect(SCREEN_WIDTH // 2 - 120, 600, 240, 50), "action": "quit"}
        ]

        for btn in buttons:
            if btn["rect"].collidepoint(pos):
                if btn["action"] == "quit":
                    pygame.quit()
                    exit()
                elif btn["action"] == "developer_mode":
                    if self.cheat_unlocked:
                        self.developer_mode = not self.developer_mode
                        if self.developer_mode:
                            for level in self.levels:
                                level.unlocked = True
                    else:
                        self.show_cheat_password_dialog = True
                else:
                    self.game_state = GameState[btn["action"].upper()]
                return

    def handle_level_select_click(self, pos):
        if pygame.Rect(50, 50, 100, 40).collidepoint(pos):
            self.game_state = GameState.MENU
            return

        for i, level in enumerate(self.levels):
            x = 100 + (i % 3) * 250
            y = 150 + (i // 3) * 200
            
            if pygame.Rect(x, y, 200, 150).collidepoint(pos):
                if level.unlocked:
                    self.selected_level = i
                    self.start_level(level)
                else:
                    self.locked_level_index = i
                    self.show_locked_level_dialog = True
                return

    def handle_game_click(self, pos):
        if pygame.Rect(SCREEN_WIDTH - 100, 15, 80, 30).collidepoint(pos):
            self.game_state = GameState.PAUSE
            return
        
        if self.developer_mode:
            dev_panel_button = pygame.Rect(SCREEN_WIDTH // 2 - 90, 15, 180, 30)
            if dev_panel_button.collidepoint(pos):
                self.dev_panel_active = not self.dev_panel_active
                return

        if self.selected_tower_type:
            for pos_tower in self.current_level.tower_positions:
                if math.hypot(pos[0] - pos_tower[0], pos[1] - pos_tower[1]) < 25:
                    occupied = False
                    for tower in self.towers:
                        if math.hypot(tower.x - pos_tower[0], tower.y - pos_tower[1]) < 30:
                            occupied = True
                            break
                    
                    if not occupied:
                        info = self.tower_info[self.selected_tower_type]
                        if self.gold >= info["cost"]:
                            self.gold -= info["cost"]
                            tower = TowerFactory.create_tower(self.selected_tower_type, pos_tower[0], pos_tower[1])
                            self.towers.append(tower)
                            self.particles.add_explosion(pos_tower[0], pos_tower[1], COLOR_GOLD)
            
            self.selected_tower_type = None
            return

        if self.selected_tower:
            ui_height = 140
            upgrade_rect = pygame.Rect(SCREEN_WIDTH - 200, SCREEN_HEIGHT - ui_height + 20, 100, 40)
            sell_rect = pygame.Rect(SCREEN_WIDTH - 80, SCREEN_HEIGHT - ui_height + 20, 60, 40)
            skill_rect = pygame.Rect(SCREEN_WIDTH - 140, SCREEN_HEIGHT - ui_height + 70, 120, 40)
            
            if upgrade_rect.collidepoint(pos) and self.selected_tower.level < 3:
                cost = self.selected_tower.get_upgrade_cost()
                if self.gold >= cost:
                    self.gold -= cost
                    self.selected_tower.upgrade()
                    self.particles.add_explosion(self.selected_tower.x, self.selected_tower.y, COLOR_BLUE)
                return
            elif sell_rect.collidepoint(pos):
                self.gold += self.selected_tower.get_sell_value()
                self.particles.add_explosion(self.selected_tower.x, self.selected_tower.y, COLOR_GOLD)
                self.towers.remove(self.selected_tower)
                self.selected_tower = None
                return
            elif skill_rect.collidepoint(pos):
                if self.selected_tower.skill_ready:
                    self.selected_tower.try_use_skill(self.enemies, self.projectiles)
                return
            else:
                self.selected_tower = None
                return

        for tower in self.towers:
            if math.hypot(pos[0] - tower.x, pos[1] - tower.y) < 25:
                self.selected_tower = tower
                return

        x = 20
        y = SCREEN_HEIGHT - 80
        
        for tower_type in TowerType:
            button_rect = pygame.Rect(x, y, 80, 70)
            if button_rect.collidepoint(pos):
                info = self.tower_info[tower_type]
                if self.gold >= info["cost"]:
                    self.selected_tower_type = tower_type
                return
            x += 90

    def handle_pause_click(self, pos):
        buttons = [
            {"rect": pygame.Rect(SCREEN_WIDTH // 2 - 120, 300, 240, 50), "action": "continue"},
            {"rect": pygame.Rect(SCREEN_WIDTH // 2 - 120, 370, 240, 50), "action": "menu"},
            {"rect": pygame.Rect(SCREEN_WIDTH // 2 - 120, 440, 240, 50), "action": "restart"}
        ]

        for btn in buttons:
            if btn["rect"].collidepoint(pos):
                if btn["action"] == "continue":
                    self.game_state = GameState.GAME
                elif btn["action"] == "menu":
                    self.game_state = GameState.MENU
                elif btn["action"] == "restart":
                    self.start_level(self.levels[self.selected_level])
                return

    def handle_game_over_click(self, pos):
        buttons = [
            {"rect": pygame.Rect(SCREEN_WIDTH // 2 - 120, 380, 240, 50), "action": "restart"},
            {"rect": pygame.Rect(SCREEN_WIDTH // 2 - 120, 450, 240, 50), "action": "menu"}
        ]

        for btn in buttons:
            if btn["rect"].collidepoint(pos):
                if btn["action"] == "restart":
                    self.start_level(self.levels[self.selected_level])
                elif btn["action"] == "menu":
                    self.game_state = GameState.MENU
                return

    def handle_victory_click(self, pos):
        buttons = [
            {"rect": pygame.Rect(SCREEN_WIDTH // 2 - 120, 420, 240, 50), "action": "next_level"},
            {"rect": pygame.Rect(SCREEN_WIDTH // 2 - 120, 490, 240, 50), "action": "menu"}
        ]

        for btn in buttons:
            if btn["rect"].collidepoint(pos):
                self.levels[self.selected_level].completed = True
                self.levels[self.selected_level].high_score = max(self.levels[self.selected_level].high_score, self.score)
                
                next_index = self.selected_level + 1
                if next_index < len(self.levels):
                    self.levels[next_index].unlocked = True
                else:
                    if not self.cheat_unlocked:
                        self.cheat_unlocked = True
                        self.save_cheat_unlock_status()
                        self.show_cheat_unlock_notification = True
                
                self.update_level_achievements()
                
                self.save_game_progress()
                
                if btn["action"] == "next_level":
                    if next_index < len(self.levels):
                        self.selected_level = next_index
                        self.start_level(self.levels[next_index])
                    else:
                        self.game_state = GameState.MENU
                elif btn["action"] == "menu":
                    self.game_state = GameState.MENU
                return

    def update_level_achievements(self):
        completed_count = sum(1 for level in self.levels if level.completed)
        
        for achievement in self.achievement_manager.achievements:
            if achievement.id == "level_complete" and completed_count >= 1:
                if achievement.update_progress(completed_count - achievement.progress):
                    self.show_achievement_notification(achievement)
            elif achievement.id == "all_levels":
                if achievement.update_progress(completed_count - achievement.progress):
                    self.show_achievement_notification(achievement)
            elif achievement.id == "perfect_all" and self.damage_taken == 0:
                if achievement.update_progress(1):
                    self.show_achievement_notification(achievement)
        
        self.achievement_manager.total_score += self.score
        self.achievement_manager.total_gold_earned += self.gold
        
        for achievement in self.achievement_manager.achievements:
            if achievement.id == "high_score":
                if achievement.update_progress(self.achievement_manager.total_score - achievement.progress):
                    self.show_achievement_notification(achievement)
            elif achievement.id == "mega_score":
                if achievement.update_progress(self.achievement_manager.total_score - achievement.progress):
                    self.show_achievement_notification(achievement)
            elif achievement.id == "gold_rush":
                if achievement.update_progress(self.achievement_manager.total_gold_earned - achievement.progress):
                    self.show_achievement_notification(achievement)
            elif achievement.id == "gold_mine":
                if achievement.update_progress(self.achievement_manager.total_gold_earned - achievement.progress):
                    self.show_achievement_notification(achievement)
            elif achievement.id == "gold_king":
                if achievement.update_progress(self.achievement_manager.total_gold_earned - achievement.progress):
                    self.show_achievement_notification(achievement)

    def show_achievement_notification(self, achievement):
        self.achievement_notification = {
            'achievement': achievement,
            'time': pygame.time.get_ticks(),
            'alpha': 0,
            'y_offset': -50
        }

    def start_level(self, level):
        self.current_level = level
        
        level_gold = [200, 300, 400, 500, 550, 550]
        if self.selected_level < len(level_gold):
            self.gold = level_gold[self.selected_level]
        else:
            self.gold = 550
        
        self.lives = 20
        self.score = 0
        self.wave_index = 0
        self.wave_in_progress = False
        self.spawn_queue = []
        self.spawn_timer = 0
        self.towers = []
        self.enemies = []
        self.projectiles = []
        self.particles = ParticleSystem()
        self.selected_tower_type = None
        self.selected_tower = None
        self.game_state = GameState.GAME

    def save_game_progress(self):
        import json
        
        progress_data = {
            'levels': []
        }
        
        for i, level in enumerate(self.levels):
            progress_data['levels'].append({
                'index': i,
                'unlocked': level.unlocked,
                'completed': level.completed,
                'high_score': level.high_score,
                'stars': level.stars
            })
        
        try:
            with open('game_progress.json', 'w', encoding='utf-8') as f:
                json.dump(progress_data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存进度失败: {e}")

    def load_game_progress(self):
        import json
        
        try:
            with open('game_progress.json', 'r', encoding='utf-8') as f:
                progress_data = json.load(f)
                
                for level_data in progress_data.get('levels', []):
                    index = level_data.get('index', 0)
                    if 0 <= index < len(self.levels):
                        self.levels[index].unlocked = level_data.get('unlocked', False)
                        self.levels[index].completed = level_data.get('completed', False)
                        self.levels[index].high_score = level_data.get('high_score', 0)
                        self.levels[index].stars = level_data.get('stars', 0)
                
                if not any(l.unlocked for l in self.levels):
                    self.levels[0].unlocked = True
                    
        except FileNotFoundError:
            self.levels[0].unlocked = True
        except Exception as e:
            print(f"加载进度失败: {e}")
            self.levels[0].unlocked = True

    def clear_game_progress(self):
        import os
        
        for level in self.levels:
            level.unlocked = False
            level.completed = False
            level.high_score = 0
            level.stars = 0
        self.levels[0].unlocked = True
        
        try:
            if os.path.exists('game_progress.json'):
                os.remove('game_progress.json')
        except Exception as e:
            print(f"清除进度失败: {e}")
        
        self.current_wave_total_enemies = 0
        self.current_wave_killed_enemies = 0

    def spawn_wave(self):
        if self.wave_index >= len(self.current_level.waves):
            return
        
        wave_data = self.current_level.waves[self.wave_index]
        self.spawn_queue = list(wave_data["enemies"])
        self.spawn_timer = wave_data["delay"]
        self.wave_in_progress = True
        
        self.current_wave_total_enemies = len(self.spawn_queue)
        self.current_wave_killed_enemies = 0

    def update_game(self, dt):
        if not self.wave_in_progress and self.wave_index < len(self.current_level.waves):
            self.spawn_wave()
        
        self.spawn_timer -= dt
        if self.spawn_timer <= 0 and self.spawn_queue:
            enemy_type = self.spawn_queue.pop(0)
            start_x, start_y = self.current_level.path_points[0]
            enemy = EnemyFactory.create_enemy(enemy_type, start_x, start_y, self.current_level.path_points, self.wave_index + 1)
            self.enemies.append(enemy)
            self.spawn_timer = self.current_level.waves[self.wave_index]["delay"]
        
        for tower in self.towers:
            tower.update(self.enemies, pygame.time.get_ticks(), self.projectiles)
        
        for proj in list(self.projectiles):
            proj.update(self.enemies)
            if not proj.active:
                self.projectiles.remove(proj)
        
        for enemy in list(self.enemies):
            enemy.update(dt)
            
            if hasattr(enemy, 'is_ranged') and enemy.is_ranged:
                self.check_enemy_attack_tower(enemy)
            
            if not enemy.alive:
                self.score += enemy.reward
                self.gold += enemy.reward
                self.particles.add_explosion(enemy.x, enemy.y)
                self.enemies.remove(enemy)
                self.current_wave_killed_enemies += 1
            elif enemy.reached_end:
                self.lives -= 1
                self.enemies.remove(enemy)
                if self.lives <= 0:
                    self.game_state = GameState.GAME_OVER
        
        if self.spawn_queue:
            self.wave_in_progress = True
        elif not self.enemies:
            self.wave_in_progress = False
        
        if not self.spawn_queue and not self.enemies and self.wave_in_progress == False:
            if self.wave_index < len(self.current_level.waves) - 1:
                self.wave_index += 1
            elif self.wave_index == len(self.current_level.waves) - 1:
                self.game_state = GameState.VICTORY

        self.particles.update(dt)
    
    def check_enemy_attack_tower(self, enemy):
        attack_range = getattr(enemy, 'attack_range', 100)
        for tower in self.towers:
            dist = math.hypot(enemy.x - tower.x, enemy.y - tower.y)
            if dist <= attack_range:
                tower.take_damage(5)
                break

    def draw_game(self):
        self.draw_background(self.current_level.theme)
        
        for tower in self.towers:
            tower.draw(self.screen, self.font_small)
        
        for enemy in self.enemies:
            enemy.draw(self.screen, self.font_small)
        
        for proj in self.projectiles:
            proj.draw(self.screen)
        
        self.particles.draw(self.screen)
        
        if self.selected_tower:
            pygame.draw.circle(self.screen, COLOR_WHITE, (int(self.selected_tower.x), int(self.selected_tower.y)), int(self.selected_tower.range), 2)
        
        self.draw_game_ui()

    def run(self):
        running = True
        while running:
            dt = self.clock.tick(60) / 1000
            
            self.animation_timer += dt
            
            mouse_pos = pygame.mouse.get_pos()
            
            if self.showing_intro and self.intro_sequence:
                intro_done = self.intro_sequence.update(mouse_pos)
                if intro_done:
                    self.showing_intro = False
                    self.intro_sequence = None
                
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    elif self.intro_sequence:
                        if self.intro_sequence.handle_event(event):
                            self.showing_intro = False
                            self.intro_sequence = None
                
                self.screen.fill(COLOR_BLACK)
                if self.intro_sequence:
                    self.intro_sequence.draw()
                pygame.display.flip()
                continue
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_F1 and self.developer_mode:
                        self.dev_panel_active = not self.dev_panel_active
                    
                    if self.show_cheat_password_dialog:
                        if event.key == pygame.K_BACKSPACE:
                            self.cheat_password_input = self.cheat_password_input[:-1]
                        elif event.key == pygame.K_RETURN:
                            if self.cheat_password_input == self.cheat_password:
                                self.cheat_unlocked = True
                                self.save_cheat_unlock_status()
                            self.show_cheat_password_dialog = False
                            self.cheat_password_input = ""
                        elif event.unicode.isdigit():
                            if len(self.cheat_password_input) < 9:
                                self.cheat_password_input += event.unicode
                elif event.type == pygame.MOUSEMOTION:
                    if self.dev_panel_dragging:
                        new_x = event.pos[0] - self.dev_panel_drag_offset[0]
                        new_y = event.pos[1] - self.dev_panel_drag_offset[1]
                        self.dev_panel_x = max(0, min(new_x, SCREEN_WIDTH - 360))
                        self.dev_panel_y = max(0, min(new_y, SCREEN_HEIGHT - 80))
                    if self.game_state == GameState.ACHIEVEMENTS:
                        self.achievement_manager.handle_scroll_drag(event.pos)
                elif event.type == pygame.MOUSEBUTTONUP:
                    if self.dev_panel_dragging:
                        self.dev_panel_dragging = False
                    self.achievement_manager.handle_scroll_release()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    
                    if event.button == 4:
                        if self.game_state == GameState.ACHIEVEMENTS:
                            self.achievement_manager.handle_scroll(1)
                    elif event.button == 5:
                        if self.game_state == GameState.ACHIEVEMENTS:
                            self.achievement_manager.handle_scroll(-1)
                    
                    if self.game_state == GameState.ACHIEVEMENTS:
                        detail_clicked = self.achievement_manager.handle_detail_click(pos)
                        
                        if self.achievement_manager.selected_achievement and not detail_clicked:
                            back_button = pygame.Rect(50, 30, 100, 40)
                            if not back_button.collidepoint(pos):
                                self.achievement_manager.selected_achievement = None
                        elif not detail_clicked:
                            self.achievement_manager.handle_scroll_click(pos)
                    
                    if self.dev_panel_active and self.developer_mode:
                        self.handle_dev_panel_click(pos)
                    
                    if self.game_state == GameState.MENU:
                        if self.show_cheat_password_dialog:
                            self.handle_cheat_password_dialog_click(pos)
                        elif self.show_cheat_unlock_notification:
                            close_button = self.draw_cheat_unlock_notification()
                            if close_button and close_button.collidepoint(pos):
                                self.show_cheat_unlock_notification = False
                        else:
                            self.handle_menu_click(pos)
                    elif self.game_state == GameState.LEVEL_SELECT:
                        if self.show_locked_level_dialog:
                            self.handle_locked_level_dialog_click(pos)
                        else:
                            self.handle_level_select_click(pos)
                    elif self.game_state == GameState.GAME:
                        self.handle_game_click(pos)
                    elif self.game_state == GameState.PAUSE:
                        self.handle_pause_click(pos)
                    elif self.game_state == GameState.GAME_OVER:
                        self.handle_game_over_click(pos)
                    elif self.game_state == GameState.VICTORY:
                        self.handle_victory_click(pos)
                    elif self.game_state == GameState.ACHIEVEMENTS:
                        if pygame.Rect(50, 30, 100, 40).collidepoint(pos):
                            self.game_state = GameState.MENU
                            self.achievement_manager.selected_achievement = None
                    elif self.game_state == GameState.TOWER_ENCYCLOPEDIA:
                        if pygame.Rect(50, 50, 100, 40).collidepoint(pos):
                            self.game_state = GameState.MENU
                    elif self.game_state == GameState.ENEMY_ENCYCLOPEDIA:
                        if pygame.Rect(50, 50, 100, 40).collidepoint(pos):
                            self.game_state = GameState.MENU
                        elif pygame.Rect(SCREEN_WIDTH // 2 - 150, 200, 300, 80).collidepoint(pos):
                            self.game_state = GameState.MONSTER_ENCYCLOPEDIA
                        elif pygame.Rect(SCREEN_WIDTH // 2 - 150, 320, 300, 80).collidepoint(pos):
                            self.game_state = GameState.BOSS_ENCYCLOPEDIA
                    elif self.game_state == GameState.MONSTER_ENCYCLOPEDIA:
                        if pygame.Rect(50, 50, 100, 40).collidepoint(pos):
                            self.game_state = GameState.ENEMY_ENCYCLOPEDIA
                    elif self.game_state == GameState.BOSS_ENCYCLOPEDIA:
                        if pygame.Rect(50, 50, 100, 40).collidepoint(pos):
                            self.game_state = GameState.ENEMY_ENCYCLOPEDIA

            if self.game_state == GameState.GAME:
                self.update_game(dt)
            
            self.screen.fill(COLOR_BLACK)
            
            if self.game_state == GameState.MENU:
                self.draw_menu()
                self.draw_cheat_password_dialog()
                if self.show_cheat_unlock_notification:
                    self.draw_cheat_unlock_notification()
            elif self.game_state == GameState.LEVEL_SELECT:
                self.draw_level_select()
                if self.show_locked_level_dialog:
                    self.draw_locked_level_dialog()
            elif self.game_state == GameState.GAME:
                self.draw_game()
            elif self.game_state == GameState.PAUSE:
                self.draw_game()
                self.draw_pause()
            elif self.game_state == GameState.GAME_OVER:
                self.draw_game()
                self.draw_game_over()
            elif self.game_state == GameState.VICTORY:
                self.draw_game()
                self.draw_victory()
            elif self.game_state == GameState.ACHIEVEMENTS:
                self.achievement_manager.draw_achievements(self.screen, self.font, self.font_small)
            elif self.game_state == GameState.TOWER_ENCYCLOPEDIA:
                self.draw_tower_encyclopedia()
            elif self.game_state == GameState.ENEMY_ENCYCLOPEDIA:
                self.draw_enemy_encyclopedia()
            elif self.game_state == GameState.MONSTER_ENCYCLOPEDIA:
                self.draw_monster_encyclopedia()
            elif self.game_state == GameState.BOSS_ENCYCLOPEDIA:
                self.draw_boss_encyclopedia()
            
            if self.dev_panel_active and self.developer_mode:
                self.draw_dev_panel()
            
            self.draw_achievement_notification()
            
            pygame.display.flip()
        
        pygame.quit()


class SoundManager:
    def __init__(self):
        self.sounds = {}
        self.music_enabled = True
        self.sfx_enabled = True

    def play_sound(self, sound_name):
        if not self.sfx_enabled:
            return
        
        if sound_name == "tower_build":
            pass
        elif sound_name == "tower_upgrade":
            pass
        elif sound_name == "tower_sell":
            pass
        elif sound_name == "enemy_hit":
            pass
        elif sound_name == "enemy_death":
            pass
        elif sound_name == "projectile_fire":
            pass
        elif sound_name == "magic_circle":
            pass
        elif sound_name == "victory":
            pass
        elif sound_name == "game_over":
            pass
        elif sound_name == "wave_start":
            pass

    def play_music(self, track_name):
        if not self.music_enabled:
            return
        pass


class Achievement:
    def __init__(self, id_, name, description, icon, unlocked=False, progress=0, max_progress=1):
        self.id = id_
        self.name = name
        self.description = description
        self.icon = icon
        self.unlocked = unlocked
        self.progress = progress
        self.max_progress = max_progress

    def update_progress(self, amount=1):
        self.progress = min(self.progress + amount, self.max_progress)
        if self.progress >= self.max_progress and not self.unlocked:
            self.unlocked = True
            return True
        return False


class Achievement:
    def __init__(self, achievement_id, name, description, icon, max_progress=1):
        self.id = achievement_id
        self.name = name
        self.description = description
        self.icon = icon
        self.max_progress = max_progress
        self.progress = 0
        self.unlocked = False
        self.claimed = False
    
    def update_progress(self, amount=1):
        if not self.unlocked:
            self.progress = min(self.progress + amount, self.max_progress)
            if self.progress >= self.max_progress:
                self.unlocked = True
                return True
        return False

class AchievementManager:
    def __init__(self):
        self.achievements = [
            Achievement("first_blood", "第一滴血", "击杀第一个敌人", "🗡️"),
            Achievement("gold_rush", "淘金热", "累计获得1000金币", "💰", max_progress=1000),
            Achievement("gold_mine", "金矿大亨", "累计获得5000金币", "⛏️", max_progress=5000),
            Achievement("gold_king", "黄金之王", "累计获得10000金币", "👑", max_progress=10000),
            Achievement("tower_master", "塔之大师", "建造所有类型的塔", "🏰", max_progress=8),
            Achievement("level_complete", "初战告捷", "完成第一个关卡", "⭐"),
            Achievement("all_levels", "征服一切", "完成所有关卡", "🏆", max_progress=6),
            Achievement("perfect_run", "完美通关", "在不损失生命的情况下完成一关", "💎"),
            Achievement("perfect_all", "无懈可击", "完美通关所有关卡", "💠"),
            Achievement("high_score", "高分达人", "累计获得10000分", "🎯", max_progress=10000),
            Achievement("mega_score", "超级得分", "累计获得50000分", "🌟", max_progress=50000),
            Achievement("wave_survivor", "波次幸存者", "存活50波敌人", "🌊", max_progress=50),
            Achievement("wave_master", "波次大师", "存活200波敌人", "🌊", max_progress=200),
            Achievement("archer_ace", "弓术大师", "使用弓箭塔击杀200个敌人", "🏹", max_progress=200),
            Achievement("cannon_fodder", "炮火连天", "使用炮塔击杀100个敌人", "💣", max_progress=100),
            Achievement("ice_king", "冰霜之王", "使用冰霜塔减速200个敌人", "❄️", max_progress=200),
            Achievement("lightning_storm", "闪电风暴", "使用雷电塔击杀100个敌人", "⚡", max_progress=100),
            Achievement("magic_master", "魔法大师", "使用魔法塔击杀150个敌人", "✨", max_progress=150),
            Achievement("tower_collector", "塔收藏家", "同时拥有10座塔", "🏗️", max_progress=10),
            Achievement("tower_king", "塔之王者", "同时拥有20座塔", "🏛️", max_progress=20),
            Achievement("boss_killer", "BOSS杀手", "击杀5个BOSS", "👹", max_progress=5),
            Achievement("boss_master", "BOSS征服者", "击杀20个BOSS", "💀", max_progress=20),
            Achievement("wiznan_slayer", "维兹南终结者", "击杀维兹南", "👿"),
            Achievement("dragonslayer", "屠龙勇士", "击杀幼龙", "🐉"),
            Achievement("speed_runner", "速通达人", "在5分钟内完成一关", "🚀"),
            Achievement("speed_demon", "极速传说", "在3分钟内完成一关", "⚡"),
            Achievement("skill_master", "技能大师", "使用塔技能100次", "🔮", max_progress=100),
            Achievement("upgrade_pro", "升级专家", "升级塔50次", "⬆️", max_progress=50),
            Achievement("sell_expert", "买卖达人", "卖出塔20次", "💰", max_progress=20),
            Achievement("no_damage", "无伤大师", "连续5波未受伤害", "🛡️", max_progress=5),
            Achievement("survival_king", "生存之王", "在一关内承受1000点伤害并获胜", "❤️", max_progress=1000),
        ]
        
        self.tower_types_built = set()
        self.total_gold_earned = 0
        self.total_score = 0
        self.total_waves_survived = 0
        self.tower_kills = {tower_type: 0 for tower_type in TowerType}
        self.slow_count = 0
        self.boss_kills = 0
        self.current_wave_count = 0
        self.current_tower_count = 0
        self.skill_uses = 0
        self.upgrade_count = 0
        self.sell_count = 0
        self.perfect_waves = 0
        self.damage_taken = 0
        
        self.notifications = []
        self.scroll_offset = 0
        self.scroll_dragging = False
        self.selected_achievement = None
        self.detailed_button_rects = []

    def add_notification(self, achievement):
        self.notifications.append({
            'achievement': achievement,
            'time': pygame.time.get_ticks(),
            'y_offset': 0
        })

    def update_notifications(self):
        current_time = pygame.time.get_ticks()
        self.notifications = [n for n in self.notifications if current_time - n['time'] < 3000]
        
        for n in self.notifications:
            elapsed = current_time - n['time']
            if elapsed < 500:
                n['y_offset'] = -50 + (elapsed / 500) * 50
            elif elapsed > 2500:
                n['y_offset'] = (elapsed - 2500) / 500 * -50

    def draw_notifications(self, screen, font):
        for i, n in enumerate(self.notifications):
            x = SCREEN_WIDTH // 2
            y = 100 + i * 80 + n['y_offset']
            
            card_rect = pygame.Rect(x - 150, y, 300, 60)
            pygame.draw.rect(screen, (30, 30, 60), card_rect, border_radius=8)
            pygame.draw.rect(screen, COLOR_GOLD, card_rect, 2, border_radius=8)
            
            icon_text = font.render(n['achievement'].icon, True, COLOR_GOLD)
            screen.blit(icon_text, (x - 130, y + 15))
            
            name_text = font.render(f"🎉 {n['achievement'].name}", True, COLOR_WHITE)
            screen.blit(name_text, (x - 90, y + 15))
            
            desc_text = font.render(n['achievement'].description, True, COLOR_GRAY)
            screen.blit(desc_text, (x - 90, y + 38))

    def unlock_achievement(self, achievement_id):
        for achievement in self.achievements:
            if achievement.id == achievement_id and not achievement.unlocked:
                achievement.unlocked = True
                self.add_notification(achievement)
                return True
        return False

    def update_gold(self, amount):
        self.total_gold_earned += amount
        for achievement in self.achievements:
            if achievement.id == "gold_rush":
                if achievement.update_progress(amount):
                    self.add_notification(achievement)
            elif achievement.id == "gold_mine":
                if achievement.update_progress(amount):
                    self.add_notification(achievement)
            elif achievement.id == "gold_king":
                if achievement.update_progress(amount):
                    self.add_notification(achievement)

    def update_score(self, amount):
        self.total_score += amount
        for achievement in self.achievements:
            if achievement.id == "high_score":
                if achievement.update_progress(amount):
                    self.add_notification(achievement)
            elif achievement.id == "mega_score":
                if achievement.update_progress(amount):
                    self.add_notification(achievement)

    def add_tower_type(self, tower_type):
        if tower_type not in self.tower_types_built:
            self.tower_types_built.add(tower_type)
            for achievement in self.achievements:
                if achievement.id == "tower_master":
                    if achievement.update_progress():
                        self.add_notification(achievement)

    def add_tower_kill(self, tower_type):
        self.tower_kills[tower_type] += 1
        
        tower_achievements = {
            TowerType.ARCHER: "archer_ace",
            TowerType.CANNON: "cannon_fodder",
            TowerType.ICE: "ice_king",
            TowerType.LIGHTNING: "lightning_storm",
            TowerType.MAGE: "magic_master"
        }
        
        if tower_type in tower_achievements:
            for achievement in self.achievements:
                if achievement.id == tower_achievements[tower_type]:
                    if achievement.update_progress():
                        self.add_notification(achievement)

    def add_slow(self):
        self.slow_count += 1
        
        for achievement in self.achievements:
            if achievement.id == "ice_king":
                if achievement.update_progress():
                    self.add_notification(achievement)

    def add_boss_kill(self, boss_name=""):
        self.boss_kills += 1
        for achievement in self.achievements:
            if achievement.id == "boss_killer":
                if achievement.update_progress():
                    self.add_notification(achievement)
            elif achievement.id == "boss_master":
                if achievement.update_progress():
                    self.add_notification(achievement)
            elif achievement.id == "wiznan_slayer" and boss_name == "维兹南":
                if self.unlock_achievement("wiznan_slayer"):
                    self.add_notification(achievement)
            elif achievement.id == "dragonslayer" and boss_name == "幼龙":
                if self.unlock_achievement("dragonslayer"):
                    self.add_notification(achievement)

    def add_wave(self):
        self.total_waves_survived += 1
        self.current_wave_count += 1
        
        for achievement in self.achievements:
            if achievement.id == "wave_survivor":
                if achievement.update_progress():
                    self.add_notification(achievement)
            elif achievement.id == "wave_master":
                if achievement.update_progress():
                    self.add_notification(achievement)

    def add_tower(self):
        self.current_tower_count += 1
        for achievement in self.achievements:
            if achievement.id == "tower_collector":
                if achievement.update_progress():
                    self.add_notification(achievement)
            elif achievement.id == "tower_king":
                if achievement.update_progress():
                    self.add_notification(achievement)

    def remove_tower(self):
        self.current_tower_count -= 1

    def add_skill_use(self):
        self.skill_uses += 1
        for achievement in self.achievements:
            if achievement.id == "skill_master":
                if achievement.update_progress():
                    self.add_notification(achievement)

    def add_upgrade(self):
        self.upgrade_count += 1
        for achievement in self.achievements:
            if achievement.id == "upgrade_pro":
                if achievement.update_progress():
                    self.add_notification(achievement)

    def add_sell(self):
        self.sell_count += 1
        for achievement in self.achievements:
            if achievement.id == "sell_expert":
                if achievement.update_progress():
                    self.add_notification(achievement)

    def add_damage(self, amount):
        self.damage_taken += amount
        for achievement in self.achievements:
            if achievement.id == "survival_king":
                if achievement.update_progress(amount):
                    self.add_notification(achievement)

    def reset_damage(self):
        self.damage_taken = 0

    def add_perfect_wave(self):
        self.perfect_waves += 1
        for achievement in self.achievements:
            if achievement.id == "no_damage":
                if achievement.update_progress():
                    self.add_notification(achievement)

    def reset_perfect_waves(self):
        self.perfect_waves = 0

    def check_perfect_run(self):
        for achievement in self.achievements:
            if achievement.id == "perfect_run":
                if self.damage_taken == 0 and not achievement.unlocked:
                    self.unlock_achievement("perfect_run")
                    self.add_notification(achievement)

    def check_level_complete(self, level_index):
        for achievement in self.achievements:
            if achievement.id == "level_complete" and level_index == 0:
                if self.unlock_achievement("level_complete"):
                    self.add_notification(achievement)
            elif achievement.id == "all_levels":
                if achievement.update_progress():
                    self.add_notification(achievement)

    def check_speed_run(self, elapsed_time_ms):
        for achievement in self.achievements:
            if achievement.id == "speed_runner" and elapsed_time_ms < 5 * 60 * 1000:
                if self.unlock_achievement("speed_runner"):
                    self.add_notification(achievement)
            elif achievement.id == "speed_demon" and elapsed_time_ms < 3 * 60 * 1000:
                if self.unlock_achievement("speed_demon"):
                    self.add_notification(achievement)

    def get_unlocked_count(self):
        return sum(1 for a in self.achievements if a.unlocked)

    def draw_achievements(self, screen, font, font_small):
        screen.fill((30, 30, 60))
        self.detailed_button_rects = []
        
        title_text = font.render("🏆 成就系统", True, COLOR_GOLD)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 50))
        screen.blit(title_text, title_rect)
        
        unlocked_count = self.get_unlocked_count()
        progress_text = font_small.render(f"已解锁: {unlocked_count}/{len(self.achievements)}", True, COLOR_WHITE)
        progress_rect = progress_text.get_rect(center=(SCREEN_WIDTH // 2, 85))
        screen.blit(progress_text, progress_rect)

        back_button = pygame.Rect(50, 30, 100, 40)
        pygame.draw.rect(screen, COLOR_GRAY, back_button, border_radius=6)
        pygame.draw.rect(screen, COLOR_WHITE, back_button, 2, border_radius=6)
        back_text = font_small.render("返回", True, COLOR_WHITE)
        back_rect = back_text.get_rect(center=back_button.center)
        screen.blit(back_text, back_rect)

        cols = 4
        card_width = 180
        card_height = 110
        padding_x = (SCREEN_WIDTH - cols * card_width) // (cols + 1)
        padding_y = 30
        
        total_rows = (len(self.achievements) + cols - 1) // cols
        total_height = total_rows * (card_height + padding_y) + 120
        visible_height = SCREEN_HEIGHT - 120
        
        if total_height > visible_height:
            max_scroll = total_height - visible_height
            self.scroll_offset = max(0, min(self.scroll_offset, max_scroll))
            
            scroll_bar_bg = pygame.Rect(SCREEN_WIDTH - 25, 120, 15, visible_height)
            pygame.draw.rect(screen, (50, 50, 50), scroll_bar_bg, border_radius=6)
            
            scroll_bar_height = max(40, (visible_height / total_height) * visible_height)
            scroll_bar_y = 120 + (self.scroll_offset / max_scroll) * (visible_height - scroll_bar_height)
            self.scroll_bar_rect = pygame.Rect(SCREEN_WIDTH - 23, scroll_bar_y, 11, scroll_bar_height)
            pygame.draw.rect(screen, COLOR_GOLD, self.scroll_bar_rect, border_radius=4)
        
        for i, achievement in enumerate(self.achievements):
            col = i % cols
            row = i // cols
            x = padding_x + col * card_width
            y = 120 + row * (card_height + padding_y) - self.scroll_offset
            
            if y > SCREEN_HEIGHT or y + card_height < 120:
                continue
            
            card_rect = pygame.Rect(x, y, card_width - 10, card_height)
            
            if achievement.unlocked:
                pygame.draw.rect(screen, (50, 80, 50), card_rect, border_radius=8)
                pygame.draw.rect(screen, COLOR_GOLD, card_rect, 2, border_radius=8)
                icon_color = COLOR_GOLD
            else:
                pygame.draw.rect(screen, (40, 40, 40), card_rect, border_radius=8)
                pygame.draw.rect(screen, COLOR_GRAY, card_rect, 2, border_radius=8)
                icon_color = COLOR_GRAY
            
            icon_text = font.render(achievement.icon, True, icon_color)
            icon_rect = icon_text.get_rect(left=x + 10, top=y + 10)
            screen.blit(icon_text, icon_rect)
            
            max_name_width = card_width - 70
            name_text = font_small.render(achievement.name, True, COLOR_WHITE)
            
            if name_text.get_width() > max_name_width:
                truncated_name = achievement.name
                while font_small.render(truncated_name, True, COLOR_WHITE).get_width() > max_name_width - 20:
                    truncated_name = truncated_name[:-1]
                name_text = font_small.render(truncated_name + "...", True, COLOR_WHITE)
            
            name_rect = name_text.get_rect(left=x + 55, top=y + 12)
            screen.blit(name_text, name_rect)
            
            max_desc_width = card_width - 40
            desc_text = font_small.render(achievement.description, True, (150, 150, 150))
            
            if desc_text.get_width() > max_desc_width:
                truncated = achievement.description
                while font_small.render(truncated, True, (150, 150, 150)).get_width() > max_desc_width - 20:
                    truncated = truncated[:-1]
                desc_text = font_small.render(truncated + "...", True, (150, 150, 150))
            
            desc_rect = desc_text.get_rect(left=x + 10, top=y + 50)
            screen.blit(desc_text, desc_rect)
            
            detail_button = pygame.Rect(x + card_width - 35, y + 48, 20, 20)
            pygame.draw.rect(screen, (60, 60, 60), detail_button, border_radius=4)
            pygame.draw.rect(screen, COLOR_GRAY, detail_button, 1, border_radius=4)
            detail_text = font_small.render("...", True, COLOR_GRAY)
            detail_text_rect = detail_text.get_rect(center=detail_button.center)
            screen.blit(detail_text, detail_text_rect)
            
            self.detailed_button_rects.append((detail_button, achievement))
            
            if achievement.max_progress > 1:
                progress = int((achievement.progress / achievement.max_progress) * 100)
                bar_bg_rect = pygame.Rect(x + 10, y + 85, card_width - 30, 8)
                pygame.draw.rect(screen, (60, 60, 60), bar_bg_rect, border_radius=4)
                
                bar_width = int((achievement.progress / achievement.max_progress) * (card_width - 30))
                bar_rect = pygame.Rect(x + 10, y + 85, bar_width, 8)
                if achievement.unlocked:
                    pygame.draw.rect(screen, COLOR_GOLD, bar_rect, border_radius=4)
                else:
                    pygame.draw.rect(screen, COLOR_BLUE, bar_rect, border_radius=4)
                
                progress_text = font_small.render(f"{achievement.progress}/{achievement.max_progress}", True, COLOR_WHITE)
                progress_rect = progress_text.get_rect(right=x + card_width - 15, top=y + 82)
                screen.blit(progress_text, progress_rect)
        
        if self.selected_achievement:
            detail_box_x = SCREEN_WIDTH // 2 - 150
            detail_box_y = SCREEN_HEIGHT // 2 - 80
            detail_box = pygame.Rect(detail_box_x, detail_box_y, 300, 160)
            pygame.draw.rect(screen, (40, 40, 70), detail_box, border_radius=10)
            pygame.draw.rect(screen, COLOR_GOLD, detail_box, 2, border_radius=10)
            
            icon_text = font.render(self.selected_achievement.icon, True, COLOR_GOLD)
            icon_rect = icon_text.get_rect(left=detail_box_x + 20, top=detail_box_y + 20)
            screen.blit(icon_text, icon_rect)
            
            name_text = font.render(self.selected_achievement.name, True, COLOR_WHITE)
            name_rect = name_text.get_rect(left=detail_box_x + 70, top=detail_box_y + 22)
            screen.blit(name_text, name_rect)
            
            desc_lines = self.wrap_text(self.selected_achievement.description, font_small, 260)
            y_offset = 60
            for line in desc_lines:
                line_text = font_small.render(line, True, (180, 180, 180))
                line_rect = line_text.get_rect(left=detail_box_x + 20, top=detail_box_y + y_offset)
                screen.blit(line_text, line_rect)
                y_offset += 20
            
            status_text = font_small.render(f"状态: {'已解锁' if self.selected_achievement.unlocked else '未解锁'}", True, COLOR_GREEN if self.selected_achievement.unlocked else COLOR_RED)
            status_rect = status_text.get_rect(right=detail_box_x + 280, top=detail_box_y + 130)
            screen.blit(status_text, status_rect)
    
    def wrap_text(self, text, font, max_width):
        words = text.split(' ')
        lines = []
        current_line = ''
        
        for word in words:
            test_line = current_line + (word if not current_line else ' ' + word)
            if font.render(test_line, True, COLOR_WHITE).get_width() <= max_width:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word
        
        if current_line:
            lines.append(current_line)
        
        return lines
    
    def handle_scroll(self, dy):
        cols = 4
        card_height = 110
        padding_y = 30
        total_rows = (len(self.achievements) + cols - 1) // cols
        total_height = total_rows * (card_height + padding_y) + 120
        visible_height = SCREEN_HEIGHT - 120
        
        if total_height > visible_height:
            max_scroll = total_height - visible_height
            self.scroll_offset = max(0, min(self.scroll_offset - dy * 20, max_scroll))
    
    def handle_scroll_click(self, pos):
        cols = 4
        card_width = 180
        card_height = 110
        padding_x = (SCREEN_WIDTH - cols * card_width) // (cols + 1)
        padding_y = 30
        
        total_rows = (len(self.achievements) + cols - 1) // cols
        total_height = total_rows * (card_height + padding_y) + 120
        visible_height = SCREEN_HEIGHT - 120
        
        if total_height > visible_height:
            achievements_area = pygame.Rect(0, 120, SCREEN_WIDTH - 30, visible_height)
            
            if achievements_area.collidepoint(pos):
                self.scroll_dragging = True
                self.scroll_drag_start_y = pos[1]
                self.scroll_drag_start_offset = self.scroll_offset
                return True
        
        return False
    
    def handle_scroll_drag(self, pos):
        if self.scroll_dragging:
            cols = 4
            card_height = 110
            padding_y = 30
            total_rows = (len(self.achievements) + cols - 1) // cols
            total_height = total_rows * (card_height + padding_y) + 120
            visible_height = SCREEN_HEIGHT - 120
            
            if total_height > visible_height:
                max_scroll = total_height - visible_height
                scroll_bar_height = max(40, (visible_height / total_height) * visible_height)
                delta_y = pos[1] - self.scroll_drag_start_y
                delta_offset = (delta_y / (visible_height - scroll_bar_height)) * max_scroll
                self.scroll_offset = max(0, min(self.scroll_drag_start_offset + delta_offset, max_scroll))
    
    def handle_scroll_release(self):
        self.scroll_dragging = False
    
    def handle_detail_click(self, pos):
        for button_rect, achievement in self.detailed_button_rects:
            if button_rect.collidepoint(pos):
                if self.selected_achievement == achievement:
                    self.selected_achievement = None
                else:
                    self.selected_achievement = achievement
                return True
        return False


class GameDebug:
    def __init__(self):
        self.enabled = False
        self.show_fps = False
        self.show_tower_range = False
        self.show_enemy_info = False
        self.show_path = False

    def draw_debug_info(self, screen, font, fps, towers, enemies):
        if not self.enabled:
            return
        
        y = 20
        
        if self.show_fps:
            fps_text = font.render(f"FPS: {int(fps)}", True, COLOR_GREEN)
            screen.blit(fps_text, (SCREEN_WIDTH - 100, y))
            y += 20
        
        if self.show_tower_range:
            for tower in towers:
                pygame.draw.circle(screen, (255, 0, 0, 50), (int(tower.x), int(tower.y)), int(tower.range), 1)
        
        if self.show_enemy_info:
            for enemy in enemies:
                info_text = font.render(f"HP: {int(enemy.health)}/{enemy.max_health}", True, COLOR_RED)
                screen.blit(info_text, (int(enemy.x), int(enemy.y) - 30))
        
        debug_text = font.render("DEBUG MODE", True, COLOR_RED)
        screen.blit(debug_text, (20, SCREEN_HEIGHT - 30))


class WaveIndicator:
    def __init__(self):
        self.wave_number = 0
        self.total_waves = 0
        self.active = False
        self.start_time = 0
        self.duration = 2.0

    def start(self, wave_number, total_waves):
        self.wave_number = wave_number
        self.total_waves = total_waves
        self.active = True
        self.start_time = pygame.time.get_ticks()

    def update(self):
        elapsed = (pygame.time.get_ticks() - self.start_time) / 1000
        if elapsed >= self.duration:
            self.active = False

    def draw(self, screen, font_large):
        if not self.active:
            return
        
        elapsed = (pygame.time.get_ticks() - self.start_time) / 1000
        alpha = int(255 * (1 - elapsed / self.duration))
        
        overlay = pygame.Surface((SCREEN_WIDTH, 100))
        overlay.set_alpha(alpha)
        overlay.fill(COLOR_BLACK)
        screen.blit(overlay, (0, SCREEN_HEIGHT // 2 - 50))
        
        wave_text = font_large.render(f"第 {self.wave_number} 波", True, COLOR_GOLD)
        wave_rect = wave_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(wave_text, wave_rect)
        
        progress_text = font_large.render(f"{self.wave_number}/{self.total_waves}", True, COLOR_WHITE)
        progress_rect = progress_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40))
        screen.blit(progress_text, progress_rect)


class GameHUD:
    def __init__(self):
        self.gold = 0
        self.lives = 0
        self.score = 0
        self.wave = 0
        self.total_waves = 0
        self.selected_tower_info = None
        self.show_tower_panel = False

    def update(self, gold, lives, score, wave, total_waves):
        self.gold = gold
        self.lives = lives
        self.score = score
        self.wave = wave
        self.total_waves = total_waves

    def draw(self, screen, font, font_small):
        pygame.draw.rect(screen, COLOR_BLACK, (0, 0, SCREEN_WIDTH, 60))
        
        gold_text = font.render(f"💰 {self.gold}", True, COLOR_GOLD)
        screen.blit(gold_text, (20, 15))
        
        lives_text = font.render(f"❤️ {self.lives}", True, COLOR_RED)
        screen.blit(lives_text, (20, 40))
        
        score_text = font.render(f"⭐ {self.score}", True, COLOR_WHITE)
        score_rect = score_text.get_rect(right=SCREEN_WIDTH - 20, top=15)
        screen.blit(score_text, score_rect)
        
        wave_text = font.render(f"🌊 {self.wave}/{self.total_waves}", True, COLOR_WHITE)
        wave_rect = wave_text.get_rect(right=SCREEN_WIDTH - 20, top=40)
        screen.blit(wave_text, wave_rect)

        if self.show_tower_panel and self.selected_tower_info:
            self.draw_tower_panel(screen, font, font_small)

    def draw_tower_panel(self, screen, font, font_small):
        panel_rect = pygame.Rect(SCREEN_WIDTH - 220, 80, 200, 150)
        pygame.draw.rect(screen, (50, 50, 50), panel_rect)
        pygame.draw.rect(screen, COLOR_WHITE, panel_rect, 2)
        
        name_text = font.render(self.selected_tower_info["name"], True, COLOR_GOLD)
        screen.blit(name_text, (SCREEN_WIDTH - 200, 100))
        
        damage_text = font_small.render(f"伤害: {self.selected_tower_info['damage']}", True, COLOR_RED)
        screen.blit(damage_text, (SCREEN_WIDTH - 200, 130))
        
        range_text = font_small.render(f"范围: {self.selected_tower_info['range']}", True, COLOR_BLUE)
        screen.blit(range_text, (SCREEN_WIDTH - 200, 150))
        
        speed_text = font_small.render(f"攻速: {self.selected_tower_info['speed']}/秒", True, COLOR_GREEN)
        screen.blit(speed_text, (SCREEN_WIDTH - 200, 170))
        
        cost_text = font_small.render(f"费用: {self.selected_tower_info['cost']} 金币", True, COLOR_YELLOW)
        screen.blit(cost_text, (SCREEN_WIDTH - 200, 190))


class TowerSpecialAbility:
    def __init__(self, tower_type):
        self.tower_type = tower_type
        self.cooldown = 0
        self.max_cooldown = 10.0
        self.active = False
        self.duration = 0
        self.max_duration = 5.0

    def update(self, dt):
        if self.active:
            self.duration -= dt
            if self.duration <= 0:
                self.active = False
        else:
            if self.cooldown > 0:
                self.cooldown -= dt

    def activate(self):
        if self.cooldown <= 0 and not self.active:
            self.active = True
            self.duration = self.max_duration
            self.cooldown = self.max_cooldown
            return True
        return False

    def get_effect(self):
        effects = {
            TowerType.ARCHER: {"name": "穿透射击", "desc": "箭矢穿透所有敌人", "damage_multiplier": 1.5},
            TowerType.CANNON: {"name": "范围轰炸", "desc": "造成大范围爆炸伤害", "radius_multiplier": 2.0},
            TowerType.MAGE: {"name": "奥术风暴", "desc": "召唤魔法风暴持续伤害", "duration": 3.0},
            TowerType.ICE: {"name": "绝对零度", "desc": "冻结所有敌人", "freeze_duration": 2.0},
            TowerType.LIGHTNING: {"name": "雷霆万钧", "desc": "召唤闪电链攻击多个敌人", "chain_count": 5}
        }
        return effects.get(self.tower_type, {"name": "未知", "desc": "无", "value": 1.0})


class TowerAI:
    def __init__(self, tower):
        self.tower = tower
        self.target_priority = "first"
        self.last_target = None

    def set_priority(self, priority):
        self.target_priority = priority

    def find_target(self, enemies):
        if not enemies:
            self.tower.target = None
            return

        valid_enemies = [e for e in enemies if e.alive and self.is_in_range(e)]

        if not valid_enemies:
            self.tower.target = None
            return

        if self.target_priority == "first":
            self.tower.target = self.find_first_enemy(valid_enemies)
        elif self.target_priority == "last":
            self.tower.target = self.find_last_enemy(valid_enemies)
        elif self.target_priority == "strongest":
            self.tower.target = self.find_strongest_enemy(valid_enemies)
        elif self.target_priority == "weakest":
            self.tower.target = self.find_weakest_enemy(valid_enemies)
        elif self.target_priority == "closest":
            self.tower.target = self.find_closest_enemy(valid_enemies)
        else:
            self.tower.target = valid_enemies[0]

    def is_in_range(self, enemy):
        return math.hypot(self.tower.x - enemy.x, self.tower.y - enemy.y) <= self.tower.range

    def find_first_enemy(self, enemies):
        return max(enemies, key=lambda e: e.path_index)

    def find_last_enemy(self, enemies):
        return min(enemies, key=lambda e: e.path_index)

    def find_strongest_enemy(self, enemies):
        return max(enemies, key=lambda e: e.max_health)

    def find_weakest_enemy(self, enemies):
        return min(enemies, key=lambda e: e.health)

    def find_closest_enemy(self, enemies):
        return min(enemies, key=lambda e: math.hypot(self.tower.x - e.x, self.tower.y - e.y))


class EnemyAI:
    def __init__(self, enemy):
        self.enemy = enemy
        self.aggro_range = 200
        self.target_tower = None

    def update(self, towers):
        if self.enemy.reached_end:
            self.target_tower = None
            return

        if self.target_tower and not self.target_tower in towers:
            self.target_tower = None

        if not self.target_tower:
            self.find_target_tower(towers)

    def find_target_tower(self, towers):
        for tower in towers:
            dist = math.hypot(self.enemy.x - tower.x, self.enemy.y - tower.y)
            if dist <= self.aggro_range:
                self.target_tower = tower
                break


class GameConfig:
    def __init__(self):
        self.screen_width = SCREEN_WIDTH
        self.screen_height = SCREEN_HEIGHT
        self.fps = 60
        self.music_volume = 0.5
        self.sfx_volume = 0.7
        self.difficulty = "normal"
        self.show_fps = False
        self.show_grid = False
        self.show_range = False
        self.language = "zh"

    def load_config(self, filename="config.json"):
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.music_volume = data.get("music_volume", 0.5)
                self.sfx_volume = data.get("sfx_volume", 0.7)
                self.difficulty = data.get("difficulty", "normal")
                self.show_fps = data.get("show_fps", False)
                self.show_grid = data.get("show_grid", False)
                self.show_range = data.get("show_range", False)
                self.language = data.get("language", "zh")
        except:
            pass

    def save_config(self, filename="config.json"):
        data = {
            "music_volume": self.music_volume,
            "sfx_volume": self.sfx_volume,
            "difficulty": self.difficulty,
            "show_fps": self.show_fps,
            "show_grid": self.show_grid,
            "show_range": self.show_range,
            "language": self.language
        }
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4)
        except:
            pass


class LevelEditor:
    def __init__(self):
        self.path_points = []
        self.tower_positions = []
        self.waves = []
        self.theme = LevelTheme.FOREST
        self.name = "未命名关卡"
        self.gold_reward = 100

    def add_path_point(self, x, y):
        self.path_points.append((x, y))

    def remove_path_point(self, index):
        if 0 <= index < len(self.path_points):
            del self.path_points[index]

    def add_tower_position(self, x, y):
        self.tower_positions.append((x, y))

    def remove_tower_position(self, index):
        if 0 <= index < len(self.tower_positions):
            del self.tower_positions[index]

    def add_wave(self, enemies, delay):
        self.waves.append({"enemies": enemies, "delay": delay})

    def remove_wave(self, index):
        if 0 <= index < len(self.waves):
            del self.waves[index]

    def save_level(self, filename):
        level_data = {
            "name": self.name,
            "theme": self.theme.value,
            "path_points": self.path_points,
            "tower_positions": self.tower_positions,
            "waves": [{"enemies": [e.value for e in wave["enemies"]], "delay": wave["delay"]} for wave in self.waves],
            "gold_reward": self.gold_reward
        }
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(level_data, f, indent=4)
            return True
        except:
            return False

    def load_level(self, filename):
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.name = data.get("name", "未命名关卡")
                self.theme = LevelTheme(data.get("theme", "forest"))
                self.path_points = data.get("path_points", [])
                self.tower_positions = data.get("tower_positions", [])
                self.waves = [{"enemies": [EnemyType(e) for e in wave["enemies"]], "delay": wave["delay"]} for wave in data.get("waves", [])]
                self.gold_reward = data.get("gold_reward", 100)
            return True
        except:
            return False


class GameStats:
    def __init__(self):
        self.total_games_played = 0
        self.total_waves_survived = 0
        self.total_enemies_killed = 0
        self.total_gold_earned = 0
        self.total_score = 0
        self.best_score = 0
        self.levels_completed = 0
        self.total_towers_built = 0
        self.total_towers_upgraded = 0
        self.total_towers_sold = 0
        self.total_damage_dealt = 0
        self.total_damage_taken = 0
        self.avg_waves_per_game = 0
        self.avg_score_per_game = 0

    def update_stats(self, enemies_killed, gold_earned, score, waves_survived, towers_built, towers_upgraded, towers_sold, damage_dealt, damage_taken):
        self.total_games_played += 1
        self.total_waves_survived += waves_survived
        self.total_enemies_killed += enemies_killed
        self.total_gold_earned += gold_earned
        self.total_score += score
        self.total_towers_built += towers_built
        self.total_towers_upgraded += towers_upgraded
        self.total_towers_sold += towers_sold
        self.total_damage_dealt += damage_dealt
        self.total_damage_taken += damage_taken
        
        if score > self.best_score:
            self.best_score = score
        
        self.avg_waves_per_game = self.total_waves_survived / max(self.total_games_played, 1)
        self.avg_score_per_game = self.total_score / max(self.total_games_played, 1)

    def reset_stats(self):
        self.__init__()

    def save_stats(self, filename="stats.json"):
        data = {
            "total_games_played": self.total_games_played,
            "total_waves_survived": self.total_waves_survived,
            "total_enemies_killed": self.total_enemies_killed,
            "total_gold_earned": self.total_gold_earned,
            "total_score": self.total_score,
            "best_score": self.best_score,
            "levels_completed": self.levels_completed,
            "total_towers_built": self.total_towers_built,
            "total_towers_upgraded": self.total_towers_upgraded,
            "total_towers_sold": self.total_towers_sold,
            "total_damage_dealt": self.total_damage_dealt,
            "total_damage_taken": self.total_damage_taken,
            "avg_waves_per_game": self.avg_waves_per_game,
            "avg_score_per_game": self.avg_score_per_game
        }
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4)
            return True
        except:
            return False

    def load_stats(self, filename="stats.json"):
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.total_games_played = data.get("total_games_played", 0)
                self.total_waves_survived = data.get("total_waves_survived", 0)
                self.total_enemies_killed = data.get("total_enemies_killed", 0)
                self.total_gold_earned = data.get("total_gold_earned", 0)
                self.total_score = data.get("total_score", 0)
                self.best_score = data.get("best_score", 0)
                self.levels_completed = data.get("levels_completed", 0)
                self.total_towers_built = data.get("total_towers_built", 0)
                self.total_towers_upgraded = data.get("total_towers_upgraded", 0)
                self.total_towers_sold = data.get("total_towers_sold", 0)
                self.total_damage_dealt = data.get("total_damage_dealt", 0)
                self.total_damage_taken = data.get("total_damage_taken", 0)
                self.avg_waves_per_game = data.get("avg_waves_per_game", 0)
                self.avg_score_per_game = data.get("avg_score_per_game", 0)
            return True
        except:
            return False


class EnemyWaveManager:
    def __init__(self, level):
        self.level = level
        self.current_wave = 0
        self.wave_in_progress = False
        self.spawn_queue = []
        self.spawn_timer = 0
        self.enemies_spawned = 0
        self.wave_delay = 3.0
        self.wave_timer = 0

    def start_wave(self):
        if self.current_wave >= len(self.level.waves):
            return False
        
        wave_data = self.level.waves[self.current_wave]
        self.spawn_queue = list(wave_data["enemies"])
        self.spawn_timer = wave_data["delay"]
        self.wave_in_progress = True
        self.enemies_spawned = 0
        return True

    def update(self, dt, enemies, path_points):
        if not self.wave_in_progress:
            self.wave_timer += dt
            if self.wave_timer >= self.wave_delay:
                self.start_wave()
            return

        self.spawn_timer -= dt
        if self.spawn_timer <= 0 and self.spawn_queue:
            enemy_type = self.spawn_queue.pop(0)
            start_x, start_y = path_points[0]
            enemy = EnemyFactory.create_enemy(enemy_type, start_x, start_y, path_points, self.current_wave + 1)
            enemies.append(enemy)
            self.enemies_spawned += 1
            self.spawn_timer = self.level.waves[self.current_wave]["delay"]

        if not self.spawn_queue and not self.wave_in_progress:
            if not enemies:
                self.current_wave += 1
                self.wave_timer = 0
                if self.current_wave >= len(self.level.waves):
                    return True
        elif not self.spawn_queue:
            self.wave_in_progress = False

        return False

    def get_wave_progress(self):
        if not self.level.waves:
            return 0, 0
        return self.current_wave + 1, len(self.level.waves)

    def get_enemies_remaining(self):
        return len(self.spawn_queue)


class ProjectileManager:
    def __init__(self):
        self.projectiles = []
        self.explosions = []

    def add_projectile(self, projectile):
        self.projectiles.append(projectile)

    def add_explosion(self, x, y, radius=30, damage=20):
        self.explosions.append({"x": x, "y": y, "radius": radius, "damage": damage, "life": 0.5})

    def update(self, enemies):
        for proj in list(self.projectiles):
            proj.update(enemies)
            if not proj.active:
                self.projectiles.remove(proj)
                if proj.type == "cannonball" or proj.type == "magic":
                    self.add_explosion(proj.x, proj.y)

        for exp in list(self.explosions):
            exp["life"] -= 0.016
            if exp["life"] <= 0:
                self.explosions.remove(exp)
            else:
                for enemy in enemies:
                    if enemy.alive:
                        dist = math.hypot(exp["x"] - enemy.x, exp["y"] - enemy.y)
                        if dist <= exp["radius"]:
                            enemy.take_damage(exp["damage"])

    def draw(self, screen):
        for proj in self.projectiles:
            proj.draw(screen)
        
        for exp in self.explosions:
            alpha = int(255 * (exp["life"] / 0.5))
            pygame.draw.circle(screen, (255, 100, 50, alpha), (int(exp["x"]), int(exp["y"])), int(exp["radius"]))


class GameEvent:
    def __init__(self, event_type, data=None):
        self.event_type = event_type
        self.data = data
        self.timestamp = pygame.time.get_ticks()


class EventManager:
    def __init__(self):
        self.events = []
        self.listeners = {}

    def add_event(self, event_type, data=None):
        event = GameEvent(event_type, data)
        self.events.append(event)
        self.notify_listeners(event)

    def notify_listeners(self, event):
        if event.event_type in self.listeners:
            for listener in self.listeners[event.event_type]:
                listener(event)

    def add_listener(self, event_type, callback):
        if event_type not in self.listeners:
            self.listeners[event_type] = []
        self.listeners[event_type].append(callback)

    def remove_listener(self, event_type, callback):
        if event_type in self.listeners:
            self.listeners[event_type].remove(callback)

    def clear_events(self):
        self.events = []


class TowerUpgradeManager:
    def __init__(self):
        self.upgrade_paths = {
            TowerType.ARCHER: [
                {"name": "精准射击", "damage": 1.2, "range": 1.1, "cost": 50},
                {"name": "穿透箭矢", "damage": 1.5, "range": 1.0, "pierce": True, "cost": 80},
                {"name": "致命一击", "damage": 2.0, "range": 1.2, "critical": True, "cost": 120}
            ],
            TowerType.CANNON: [
                {"name": "强化炮弹", "damage": 1.3, "range": 1.0, "cost": 80},
                {"name": "范围扩大", "damage": 1.0, "radius": 1.5, "cost": 100},
                {"name": "毁灭打击", "damage": 2.0, "radius": 2.0, "cost": 150}
            ],
            TowerType.MAGE: [
                {"name": "奥术强化", "damage": 1.3, "range": 1.1, "cost": 70},
                {"name": "魔法风暴", "damage": 1.0, "aoe": True, "cost": 90},
                {"name": "时空裂隙", "damage": 2.0, "slow": True, "cost": 130}
            ],
            TowerType.ICE: [
                {"name": "寒冰强化", "damage": 1.2, "slow": 0.8, "cost": 65},
                {"name": "冰冻光环", "damage": 1.0, "aoe_slow": True, "cost": 85},
                {"name": "绝对零度", "damage": 1.5, "freeze": True, "cost": 110}
            ],
            TowerType.LIGHTNING: [
                {"name": "雷电强化", "damage": 1.3, "range": 1.1, "cost": 75},
                {"name": "连锁闪电", "damage": 1.0, "chain": True, "cost": 95},
                {"name": "雷霆风暴", "damage": 2.0, "chain": True, "cost": 140}
            ]
        }

    def get_upgrade_options(self, tower_type, current_level):
        if tower_type not in self.upgrade_paths:
            return []
        if current_level >= 3:
            return []
        return self.upgrade_paths[tower_type][current_level - 1]

    def apply_upgrade(self, tower, upgrade_index):
        upgrade = self.get_upgrade_options(tower.tower_type, tower.level)
        if not upgrade:
            return False
        
        tower.level += 1
        tower.damage *= upgrade.get("damage", 1.0)
        tower.range *= upgrade.get("range", 1.0)
        return True


class CampaignManager:
    def __init__(self):
        self.levels = LevelData.get_levels()
        self.current_level_index = 0
        self.campaign_progress = {}
        self.total_stars = 0
        self.load_progress()

    def load_progress(self):
        try:
            with open("campaign_progress.json", 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.current_level_index = data.get("current_level", 0)
                self.campaign_progress = data.get("progress", {})
                self.total_stars = data.get("total_stars", 0)
        except:
            self.current_level_index = 0
            self.campaign_progress = {}
            self.total_stars = 0

    def save_progress(self):
        data = {
            "current_level": self.current_level_index,
            "progress": self.campaign_progress,
            "total_stars": self.total_stars
        }
        try:
            with open("campaign_progress.json", 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4)
        except:
            pass

    def complete_level(self, level_index, stars, score):
        if level_index not in self.campaign_progress:
            self.campaign_progress[level_index] = {"stars": 0, "high_score": 0}
        
        if stars > self.campaign_progress[level_index]["stars"]:
            self.total_stars += stars - self.campaign_progress[level_index]["stars"]
            self.campaign_progress[level_index]["stars"] = stars
        
        if score > self.campaign_progress[level_index]["high_score"]:
            self.campaign_progress[level_index]["high_score"] = score
        
        if level_index + 1 < len(self.levels):
            self.current_level_index = level_index + 1
        
        self.save_progress()

    def is_level_unlocked(self, level_index):
        if level_index == 0:
            return True
        if level_index - 1 in self.campaign_progress:
            return self.campaign_progress[level_index - 1]["stars"] >= 1
        return False

    def get_level_progress(self, level_index):
        if level_index in self.campaign_progress:
            return self.campaign_progress[level_index]
        return {"stars": 0, "high_score": 0}


class TowerPlacementSystem:
    def __init__(self):
        self.placement_grid = {}
        self.grid_size = 40
        self.tower_positions = []

    def initialize_grid(self, width, height):
        for x in range(0, width, self.grid_size):
            for y in range(0, height, self.grid_size):
                self.placement_grid[(x, y)] = {"available": True, "blocked": False}

    def set_blocked(self, x, y, blocked=True):
        grid_x = (x // self.grid_size) * self.grid_size
        grid_y = (y // self.grid_size) * self.grid_size
        if (grid_x, grid_y) in self.placement_grid:
            self.placement_grid[(grid_x, grid_y)]["blocked"] = blocked

    def is_available(self, x, y):
        grid_x = (x // self.grid_size) * self.grid_size
        grid_y = (y // self.grid_size) * self.grid_size
        
        if (grid_x, grid_y) not in self.placement_grid:
            return False
        
        if not self.placement_grid[(grid_x, grid_y)]["available"]:
            return False
        
        if self.placement_grid[(grid_x, grid_y)]["blocked"]:
            return False
        
        for pos in self.tower_positions:
            dist = math.hypot(x - pos[0], y - pos[1])
            if dist < 40:
                return False
        
        return True

    def place_tower(self, x, y):
        if self.is_available(x, y):
            self.tower_positions.append((x, y))
            grid_x = (x // self.grid_size) * self.grid_size
            grid_y = (y // self.grid_size) * self.grid_size
            if (grid_x, grid_y) in self.placement_grid:
                self.placement_grid[(grid_x, grid_y)]["available"] = False
            return True
        return False

    def remove_tower(self, x, y):
        for i, pos in enumerate(self.tower_positions):
            if math.hypot(x - pos[0], y - pos[1]) < 20:
                del self.tower_positions[i]
                grid_x = (pos[0] // self.grid_size) * self.grid_size
                grid_y = (pos[1] // self.grid_size) * self.grid_size
                if (grid_x, grid_y) in self.placement_grid:
                    self.placement_grid[(grid_x, grid_y)]["available"] = True
                return True
        return False

    def draw_grid(self, screen):
        for (x, y), info in self.placement_grid.items():
            if info["available"] and not info["blocked"]:
                color = (100, 200, 100)
            elif info["blocked"]:
                color = (200, 100, 100)
            else:
                color = (150, 150, 150)
            
            pygame.draw.rect(screen, color, (x, y, self.grid_size, self.grid_size), 1)


class EnemyPathfinding:
    def __init__(self, path_points):
        self.path_points = path_points
        self.path = []
        self.generate_path()

    def generate_path(self):
        if len(self.path_points) < 2:
            return
        
        self.path = []
        for i in range(len(self.path_points) - 1):
            x1, y1 = self.path_points[i]
            x2, y2 = self.path_points[i + 1]
            
            dx = x2 - x1
            dy = y2 - y1
            distance = math.hypot(dx, dy)
            
            steps = int(distance / 5)
            for j in range(steps + 1):
                t = j / steps
                x = int(x1 + dx * t)
                y = int(y1 + dy * t)
                self.path.append((x, y))

    def get_position_at_index(self, index):
        if index < 0:
            return self.path[0]
        if index >= len(self.path):
            return self.path[-1]
        return self.path[index]

    def get_path_length(self):
        return len(self.path)

    def find_closest_point(self, x, y):
        min_dist = float('inf')
        closest_idx = 0
        
        for i, (px, py) in enumerate(self.path):
            dist = math.hypot(x - px, y - py)
            if dist < min_dist:
                min_dist = dist
                closest_idx = i
        
        return closest_idx, min_dist


class GamePerformanceMonitor:
    def __init__(self):
        self.fps_history = []
        self.frame_time_history = []
        self.max_fps = 60
        self.min_fps = 0
        self.avg_fps = 0
        self.max_frame_time = 0
        self.min_frame_time = float('inf')
        self.avg_frame_time = 0
        self.entity_count = {"towers": 0, "enemies": 0, "projectiles": 0, "particles": 0}
        self.frame_count = 0
        self.last_time = pygame.time.get_ticks()

    def update(self, towers, enemies, projectiles, particles, current_time):
        self.frame_count += 1
        
        current_fps = 1.0 / max(current_time, 0.001)
        self.fps_history.append(current_fps)
        if len(self.fps_history) > 60:
            self.fps_history.pop(0)
        
        self.frame_time_history.append(current_time * 1000)
        if len(self.frame_time_history) > 60:
            self.frame_time_history.pop(0)
        
        self.max_fps = max(self.fps_history)
        self.min_fps = min(self.fps_history)
        self.avg_fps = sum(self.fps_history) / len(self.fps_history)
        
        self.max_frame_time = max(self.frame_time_history)
        self.min_frame_time = min(self.frame_time_history)
        self.avg_frame_time = sum(self.frame_time_history) / len(self.frame_time_history)
        
        self.entity_count["towers"] = len(towers)
        self.entity_count["enemies"] = len(enemies)
        self.entity_count["projectiles"] = len(projectiles)
        self.entity_count["particles"] = len(particles)

    def get_performance_report(self):
        return {
            "fps": {
                "current": self.avg_fps,
                "max": self.max_fps,
                "min": self.min_fps
            },
            "frame_time": {
                "avg": self.avg_frame_time,
                "max": self.max_frame_time,
                "min": self.min_frame_time
            },
            "entities": self.entity_count,
            "frame_count": self.frame_count
        }

    def reset(self):
        self.fps_history = []
        self.frame_time_history = []
        self.frame_count = 0
        self.last_time = pygame.time.get_ticks()


class TowerBalanceSystem:
    def __init__(self):
        self.balance_factors = {
            TowerType.ARCHER: {"damage": 1.0, "range": 1.0, "speed": 1.0, "cost": 1.0},
            TowerType.CANNON: {"damage": 1.0, "range": 1.0, "speed": 1.0, "cost": 1.0},
            TowerType.MAGE: {"damage": 1.0, "range": 1.0, "speed": 1.0, "cost": 1.0},
            TowerType.ICE: {"damage": 1.0, "range": 1.0, "speed": 1.0, "cost": 1.0},
            TowerType.LIGHTNING: {"damage": 1.0, "range": 1.0, "speed": 1.0, "cost": 1.0}
        }

    def set_balance_factor(self, tower_type, factor_type, value):
        if tower_type in self.balance_factors and factor_type in self.balance_factors[tower_type]:
            self.balance_factors[tower_type][factor_type] = value

    def get_balance_factor(self, tower_type, factor_type):
        if tower_type in self.balance_factors and factor_type in self.balance_factors[tower_type]:
            return self.balance_factors[tower_type][factor_type]
        return 1.0

    def apply_balance(self, tower):
        factors = self.balance_factors.get(tower.tower_type, {})
        tower.damage *= factors.get("damage", 1.0)
        tower.range *= factors.get("range", 1.0)
        tower.attack_speed *= factors.get("speed", 1.0)

    def reset_balance(self):
        for tower_type in self.balance_factors:
            for factor in self.balance_factors[tower_type]:
                self.balance_factors[tower_type][factor] = 1.0


class AdvancedParticleSystem:
    def __init__(self):
        self.particles = []
        self.emitters = []

    def add_emitter(self, x, y, rate=10, color=COLOR_WHITE, speed=50, lifetime=1.0, 
                    gravity=0, shape='circle', spread=360, color_range=None):
        emitter = {
            'x': x, 'y': y, 'rate': rate, 'color': color, 'speed': speed,
            'lifetime': lifetime, 'gravity': gravity, 'shape': shape,
            'spread': spread, 'color_range': color_range, 'timer': 0
        }
        self.emitters.append(emitter)

    def remove_emitter(self, index):
        if 0 <= index < len(self.emitters):
            del self.emitters[index]

    def update(self, dt):
        for emitter in self.emitters:
            emitter['timer'] += dt
            spawn_count = int(emitter['timer'] * emitter['rate'])
            if spawn_count > 0:
                for _ in range(spawn_count):
                    self.emit_particle(emitter)
                emitter['timer'] -= spawn_count / emitter['rate']
        
        for particle in list(self.particles):
            particle['life'] -= dt
            particle['x'] += particle['vx'] * dt
            particle['y'] += particle['vy'] * dt
            particle['vy'] += particle['gravity'] * dt
            particle['size'] *= 0.99
            
            if particle['color_range']:
                r = int(particle['color_range'][0][0] + (particle['color_range'][1][0] - particle['color_range'][0][0]) * (1 - particle['life'] / particle['max_life']))
                g = int(particle['color_range'][0][1] + (particle['color_range'][1][1] - particle['color_range'][0][1]) * (1 - particle['life'] / particle['max_life']))
                b = int(particle['color_range'][0][2] + (particle['color_range'][1][2] - particle['color_range'][0][2]) * (1 - particle['life'] / particle['max_life']))
                particle['color'] = (r, g, b)
            
            if particle['life'] <= 0:
                self.particles.remove(particle)

    def emit_particle(self, emitter):
        angle = random.uniform(0, math.radians(emitter['spread']))
        speed = random.uniform(emitter['speed'] * 0.3, emitter['speed'])
        
        if emitter['shape'] == 'circle':
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed
        elif emitter['shape'] == 'cone':
            vx = speed
            vy = random.uniform(-speed * 0.5, speed * 0.5)
        elif emitter['shape'] == 'line':
            vx = 0
            vy = random.uniform(-speed, speed)
        else:
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed
        
        color = emitter['color']
        if emitter['color_range']:
            r = random.randint(emitter['color_range'][0][0], emitter['color_range'][1][0])
            g = random.randint(emitter['color_range'][0][1], emitter['color_range'][1][1])
            b = random.randint(emitter['color_range'][0][2], emitter['color_range'][1][2])
            color = (r, g, b)
        
        particle = {
            'x': emitter['x'], 'y': emitter['y'],
            'vx': vx, 'vy': vy,
            'color': color, 'color_range': emitter['color_range'],
            'life': emitter['lifetime'], 'max_life': emitter['lifetime'],
            'size': random.uniform(2, 6), 'gravity': emitter['gravity']
        }
        self.particles.append(particle)

    def burst(self, x, y, count=20, color=COLOR_WHITE, speed=100, lifetime=0.5, gravity=0):
        for _ in range(count):
            angle = random.uniform(0, math.pi * 2)
            spd = random.uniform(speed * 0.3, speed)
            particle = {
                'x': x, 'y': y,
                'vx': math.cos(angle) * spd,
                'vy': math.sin(angle) * spd,
                'color': color, 'color_range': None,
                'life': lifetime * random.uniform(0.5, 1.5),
                'max_life': lifetime,
                'size': random.uniform(2, 6), 'gravity': gravity
            }
            self.particles.append(particle)

    def draw(self, screen):
        for particle in self.particles:
            alpha = int(255 * (particle['life'] / particle['max_life']))
            color = (particle['color'][0], particle['color'][1], particle['color'][2], alpha)
            pygame.draw.circle(screen, color, (int(particle['x']), int(particle['y'])), int(particle['size']))


class WeatherSystem:
    def __init__(self):
        self.weather_type = "clear"
        self.intensity = 0.5
        self.particles = AdvancedParticleSystem()
        self.timer = 0

    def set_weather(self, weather_type, intensity=0.5):
        self.weather_type = weather_type
        self.intensity = max(0.1, min(1.0, intensity))
        self.particles.emitters = []
        
        if weather_type == "rain":
            for i in range(10):
                self.particles.add_emitter(
                    x=random.randint(0, SCREEN_WIDTH),
                    y=-10,
                    rate=50 * intensity,
                    color=(150, 180, 200),
                    speed=300 * intensity,
                    lifetime=2.0,
                    gravity=200 * intensity,
                    shape='line',
                    spread=10
                )
        elif weather_type == "snow":
            for i in range(5):
                self.particles.add_emitter(
                    x=random.randint(0, SCREEN_WIDTH),
                    y=-10,
                    rate=30 * intensity,
                    color=(255, 255, 255),
                    speed=50 * intensity,
                    lifetime=5.0,
                    gravity=30 * intensity,
                    shape='line',
                    spread=30
                )
        elif weather_type == "fog":
            self.fog_alpha = int(100 * intensity)
        elif weather_type == "storm":
            for i in range(15):
                self.particles.add_emitter(
                    x=random.randint(0, SCREEN_WIDTH),
                    y=-10,
                    rate=80 * intensity,
                    color=(100, 120, 140),
                    speed=400 * intensity,
                    lifetime=1.5,
                    gravity=300 * intensity,
                    shape='line',
                    spread=15
                )

    def update(self, dt):
        self.timer += dt
        self.particles.update(dt)
        
        if self.weather_type == "storm" and self.timer > 2.0:
            self.timer = 0

    def draw(self, screen):
        self.particles.draw(screen)
        
        if self.weather_type == "fog":
            fog_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            fog_surface.set_alpha(self.fog_alpha)
            fog_surface.fill((200, 200, 200))
            screen.blit(fog_surface, (0, 0))


class AmbientEffects:
    def __init__(self):
        self.effects = []
        self.particles = AdvancedParticleSystem()

    def add_effect(self, effect_type, x, y, duration=3.0, **kwargs):
        effect = {
            'type': effect_type,
            'x': x, 'y': y,
            'duration': duration,
            'life': duration,
            'kwargs': kwargs
        }
        self.effects.append(effect)
        
        if effect_type == "glow":
            self.particles.add_emitter(
                x=x, y=y,
                rate=20,
                color=kwargs.get('color', (255, 200, 100)),
                speed=10,
                lifetime=1.0,
                gravity=0,
                shape='circle',
                spread=360
            )
        elif effect_type == "smoke":
            self.particles.add_emitter(
                x=x, y=y,
                rate=15,
                color=(100, 100, 100),
                speed=20,
                lifetime=2.0,
                gravity=-10,
                shape='cone',
                spread=60,
                color_range=((100, 100, 100), (150, 150, 150))
            )
        elif effect_type == "sparkle":
            for _ in range(20):
                self.particles.burst(
                    x=x, y=y,
                    count=5,
                    color=kwargs.get('color', (255, 255, 200)),
                    speed=50,
                    lifetime=0.5
                )

    def update(self, dt):
        for effect in list(self.effects):
            effect['life'] -= dt
            if effect['life'] <= 0:
                self.effects.remove(effect)
        
        self.particles.update(dt)

    def draw(self, screen):
        self.particles.draw(screen)


class DialogSystem:
    def __init__(self):
        self.dialogs = []
        self.current_dialog = None
        self.text_index = 0
        self.text_timer = 0
        self.speed = 0.05
        self.font = get_chinese_font(24)

    def add_dialog(self, speaker, text, choices=None):
        dialog = {
            'speaker': speaker,
            'text': text,
            'choices': choices or [],
            'completed': False
        }
        self.dialogs.append(dialog)

    def start_dialog(self):
        if self.dialogs:
            self.current_dialog = self.dialogs[0]
            self.text_index = 0
            self.text_timer = 0

    def update(self, dt):
        if not self.current_dialog:
            return
        
        self.text_timer += dt
        if self.text_timer >= self.speed:
            self.text_timer = 0
            if self.text_index < len(self.current_dialog['text']):
                self.text_index += 1

    def is_complete(self):
        return self.text_index >= len(self.current_dialog['text']) if self.current_dialog else True

    def next(self):
        if self.is_complete():
            if self.current_dialog:
                self.current_dialog['completed'] = True
                self.dialogs.pop(0)
                self.current_dialog = None
                self.text_index = 0
            self.start_dialog()

    def draw(self, screen):
        if not self.current_dialog:
            return
        
        dialog_box = pygame.Rect(100, SCREEN_HEIGHT - 150, SCREEN_WIDTH - 200, 130)
        pygame.draw.rect(screen, (30, 30, 50), dialog_box)
        pygame.draw.rect(screen, COLOR_WHITE, dialog_box, 3)
        
        speaker_text = self.font.render(self.current_dialog['speaker'], True, COLOR_GOLD)
        screen.blit(speaker_text, (120, SCREEN_HEIGHT - 130))
        
        displayed_text = self.current_dialog['text'][:self.text_index]
        text_surface = self.font.render(displayed_text, True, COLOR_WHITE)
        screen.blit(text_surface, (120, SCREEN_HEIGHT - 90))
        
        if self.is_complete():
            continue_text = self.font.render("按任意键继续...", True, COLOR_GRAY)
            screen.blit(continue_text, (SCREEN_WIDTH - 200, SCREEN_HEIGHT - 40))


class QuestSystem:
    def __init__(self):
        self.quests = []
        self.active_quests = []
        self.completed_quests = []
        self.objectives = {}

    def add_quest(self, quest_id, title, description, objectives, rewards):
        quest = {
            'id': quest_id,
            'title': title,
            'description': description,
            'objectives': objectives,
            'rewards': rewards,
            'progress': {obj['id']: 0 for obj in objectives},
            'completed': False,
            'active': False
        }
        self.quests.append(quest)

    def activate_quest(self, quest_id):
        for quest in self.quests:
            if quest['id'] == quest_id and not quest['completed']:
                quest['active'] = True
                self.active_quests.append(quest)
                return True
        return False

    def update_objective(self, objective_id, amount=1):
        for quest in self.active_quests:
            for obj in quest['objectives']:
                if obj['id'] == objective_id:
                    quest['progress'][objective_id] = min(
                        quest['progress'][objective_id] + amount,
                        obj['target']
                    )
                    self.check_quest_completion(quest)

    def check_quest_completion(self, quest):
        for obj in quest['objectives']:
            if quest['progress'][obj['id']] < obj['target']:
                return
        
        quest['completed'] = True
        quest['active'] = False
        self.active_quests.remove(quest)
        self.completed_quests.append(quest)

    def get_rewards(self, quest_id):
        for quest in self.completed_quests:
            if quest['id'] == quest_id:
                return quest['rewards']
        return {}

    def draw_quest_log(self, screen, font):
        screen.fill((30, 30, 60))
        
        title_text = font.render("任务日志", True, COLOR_GOLD)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 50))
        screen.blit(title_text, title_rect)

        back_button = pygame.Rect(50, 50, 100, 40)
        pygame.draw.rect(screen, COLOR_GRAY, back_button)
        pygame.draw.rect(screen, COLOR_WHITE, back_button, 2)
        back_text = font.render("返回", True, COLOR_WHITE)
        back_rect = back_text.get_rect(center=back_button.center)
        screen.blit(back_text, back_rect)

        y = 120
        for quest in self.active_quests:
            quest_box = pygame.Rect(50, y, SCREEN_WIDTH - 100, 100)
            pygame.draw.rect(screen, (50, 50, 80), quest_box)
            pygame.draw.rect(screen, COLOR_WHITE, quest_box, 2)
            
            title_text = font.render(quest['title'], True, COLOR_GOLD)
            screen.blit(title_text, (70, y + 15))
            
            desc_text = font.render(quest['description'], True, COLOR_WHITE)
            screen.blit(desc_text, (70, y + 45))
            
            for obj in quest['objectives']:
                progress = quest['progress'][obj['id']]
                progress_text = font.render(f"{obj['description']}: {progress}/{obj['target']}", True, COLOR_GREEN)
                screen.blit(progress_text, (70, y + 70))
            
            y += 120

        if not self.active_quests:
            empty_text = font.render("暂无活跃任务", True, COLOR_GRAY)
            empty_rect = empty_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(empty_text, empty_rect)


class ShopSystem:
    def __init__(self):
        self.items = []
        self.gold = 0

    def add_item(self, item_id, name, description, price, type_, effect):
        item = {
            'id': item_id,
            'name': name,
            'description': description,
            'price': price,
            'type': type_,
            'effect': effect,
            'purchased': False
        }
        self.items.append(item)

    def purchase_item(self, item_id):
        for item in self.items:
            if item['id'] == item_id and not item['purchased']:
                if self.gold >= item['price']:
                    self.gold -= item['price']
                    item['purchased'] = True
                    return item
        return None

    def get_item_effect(self, item_id):
        for item in self.items:
            if item['id'] == item_id and item['purchased']:
                return item['effect']
        return None

    def draw_shop(self, screen, font):
        screen.fill((30, 30, 60))
        
        title_text = font.render("商店", True, COLOR_GOLD)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 50))
        screen.blit(title_text, title_rect)

        back_button = pygame.Rect(50, 50, 100, 40)
        pygame.draw.rect(screen, COLOR_GRAY, back_button)
        pygame.draw.rect(screen, COLOR_WHITE, back_button, 2)
        back_text = font.render("返回", True, COLOR_WHITE)
        back_rect = back_text.get_rect(center=back_button.center)
        screen.blit(back_text, back_rect)

        gold_text = font.render(f"金币: {self.gold}", True, COLOR_YELLOW)
        gold_rect = gold_text.get_rect(right=SCREEN_WIDTH - 50, top=50)
        screen.blit(gold_text, gold_rect)

        cols = 2
        rows = (len(self.items) + cols - 1) // cols
        
        for i, item in enumerate(self.items):
            x = 50 + (i % cols) * (SCREEN_WIDTH // 2 - 50)
            y = 120 + (i // cols) * 180
            
            item_box = pygame.Rect(x, y, SCREEN_WIDTH // 2 - 70, 160)
            
            if item['purchased']:
                pygame.draw.rect(screen, (50, 80, 50), item_box)
                pygame.draw.rect(screen, COLOR_GREEN, item_box, 2)
            elif self.gold >= item['price']:
                pygame.draw.rect(screen, (50, 50, 80), item_box)
                pygame.draw.rect(screen, COLOR_WHITE, item_box, 2)
            else:
                pygame.draw.rect(screen, (40, 40, 40), item_box)
                pygame.draw.rect(screen, COLOR_GRAY, item_box, 2)
            
            name_text = font.render(item['name'], True, COLOR_GOLD if not item['purchased'] else COLOR_GREEN)
            screen.blit(name_text, (x + 20, y + 20))
            
            desc_lines = self.wrap_text(item['description'], 40)
            for j, line in enumerate(desc_lines[:3]):
                desc_text = font.render(line, True, COLOR_WHITE)
                screen.blit(desc_text, (x + 20, y + 50 + j * 25))
            
            if item['purchased']:
                purchased_text = font.render("已购买", True, COLOR_GREEN)
                screen.blit(purchased_text, (x + 20, y + 120))
            else:
                price_text = font.render(f"价格: {item['price']} 金币", True, COLOR_YELLOW if self.gold >= item['price'] else COLOR_RED)
                screen.blit(price_text, (x + 20, y + 120))

    def wrap_text(self, text, max_chars):
        lines = []
        current_line = ""
        for char in text:
            if len(current_line) >= max_chars:
                lines.append(current_line)
                current_line = char
            else:
                current_line += char
        if current_line:
            lines.append(current_line)
        return lines


class MiniMap:
    def __init__(self, level):
        self.level = level
        self.surface = pygame.Surface((200, 150))
        self.rect = pygame.Rect(SCREEN_WIDTH - 220, 80, 200, 150)
        self.scale_x = 200 / SCREEN_WIDTH
        self.scale_y = 150 / (SCREEN_HEIGHT - 200)

    def update(self, enemies, towers):
        self.surface.fill((30, 30, 50))
        
        if self.level:
            path_points = [(int(p[0] * self.scale_x), int(p[1] * self.scale_y)) for p in self.level.path_points]
            for i in range(len(path_points) - 1):
                pygame.draw.line(self.surface, COLOR_GRAY, path_points[i], path_points[i + 1], 3)
            
            for tower in towers:
                tx = int(tower.x * self.scale_x)
                ty = int(tower.y * self.scale_y)
                pygame.draw.circle(self.surface, COLOR_GREEN, (tx, ty), 4)
            
            for enemy in enemies:
                ex = int(enemy.x * self.scale_x)
                ey = int(enemy.y * self.scale_y)
                pygame.draw.circle(self.surface, COLOR_RED, (ex, ey), 3)

    def draw(self, screen):
        pygame.draw.rect(screen, COLOR_BLACK, self.rect)
        pygame.draw.rect(screen, COLOR_WHITE, self.rect, 2)
        screen.blit(self.surface, (SCREEN_WIDTH - 220, 80))
        
        legend_x = SCREEN_WIDTH - 210
        legend_y = 240
        
        pygame.draw.circle(screen, COLOR_GREEN, (legend_x, legend_y), 4)
        legend_text = get_chinese_font(12).render("塔", True, COLOR_WHITE)
        screen.blit(legend_text, (legend_x + 10, legend_y - 5))
        
        pygame.draw.circle(screen, COLOR_RED, (legend_x, legend_y + 20), 3)
        legend_text = get_chinese_font(12).render("敌人", True, COLOR_WHITE)
        screen.blit(legend_text, (legend_x + 10, legend_y + 15))


class InputManager:
    def __init__(self):
        self.key_states = {}
        self.mouse_pos = (0, 0)
        self.mouse_buttons = {1: False, 2: False, 3: False}
        self.click_handlers = []
        self.key_handlers = []

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEMOTION:
                self.mouse_pos = event.pos
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button in self.mouse_buttons:
                    self.mouse_buttons[event.button] = True
                    for handler in self.click_handlers:
                        handler(event.pos, event.button)
            
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button in self.mouse_buttons:
                    self.mouse_buttons[event.button] = False
            
            elif event.type == pygame.KEYDOWN:
                self.key_states[event.key] = True
                for handler in self.key_handlers:
                    handler(event.key, True)
            
            elif event.type == pygame.KEYUP:
                self.key_states[event.key] = False
                for handler in self.key_handlers:
                    handler(event.key, False)

    def is_key_pressed(self, key):
        return self.key_states.get(key, False)

    def is_mouse_button_down(self, button):
        return self.mouse_buttons.get(button, False)

    def add_click_handler(self, handler):
        self.click_handlers.append(handler)

    def remove_click_handler(self, handler):
        if handler in self.click_handlers:
            self.click_handlers.remove(handler)

    def add_key_handler(self, handler):
        self.key_handlers.append(handler)

    def remove_key_handler(self, handler):
        if handler in self.key_handlers:
            self.key_handlers.remove(handler)


class Camera:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.target_x = 0
        self.target_y = 0
        self.speed = 5.0
        self.zoom = 1.0
        self.min_zoom = 0.5
        self.max_zoom = 2.0

    def update(self, dt):
        self.x += (self.target_x - self.x) * self.speed * dt
        self.y += (self.target_y - self.y) * self.speed * dt
        
        self.x = max(0, min(self.x, SCREEN_WIDTH * (self.zoom - 1)))
        self.y = max(0, min(self.y, SCREEN_HEIGHT * (self.zoom - 1)))

    def set_target(self, x, y):
        self.target_x = x
        self.target_y = y

    def zoom_in(self, amount=0.1):
        self.zoom = min(self.zoom + amount, self.max_zoom)

    def zoom_out(self, amount=0.1):
        self.zoom = max(self.zoom - amount, self.min_zoom)

    def get_transform(self):
        return (self.x, self.y, self.zoom)


class ResourceManager:
    def __init__(self):
        self.images = {}
        self.sounds = {}
        self.fonts = {}
        self.load_default_resources()

    def load_default_resources(self):
        self.fonts['chinese'] = get_chinese_font(20)
        self.fonts['chinese_large'] = get_chinese_font(36)
        self.fonts['chinese_small'] = get_chinese_font(16)
        self.fonts['chinese_title'] = get_chinese_font(48)

    def load_image(self, name, path):
        try:
            self.images[name] = pygame.image.load(path).convert_alpha()
            return True
        except:
            return False

    def get_image(self, name):
        return self.images.get(name, None)

    def load_sound(self, name, path):
        try:
            self.sounds[name] = pygame.mixer.Sound(path)
            return True
        except:
            return False

    def play_sound(self, name):
        if name in self.sounds:
            self.sounds[name].play()

    def get_font(self, name):
        return self.fonts.get(name, pygame.font.Font(None, 20))


class GameStateManager:
    def __init__(self):
        self.states = {}
        self.current_state = None
        self.previous_state = None

    def add_state(self, name, state):
        self.states[name] = state

    def set_state(self, name):
        if name in self.states:
            self.previous_state = self.current_state
            self.current_state = self.states[name]
            if hasattr(self.current_state, 'enter'):
                self.current_state.enter()

    def get_state(self):
        return self.current_state

    def update(self, dt):
        if self.current_state and hasattr(self.current_state, 'update'):
            self.current_state.update(dt)

    def draw(self, screen):
        if self.current_state and hasattr(self.current_state, 'draw'):
            self.current_state.draw(screen)

    def handle_event(self, event):
        if self.current_state and hasattr(self.current_state, 'handle_event'):
            self.current_state.handle_event(event)


class BaseGameState:
    def __init__(self, game):
        self.game = game

    def enter(self):
        pass

    def exit(self):
        pass

    def update(self, dt):
        pass

    def draw(self, screen):
        pass

    def handle_event(self, event):
        pass


class MenuState(BaseGameState):
    def __init__(self, game):
        super().__init__(game)

    def draw(self, screen):
        self.game.draw_menu()


class LevelSelectState(BaseGameState):
    def __init__(self, game):
        super().__init__(game)

    def draw(self, screen):
        self.game.draw_level_select()


class InGameState(BaseGameState):
    def __init__(self, game):
        super().__init__(game)

    def update(self, dt):
        self.game.update_game(dt)

    def draw(self, screen):
        self.game.draw_game()


class TowerEncyclopediaState(BaseGameState):
    def __init__(self, game):
        super().__init__(game)

    def draw(self, screen):
        self.game.draw_tower_encyclopedia()


class EnemyEncyclopediaState(BaseGameState):
    def __init__(self, game):
        super().__init__(game)

    def draw(self, screen):
        self.game.draw_enemy_encyclopedia()


class PauseState(BaseGameState):
    def __init__(self, game):
        super().__init__(game)

    def draw(self, screen):
        self.game.draw_game()
        self.game.draw_pause()


class GameOverState(BaseGameState):
    def __init__(self, game):
        super().__init__(game)

    def draw(self, screen):
        self.game.draw_game()
        self.game.draw_game_over()


class VictoryState(BaseGameState):
    def __init__(self, game):
        super().__init__(game)

    def draw(self, screen):
        self.game.draw_game()
        self.game.draw_victory()


class TowerDamageSystem:
    def __init__(self):
        self.damage_modifiers = {}
        self.resistances = {
            EnemyType.GOBLIN: {"physical": 0.8, "magic": 1.2, "fire": 1.0, "ice": 1.0, "lightning": 1.0},
            EnemyType.SKELETON: {"physical": 1.5, "magic": 0.5, "fire": 1.2, "ice": 1.0, "lightning": 1.0},
            EnemyType.ORC: {"physical": 0.6, "magic": 1.0, "fire": 1.1, "ice": 0.9, "lightning": 1.0},
            EnemyType.SHADOW_WOLF: {"physical": 1.0, "magic": 1.2, "fire": 1.0, "ice": 0.8, "lightning": 1.1},
            EnemyType.TROLL: {"physical": 0.5, "magic": 1.1, "fire": 1.0, "ice": 0.7, "lightning": 1.2},
            EnemyType.OGRE_MAGE: {"physical": 0.7, "magic": 0.6, "fire": 1.0, "ice": 1.0, "lightning": 1.3},
            EnemyType.NECROMANCER: {"physical": 1.2, "magic": 0.4, "fire": 1.3, "ice": 0.9, "lightning": 1.1},
            EnemyType.DARK_KNIGHT: {"physical": 0.4, "magic": 0.8, "fire": 0.9, "ice": 0.9, "lightning": 1.0},
            EnemyType.DEMON: {"physical": 0.5, "magic": 0.7, "fire": 0.8, "ice": 1.3, "lightning": 1.1},
            EnemyType.DRAGON_WHELP: {"physical": 0.6, "magic": 0.9, "fire": 0.5, "ice": 1.2, "lightning": 1.0},
            EnemyType.WIZNAN: {"physical": 0.4, "magic": 0.5, "fire": 0.7, "ice": 1.0, "lightning": 0.8}
        }

    def calculate_damage(self, tower_type, enemy_type, base_damage):
        damage_type = self.get_damage_type(tower_type)
        resistance = self.resistances.get(enemy_type, {}).get(damage_type, 1.0)
        modifier = self.damage_modifiers.get(tower_type, 1.0)
        return base_damage * resistance * modifier

    def get_damage_type(self, tower_type):
        damage_types = {
            TowerType.ARCHER: "physical",
            TowerType.CANNON: "physical",
            TowerType.MAGE: "magic",
            TowerType.ICE: "ice",
            TowerType.LIGHTNING: "lightning"
        }
        return damage_types.get(tower_type, "physical")

    def add_modifier(self, tower_type, modifier):
        if tower_type in self.damage_modifiers:
            self.damage_modifiers[tower_type] *= modifier
        else:
            self.damage_modifiers[tower_type] = modifier

    def remove_modifier(self, tower_type):
        if tower_type in self.damage_modifiers:
            del self.damage_modifiers[tower_type]


class EnemyBuffSystem:
    def __init__(self):
        self.buffs = {}
        self.debuffs = {}

    def add_buff(self, enemy_id, buff_type, duration, value):
        if enemy_id not in self.buffs:
            self.buffs[enemy_id] = []
        self.buffs[enemy_id].append({
            'type': buff_type,
            'duration': duration,
            'max_duration': duration,
            'value': value
        })

    def add_debuff(self, enemy_id, debuff_type, duration, value):
        if enemy_id not in self.debuffs:
            self.debuffs[enemy_id] = []
        self.debuffs[enemy_id].append({
            'type': debuff_type,
            'duration': duration,
            'max_duration': duration,
            'value': value
        })

    def update(self, dt):
        for enemy_id in list(self.buffs.keys()):
            self.buffs[enemy_id] = [b for b in self.buffs[enemy_id] if b['duration'] > 0]
            for buff in self.buffs[enemy_id]:
                buff['duration'] -= dt
            if not self.buffs[enemy_id]:
                del self.buffs[enemy_id]

        for enemy_id in list(self.debuffs.keys()):
            self.debuffs[enemy_id] = [d for d in self.debuffs[enemy_id] if d['duration'] > 0]
            for debuff in self.debuffs[enemy_id]:
                debuff['duration'] -= dt
            if not self.debuffs[enemy_id]:
                del self.debuffs[enemy_id]

    def get_buff_value(self, enemy_id, buff_type):
        total = 0
        if enemy_id in self.buffs:
            for buff in self.buffs[enemy_id]:
                if buff['type'] == buff_type:
                    total += buff['value']
        return total

    def get_debuff_value(self, enemy_id, debuff_type):
        total = 0
        if enemy_id in self.debuffs:
            for debuff in self.debuffs[enemy_id]:
                if debuff['type'] == debuff_type:
                    total += debuff['value']
        return total

    def has_buff(self, enemy_id, buff_type):
        if enemy_id in self.buffs:
            for buff in self.buffs[enemy_id]:
                if buff['type'] == buff_type:
                    return True
        return False

    def has_debuff(self, enemy_id, debuff_type):
        if enemy_id in self.debuffs:
            for debuff in self.debuffs[enemy_id]:
                if debuff['type'] == debuff_type:
                    return True
        return False


class TowerCooldownSystem:
    def __init__(self):
        self.cooldowns = {}

    def set_cooldown(self, tower_id, cooldown_type, duration):
        if tower_id not in self.cooldowns:
            self.cooldowns[tower_id] = {}
        self.cooldowns[tower_id][cooldown_type] = {
            'end_time': pygame.time.get_ticks() + duration * 1000,
            'duration': duration
        }

    def is_ready(self, tower_id, cooldown_type):
        if tower_id not in self.cooldowns:
            return True
        if cooldown_type not in self.cooldowns[tower_id]:
            return True
        return pygame.time.get_ticks() >= self.cooldowns[tower_id][cooldown_type]['end_time']

    def get_remaining_time(self, tower_id, cooldown_type):
        if tower_id not in self.cooldowns or cooldown_type not in self.cooldowns[tower_id]:
            return 0
        remaining = (self.cooldowns[tower_id][cooldown_type]['end_time'] - pygame.time.get_ticks()) / 1000
        return max(0, remaining)

    def update(self):
        current_time = pygame.time.get_ticks()
        for tower_id in list(self.cooldowns.keys()):
            self.cooldowns[tower_id] = {
                k: v for k, v in self.cooldowns[tower_id].items()
                if v['end_time'] > current_time
            }
            if not self.cooldowns[tower_id]:
                del self.cooldowns[tower_id]


class GameTutorial:
    def __init__(self):
        self.steps = []
        self.current_step = 0
        self.active = False
        self.completed = False

    def add_step(self, title, description, target_area=None, highlight=True):
        step = {
            'title': title,
            'description': description,
            'target_area': target_area,
            'highlight': highlight,
            'completed': False
        }
        self.steps.append(step)

    def start(self):
        self.current_step = 0
        self.active = True
        self.completed = False

    def next_step(self):
        if self.current_step < len(self.steps):
            self.steps[self.current_step]['completed'] = True
        self.current_step += 1
        if self.current_step >= len(self.steps):
            self.active = False
            self.completed = True

    def get_current_step(self):
        if self.current_step < len(self.steps):
            return self.steps[self.current_step]
        return None

    def draw(self, screen, font):
        if not self.active:
            return

        step = self.get_current_step()
        if not step:
            return

        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(100)
        overlay.fill(COLOR_BLACK)
        screen.blit(overlay, (0, 0))

        if step['target_area'] and step['highlight']:
            pygame.draw.rect(screen, COLOR_YELLOW, step['target_area'], 3)

        dialog_box = pygame.Rect(100, SCREEN_HEIGHT - 180, SCREEN_WIDTH - 200, 160)
        pygame.draw.rect(screen, (30, 30, 50), dialog_box)
        pygame.draw.rect(screen, COLOR_WHITE, dialog_box, 3)

        title_text = font.render(step['title'], True, COLOR_GOLD)
        screen.blit(title_text, (120, SCREEN_HEIGHT - 160))

        desc_lines = self.wrap_text(step['description'], 50)
        for i, line in enumerate(desc_lines[:4]):
            desc_text = font.render(line, True, COLOR_WHITE)
            screen.blit(desc_text, (120, SCREEN_HEIGHT - 120 + i * 25))

        continue_text = font.render("按空格键继续...", True, COLOR_GRAY)
        continue_rect = continue_text.get_rect(right=SCREEN_WIDTH - 120, bottom=SCREEN_HEIGHT - 30)
        screen.blit(continue_text, continue_rect)

    def wrap_text(self, text, max_chars):
        lines = []
        current_line = ""
        for char in text:
            if len(current_line) >= max_chars:
                lines.append(current_line)
                current_line = char
            else:
                current_line += char
        if current_line:
            lines.append(current_line)
        return lines


class AchievementNotification:
    def __init__(self):
        self.notifications = []
        self.font = get_chinese_font(20)

    def add_notification(self, achievement):
        notification = {
            'achievement': achievement,
            'life': 3.0,
            'max_life': 3.0,
            'x': SCREEN_WIDTH // 2,
            'y': -50,
            'target_y': 50
        }
        self.notifications.append(notification)

    def update(self, dt):
        for notification in list(self.notifications):
            notification['life'] -= dt
            notification['y'] += (notification['target_y'] - notification['y']) * 0.1

            if notification['life'] <= 0:
                self.notifications.remove(notification)

    def draw(self, screen):
        for notification in self.notifications:
            alpha = int(255 * (notification['life'] / notification['max_life']))
            
            bg_surface = pygame.Surface((300, 80))
            bg_surface.set_alpha(alpha)
            bg_surface.fill((50, 50, 50))
            pygame.draw.rect(bg_surface, COLOR_GOLD, (0, 0, 300, 80), 2)
            
            icon_text = self.font.render(notification['achievement'].icon, True, COLOR_GOLD)
            bg_surface.blit(icon_text, (20, 25))
            
            name_text = self.font.render(notification['achievement'].name, True, COLOR_WHITE)
            bg_surface.blit(name_text, (60, 20))
            
            desc_text = self.font.render(notification['achievement'].description, True, COLOR_GRAY)
            bg_surface.blit(desc_text, (60, 50))
            
            screen.blit(bg_surface, (notification['x'] - 150, notification['y']))


class QuickSaveSystem:
    def __init__(self):
        self.save_slots = 5
        self.auto_save_interval = 60
        self.last_auto_save_time = 0

    def create_save(self, game_state, slot=0):
        save_data = {
            'timestamp': pygame.time.get_ticks(),
            'level': game_state.get('level', 0),
            'wave': game_state.get('wave', 0),
            'gold': game_state.get('gold', 150),
            'lives': game_state.get('lives', 20),
            'score': game_state.get('score', 0),
            'towers': game_state.get('towers', []),
            'enemies': game_state.get('enemies', []),
            'campaign_progress': game_state.get('campaign_progress', {})
        }
        
        try:
            with open(f"save_slot_{slot}.json", 'w', encoding='utf-8') as f:
                json.dump(save_data, f, indent=4)
            return True
        except:
            return False

    def load_save(self, slot=0):
        try:
            with open(f"save_slot_{slot}.json", 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return None

    def auto_save(self, game_state):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_auto_save_time >= self.auto_save_interval * 1000:
            self.create_save(game_state, slot=0)
            self.last_auto_save_time = current_time

    def get_save_info(self, slot=0):
        try:
            with open(f"save_slot_{slot}.json", 'r', encoding='utf-8') as f:
                data = json.load(f)
                return {
                    'exists': True,
                    'timestamp': data.get('timestamp', 0),
                    'level': data.get('level', 0),
                    'wave': data.get('wave', 0),
                    'score': data.get('score', 0)
                }
        except:
            return {'exists': False}


class LocalizationSystem:
    def __init__(self):
        self.language = "zh"
        self.strings = {
            "zh": {
                "menu_title": "王国防线",
                "menu_subtitle": "Kingdom Defense",
                "menu_start": "开始游戏",
                "menu_tower_encyclopedia": "塔图鉴",
                "menu_enemy_encyclopedia": "敌人图鉴",
                "menu_achievements": "成就",
                "menu_settings": "设置",
                "menu_quit": "退出游戏",
                "level_select_title": "选择关卡",
                "level_select_back": "返回",
                "level_reward": "奖励: {gold} 金币",
                "level_completed": "已通关",
                "game_gold": "金币: {gold}",
                "game_lives": "生命: {lives}",
                "game_score": "得分: {score}",
                "game_wave": "波次: {current}/{total}",
                "game_pause": "暂停",
                "pause_title": "游戏暂停",
                "pause_continue": "继续游戏",
                "pause_menu": "返回主菜单",
                "pause_restart": "重新开始",
                "game_over_title": "游戏结束",
                "game_over_score": "最终得分: {score}",
                "victory_title": "胜利!",
                "victory_reward": "奖励: {gold} 金币",
                "victory_next_level": "下一关",
                "tower_archer": "弓箭塔",
                "tower_cannon": "炮塔",
                "tower_magic": "魔法塔",
                "tower_flame": "火焰塔",
                "tower_ice": "冰霜塔",
                "tower_lightning": "雷电塔",
                "tower_slow": "减速塔",
                "tower_sniper": "狙击塔",
                "upgrade": "升级",
                "sell": "出售",
                "cancel": "取消",
                "select_tower": "选择塔类型",
                "upgrade_cost": "{cost}金币",
                "sell_value": "卖 {value}",
                "damage": "伤害",
                "range": "范围",
                "speed": "攻速",
                "cost": "费用",
                "normal_enemies": "普通敌人",
                "elite_enemies": "精英敌人",
                "boss_enemies": "BOSS",
                "hp": "生命",
                "speed_stat": "速度",
                "reward": "奖励"
            },
            "en": {
                "menu_title": "Kingdom Defense",
                "menu_subtitle": "王国防线",
                "menu_start": "Start Game",
                "menu_tower_encyclopedia": "Tower Encyclopedia",
                "menu_enemy_encyclopedia": "Enemy Encyclopedia",
                "menu_achievements": "Achievements",
                "menu_settings": "Settings",
                "menu_quit": "Quit",
                "level_select_title": "Select Level",
                "level_select_back": "Back",
                "level_reward": "Reward: {gold} Gold",
                "level_completed": "Completed",
                "game_gold": "Gold: {gold}",
                "game_lives": "Lives: {lives}",
                "game_score": "Score: {score}",
                "game_wave": "Wave: {current}/{total}",
                "game_pause": "Pause",
                "pause_title": "Game Paused",
                "pause_continue": "Continue",
                "pause_menu": "Main Menu",
                "pause_restart": "Restart",
                "game_over_title": "Game Over",
                "game_over_score": "Final Score: {score}",
                "victory_title": "Victory!",
                "victory_reward": "Reward: {gold} Gold",
                "victory_next_level": "Next Level",
                "tower_archer": "Archer Tower",
                "tower_cannon": "Cannon Tower",
                "tower_magic": "Magic Tower",
                "tower_flame": "Flame Tower",
                "tower_ice": "Ice Tower",
                "tower_lightning": "Lightning Tower",
                "tower_slow": "Slow Tower",
                "tower_sniper": "Sniper Tower",
                "upgrade": "Upgrade",
                "sell": "Sell",
                "cancel": "Cancel",
                "select_tower": "Select Tower Type",
                "upgrade_cost": "{cost} Gold",
                "sell_value": "Sell {value}",
                "damage": "Damage",
                "range": "Range",
                "speed": "Speed",
                "cost": "Cost",
                "normal_enemies": "Normal Enemies",
                "elite_enemies": "Elite Enemies",
                "boss_enemies": "Bosses",
                "hp": "HP",
                "speed_stat": "Speed",
                "reward": "Reward"
            }
        }

    def set_language(self, language):
        if language in self.strings:
            self.language = language

    def get_string(self, key, **kwargs):
        if self.language in self.strings and key in self.strings[self.language]:
            return self.strings[self.language][key].format(**kwargs)
        return key


class PerformanceProfiler:
    def __init__(self):
        self.frame_times = []
        self.max_frame_time = 0
        self.min_frame_time = float('inf')
        self.avg_frame_time = 0
        self.fps_history = []
        self.entity_counts = {
            'towers': [],
            'enemies': [],
            'projectiles': [],
            'particles': []
        }
        self.section_times = {}

    def start_section(self, section_name):
        self.section_times[section_name] = pygame.time.get_ticks()

    def end_section(self, section_name):
        if section_name in self.section_times:
            elapsed = pygame.time.get_ticks() - self.section_times[section_name]
            self.section_times[section_name] = elapsed
        else:
            self.section_times[section_name] = 0

    def update_frame_time(self, frame_time_ms):
        self.frame_times.append(frame_time_ms)
        if len(self.frame_times) > 60:
            self.frame_times.pop(0)
        
        self.max_frame_time = max(self.frame_times)
        self.min_frame_time = min(self.frame_times)
        self.avg_frame_time = sum(self.frame_times) / len(self.frame_times)
        
        fps = 1000 / max(frame_time_ms, 0.001)
        self.fps_history.append(fps)
        if len(self.fps_history) > 60:
            self.fps_history.pop(0)

    def update_entity_counts(self, towers, enemies, projectiles, particles):
        self.entity_counts['towers'].append(len(towers))
        self.entity_counts['enemies'].append(len(enemies))
        self.entity_counts['projectiles'].append(len(projectiles))
        self.entity_counts['particles'].append(len(particles))
        
        for key in self.entity_counts:
            if len(self.entity_counts[key]) > 60:
                self.entity_counts[key].pop(0)

    def get_report(self):
        return {
            'fps': {
                'current': 1000 / self.avg_frame_time if self.avg_frame_time > 0 else 0,
                'max': 1000 / self.min_frame_time if self.min_frame_time > 0 else 0,
                'min': 1000 / self.max_frame_time if self.max_frame_time > 0 else 0
            },
            'frame_time': {
                'avg': self.avg_frame_time,
                'max': self.max_frame_time,
                'min': self.min_frame_time
            },
            'sections': self.section_times,
            'entities': {
                key: sum(vals) / len(vals) if vals else 0
                for key, vals in self.entity_counts.items()
            }
        }

    def reset(self):
        self.frame_times = []
        self.max_frame_time = 0
        self.min_frame_time = float('inf')
        self.avg_frame_time = 0
        self.fps_history = []
        self.section_times = {}


class GameEventSystem:
    def __init__(self, game):
        self.game = game
        self.events = []
        self.event_queue = []

    def add_event(self, event_type, data=None, delay=0):
        event = {
            'type': event_type,
            'data': data,
            'delay': delay,
            'trigger_time': pygame.time.get_ticks() + delay * 1000
        }
        self.event_queue.append(event)

    def update(self):
        current_time = pygame.time.get_ticks()
        self.event_queue = [e for e in self.event_queue if e['trigger_time'] > current_time]
        
        ready_events = [e for e in self.event_queue if e['trigger_time'] <= current_time]
        for event in ready_events:
            self.handle_event(event)

    def handle_event(self, event):
        if event['type'] == 'wave_start':
            self.game.start_wave()
        elif event['type'] == 'wave_complete':
            self.game.wave_complete()
        elif event['type'] == 'game_over':
            self.game.game_over()
        elif event['type'] == 'victory':
            self.game.victory()
        elif event['type'] == 'enemy_spawn':
            data = event['data']
            self.game.spawn_enemy(data['type'], data['path'])
        elif event['type'] == 'tower_buff':
            data = event['data']
            for tower in self.game.towers:
                if tower.tower_type == data['tower_type']:
                    tower.damage *= data['multiplier']
        elif event['type'] == 'show_message':
            self.game.show_message(event['data'])


class GameCheatSystem:
    def __init__(self, game):
        self.game = game
        self.cheats_enabled = False
        self.cheat_codes = {
            'gold': lambda: setattr(self.game, 'gold', self.game.gold + 1000),
            'lives': lambda: setattr(self.game, 'lives', self.game.lives + 10),
            'win': lambda: self.game.victory(),
            'killall': lambda: setattr(self.game, 'enemies', []),
            'speed': lambda: self.toggle_speed(),
            'freebuild': lambda: setattr(self.game, 'free_build', not self.game.free_build)
        }
        self.speed_multiplier = 1.0

    def toggle_speed(self):
        self.speed_multiplier = 2.0 if self.speed_multiplier == 1.0 else 1.0
        self.game.game_speed = self.speed_multiplier

    def check_cheat(self, key_sequence):
        if self.cheats_enabled and key_sequence in self.cheat_codes:
            self.cheat_codes[key_sequence]()
            return True
        return False


class GameStatistics:
    def __init__(self):
        self.total_gold_earned = 0
        self.total_gold_spent = 0
        self.total_towers_built = 0
        self.total_towers_upgraded = 0
        self.total_towers_sold = 0
        self.total_enemies_killed = 0
        self.total_damage_dealt = 0
        self.total_waves_completed = 0
        self.total_levels_completed = 0
        self.total_lives_lost = 0
        self.play_time = 0
        self.best_score = 0

    def reset(self):
        self.__init__()

    def update_play_time(self, dt):
        self.play_time += dt

    def add_gold_earned(self, amount):
        self.total_gold_earned += amount

    def add_gold_spent(self, amount):
        self.total_gold_spent += amount

    def add_tower_built(self):
        self.total_towers_built += 1

    def add_tower_upgraded(self):
        self.total_towers_upgraded += 1

    def add_tower_sold(self):
        self.total_towers_sold += 1

    def add_enemy_killed(self, enemy):
        self.total_enemies_killed += 1
        self.total_damage_dealt += enemy.max_hp

    def add_wave_completed(self):
        self.total_waves_completed += 1

    def add_level_completed(self):
        self.total_levels_completed += 1

    def add_life_lost(self):
        self.total_lives_lost += 1

    def update_best_score(self, score):
        if score > self.best_score:
            self.best_score = score


class GameDifficultySettings:
    def __init__(self):
        self.difficulty = 'normal'
        self.settings = {
            'easy': {
                'enemy_health_multiplier': 0.7,
                'enemy_speed_multiplier': 0.8,
                'gold_reward_multiplier': 1.3,
                'tower_cost_multiplier': 0.8,
                'starting_lives': 30
            },
            'normal': {
                'enemy_health_multiplier': 1.0,
                'enemy_speed_multiplier': 1.0,
                'gold_reward_multiplier': 1.0,
                'tower_cost_multiplier': 1.0,
                'starting_lives': 20
            },
            'hard': {
                'enemy_health_multiplier': 1.5,
                'enemy_speed_multiplier': 1.2,
                'gold_reward_multiplier': 0.8,
                'tower_cost_multiplier': 1.2,
                'starting_lives': 15
            },
            'impossible': {
                'enemy_health_multiplier': 2.0,
                'enemy_speed_multiplier': 1.5,
                'gold_reward_multiplier': 0.5,
                'tower_cost_multiplier': 1.5,
                'starting_lives': 10
            }
        }

    def set_difficulty(self, difficulty):
        if difficulty in self.settings:
            self.difficulty = difficulty

    def get_setting(self, setting_name):
        return self.settings[self.difficulty].get(setting_name, 1.0)

    def get_starting_lives(self):
        return self.settings[self.difficulty]['starting_lives']


class GameAchievementManager:
    def __init__(self):
        self.achievements = {
            'first_blood': {'name': '初战告捷', 'description': '击杀第一个敌人', 'unlocked': False, 'icon': '🗡️'},
            'gold_rush': {'name': '淘金热', 'description': '累计获得1000金币', 'unlocked': False, 'icon': '💰', 'progress': 0, 'target': 1000},
            'tower_master': {'name': '塔防大师', 'description': '建造50座塔', 'unlocked': False, 'icon': '🏰', 'progress': 0, 'target': 50},
            'wave_conqueror': {'name': '波次征服者', 'description': '完成100波敌人', 'unlocked': False, 'icon': '🌊', 'progress': 0, 'target': 100},
            'speed_demon': {'name': '速通达人', 'description': '在30秒内完成一波', 'unlocked': False, 'icon': '⚡'},
            'no_damage': {'name': '无伤通关', 'description': '完成一关未损失生命', 'unlocked': False, 'icon': '❤️'},
            'level_master': {'name': '关卡大师', 'description': '完成所有关卡', 'unlocked': False, 'icon': '⭐'},
            'sniper': {'name': '神枪手', 'description': '用狙击塔击杀100个敌人', 'unlocked': False, 'icon': '🎯', 'progress': 0, 'target': 100},
            'pyromancer': {'name': '纵火者', 'description': '用火焰塔造成1000点伤害', 'unlocked': False, 'icon': '🔥', 'progress': 0, 'target': 1000},
            'cryomancer': {'name': '冰霜法师', 'description': '用冰霜塔减速100个敌人', 'unlocked': False, 'icon': '❄️', 'progress': 0, 'target': 100},
            'electromancer': {'name': '雷电法师', 'description': '用雷电塔连锁击杀50个敌人', 'unlocked': False, 'icon': '⚡', 'progress': 0, 'target': 50},
            'millionaire': {'name': '百万富翁', 'description': '累计获得10000金币', 'unlocked': False, 'icon': '💎', 'progress': 0, 'target': 10000},
            'undefeated': {'name': '不败神话', 'description': '完成所有关卡无伤', 'unlocked': False, 'icon': '🏆'},
            'speed_runner': {'name': '速跑者', 'description': '在5分钟内完成一关', 'unlocked': False, 'icon': '⏱️'},
            'perfectionist': {'name': '完美主义者', 'description': '在所有关卡获得三星', 'unlocked': False, 'icon': '💯'}
        }
        self.notifications = []

    def unlock_achievement(self, achievement_id):
        if achievement_id in self.achievements and not self.achievements[achievement_id]['unlocked']:
            self.achievements[achievement_id]['unlocked'] = True
            self.notifications.append(self.achievements[achievement_id])
            return True
        return False

    def update_progress(self, achievement_id, amount=1):
        if achievement_id in self.achievements:
            achievement = self.achievements[achievement_id]
            if 'progress' in achievement:
                achievement['progress'] += amount
                if achievement['progress'] >= achievement['target'] and not achievement['unlocked']:
                    return self.unlock_achievement(achievement_id)
        return False

    def get_unlocked_count(self):
        return sum(1 for a in self.achievements.values() if a['unlocked'])

    def draw_notifications(self, screen, font):
        for i, notification in enumerate(self.notifications):
            x = SCREEN_WIDTH // 2 - 150
            y = 50 + i * 100
            pygame.draw.rect(screen, (30, 30, 60), (x, y, 300, 80))
            pygame.draw.rect(screen, COLOR_GOLD, (x, y, 300, 80), 2)
            
            icon_text = font.render(notification['icon'], True, COLOR_GOLD)
            screen.blit(icon_text, (x + 20, y + 25))
            
            name_text = font.render(notification['name'], True, COLOR_WHITE)
            screen.blit(name_text, (x + 60, y + 20))
            
            desc_text = font.render(notification['description'], True, COLOR_GRAY)
            screen.blit(desc_text, (x + 60, y + 50))

    def update_notifications(self, dt):
        self.notifications = [n for n in self.notifications if self.notifications.index(n) < 3]


class GameTutorialManager:
    def __init__(self, game):
        self.game = game
        self.tutorial_enabled = True
        self.current_step = 0
        self.tutorial_steps = [
            {'text': '欢迎来到王国防线！点击地图上的绿色圆圈建造塔', 'position': (640, 400)},
            {'text': '选择塔类型后，点击建造位置放置塔', 'position': (640, 300)},
            {'text': '点击已建造的塔可以升级或出售', 'position': (640, 350)},
            {'text': '消灭所有敌人保护你的基地！', 'position': (640, 400)},
            {'text': '按空格键开始下一波敌人', 'position': (640, 300)},
            {'text': '按ESC键暂停游戏', 'position': (640, 350)}
        ]
        self.current_message = ""
        self.message_timer = 0

    def start_tutorial(self):
        self.current_step = 0
        self.show_current_message()

    def show_current_message(self):
        if self.current_step < len(self.tutorial_steps):
            self.current_message = self.tutorial_steps[self.current_step]['text']
            self.message_timer = 3.0
        else:
            self.tutorial_enabled = False
            self.current_message = ""

    def next_step(self):
        self.current_step += 1
        self.show_current_message()

    def update(self, dt):
        if self.message_timer > 0:
            self.message_timer -= dt
            if self.message_timer <= 0:
                self.next_step()

    def draw(self, screen, font):
        if self.current_message:
            text_surface = font.render(self.current_message, True, COLOR_WHITE)
            text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, 60))
            pygame.draw.rect(screen, (30, 30, 60), (text_rect.x - 10, text_rect.y - 10, text_rect.width + 20, text_rect.height + 20))
            pygame.draw.rect(screen, COLOR_GOLD, (text_rect.x - 10, text_rect.y - 10, text_rect.width + 20, text_rect.height + 20), 2)
            screen.blit(text_surface, text_rect)


class GameMiniMap:
    def __init__(self, game):
        self.game = game
        self.size = 180
        self.position = (SCREEN_WIDTH - self.size - 15, 15)
        self.visible = True

    def draw(self, screen):
        if not self.visible:
            return

        x, y = self.position
        pygame.draw.rect(screen, COLOR_DARK_GRAY, (x, y, self.size, self.size))
        pygame.draw.rect(screen, COLOR_WHITE, (x, y, self.size, self.size), 2)

        if self.game.current_level:
            scale = self.size / max(SCREEN_WIDTH, SCREEN_HEIGHT)
            
            for i in range(len(self.game.current_level.path_points) - 1):
                px = x + self.game.current_level.path_points[i][0] * scale
                py = y + self.game.current_level.path_points[i][1] * scale
                nx = x + self.game.current_level.path_points[i+1][0] * scale
                ny = y + self.game.current_level.path_points[i+1][1] * scale
                pygame.draw.line(screen, COLOR_BROWN, (px, py), (nx, ny), 2)

            for enemy in self.game.enemies:
                if enemy.alive:
                    ex = x + enemy.x * scale
                    ey = y + enemy.y * scale
                    pygame.draw.circle(screen, COLOR_RED, (int(ex), int(ey)), 3)

            for tower in self.game.towers:
                tx = x + tower.x * scale
                ty = y + tower.y * scale
                pygame.draw.circle(screen, COLOR_GREEN, (int(tx), int(ty)), 4)

            start_x = x + self.game.current_level.path_points[0][0] * scale
            start_y = y + self.game.current_level.path_points[0][1] * scale
            pygame.draw.circle(screen, COLOR_GREEN, (int(start_x), int(start_y)), 6)

            end_x = x + self.game.current_level.path_points[-1][0] * scale
            end_y = y + self.game.current_level.path_points[-1][1] * scale
            pygame.draw.circle(screen, COLOR_RED, (int(end_x), int(end_y)), 6)


class GameDebugOverlay:
    def __init__(self, game):
        self.game = game
        self.enabled = False
        self.font = pygame.font.Font(None, 16)

    def draw(self, screen):
        if not self.enabled:
            return

        y = 10
        debug_info = [
            f"FPS: {int(self.game.clock.get_fps())}",
            f"Enemies: {len(self.game.enemies)}",
            f"Towers: {len(self.game.towers)}",
            f"Projectiles: {len(self.game.projectiles)}",
            f"Gold: {self.game.gold}",
            f"Lives: {self.game.lives}",
            f"Wave: {self.game.current_wave}/{len(self.game.current_level.waves)}",
            f"Score: {self.game.score}"
        ]

        for line in debug_info:
            text = self.font.render(line, True, COLOR_WHITE)
            screen.blit(text, (10, y))
            y += 20


class GameInputHandler:
    def __init__(self, game):
        self.game = game
        self.mouse_pos = (0, 0)
        self.mouse_down = False
        self.key_buffer = []
        self.key_buffer_timeout = 0

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.mouse_pos = event.pos
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self.mouse_down = True
            self.handle_click(event.pos)
        elif event.type == pygame.MOUSEBUTTONUP:
            self.mouse_down = False
        elif event.type == pygame.KEYDOWN:
            self.key_buffer.append(event.key)
            self.key_buffer_timeout = 2.0
            if len(self.key_buffer) > 10:
                self.key_buffer.pop(0)

    def update(self, dt):
        if self.key_buffer_timeout > 0:
            self.key_buffer_timeout -= dt
            if self.key_buffer_timeout <= 0:
                self.key_buffer = []

    def handle_click(self, pos):
        if self.game.game_state == GameState.MENU:
            self.handle_menu_click(pos)
        elif self.game.game_state == GameState.LEVEL_SELECT:
            self.handle_level_select_click(pos)
        elif self.game.game_state == GameState.GAME:
            self.handle_game_click(pos)
        elif self.game.game_state == GameState.TOWER_ENCYCLOPEDIA:
            self.handle_encyclopedia_click(pos)
        elif self.game.game_state == GameState.ENEMY_ENCYCLOPEDIA:
            self.handle_encyclopedia_click(pos)

    def handle_menu_click(self, pos):
        buttons = [
            (SCREEN_WIDTH//2 - 150, 200, 300, 50, 'start'),
            (SCREEN_WIDTH//2 - 150, 280, 300, 50, 'tower_encyclopedia'),
            (SCREEN_WIDTH//2 - 150, 360, 300, 50, 'enemy_encyclopedia'),
            (SCREEN_WIDTH//2 - 150, 440, 300, 50, 'settings'),
            (SCREEN_WIDTH//2 - 150, 520, 300, 50, 'quit')
        ]
        for x, y, w, h, action in buttons:
            if x <= pos[0] <= x + w and y <= pos[1] <= y + h:
                if action == 'start':
                    self.game.game_state = GameState.LEVEL_SELECT
                elif action == 'tower_encyclopedia':
                    self.game.game_state = GameState.TOWER_ENCYCLOPEDIA
                elif action == 'enemy_encyclopedia':
                    self.game.game_state = GameState.ENEMY_ENCYCLOPEDIA
                elif action == 'settings':
                    pass
                elif action == 'quit':
                    pygame.quit()
                    sys.exit()

    def handle_level_select_click(self, pos):
        level_width = 350
        level_height = 180
        cols = 3
        rows = 2

        for i, level in enumerate(self.game.levels):
            col = i % cols
            row = i // cols
            x = 100 + col * (level_width + 50)
            y = 150 + row * (level_height + 70)
            
            if x <= pos[0] <= x + level_width and y <= pos[1] <= y + level_height:
                if level.unlocked:
                    self.game.selected_level = i
                    self.game.start_level(level)
                    return

        back_button = (SCREEN_WIDTH//2 - 100, 650, 200, 40)
        if back_button[0] <= pos[0] <= back_button[0] + back_button[2] and \
           back_button[1] <= pos[1] <= back_button[1] + back_button[3]:
            self.game.game_state = GameState.MENU

    def handle_game_click(self, pos):
        if self.game.selected_tower_type:
            self.game.place_tower(pos)
        else:
            self.game.select_tower(pos)

    def handle_encyclopedia_click(self, pos):
        back_button = (50, 50, 100, 40)
        if back_button[0] <= pos[0] <= back_button[0] + back_button[2] and \
           back_button[1] <= pos[1] <= back_button[1] + back_button[3]:
            self.game.game_state = GameState.MENU


class GameResourceManager:
    def __init__(self):
        self.images = {}
        self.sounds = {}
        self.fonts = {}

    def load_image(self, name, path):
        try:
            self.images[name] = pygame.image.load(path).convert_alpha()
            return True
        except:
            return False

    def load_sound(self, name, path):
        try:
            self.sounds[name] = pygame.mixer.Sound(path)
            return True
        except:
            return False

    def load_font(self, name, path, size):
        try:
            self.fonts[name] = pygame.font.Font(path, size)
            return True
        except:
            self.fonts[name] = pygame.font.Font(None, size)
            return False

    def get_image(self, name):
        return self.images.get(name, None)

    def get_sound(self, name):
        return self.sounds.get(name, None)

    def get_font(self, name):
        return self.fonts.get(name, None)


class GameCamera:
    def __init__(self, width, height):
        self.rect = pygame.Rect(0, 0, width, height)
        self.target_x = 0
        self.target_y = 0
        self.smooth_factor = 0.05
        self.zoom = 1.0
        self.min_zoom = 0.5
        self.max_zoom = 2.0

    def update(self):
        self.rect.x += (self.target_x - self.rect.x) * self.smooth_factor
        self.rect.y += (self.target_y - self.rect.y) * self.smooth_factor

    def set_target(self, x, y):
        self.target_x = x - self.rect.width // 2
        self.target_y = y - self.rect.height // 2

    def zoom_in(self):
        self.zoom = min(self.max_zoom, self.zoom + 0.1)

    def zoom_out(self):
        self.zoom = max(self.min_zoom, self.zoom - 0.1)

    def apply(self, pos):
        return (
            int((pos[0] - self.rect.x) * self.zoom),
            int((pos[1] - self.rect.y) * self.zoom)
        )


class GameParticleSystem:
    def __init__(self):
        self.particles = []

    def add_particle(self, x, y, color, velocity=(0, 0), lifetime=1.0, size=5, gravity=(0, 0)):
        particle = {
            'x': x,
            'y': y,
            'color': color,
            'vx': velocity[0],
            'vy': velocity[1],
            'lifetime': lifetime,
            'max_lifetime': lifetime,
            'size': size,
            'gx': gravity[0],
            'gy': gravity[1]
        }
        self.particles.append(particle)

    def add_explosion(self, x, y, color=(255, 100, 50), count=20):
        for _ in range(count):
            angle = random.uniform(0, math.pi * 2)
            speed = random.uniform(2, 6)
            self.add_particle(
                x, y,
                color,
                velocity=(math.cos(angle) * speed, math.sin(angle) * speed),
                lifetime=random.uniform(0.5, 1.0),
                size=random.uniform(2, 6)
            )

    def add_magic_circle(self, x, y, color=(150, 100, 200), count=36):
        for i in range(count):
            angle = i * math.pi * 2 / count
            self.add_particle(
                x + math.cos(angle) * 30,
                y + math.sin(angle) * 30,
                color,
                velocity=(-math.cos(angle) * 2, -math.sin(angle) * 2),
                lifetime=random.uniform(1.0, 2.0),
                size=3
            )

    def update(self, dt):
        self.particles = [p for p in self.particles if p['lifetime'] > 0]
        for particle in self.particles:
            particle['x'] += particle['vx'] * 60 * dt
            particle['y'] += particle['vy'] * 60 * dt
            particle['vx'] += particle['gx'] * 60 * dt
            particle['vy'] += particle['gy'] * 60 * dt
            particle['lifetime'] -= dt

    def draw(self, screen):
        for particle in self.particles:
            alpha = int(255 * (particle['lifetime'] / particle['max_lifetime']))
            color = (
                particle['color'][0],
                particle['color'][1],
                particle['color'][2]
            )
            pygame.draw.circle(screen, color, (int(particle['x']), int(particle['y'])), int(particle['size']))


class GameWaveManager:
    def __init__(self, game):
        self.game = game
        self.waves = []
        self.current_wave = 0
        self.wave_active = False
        self.enemy_queue = []
        self.spawn_timer = 0

    def load_waves(self, waves):
        self.waves = waves
        self.current_wave = 0

    def start_wave(self):
        if self.current_wave < len(self.waves):
            wave_data = self.waves[self.current_wave]
            self.enemy_queue = []
            for enemy_type in wave_data['enemies']:
                self.enemy_queue.append(enemy_type)
            self.spawn_timer = 0
            self.wave_active = True

    def update(self, dt):
        if not self.wave_active:
            return

        spawn_delay = self.waves[self.current_wave].get('delay', 1.0)
        
        if self.enemy_queue:
            self.spawn_timer += dt
            if self.spawn_timer >= spawn_delay:
                enemy_type = self.enemy_queue.pop(0)
                self.game.spawn_enemy(enemy_type)
                self.spawn_timer = 0
        elif not self.game.enemies:
            self.wave_complete()

    def wave_complete(self):
        self.wave_active = False
        self.current_wave += 1
        if self.current_wave >= len(self.waves):
            self.game.victory()

    def is_wave_active(self):
        return self.wave_active

    def get_wave_progress(self):
        if not self.waves:
            return 0
        return self.current_wave / len(self.waves)


class GameProjectileSystem:
    def __init__(self):
        self.projectiles = []

    def add_projectile(self, x, y, target_x, target_y, damage, speed=8, type_='arrow', splash_radius=0):
        projectile = {
            'x': x,
            'y': y,
            'target_x': target_x,
            'target_y': target_y,
            'damage': damage,
            'speed': speed,
            'type': type_,
            'splash_radius': splash_radius,
            'active': True
        }
        dx = target_x - x
        dy = target_y - y
        dist = math.hypot(dx, dy)
        if dist > 0:
            projectile['vx'] = (dx / dist) * speed
            projectile['vy'] = (dy / dist) * speed
        else:
            projectile['vx'] = 0
            projectile['vy'] = 0
        self.projectiles.append(projectile)

    def update(self, enemies):
        for projectile in self.projectiles:
            if not projectile['active']:
                continue

            projectile['x'] += projectile['vx'] * 60 * 0.05
            projectile['y'] += projectile['vy'] * 60 * 0.05

            hit = False
            for enemy in enemies:
                if enemy.alive:
                    dist = math.hypot(projectile['x'] - enemy.x, projectile['y'] - enemy.y)
                    if dist < 15:
                        enemy.take_damage(projectile['damage'])
                        hit = True
                        break

            if hit:
                projectile['active'] = False

        self.projectiles = [p for p in self.projectiles if p['active']]

    def draw(self, screen):
        for projectile in self.projectiles:
            if not projectile['active']:
                continue
            x, y = int(projectile['x']), int(projectile['y'])
            
            if projectile['type'] == 'arrow':
                pygame.draw.circle(screen, COLOR_BROWN, (x, y), 4)
            elif projectile['type'] == 'cannonball':
                pygame.draw.circle(screen, COLOR_GRAY, (x, y), 8)
            elif projectile['type'] == 'magic':
                pygame.draw.circle(screen, (150, 100, 200), (x, y), 6)
            elif projectile['type'] == 'flame':
                pygame.draw.circle(screen, COLOR_ORANGE, (x, y), 5)
            elif projectile['type'] == 'ice':
                pygame.draw.circle(screen, COLOR_LIGHT_BLUE, (x, y), 5)
            elif projectile['type'] == 'lightning':
                pygame.draw.circle(screen, COLOR_YELLOW, (x, y), 4)
            else:
                pygame.draw.circle(screen, COLOR_WHITE, (x, y), 4)


class GameUI:
    def __init__(self, game):
        self.game = game
        self.font = pygame.font.Font(None, 24)
        self.font_large = pygame.font.Font(None, 36)

    def draw_hud(self, screen):
        gold_text = self.font.render(f"金币: {self.game.gold}", True, COLOR_YELLOW)
        lives_text = self.font.render(f"生命: {self.game.lives}", True, COLOR_RED)
        score_text = self.font.render(f"得分: {self.game.score}", True, COLOR_WHITE)
        
        if self.game.current_level:
            wave_text = self.font.render(f"波次: {self.game.current_wave}/{len(self.game.current_level.waves)}", True, COLOR_GREEN)
            screen.blit(wave_text, (SCREEN_WIDTH - 200, 10))
        
        screen.blit(gold_text, (10, 10))
        screen.blit(lives_text, (10, 40))
        screen.blit(score_text, (10, 70))

    def draw_message(self, screen, message, duration=2.0):
        text_surface = self.font_large.render(message, True, COLOR_WHITE)
        text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        pygame.draw.rect(screen, (30, 30, 60), (text_rect.x - 20, text_rect.y - 20, text_rect.width + 40, text_rect.height + 40))
        pygame.draw.rect(screen, COLOR_GOLD, (text_rect.x - 20, text_rect.y - 20, text_rect.width + 40, text_rect.height + 40), 2)
        screen.blit(text_surface, text_rect)

    def draw_button(self, screen, x, y, width, height, text, color=COLOR_GRAY, hover_color=COLOR_DARK_GRAY):
        mouse_pos = pygame.mouse.get_pos()
        is_hovered = x <= mouse_pos[0] <= x + width and y <= mouse_pos[1] <= y + height
        
        button_color = hover_color if is_hovered else color
        pygame.draw.rect(screen, button_color, (x, y, width, height))
        pygame.draw.rect(screen, COLOR_WHITE, (x, y, width, height), 2)
        
        text_surface = self.font.render(text, True, COLOR_WHITE)
        text_rect = text_surface.get_rect(center=(x + width // 2, y + height // 2))
        screen.blit(text_surface, text_rect)
        
        return is_hovered


class WeatherSystem:
    def __init__(self):
        self.weather_type = "clear"
        self.intensity = 0.0
        self.transition_timer = 0.0
        self.target_weather = "clear"
        self.particles = []
        
    def set_weather(self, weather_type, duration=3.0):
        self.target_weather = weather_type
        self.transition_timer = duration
        
    def update(self, dt):
        if self.transition_timer > 0:
            self.transition_timer -= dt
            progress = 1 - self.transition_timer / 3.0
            self.intensity = progress
            self.weather_type = self.target_weather
        else:
            if self.weather_type == "clear":
                self.intensity = 1.0
            elif self.weather_type == "rain":
                self.intensity = 0.8 + math.sin(pygame.time.get_ticks() * 0.002) * 0.2
            elif self.weather_type == "snow":
                self.intensity = 0.8 + math.sin(pygame.time.get_ticks() * 0.0015) * 0.2
            elif self.weather_type == "fog":
                self.intensity = 0.6 + math.sin(pygame.time.get_ticks() * 0.001) * 0.1
        
        self.update_particles(dt)
        
    def update_particles(self, dt):
        self.particles = [p for p in self.particles if p['life'] > 0]
        
        if self.weather_type == "rain":
            if random.random() < 0.3:
                self.particles.append({
                    'x': random.randint(0, SCREEN_WIDTH),
                    'y': -10,
                    'vy': 150 + random.randint(50, 100),
                    'life': 5.0
                })
        elif self.weather_type == "snow":
            if random.random() < 0.15:
                self.particles.append({
                    'x': random.randint(0, SCREEN_WIDTH),
                    'y': -10,
                    'vy': 30 + random.randint(20, 40),
                    'vx': (random.random() - 0.5) * 20,
                    'life': 10.0
                })
        
        for p in self.particles:
            p['x'] += p.get('vx', 0) * dt
            p['y'] += p['vy'] * dt
            p['life'] -= dt
            if self.weather_type == "snow":
                p['vx'] += (random.random() - 0.5) * 0.5
        
    def draw(self, screen):
        if self.weather_type == "rain":
            for p in self.particles:
                alpha = int(150 * (p['life'] / 5.0))
                pygame.draw.line(screen, (150, 180, 200, alpha),
                               (p['x'], p['y']),
                               (p['x'], p['y'] + 15), 1)
        elif self.weather_type == "snow":
            for p in self.particles:
                alpha = int(200 * (p['life'] / 10.0))
                size = 2 + random.randint(0, 2)
                pygame.draw.circle(screen, (255, 255, 255, alpha),
                                 (int(p['x']), int(p['y'])), size)
        elif self.weather_type == "fog":
            fog_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            fog_alpha = int(80 * self.intensity)
            fog_surface.fill((150, 160, 170, fog_alpha))
            screen.blit(fog_surface, (0, 0))


class AchievementSystem:
    def __init__(self):
        self.achievements = {
            'first_blood': {'name': '初战告捷', 'desc': '击杀第一个敌人', 'unlocked': False, 'icon': '🗡️'},
            'wave_master': {'name': '波次掌控者', 'desc': '完成10个波次', 'unlocked': False, 'icon': '🌊', 'progress': 0, 'target': 10},
            'gold_rush': {'name': '淘金热', 'desc': '累计获得1000金币', 'unlocked': False, 'icon': '💰', 'progress': 0, 'target': 1000},
            'tower_collector': {'name': '塔防大师', 'desc': '建造10座塔', 'unlocked': False, 'icon': '🏰', 'progress': 0, 'target': 10},
            'perfect_defense': {'name': '完美防御', 'desc': '不让任何敌人到达终点', 'unlocked': False, 'icon': '🛡️'},
            'speed_demon': {'name': '速战速决', 'desc': '在3分钟内完成一关', 'unlocked': False, 'icon': '⚡'},
            'wealthy': {'name': '富可敌国', 'desc': '累计获得5000金币', 'unlocked': False, 'icon': '👑', 'progress': 0, 'target': 5000},
            'level_conqueror': {'name': '关卡征服者', 'desc': '通关所有关卡', 'unlocked': False, 'icon': '🏆'},
            'tower_destroyer': {'name': '塔楼克星', 'desc': '累计击杀100个敌人', 'unlocked': False, 'icon': '💀', 'progress': 0, 'target': 100},
            'elite_hunter': {'name': '精英猎手', 'desc': '击杀10个精英敌人', 'unlocked': False, 'icon': '⭐', 'progress': 0, 'target': 10},
            'boss_slayer': {'name': 'BOSS杀手', 'desc': '击杀5个BOSS', 'unlocked': False, 'icon': '👹', 'progress': 0, 'target': 5},
            'upgrade_master': {'name': '升级大师', 'desc': '将塔升级到最高级10次', 'unlocked': False, 'icon': '⬆️', 'progress': 0, 'target': 10},
            'sell_expert': {'name': '交易专家', 'desc': '卖出5座塔', 'unlocked': False, 'icon': '💰', 'progress': 0, 'target': 5},
            'chain_master': {'name': '连锁大师', 'desc': '使用连锁闪电击杀5个敌人', 'unlocked': False, 'icon': '⚡', 'progress': 0, 'target': 5},
            'splash_master': {'name': '范围大师', 'desc': '使用范围攻击击杀10个敌人', 'unlocked': False, 'icon': '💥', 'progress': 0, 'target': 10},
            'slow_master': {'name': '减速大师', 'desc': '累计减速100个敌人', 'unlocked': False, 'icon': '❄️', 'progress': 0, 'target': 100},
            'burn_master': {'name': '灼烧大师', 'desc': '累计灼烧50个敌人', 'unlocked': False, 'icon': '🔥', 'progress': 0, 'target': 50},
            'freeze_master': {'name': '冰冻大师', 'desc': '累计冰冻20个敌人', 'unlocked': False, 'icon': '🧊', 'progress': 0, 'target': 20},
            'combo_master': {'name': '连击大师', 'desc': '连续击杀10个敌人', 'unlocked': False, 'icon': '🎯', 'progress': 0, 'target': 10},
            'survivor': {'name': '幸存者', 'desc': '生命值低于10时获胜', 'unlocked': False, 'icon': '❤️'}
        }
        
    def unlock(self, achievement_id):
        if achievement_id in self.achievements:
            self.achievements[achievement_id]['unlocked'] = True
            return True
        return False
    
    def update_progress(self, achievement_id, value):
        if achievement_id in self.achievements:
            self.achievements[achievement_id]['progress'] = min(
                self.achievements[achievement_id].get('target', 0),
                self.achievements[achievement_id].get('progress', 0) + value
            )
            if self.achievements[achievement_id]['progress'] >= self.achievements[achievement_id].get('target', 0):
                self.unlock(achievement_id)
                return True
        return False
    
    def get_unlocked_count(self):
        return sum(1 for a in self.achievements.values() if a['unlocked'])
    
    def draw(self, screen, font, font_small):
        screen.fill((25, 25, 50))
        title_text = font.render("成就系统", True, COLOR_GOLD)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 50))
        screen.blit(title_text, title_rect)
        
        back_button = pygame.Rect(50, 50, 100, 40)
        pygame.draw.rect(screen, COLOR_GRAY, back_button)
        pygame.draw.rect(screen, COLOR_WHITE, back_button, 2)
        back_text = font.render("返回", True, COLOR_WHITE)
        back_rect = back_text.get_rect(center=back_button.center)
        screen.blit(back_text, back_rect)
        
        achievements_list = list(self.achievements.values())
        for i, achievement in enumerate(achievements_list):
            x = 100 + (i % 3) * 380
            y = 120 + (i // 3) * 120
            
            bg_color = (60, 60, 80) if achievement['unlocked'] else (30, 30, 45)
            border_color = COLOR_GOLD if achievement['unlocked'] else COLOR_GRAY
            
            pygame.draw.rect(screen, bg_color, (x, y, 350, 100), border_radius=10)
            pygame.draw.rect(screen, border_color, (x, y, 350, 100), 2, border_radius=10)
            
            icon_text = font.render(achievement['icon'], True, COLOR_WHITE)
            icon_rect = icon_text.get_rect(center=(x + 35, y + 50))
            screen.blit(icon_text, icon_rect)
            
            name_text = font.render(achievement['name'], True, COLOR_WHITE if achievement['unlocked'] else COLOR_GRAY)
            name_rect = name_text.get_rect(topleft=(x + 70, y + 15))
            screen.blit(name_text, name_rect)
            
            desc_text = font_small.render(achievement['desc'], True, (180, 180, 180) if achievement['unlocked'] else COLOR_DARK_GRAY)
            desc_rect = desc_text.get_rect(topleft=(x + 70, y + 45))
            screen.blit(desc_text, desc_rect)
            
            if 'progress' in achievement and achievement['target'] > 0:
                progress = achievement['progress'] / achievement['target']
                progress_bar_bg = pygame.Rect(x + 70, y + 75, 200, 12)
                pygame.draw.rect(screen, COLOR_DARK_GRAY, progress_bar_bg)
                progress_bar = pygame.Rect(x + 70, y + 75, 200 * progress, 12)
                pygame.draw.rect(screen, COLOR_GOLD, progress_bar)
                progress_text = font_small.render(f"{achievement['progress']}/{achievement['target']}", True, COLOR_WHITE)
                progress_rect = progress_text.get_rect(left=x + 280, centery=y + 81)
                screen.blit(progress_text, progress_rect)
            
            if achievement['unlocked']:
                unlocked_text = font.render("✓", True, COLOR_GREEN)
                unlocked_rect = unlocked_text.get_rect(center=(x + 320, y + 50))
                screen.blit(unlocked_text, unlocked_rect)


class TowerSkillSystem:
    def __init__(self):
        self.skills = {
            TowerType.ARCHER: {
                'name': '穿透射击',
                'desc': '箭矢穿透多个敌人',
                'cooldown': 15000,
                'duration': 5000,
                'effect': 'pierce'
            },
            TowerType.CANNON: {
                'name': '地震冲击',
                'desc': '对范围内敌人造成大量伤害',
                'cooldown': 20000,
                'radius': 150,
                'damage': 150
            },
            TowerType.ICE: {
                'name': '暴风雪',
                'desc': '冻结范围内所有敌人',
                'cooldown': 25000,
                'radius': 180,
                'duration': 3000
            },
            TowerType.LIGHTNING: {
                'name': '雷霆风暴',
                'desc': '持续释放闪电攻击敌人',
                'cooldown': 30000,
                'duration': 8000,
                'damage': 25
            },
            TowerType.MAGE: {
                'name': '陨石坠落',
                'desc': '召唤陨石砸向敌人',
                'cooldown': 35000,
                'radius': 120,
                'damage': 300,
                'burn_duration': 5000
            }
        }
        
        self.active_skills = {}
        
    def activate_skill(self, tower_type, x, y):
        if tower_type not in self.skills:
            return False
        
        skill = self.skills[tower_type]
        self.active_skills[(x, y)] = {
            'type': tower_type,
            'start_time': pygame.time.get_ticks(),
            'duration': skill.get('duration', 5000),
            **skill
        }
        return True
    
    def update(self, enemies):
        current_time = pygame.time.get_ticks()
        to_remove = []
        
        for key, skill in self.active_skills.items():
            elapsed = current_time - skill['start_time']
            
            if elapsed >= skill['duration']:
                to_remove.append(key)
                continue
            
            if skill['type'] == TowerType.LIGHTNING:
                for enemy in enemies:
                    if enemy.alive:
                        dist = math.hypot(key[0] - enemy.x, key[1] - enemy.y)
                        if dist < 150:
                            if elapsed % 200 < 50:
                                enemy.take_damage(skill['damage'])
            elif skill['type'] == TowerType.MAGE:
                if elapsed < 1000:
                    for enemy in enemies:
                        if enemy.alive:
                            dist = math.hypot(key[0] - enemy.x, key[1] - enemy.y)
                            if dist < skill['radius']:
                                enemy.take_damage(skill['damage'] // 10)
                elif elapsed < 2000:
                    for enemy in enemies:
                        if enemy.alive:
                            dist = math.hypot(key[0] - enemy.x, key[1] - enemy.y)
                            if dist < skill['radius']:
                                enemy.take_damage(skill['damage'] // 5)
                elif elapsed < 3000:
                    for enemy in enemies:
                        if enemy.alive:
                            dist = math.hypot(key[0] - enemy.x, key[1] - enemy.y)
                            if dist < skill['radius']:
                                enemy.take_damage(skill['damage'] // 2)
                                enemy.apply_burn(skill['damage'] * 0.1, skill['burn_duration'])
        
        for key in to_remove:
            del self.active_skills[key]
    
    def draw(self, screen):
        current_time = pygame.time.get_ticks()
        
        for key, skill in self.active_skills.items():
            elapsed = current_time - skill['start_time']
            progress = elapsed / skill['duration']
            
            x, y = key
            
            if skill['type'] == TowerType.ICE:
                ice_radius = int(skill['radius'] * (0.5 + progress * 0.5))
                pygame.draw.circle(screen, (100, 200, 255, int(100 * (1 - progress))), (x, y), ice_radius, 3)
                pygame.draw.circle(screen, (150, 220, 255, int(50 * (1 - progress))), (x, y), ice_radius - 10)
                
                for i in range(8):
                    spike_angle = i * 45 + current_time * 0.1
                    spike_length = ice_radius * 0.8
                    sx = x + int(spike_length * math.cos(math.radians(spike_angle)))
                    sy = y + int(spike_length * math.sin(math.radians(spike_angle)))
                    pygame.draw.line(screen, (100, 200, 255), (x, y), (sx, sy), 2)
            
            elif skill['type'] == TowerType.LIGHTNING:
                for i in range(5):
                    bolt_angle = (i * 72 + current_time * 0.2) % 360
                    bolt_length = 80 + int(40 * math.sin(current_time * 0.01 + i))
                    bx = x + int(bolt_length * math.cos(math.radians(bolt_angle)))
                    by = y + int(bolt_length * math.sin(math.radians(bolt_angle)))
                    pygame.draw.line(screen, COLOR_YELLOW, (x, y), (bx, by), 3)
                    pygame.draw.line(screen, COLOR_WHITE, (x, y), (bx, by), 1)
            
            elif skill['type'] == TowerType.MAGE:
                meteor_radius = int(skill['radius'] * (0.3 + progress * 0.7))
                pygame.draw.circle(screen, (255, 100, 50, int(150 * (1 - progress))), (x, y), meteor_radius, 2)
                pygame.draw.circle(screen, (255, 150, 100, int(80 * (1 - progress))), (x, y), meteor_radius - 15)
                
                for i in range(12):
                    spark_angle = i * 30 + current_time * 0.3
                    spark_length = meteor_radius * 1.2
                    sx = x + int(spark_length * math.cos(math.radians(spark_angle)))
                    sy = y + int(spark_length * math.sin(math.radians(spark_angle)))
                    pygame.draw.circle(screen, (255, 200, 100, int(100 * (1 - progress))), (sx, sy), 3)


class EnemyAbilitySystem:
    def __init__(self):
        self.abilities = {
            EnemyType.OGRE_MAGE: {
                'name': '火球术',
                'cooldown': 8000,
                'damage': 25,
                'range': 100
            },
            EnemyType.NECROMANCER: {
                'name': '召唤骷髅',
                'cooldown': 15000,
                'count': 3
            },
            EnemyType.DARK_KNIGHT: {
                'name': '暗影斩',
                'cooldown': 10000,
                'damage': 40,
                'range': 50
            },
            EnemyType.DEMON: {
                'name': '地狱火',
                'cooldown': 12000,
                'damage': 35,
                'radius': 80
            },
            EnemyType.DRAGON_WHELP: {
                'name': '龙息',
                'cooldown': 6000,
                'damage': 30,
                'range': 150
            },
            EnemyType.WIZNAN: {
                'name': '时空裂隙',
                'cooldown': 10000,
                'teleport_range': 150
            }
        }
        
        self.cooldowns = {}
        
    def can_use_ability(self, enemy_type, enemy_id):
        if enemy_type not in self.abilities:
            return False
        
        if enemy_id not in self.cooldowns:
            return True
        
        return pygame.time.get_ticks() >= self.cooldowns[enemy_id]
    
    def use_ability(self, enemy_type, enemy_id, x, y, enemies, towers):
        if not self.can_use_ability(enemy_type, enemy_id):
            return None
        
        ability = self.abilities[enemy_type]
        self.cooldowns[enemy_id] = pygame.time.get_ticks() + ability['cooldown']
        
        result = {'type': enemy_type, 'ability': ability['name'], 'x': x, 'y': y}
        
        if enemy_type == EnemyType.OGRE_MAGE:
            target_tower = None
            min_dist = float('inf')
            for tower in towers:
                dist = math.hypot(x - tower.x, y - tower.y)
                if dist <= ability['range'] and dist < min_dist:
                    min_dist = dist
                    target_tower = tower
            
            if target_tower:
                result['target'] = (target_tower.x, target_tower.y)
                target_tower.take_damage(ability['damage'])
        
        elif enemy_type == EnemyType.NECROMANCER:
            result['skeletons'] = []
            for i in range(ability['count']):
                skeleton_x = x + (i - 1) * 30
                skeleton_y = y + 20
                result['skeletons'].append((skeleton_x, skeleton_y))
        
        elif enemy_type == EnemyType.DARK_KNIGHT:
            result['damage'] = ability['damage']
            result['range'] = ability['range']
        
        elif enemy_type == EnemyType.DEMON:
            result['damage'] = ability['damage']
            result['radius'] = ability['radius']
            for tower in towers:
                dist = math.hypot(x - tower.x, y - tower.y)
                if dist <= ability['radius']:
                    tower.take_damage(ability['damage'] * (1 - dist / ability['radius']))
        
        elif enemy_type == EnemyType.DRAGON_WHELP:
            result['damage'] = ability['damage']
            result['range'] = ability['range']
            for tower in towers:
                dist = math.hypot(x - tower.x, y - tower.y)
                if dist <= ability['range']:
                    tower.take_damage(ability['damage'])
        
        elif enemy_type == EnemyType.WIZNAN:
            result['teleport'] = True
        
        return result


class GameEventSystem:
    def __init__(self):
        self.events = []
        self.event_queue = []
        
    def add_event(self, event_type, data, delay=0):
        self.event_queue.append({
            'type': event_type,
            'data': data,
            'delay': delay,
            'start_time': pygame.time.get_ticks()
        })
    
    def update(self):
        current_time = pygame.time.get_ticks()
        new_events = []
        
        for event in self.event_queue:
            if current_time >= event['start_time'] + event['delay']:
                self.events.append({
                    'type': event['type'],
                    'data': event['data'],
                    'time': current_time,
                    'displayed': False
                })
            else:
                new_events.append(event)
        
        self.event_queue = new_events
        self.events = [e for e in self.events if current_time - e['time'] < 5000]
    
    def draw(self, screen, font):
        for i, event in enumerate(self.events):
            if not event['displayed']:
                event['displayed'] = True
            
            elapsed = pygame.time.get_ticks() - event['time']
            alpha = max(0, 255 - int(elapsed / 5000 * 255))
            
            y = SCREEN_HEIGHT - 50 - i * 40
            bg_rect = pygame.Rect(50, y, 400, 35)
            bg_surface = pygame.Surface((400, 35), pygame.SRCALPHA)
            bg_surface.fill((25, 25, 50, alpha))
            screen.blit(bg_surface, (50, y))
            
            pygame.draw.rect(screen, (100, 100, 120, alpha), bg_rect, 2)
            
            icon = ''
            if event['type'] == 'enemy_killed':
                icon = '💀'
            elif event['type'] == 'wave_complete':
                icon = '🌊'
            elif event['type'] == 'tower_built':
                icon = '🏰'
            elif event['type'] == 'tower_upgraded':
                icon = '⬆️'
            elif event['type'] == 'achievement_unlocked':
                icon = '🏆'
            elif event['type'] == 'gold_earned':
                icon = '💰'
            elif event['type'] == 'damage_taken':
                icon = '❤️'
            
            text = f"{icon} {event['data']}"
            event_text = font.render(text, True, (255, 255, 255, alpha))
            text_rect = event_text.get_rect(center=(250, y + 17))
            screen.blit(event_text, text_rect)


class TutorialSystem:
    def __init__(self):
        self.tutorials = [
            {'id': 'welcome', 'text': '欢迎来到王国防线！', 'position': (SCREEN_WIDTH//2, SCREEN_HEIGHT//2)},
            {'id': 'tower_select', 'text': '点击下方塔图标选择要建造的塔', 'position': (SCREEN_WIDTH - 100, SCREEN_HEIGHT - 80)},
            {'id': 'tower_place', 'text': '点击地图上的绿色圆圈放置塔', 'position': (SCREEN_WIDTH//2, SCREEN_HEIGHT//2)},
            {'id': 'tower_info', 'text': '点击已建造的塔查看详情和升级', 'position': (SCREEN_WIDTH//2, SCREEN_HEIGHT//2)},
            {'id': 'wave_start', 'text': '点击开始波次按钮释放敌人', 'position': (SCREEN_WIDTH//2, SCREEN_HEIGHT - 50)},
            {'id': 'enemy_path', 'text': '敌人会沿着路径前进，阻止他们到达终点！', 'position': (SCREEN_WIDTH//2, SCREEN_HEIGHT//2)},
            {'id': 'skill_use', 'text': '塔有特殊技能，点击技能按钮使用', 'position': (SCREEN_WIDTH - 100, SCREEN_HEIGHT - 40)},
            {'id': 'gold_manage', 'text': '击杀敌人获得金币，合理管理资源！', 'position': (50, 50)}
        ]
        
        self.current_tutorial = 0
        self.active = False
        self.completed = set()
        
    def start(self):
        self.active = True
        self.current_tutorial = 0
        
    def next(self):
        if self.current_tutorial < len(self.tutorials) - 1:
            self.current_tutorial += 1
            return True
        return False
    
    def complete(self, tutorial_id):
        self.completed.add(tutorial_id)
        
    def is_completed(self, tutorial_id):
        return tutorial_id in self.completed
    
    def draw(self, screen, font):
        if not self.active:
            return
        
        tutorial = self.tutorials[self.current_tutorial]
        x, y = tutorial['position']
        
        bg_surface = pygame.Surface((400, 80), pygame.SRCALPHA)
        bg_surface.fill((25, 25, 50, 220))
        bg_rect = bg_surface.get_rect(center=(x, y))
        screen.blit(bg_surface, bg_rect)
        
        pygame.draw.rect(screen, COLOR_GOLD, bg_rect, 2)
        
        text_lines = [tutorial['text'], '', '按 ENTER 继续']
        for i, line in enumerate(text_lines):
            text = font.render(line, True, COLOR_WHITE)
            text_rect = text.get_rect(center=(x, y - 20 + i * 25))
            screen.blit(text, text_rect)


class MapDecorationSystem:
    def __init__(self):
        self.decorations = []
        
    def generate_decorations(self, theme):
        self.decorations = []
        
        if theme == LevelTheme.FOREST:
            for i in range(8):
                self.decorations.append({
                    'type': 'flower',
                    'x': 50 + i * 160,
                    'y': 400 + (i % 2) * 20,
                    'color': random.choice([(255, 100, 150), (255, 200, 100), (150, 100, 255)]),
                    'size': 3 + random.randint(0, 2)
                })
            for i in range(5):
                self.decorations.append({
                    'type': 'mushroom',
                    'x': 100 + i * 250,
                    'y': 460,
                    'height': 15 + random.randint(5, 10),
                    'color': random.choice([(255, 100, 100), (200, 100, 200), (100, 200, 100)])
                })
        
        elif theme == LevelTheme.ICE:
            for i in range(10):
                self.decorations.append({
                    'type': 'ice_crystal',
                    'x': 30 + i * 130,
                    'y': 390 + (i % 3) * 15,
                    'height': 20 + random.randint(10, 20),
                    'color': (100 + random.randint(50, 100), 200 + random.randint(0, 55), 255)
                })
        
        elif theme == LevelTheme.CASTLE:
            for i in range(6):
                self.decorations.append({
                    'type': 'torch',
                    'x': 150 + i * 200,
                    'y': 360,
                    'flame_height': 15 + random.randint(0, 10)
                })
            for i in range(4):
                self.decorations.append({
                    'type': 'banner',
                    'x': 200 + i * 350,
                    'y': 280,
                    'color': random.choice([COLOR_RED, COLOR_BLUE, COLOR_GOLD])
                })
        
        elif theme == LevelTheme.DESERT:
            for i in range(5):
                self.decorations.append({
                    'type': 'cactus',
                    'x': 100 + i * 260,
                    'y': 450,
                    'height': 30 + random.randint(10, 20)
                })
            for i in range(3):
                self.decorations.append({
                    'type': 'pyramid',
                    'x': 300 + i * 400,
                    'y': 420,
                    'size': 20 + random.randint(10, 15)
                })
        
        elif theme == LevelTheme.VOLCANO:
            for i in range(8):
                self.decorations.append({
                    'type': 'lava_pool',
                    'x': 50 + i * 160,
                    'y': 470,
                    'size': 15 + random.randint(5, 10)
                })
            for i in range(4):
                self.decorations.append({
                    'type': 'smoke_stack',
                    'x': 200 + i * 300,
                    'y': 300
                })
        
        elif theme == LevelTheme.SHADOW:
            for i in range(6):
                self.decorations.append({
                    'type': 'ghost',
                    'x': 100 + i * 220,
                    'y': 350 + (i % 2) * 30,
                    'float_offset': random.randint(0, 20)
                })
            for i in range(8):
                self.decorations.append({
                    'type': 'spider_web',
                    'x': 50 + i * 160,
                    'y': 380
                })
        
        elif theme == LevelTheme.CAVE:
            for i in range(10):
                self.decorations.append({
                    'type': 'stalagmite',
                    'x': 30 + i * 130,
                    'y': 470,
                    'height': 15 + random.randint(10, 25)
                })
            for i in range(5):
                self.decorations.append({
                    'type': 'crystal',
                    'x': 100 + i * 250,
                    'y': 450,
                    'color': random.choice([(150, 100, 255), (100, 200, 255), (255, 100, 200)]),
                    'size': 8 + random.randint(4, 8)
                })
        
        elif theme == LevelTheme.OCEAN:
            for i in range(8):
                self.decorations.append({
                    'type': 'coral',
                    'x': 50 + i * 160,
                    'y': 460,
                    'color': random.choice([(255, 100, 100), (100, 200, 200), (200, 100, 200)]),
                    'height': 20 + random.randint(10, 15)
                })
            for i in range(6):
                self.decorations.append({
                    'type': 'bubble',
                    'x': 80 + i * 200,
                    'y': 480,
                    'size': 5 + random.randint(3, 8)
                })
        
        elif theme == LevelTheme.SKY:
            for i in range(5):
                self.decorations.append({
                    'type': 'cloud',
                    'x': 100 + i * 250,
                    'y': 80 + (i % 2) * 40,
                    'size': 30 + random.randint(10, 20)
                })
            for i in range(3):
                self.decorations.append({
                    'type': 'rainbow',
                    'x': 300 + i * 400,
                    'y': 150
                })
        
        elif theme == LevelTheme.SWAMP:
            for i in range(6):
                self.decorations.append({
                    'type': 'lily_pad',
                    'x': 80 + i * 200,
                    'y': 450 + (i % 2) * 25,
                    'size': 12 + random.randint(4, 8)
                })
            for i in range(4):
                self.decorations.append({
                    'type': 'crocodile',
                    'x': 150 + i * 300,
                    'y': 470
                })
        
        elif theme == LevelTheme.JUNGLE:
            for i in range(8):
                self.decorations.append({
                    'type': 'vine',
                    'x': 50 + i * 160,
                    'y': 350,
                    'length': 80 + random.randint(40, 60)
                })
            for i in range(5):
                self.decorations.append({
                    'type': 'banana_tree',
                    'x': 150 + i * 250,
                    'y': 440
                })
        
    def draw(self, screen, anim):
        for deco in self.decorations:
            x, y = deco['x'], deco['y']
            
            if deco['type'] == 'flower':
                pygame.draw.circle(screen, deco['color'], (x, y), deco['size'])
                for i in range(5):
                    petal_angle = i * 72
                    px = x + deco['size'] * 1.5 * math.cos(math.radians(petal_angle))
                    py = y + deco['size'] * 1.5 * math.sin(math.radians(petal_angle))
                    pygame.draw.circle(screen, deco['color'], (int(px), int(py)), deco['size'] // 2)
            
            elif deco['type'] == 'mushroom':
                pygame.draw.rect(screen, (100, 80, 60), (x - 5, y - deco['height'], 10, deco['height']))
                pygame.draw.ellipse(screen, deco['color'], (x - 12, y - deco['height'] - 10, 24, 15))
            
            elif deco['type'] == 'ice_crystal':
                sparkle = int((math.sin(anim * 2 + x) + 1) * 127)
                color = (deco['color'][0], deco['color'][1], min(255, deco['color'][2] + sparkle))
                pygame.draw.polygon(screen, color, [(x, y), (x - 5, y - deco['height']), (x + 5, y)])
                pygame.draw.polygon(screen, COLOR_WHITE, [(x, y - deco['height'] + 5), (x - 2, y), (x + 2, y)])
            
            elif deco['type'] == 'torch':
                pygame.draw.rect(screen, COLOR_BROWN, (x - 3, y - 20, 6, 20))
                flame_y = y - 25 + math.sin(anim * 5) * 3
                flame_height = deco['flame_height'] + int(math.sin(anim * 8) * 3)
                pygame.draw.polygon(screen, COLOR_RED, [(x, y - 20), (x - 5, flame_y), (x + 5, y - 20)])
                pygame.draw.polygon(screen, COLOR_ORANGE, [(x, y - 20), (x - 3, flame_y + 5), (x + 3, y - 20)])
                pygame.draw.polygon(screen, COLOR_YELLOW, [(x, y - 20), (x - 1, flame_y + 10), (x + 1, y - 20)])
            
            elif deco['type'] == 'banner':
                banner_y = y + math.sin(anim * 2 + x) * 5
                pygame.draw.line(screen, COLOR_BROWN, (x, y - 30), (x, y + 40))
                pygame.draw.polygon(screen, deco['color'], [(x - 20, y), (x + 20, y), (x + 20, banner_y), (x, banner_y + 15), (x - 20, banner_y)])
            
            elif deco['type'] == 'cactus':
                pygame.draw.rect(screen, (50, 150, 50), (x - 8, y - deco['height'], 16, deco['height']))
                for i in range(3):
                    pygame.draw.rect(screen, (50, 150, 50), (x - 15, y - deco['height'] // 3 * (i + 1), 10, 8))
                    pygame.draw.rect(screen, (50, 150, 50), (x + 5, y - deco['height'] // 3 * (i + 1), 10, 8))
            
            elif deco['type'] == 'pyramid':
                pygame.draw.polygon(screen, (200, 150, 100), [(x, y - deco['size']), (x - deco['size'], y), (x + deco['size'], y)])
                pygame.draw.polygon(screen, (220, 170, 120), [(x, y - deco['size'] + 5), (x - deco['size'] + 5, y), (x + deco['size'] - 5, y)])
            
            elif deco['type'] == 'lava_pool':
                lava_glow = int((math.sin(anim * 3 + x) + 1) * 50)
                pygame.draw.circle(screen, (255, 80 + lava_glow, 0), (x, y), deco['size'])
                pygame.draw.circle(screen, (255, 150 + lava_glow, 50), (x, y), deco['size'] // 2)
            
            elif deco['type'] == 'smoke_stack':
                for i in range(3):
                    smoke_y = y - i * 15 + math.sin(anim * 0.5 + x + i) * 10
                    smoke_size = 10 + i * 5
                    pygame.draw.circle(screen, (80 + i * 20, 80 + i * 20, 80 + i * 20), (x, int(smoke_y)), smoke_size)
            
            elif deco['type'] == 'ghost':
                ghost_y = y + math.sin(anim * 1.5 + x) * deco['float_offset']
                pygame.draw.ellipse(screen, (200, 200, 220, 150), (x - 10, ghost_y, 20, 25))
                pygame.draw.circle(screen, (200, 200, 220, 150), (x, ghost_y + 10), 8)
                pygame.draw.circle(screen, COLOR_BLACK, (x - 3, ghost_y + 8), 2)
                pygame.draw.circle(screen, COLOR_BLACK, (x + 3, ghost_y + 8), 2)
            
            elif deco['type'] == 'spider_web':
                for i in range(5):
                    web_angle = i * 36
                    wx = x + 20 * math.cos(math.radians(web_angle))
                    wy = y + 20 * math.sin(math.radians(web_angle))
                    pygame.draw.line(screen, (180, 180, 180, 100), (x, y), (wx, wy), 1)
            
            elif deco['type'] == 'stalagmite':
                pygame.draw.polygon(screen, (70, 65, 60), [(x, y), (x - 6, y - deco['height']), (x + 6, y)])
                pygame.draw.polygon(screen, (90, 85, 80), [(x - 2, y), (x, y - deco['height'] + 5), (x + 2, y)])
            
            elif deco['type'] == 'crystal':
                crystal_glow = int((math.sin(anim * 2 + x) + 1) * 100)
                pygame.draw.polygon(screen, deco['color'], [(x, y - deco['size']), (x - deco['size'] // 2, y), (x, y - deco['size'] // 2), (x + deco['size'] // 2, y)])
                pygame.draw.circle(screen, (255, 255, 255, crystal_glow), (x, y - deco['size'] // 2), 2)
            
            elif deco['type'] == 'coral':
                for i in range(5):
                    branch_angle = i * 72
                    bx = x + deco['height'] * math.cos(math.radians(branch_angle)) * 0.5
                    by = y - deco['height'] * math.sin(math.radians(branch_angle)) * 0.5
                    pygame.draw.line(screen, deco['color'], (x, y), (bx, by), 3)
            
            elif deco['type'] == 'bubble':
                bubble_y = (y - anim * 30) % 100
                pygame.draw.circle(screen, (150, 200, 255, 100), (x, y - bubble_y), deco['size'])
                pygame.draw.circle(screen, (200, 230, 255, 150), (x - 2, y - bubble_y - 2), deco['size'] // 3)
            
            elif deco['type'] == 'cloud':
                pygame.draw.ellipse(screen, COLOR_WHITE, (x - deco['size'], y, deco['size'] * 1.5, deco['size'] // 2))
                pygame.draw.ellipse(screen, COLOR_WHITE, (x - deco['size'] // 2, y - deco['size'] // 4, deco['size'], deco['size'] // 2))
            
            elif deco['type'] == 'rainbow':
                for i in range(7):
                    rainbow_colors = [COLOR_RED, COLOR_ORANGE, COLOR_YELLOW, COLOR_GREEN, COLOR_BLUE, COLOR_CYAN, COLOR_PURPLE]
                    pygame.draw.arc(screen, rainbow_colors[i], (x - 50 + i * 3, y - 30, 100, 60), math.pi, 0, 2)
            
            elif deco['type'] == 'lily_pad':
                pygame.draw.circle(screen, (60, 100, 60), (x, y), deco['size'])
                pygame.draw.circle(screen, (80, 130, 80), (x, y), deco['size'] - 3)
                pygame.draw.polygon(screen, (100, 180, 100), [(x, y - deco['size'] // 2), (x - 3, y - deco['size'] // 4), (x + 3, y - deco['size'] // 4)])
            
            elif deco['type'] == 'crocodile':
                pygame.draw.ellipse(screen, (60, 80, 60), (x, y, 30, 10))
                pygame.draw.circle(screen, (60, 80, 60), (x + 28, y + 5), 5)
                pygame.draw.circle(screen, COLOR_WHITE, (x + 30, y + 3), 2)
            
            elif deco['type'] == 'vine':
                vine_length = deco['length'] + int(math.sin(anim * 2 + x) * 10)
                for i in range(10):
                    vine_x = x + int(math.sin(anim * 0.5 + i + x) * 5)
                    vine_y = y + i * vine_length // 10
                    pygame.draw.circle(screen, (40, 80, 40), (vine_x, vine_y), 3)
            
            elif deco['type'] == 'banana_tree':
                pygame.draw.rect(screen, (100, 80, 40), (x - 5, y - 40, 10, 40))
                for i in range(3):
                    banana_x = x + (i - 1) * 8
                    banana_y = y - 50 + math.sin(anim + i) * 3
                    pygame.draw.ellipse(screen, COLOR_YELLOW, (banana_x - 3, banana_y, 6, 12))


if __name__ == "__main__":
    game = Game()
    game.run()

