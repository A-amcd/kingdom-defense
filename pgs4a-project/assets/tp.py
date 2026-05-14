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
MAP_THEME_PLAIN = {
    'sky_top': (135, 206, 235), 'sky_bottom': (86, 176, 58),
    'ground': (68, 140, 46), 'ground_alt': (50, 120, 35),
    'path': (180, 140, 100), 'path_border': (140, 100, 70),
    'name': '万象平原'
}
MAP_THEME_SWAMP = {
    'sky_top': (50, 55, 60), 'sky_bottom': (40, 60, 45),
    'ground': (25, 40, 30), 'ground_alt': (35, 50, 35),
    'path': (80, 70, 60), 'path_border': (60, 50, 45),
    'name': '恶地沼泽'
}
MAP_THEME_SKY = {
    'sky_top': (135, 206, 235), 'sky_bottom': (255, 160, 122),
    'ground': (144, 238, 144), 'ground_alt': (139, 90, 43),
    'path': (160, 140, 120), 'path_border': (120, 100, 80),
    'name': '天落殷园'
}
MAP_THEME_CORRUPT = {
    'sky_top': (80, 90, 70), 'sky_bottom': (40, 35, 30),
    'ground': (60, 50, 40), 'ground_alt': (40, 35, 30),
    'path': (100, 90, 80), 'path_border': (70, 60, 50),
    'name': '污染花园'
}
MAP_THEME_APOCALYPSE = {
    'sky_top': (50, 45, 55), 'sky_bottom': (45, 40, 35),
    'ground': (55, 50, 45), 'ground_alt': (45, 40, 35),
    'path': (75, 70, 65), 'path_border': (55, 50, 45),
    'name': '终末地'
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
    SLIME = 12
    SWAMP_BAT = 13
    MUD_GIANT = 14
    SWAMP_LORD = 15
    CHERRY_SPIRIT = 16
    CLOUD_BIRD = 17
    CLOUD_DEMON = 18
    SKY_LORD = 19
    WITHERED_SPIRIT = 20
    POISON_MUSHROOM = 21
    CORRUPT_BEETLE = 22
    CORRUPT_LORD = 23
    ASH_WALKER = 24
    FUSION_PLAINS = 25
    FUSION_SWAMP = 26
    FUSION_SKY = 27
    FUSION_CORRUPT = 28
    APOCALYPSE_LORD = 29


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

        if self.type == "arrow":
            pygame.draw.line(screen, COLOR_BROWN, (x, y), (x - self.vx * 2, y - self.vy * 2), 3)
        elif self.type == "cannonball":
            pygame.draw.circle(screen, COLOR_DARK_GRAY, (x, y), 8)
            pygame.draw.circle(screen, COLOR_GRAY, (x, y), 8, 2)
        elif self.type == "magic":
            pygame.draw.circle(screen, (150, 100, 200), (x, y), 6)
            pygame.draw.circle(screen, (200, 150, 255), (x, y), 3)
        elif self.type == "flame":
            pygame.draw.circle(screen, COLOR_ORANGE, (x, y), 7)
            pygame.draw.circle(screen, COLOR_RED, (x, y), 4)
        elif self.type == "ice":
            pygame.draw.circle(screen, (100, 200, 255), (x, y), 6)
            pygame.draw.circle(screen, COLOR_WHITE, (x, y), 3)
        elif self.type == "lightning":
            pygame.draw.line(screen, COLOR_YELLOW, (x, y), (x - self.vx, y - self.vy), 3)
            pygame.draw.line(screen, COLOR_WHITE, (x, y), (x - self.vx * 0.5, y - self.vy * 0.5), 2)
        elif self.type == "slow":
            pygame.draw.circle(screen, COLOR_GRAY, (x, y), 5)
            pygame.draw.circle(screen, COLOR_WHITE, (x, y), 5, 2)
        elif self.type == "sniper":
            pygame.draw.line(screen, COLOR_WHITE, (x, y), (x - self.vx * 3, y - self.vy * 3), 2)
            pygame.draw.circle(screen, COLOR_GRAY, (x, y), 4)
        elif self.type == "archer":
            pygame.draw.line(screen, (100, 180, 255), (x, y), (x - self.vx * 2, y - self.vy * 2), 3)
            pygame.draw.circle(screen, (150, 200, 255), (x, y), 4)
        elif self.type == "cannon":
            pygame.draw.circle(screen, (200, 100, 50), (x, y), 10)
            pygame.draw.circle(screen, (255, 150, 100), (x, y), 6)
        elif self.type == "mage":
            pygame.draw.circle(screen, (180, 100, 255), (x, y), 8)
            pygame.draw.circle(screen, (200, 150, 255), (x, y), 4)
            pygame.draw.circle(screen, (220, 200, 255), (x, y), 8, 2)
        elif self.type == "ice":
            pygame.draw.circle(screen, (100, 200, 255), (x, y), 7)
            pygame.draw.circle(screen, (150, 230, 255), (x, y), 4)
            pygame.draw.circle(screen, COLOR_WHITE, (x, y), 7, 2)
        elif self.type == "lightning":
            pygame.draw.line(screen, COLOR_YELLOW, (x, y), (x - self.vx * 1.5, y - self.vy * 1.5), 3)
            pygame.draw.circle(screen, COLOR_WHITE, (x, y), 5)
        else:
            pygame.draw.circle(screen, COLOR_WHITE, (x, y), 5)


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


class CannonballProjectile(Projectile):
    def __init__(self, x, y, target_x, target_y, damage, splash_radius):
        super().__init__(x, y, target_x, target_y, damage, 'cannonball')
        self.speed = 5
        self.splash_radius = splash_radius
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
                    if dist < 20:
                        self.hit = True
                        break
        else:
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
            pygame.draw.circle(screen, (255, 100, 50), (x, y), int(self.splash_radius), 2)
            pygame.draw.circle(screen, (255, 150, 100), (x, y), int(self.splash_radius * 0.6), 1)
        else:
            pygame.draw.circle(screen, COLOR_DARK_GRAY, (x, y), 12)
            pygame.draw.circle(screen, COLOR_GRAY, (x, y), 12, 2)
            pygame.draw.circle(screen, (180, 180, 180), (x, y), 6)


class FireballProjectile(CannonballProjectile):
    def __init__(self, x, y, target_x, target_y, damage, splash_radius):
        super().__init__(x, y, target_x, target_y, damage, splash_radius)
        self.burn_damage = damage * 0.2
        self.burn_duration = 2.0

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
            pygame.draw.circle(screen, (255, 50, 0), (x, y), int(self.splash_radius), 2)
            pygame.draw.circle(screen, (255, 100, 0), (x, y), int(self.splash_radius * 0.7), 1)
            pygame.draw.circle(screen, (255, 150, 50), (x, y), int(self.splash_radius * 0.4))
        else:
            flicker = int(3 * math.sin(self.anim_timer * 10))
            pygame.draw.circle(screen, (255, 80, 0), (x, y), 10 + flicker)
            pygame.draw.circle(screen, (255, 150, 50), (x, y), 6 + flicker)
            pygame.draw.circle(screen, (255, 200, 100), (x, y), 3)


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
    PLAIN = "plain"
    SWAMP = "swamp"
    SKY = "sky"
    CORRUPT = "corrupt"
    APOCALYPSE = "apocalypse"


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

    PLAIN_PATH = [
        (50, 320), (150, 320), (150, 120), (300, 120), (300, 440),
        (600, 440), (600, 160), (800, 160), (800, 480), (1000, 480),
        (1000, 280), (1150, 280), (1150, 360), (1230, 360)
    ]
    PLAIN_TOWERS = [
        (100, 220), (225, 220), (225, 380), (375, 380), (375, 280),
        (525, 300), (525, 100), (675, 300), (675, 420), (850, 320),
        (850, 420), (975, 380), (975, 220), (1100, 200)
    ]
    PLAIN_WAVES = [
        {"enemies": [EnemyType.GOBLIN] * 6, "delay": 0.7},
        {"enemies": [EnemyType.GOBLIN] * 10 + [EnemyType.SKELETON] * 3, "delay": 0.6},
        {"enemies": [EnemyType.SKELETON] * 8 + [EnemyType.ORC] * 4, "delay": 0.6},
        {"enemies": [EnemyType.ORC] * 6 + [EnemyType.TROLL] * 2, "delay": 0.5},
        {"enemies": [EnemyType.GOBLIN] * 12 + [EnemyType.ORC] * 4 + [EnemyType.OGRE_MAGE] * 1, "delay": 0.5},
        {"enemies": [EnemyType.SKELETON] * 10 + [EnemyType.TROLL] * 3 + [EnemyType.OGRE_MAGE] * 2, "delay": 0.45},
        {"enemies": [EnemyType.TROLL] * 6 + [EnemyType.OGRE_MAGE] * 3 + [EnemyType.NECROMANCER] * 1, "delay": 0.4},
        {"enemies": [EnemyType.ORC] * 12 + [EnemyType.NECROMANCER] * 3 + [EnemyType.DARK_KNIGHT] * 2, "delay": 0.35},
        {"enemies": [EnemyType.TROLL] * 10 + [EnemyType.DARK_KNIGHT] * 3 + [EnemyType.DEMON] * 1, "delay": 0.3},
        {"enemies": [EnemyType.DEMON] * 5 + [EnemyType.DRAGON_WHELP] * 1, "delay": 0.25}
    ]

    SWAMP_PATH = [
        (50, 240), (200, 240), (200, 400), (400, 400), (400, 160),
        (640, 160), (640, 480), (880, 480), (880, 280), (1040, 280),
        (1040, 560), (1230, 560)
    ]
    SWAMP_TOWERS = [
        (125, 320), (300, 320), (300, 200), (520, 280), (520, 420),
        (760, 320), (760, 420), (960, 380), (960, 200), (1140, 420)
    ]
    SWAMP_WAVES = [
        {"enemies": [EnemyType.SLIME] * 6, "delay": 0.6},
        {"enemies": [EnemyType.SLIME] * 8 + [EnemyType.SWAMP_BAT] * 4, "delay": 0.5},
        {"enemies": [EnemyType.SWAMP_BAT] * 8 + [EnemyType.SLIME] * 6, "delay": 0.5},
        {"enemies": [EnemyType.SLIME] * 10 + [EnemyType.MUD_GIANT] * 2, "delay": 0.45},
        {"enemies": [EnemyType.SWAMP_BAT] * 12 + [EnemyType.MUD_GIANT] * 3, "delay": 0.4},
        {"enemies": [EnemyType.MUD_GIANT] * 4 + [EnemyType.OGRE_MAGE] * 2, "delay": 0.4},
        {"enemies": [EnemyType.SLIME] * 15 + [EnemyType.MUD_GIANT] * 4 + [EnemyType.OGRE_MAGE] * 2, "delay": 0.35},
        {"enemies": [EnemyType.SWAMP_BAT] * 15 + [EnemyType.MUD_GIANT] * 5 + [EnemyType.NECROMANCER] * 2, "delay": 0.35},
        {"enemies": [EnemyType.MUD_GIANT] * 6 + [EnemyType.NECROMANCER] * 3 + [EnemyType.SWAMP_LORD] * 1, "delay": 0.3},
        {"enemies": [EnemyType.SLIME] * 10 + [EnemyType.SWAMP_BAT] * 10 + [EnemyType.SWAMP_LORD] * 1, "delay": 0.25}
    ]

    SKY_PATH = [
        (50, 160), (200, 160), (200, 320), (400, 320), (400, 120),
        (600, 120), (600, 400), (800, 400), (800, 240), (1000, 240),
        (1000, 520), (1230, 520)
    ]
    SKY_TOWERS = [
        (125, 240), (300, 240), (300, 100), (500, 220), (500, 360),
        (700, 280), (700, 360), (900, 320), (900, 180), (1100, 380)
    ]
    SKY_WAVES = [
        {"enemies": [EnemyType.CHERRY_SPIRIT] * 6, "delay": 0.5},
        {"enemies": [EnemyType.CHERRY_SPIRIT] * 8 + [EnemyType.CLOUD_BIRD] * 4, "delay": 0.45},
        {"enemies": [EnemyType.CLOUD_BIRD] * 10 + [EnemyType.CHERRY_SPIRIT] * 5, "delay": 0.45},
        {"enemies": [EnemyType.CLOUD_DEMON] * 4 + [EnemyType.CHERRY_SPIRIT] * 6, "delay": 0.4},
        {"enemies": [EnemyType.CLOUD_BIRD] * 12 + [EnemyType.CLOUD_DEMON] * 4, "delay": 0.4},
        {"enemies": [EnemyType.CLOUD_DEMON] * 6 + [EnemyType.CHERRY_SPIRIT] * 8, "delay": 0.35},
        {"enemies": [EnemyType.CLOUD_BIRD] * 15 + [EnemyType.CLOUD_DEMON] * 5 + [EnemyType.CHERRY_SPIRIT] * 5, "delay": 0.35},
        {"enemies": [EnemyType.CLOUD_DEMON] * 8 + [EnemyType.NECROMANCER] * 3, "delay": 0.3},
        {"enemies": [EnemyType.CLOUD_DEMON] * 10 + [EnemyType.DARK_KNIGHT] * 3 + [EnemyType.SKY_LORD] * 1, "delay": 0.25},
        {"enemies": [EnemyType.CHERRY_SPIRIT] * 10 + [EnemyType.CLOUD_BIRD] * 10 + [EnemyType.SKY_LORD] * 1, "delay": 0.2}
    ]

    CORRUPT_PATH = [
        (50, 200), (150, 200), (150, 360), (360, 360), (360, 160),
        (520, 160), (520, 440), (760, 440), (760, 240), (920, 240),
        (920, 560), (1230, 560)
    ]
    CORRUPT_TOWERS = [
        (100, 280), (255, 280), (255, 100), (440, 260), (440, 400),
        (640, 300), (640, 400), (840, 340), (840, 180), (1060, 400)
    ]
    CORRUPT_WAVES = [
        {"enemies": [EnemyType.WITHERED_SPIRIT] * 6, "delay": 0.55},
        {"enemies": [EnemyType.WITHERED_SPIRIT] * 8 + [EnemyType.CORRUPT_BEETLE] * 4, "delay": 0.5},
        {"enemies": [EnemyType.CORRUPT_BEETLE] * 10 + [EnemyType.WITHERED_SPIRIT] * 5, "delay": 0.5},
        {"enemies": [EnemyType.POISON_MUSHROOM] * 4 + [EnemyType.WITHERED_SPIRIT] * 6, "delay": 0.45},
        {"enemies": [EnemyType.CORRUPT_BEETLE] * 12 + [EnemyType.POISON_MUSHROOM] * 4, "delay": 0.4},
        {"enemies": [EnemyType.POISON_MUSHROOM] * 6 + [EnemyType.CORRUPT_BEETLE] * 8, "delay": 0.4},
        {"enemies": [EnemyType.WITHERED_SPIRIT] * 15 + [EnemyType.POISON_MUSHROOM] * 5 + [EnemyType.CORRUPT_BEETLE] * 5, "delay": 0.35},
        {"enemies": [EnemyType.CORRUPT_BEETLE] * 15 + [EnemyType.NECROMANCER] * 3, "delay": 0.35},
        {"enemies": [EnemyType.POISON_MUSHROOM] * 8 + [EnemyType.NECROMANCER] * 4 + [EnemyType.CORRUPT_LORD] * 1, "delay": 0.3},
        {"enemies": [EnemyType.WITHERED_SPIRIT] * 10 + [EnemyType.CORRUPT_BEETLE] * 10 + [EnemyType.CORRUPT_LORD] * 1, "delay": 0.25}
    ]

    APOCALYPSE_PATH = [
        (50, 240), (200, 240), (200, 120), (400, 120), (400, 320),
        (600, 320), (600, 160), (800, 160), (800, 400), (1000, 400),
        (1000, 240), (1160, 240), (1160, 360), (1230, 360)
    ]
    APOCALYPSE_TOWERS = [
        (125, 180), (300, 180), (300, 280), (500, 240), (500, 100),
        (700, 280), (700, 100), (900, 280), (900, 460), (1080, 300),
        (1080, 420), (600, 460), (800, 460)
    ]
    APOCALYPSE_WAVES = [
        {"enemies": [EnemyType.ASH_WALKER] * 6, "delay": 0.5},
        {"enemies": [EnemyType.ASH_WALKER] * 10 + [EnemyType.FUSION_PLAINS] * 3, "delay": 0.45},
        {"enemies": [EnemyType.FUSION_PLAINS] * 6 + [EnemyType.ASH_WALKER] * 8, "delay": 0.45},
        {"enemies": [EnemyType.FUSION_SWAMP] * 4 + [EnemyType.FUSION_PLAINS] * 4, "delay": 0.4},
        {"enemies": [EnemyType.FUSION_SKY] * 6 + [EnemyType.FUSION_SWAMP] * 4, "delay": 0.4},
        {"enemies": [EnemyType.FUSION_CORRUPT] * 4 + [EnemyType.FUSION_SKY] * 6, "delay": 0.35},
        {"enemies": [EnemyType.FUSION_PLAINS] * 6 + [EnemyType.FUSION_SWAMP] * 4 + [EnemyType.FUSION_SKY] * 4, "delay": 0.35},
        {"enemies": [EnemyType.FUSION_CORRUPT] * 6 + [EnemyType.NECROMANCER] * 4, "delay": 0.3},
        {"enemies": [EnemyType.FUSION_PLAINS] * 5 + [EnemyType.FUSION_SWAMP] * 5 + [EnemyType.FUSION_SKY] * 5 + [EnemyType.FUSION_CORRUPT] * 3, "delay": 0.25},
        {"enemies": [EnemyType.FUSION_PLAINS] * 5 + [EnemyType.FUSION_SWAMP] * 5 + [EnemyType.FUSION_SKY] * 5 + [EnemyType.FUSION_CORRUPT] * 5 + [EnemyType.APOCALYPSE_LORD] * 1, "delay": 0.2}
    ]

    @staticmethod
    def get_levels():
        return [
            Level("精灵森林", LevelTheme.FOREST, LevelData.FOREST_PATH, LevelData.FOREST_TOWERS, LevelData.FOREST_WAVES, 100),
            Level("冰封峡谷", LevelTheme.ICE, LevelData.ICE_PATH, LevelData.ICE_TOWERS, LevelData.ICE_WAVES, 150),
            Level("城堡废墟", LevelTheme.CASTLE, LevelData.CASTLE_PATH, LevelData.CASTLE_TOWERS, LevelData.CASTLE_WAVES, 200),
            Level("沙漠绿洲", LevelTheme.DESERT, LevelData.DESERT_PATH, LevelData.DESERT_TOWERS, LevelData.DESERT_WAVES, 250),
            Level("火山深渊", LevelTheme.VOLCANO, LevelData.VOLCANO_PATH, LevelData.VOLCANO_TOWERS, LevelData.VOLCANO_WAVES, 300),
            Level("暗影要塞", LevelTheme.SHADOW, LevelData.SHADOW_PATH, LevelData.SHADOW_TOWERS, LevelData.SHADOW_WAVES, 500),
            Level("万象平原", LevelTheme.PLAIN, LevelData.PLAIN_PATH, LevelData.PLAIN_TOWERS, LevelData.PLAIN_WAVES, 600),
            Level("恶地沼泽", LevelTheme.SWAMP, LevelData.SWAMP_PATH, LevelData.SWAMP_TOWERS, LevelData.SWAMP_WAVES, 700),
            Level("天落殷园", LevelTheme.SKY, LevelData.SKY_PATH, LevelData.SKY_TOWERS, LevelData.SKY_WAVES, 800),
            Level("污染花园", LevelTheme.CORRUPT, LevelData.CORRUPT_PATH, LevelData.CORRUPT_TOWERS, LevelData.CORRUPT_WAVES, 900),
            Level("终末地", LevelTheme.APOCALYPSE, LevelData.APOCALYPSE_PATH, LevelData.APOCALYPSE_TOWERS, LevelData.APOCALYPSE_WAVES, 1200)
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

    def update(self, dt):
        if not self.alive:
            return

        self.anim_timer += dt

        if self.slow_timer > 0:
            self.slow_timer -= dt
            if self.slow_timer <= 0:
                self.speed = self.base_speed

        if self.burn_timer > 0:
            self.burn_timer -= dt
            self.hp -= self.burn_damage * dt
            if self.hp <= 0:
                self.alive = False

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

    def take_damage(self, damage):
        self.hp -= damage * self.damage_modifier
        if self.hp <= 0:
            self.alive = False

    def apply_slow(self, factor, duration, stackable=False):
        if stackable:
            current_factor = self.speed / self.base_speed
            new_factor = max(0.3, current_factor * factor)
            self.speed = self.base_speed * new_factor
            self.slow_timer = max(self.slow_timer, duration)
        else:
            self.speed = self.base_speed * factor
            self.slow_timer = duration

    def apply_burn(self, damage, duration):
        self.burn_damage = damage
        self.burn_timer = duration

    def freeze(self, duration):
        self.speed = 0
        self.slow_timer = duration

    def apply_magic_buff(self):
        self.has_magic_buff = True
        self.magic_buff_timer = 5.0

    def draw(self, screen, font):
        if not self.alive:
            return

        x, y = int(self.x), int(self.y)

        health_bar_width = 30
        health_bar_height = 5
        health_percent = self.hp / self.max_hp
        pygame.draw.rect(screen, COLOR_RED, (x - health_bar_width // 2, y - 20, health_bar_width, health_bar_height))
        pygame.draw.rect(screen, COLOR_GREEN, (x - health_bar_width // 2, y - 20, int(health_bar_width * health_percent), health_bar_height))

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

    def draw(self, screen, font):
        super().draw(screen, font)
        x, y = int(self.x), int(self.y)
        pygame.draw.rect(screen, (100, 180, 80), (x-10, y-10, 20, 20))
        pygame.draw.circle(screen, COLOR_GREEN, (x, y), 10)
        pygame.draw.polygon(screen, COLOR_GREEN, [(x-8, y-5), (x-3, y), (x-8, y+5)])
        self.draw_health_bar(screen, font)

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

    def draw(self, screen, font):
        super().draw(screen, font)
        x, y = int(self.x), int(self.y)
        pygame.draw.circle(screen, COLOR_GRAY, (x, y-5), 8)
        pygame.draw.line(screen, COLOR_GRAY, (x, y+3), (x, y+15), 3)
        pygame.draw.line(screen, COLOR_GRAY, (x, y+5), (x-8, y+12), 2)
        pygame.draw.line(screen, COLOR_GRAY, (x, y+5), (x+8, y+12), 2)
        self.draw_health_bar(screen, font)

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

    def draw(self, screen, font):
        super().draw(screen, font)
        x, y = int(self.x), int(self.y)
        pygame.draw.rect(screen, (80, 150, 60), (x-12, y-12, 24, 24))
        pygame.draw.circle(screen, (60, 120, 50), (x, y-3), 12)
        pygame.draw.polygon(screen, COLOR_GREEN, [(x-6, y+2), (x-2, y+8), (x-6, y+8)])
        self.draw_health_bar(screen, font)

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

    def draw(self, screen, font):
        super().draw(screen, font)
        x, y = int(self.x), int(self.y)
        bob = int(3 * math.sin(self.anim_timer * 8))
        pygame.draw.ellipse(screen, (100, 100, 150), (x-12, y-5 + bob, 24, 14))
        pygame.draw.circle(screen, (100, 100, 150), (x-8, y-8 + bob), 6)
        pygame.draw.circle(screen, COLOR_WHITE, (x-10, y-10 + bob), 2)
        self.draw_health_bar(screen, font)

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

    def draw(self, screen, font):
        super().draw(screen, font)
        x, y = int(self.x), int(self.y)
        pygame.draw.rect(screen, (120, 100, 80), (x-15, y-15, 30, 30))
        pygame.draw.circle(screen, (100, 80, 60), (x, y-5), 15)
        pygame.draw.polygon(screen, COLOR_GRAY, [(x-10, y), (x-5, y+8), (x-10, y+8)])
        pygame.draw.polygon(screen, COLOR_GRAY, [(x+10, y), (x+5, y+8), (x+10, y+8)])
        self.draw_health_bar(screen, font)

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

    def draw(self, screen, font):
        super().draw(screen, font)
        x, y = int(self.x), int(self.y)
        pygame.draw.rect(screen, (150, 80, 150), (x-14, y-14, 28, 28))
        pygame.draw.circle(screen, (130, 60, 130), (x, y-5), 14)
        pygame.draw.polygon(screen, COLOR_PURPLE, [(x, y-18), (x-4, y-6), (x+4, y-6)])
        self.draw_health_bar(screen, font)

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

    def draw(self, screen, font):
        super().draw(screen, font)
        x, y = int(self.x), int(self.y)
        pygame.draw.rect(screen, (100, 50, 120), (x-13, y-13, 26, 26))
        pygame.draw.circle(screen, COLOR_GRAY, (x, y-3), 10)
        pygame.draw.polygon(screen, COLOR_PURPLE, [(x-15, y-5), (x-5, y-15), (x+5, y-5), (x-5, y+5)])
        self.draw_health_bar(screen, font)

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

    def draw(self, screen, font):
        super().draw(screen, font)
        x, y = int(self.x), int(self.y)
        pygame.draw.rect(screen, (80, 80, 100), (x-15, y-15, 30, 30))
        pygame.draw.circle(screen, (60, 60, 80), (x, y-5), 12)
        pygame.draw.polygon(screen, COLOR_GRAY, [(x-12, y-8), (x, y-22), (x+12, y-8)])
        pygame.draw.rect(screen, COLOR_GRAY, (x-8, y+5, 16, 15))
        self.draw_health_bar(screen, font)

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

    def draw(self, screen, font):
        super().draw(screen, font)
        x, y = int(self.x), int(self.y)
        bob = int(3 * math.sin(self.anim_timer * 3))
        pygame.draw.rect(screen, (200, 80, 50), (x-16, y-16, 32, 32))
        pygame.draw.circle(screen, (180, 60, 40), (x, y-5), 14)
        pygame.draw.polygon(screen, COLOR_RED, [(x-15, y-5), (x-10, y-15), (x-5, y-5)])
        pygame.draw.polygon(screen, COLOR_RED, [(x+15, y-5), (x+10, y-15), (x+5, y-5)])
        pygame.draw.polygon(screen, COLOR_ORANGE, [(x-3, y+5 + bob), (x, y+15 + bob), (x+3, y+5 + bob)])
        self.draw_health_bar(screen, font)

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

    def draw(self, screen, font):
        super().draw(screen, font)
        x, y = int(self.x), int(self.y)
        bob = int(2 * math.sin(self.anim_timer * 4))
        pygame.draw.ellipse(screen, (180, 60, 60), (x-20, y-8 + bob, 40, 20))
        pygame.draw.circle(screen, (160, 50, 50), (x-15, y-12 + bob), 8)
        pygame.draw.polygon(screen, COLOR_ORANGE, [(x-17, y-18 + bob), (x-12, y-14 + bob), (x-17, y-10 + bob)])
        pygame.draw.polygon(screen, COLOR_RED, [(x+20, y-5 + bob), (x+28, y-8 + bob), (x+20, y-2 + bob)])
        self.draw_health_bar(screen, font)

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

    def draw(self, screen, font):
        super().draw(screen, font)
        x, y = int(self.x), int(self.y)
        mg = int(150 + 50 * math.sin(self.anim_timer * 3))
        pygame.draw.rect(screen, (80, 30, 100), (x-18, y-18, 36, 36))
        pygame.draw.circle(screen, (150, 100, 200), (x, y-8), 16)
        pygame.draw.polygon(screen, COLOR_GOLD, [(x-12, y-15), (x-8, y-28), (x-4, y-15)])
        pygame.draw.polygon(screen, COLOR_GOLD, [(x+12, y-15), (x+8, y-28), (x+4, y-15)])
        pygame.draw.circle(screen, COLOR_PURPLE, (x, y-5), 8)
        pygame.draw.circle(screen, COLOR_WHITE, (x, y-5), 4)
        self.draw_health_bar(screen, font)

    def draw_health_bar(self, screen, font):
        pass


class SwampSlime(Enemy):
    def __init__(self, x, y, path, wave_num=1):
        super().__init__(x, y, path, wave_num)
        self.max_hp = 100 + wave_num * 15
        self.hp = self.max_hp
        self.speed = 1.5
        self.base_speed = 1.5
        self.reward = 20
        self.type = "swamp_slime"

    def draw(self, screen, font):
        super().draw(screen, font)
        x, y = int(self.x), int(self.y)
        wobble = int(3 * math.sin(self.anim_timer * 5))
        pygame.draw.circle(screen, (40, 80, 60), (x, y + wobble), 12)
        pygame.draw.circle(screen, (150, 200, 100), (x-4, y-3 + wobble), 4)
        pygame.draw.circle(screen, (150, 200, 100), (x+4, y-3 + wobble), 4)
        self.draw_health_bar(screen, font)

    def draw_health_bar(self, screen, font):
        pass


class SwampBat(Enemy):
    def __init__(self, x, y, path, wave_num=1):
        super().__init__(x, y, path, wave_num)
        self.max_hp = 50 + wave_num * 8
        self.hp = self.max_hp
        self.speed = 3.0
        self.base_speed = 3.0
        self.reward = 30
        self.type = "swamp_bat"

    def draw(self, screen, font):
        super().draw(screen, font)
        x, y = int(self.x), int(self.y)
        wing_flap = int(5 * math.sin(self.anim_timer * 10))
        pygame.draw.circle(screen, (80, 70, 80), (x, y), 6)
        pygame.draw.polygon(screen, (80, 70, 80), [(x-20 + wing_flap, y), (x, y-10), (x-5, y)])
        pygame.draw.polygon(screen, (80, 70, 80), [(x+20 - wing_flap, y), (x, y-10), (x+5, y)])
        pygame.draw.circle(screen, (200, 50, 50), (x-3, y-2), 2)
        pygame.draw.circle(screen, (200, 50, 50), (x+3, y-2), 2)
        self.draw_health_bar(screen, font)

    def draw_health_bar(self, screen, font):
        pass


class MudGiant(Enemy):
    def __init__(self, x, y, path, wave_num=1):
        super().__init__(x, y, path, wave_num)
        self.max_hp = 300 + wave_num * 40
        self.hp = self.max_hp
        self.speed = 0.8
        self.base_speed = 0.8
        self.reward = 50
        self.type = "mud_giant"

    def draw(self, screen, font):
        super().draw(screen, font)
        x, y = int(self.x), int(self.y)
        pygame.draw.rect(screen, (60, 50, 45), (x-18, y-15, 36, 30))
        pygame.draw.circle(screen, (60, 50, 45), (x, y-18), 14)
        pygame.draw.circle(screen, (100, 150, 80), (x-5, y-20), 4)
        pygame.draw.circle(screen, (100, 150, 80), (x+5, y-20), 4)
        self.draw_health_bar(screen, font)

    def draw_health_bar(self, screen, font):
        pass


class SwampLord(Enemy):
    def __init__(self, x, y, path, wave_num=1):
        super().__init__(x, y, path, wave_num)
        self.max_hp = 1000 + wave_num * 100
        self.hp = self.max_hp
        self.speed = 0.5
        self.base_speed = 0.5
        self.reward = 200
        self.type = "swamp_lord"

    def draw(self, screen, font):
        super().draw(screen, font)
        x, y = int(self.x), int(self.y)
        bob = int(3 * math.sin(self.anim_timer * 2))
        pygame.draw.rect(screen, (30, 60, 40), (x-22, y-20, 44, 40))
        pygame.draw.circle(screen, (30, 60, 40), (x, y-22 + bob), 18)
        pygame.draw.circle(screen, (255, 150, 50), (x-6, y-24 + bob), 6)
        pygame.draw.circle(screen, (255, 150, 50), (x+6, y-24 + bob), 6)
        pygame.draw.polygon(screen, (40, 80, 60), [(x-15, y-25 + bob), (x-10, y-35 + bob), (x-5, y-25 + bob)])
        pygame.draw.polygon(screen, (40, 80, 60), [(x+15, y-25 + bob), (x+10, y-35 + bob), (x+5, y-25 + bob)])
        self.draw_health_bar(screen, font)

    def draw_health_bar(self, screen, font):
        pass


class CherrySpirit(Enemy):
    def __init__(self, x, y, path, wave_num=1):
        super().__init__(x, y, path, wave_num)
        self.max_hp = 80 + wave_num * 12
        self.hp = self.max_hp
        self.speed = 2.0
        self.base_speed = 2.0
        self.reward = 25
        self.type = "cherry_spirit"

    def draw(self, screen, font):
        super().draw(screen, font)
        x, y = int(self.x), int(self.y)
        float_bob = int(5 * math.sin(self.anim_timer * 3))
        pygame.draw.circle(screen, (255, 200, 220), (x, y + float_bob), 10)
        pygame.draw.circle(screen, (255, 100, 150), (x-3, y-2 + float_bob), 3)
        pygame.draw.circle(screen, (255, 100, 150), (x+3, y-2 + float_bob), 3)
        for i in range(5):
            px = x + int(12 * math.cos(math.radians(i * 72)))
            py = y + float_bob + int(12 * math.sin(math.radians(i * 72)))
            pygame.draw.circle(screen, (255, 180, 200), (px, py), 4)
        self.draw_health_bar(screen, font)

    def draw_health_bar(self, screen, font):
        pass


class CloudBird(Enemy):
    def __init__(self, x, y, path, wave_num=1):
        super().__init__(x, y, path, wave_num)
        self.max_hp = 40 + wave_num * 6
        self.hp = self.max_hp
        self.speed = 3.5
        self.base_speed = 3.5
        self.reward = 35
        self.type = "cloud_bird"

    def draw(self, screen, font):
        super().draw(screen, font)
        x, y = int(self.x), int(self.y)
        wing_flap = int(8 * math.sin(self.anim_timer * 12))
        pygame.draw.circle(screen, (180, 180, 220), (x, y), 7)
        pygame.draw.polygon(screen, (180, 180, 220), [(x-25 + wing_flap, y), (x, y-8), (x-8, y)])
        pygame.draw.polygon(screen, (180, 180, 220), [(x+25 - wing_flap, y), (x, y-8), (x+8, y)])
        pygame.draw.circle(screen, (100, 100, 180), (x-3, y-2), 2)
        pygame.draw.circle(screen, (100, 100, 180), (x+3, y-2), 2)
        self.draw_health_bar(screen, font)

    def draw_health_bar(self, screen, font):
        pass


class CloudDemon(Enemy):
    def __init__(self, x, y, path, wave_num=1):
        super().__init__(x, y, path, wave_num)
        self.max_hp = 200 + wave_num * 30
        self.hp = self.max_hp
        self.speed = 1.2
        self.base_speed = 1.2
        self.reward = 45
        self.type = "cloud_demon"

    def draw(self, screen, font):
        super().draw(screen, font)
        x, y = int(self.x), int(self.y)
        float_bob = int(4 * math.sin(self.anim_timer * 2))
        pygame.draw.circle(screen, (200, 200, 220), (x, y + float_bob), 16)
        pygame.draw.circle(screen, (80, 80, 120), (x-5, y-5 + float_bob), 5)
        pygame.draw.circle(screen, (80, 80, 120), (x+5, y-5 + float_bob), 5)
        pygame.draw.polygon(screen, (180, 180, 210), [(x-10, y+5 + float_bob), (x, y+15 + float_bob), (x+10, y+5 + float_bob)])
        self.draw_health_bar(screen, font)

    def draw_health_bar(self, screen, font):
        pass


class SkyLord(Enemy):
    def __init__(self, x, y, path, wave_num=1):
        super().__init__(x, y, path, wave_num)
        self.max_hp = 1200 + wave_num * 120
        self.hp = self.max_hp
        self.speed = 0.6
        self.base_speed = 0.6
        self.reward = 300
        self.type = "sky_lord"

    def draw(self, screen, font):
        super().draw(screen, font)
        x, y = int(self.x), int(self.y)
        float_bob = int(5 * math.sin(self.anim_timer * 1.5))
        pygame.draw.circle(screen, (150, 100, 180), (x, y + float_bob), 22)
        pygame.draw.circle(screen, (255, 200, 100), (x-7, y-5 + float_bob), 7)
        pygame.draw.circle(screen, (255, 200, 100), (x+7, y-5 + float_bob), 7)
        pygame.draw.polygon(screen, (180, 130, 200), [(x, y-25 + float_bob), (x-15, y-10 + float_bob), (x+15, y-10 + float_bob)])
        pygame.draw.polygon(screen, (180, 130, 200), [(x-20, y+5 + float_bob), (x-25, y+15 + float_bob), (x-15, y+5 + float_bob)])
        pygame.draw.polygon(screen, (180, 130, 200), [(x+20, y+5 + float_bob), (x+25, y+15 + float_bob), (x+15, y+5 + float_bob)])
        self.draw_health_bar(screen, font)

    def draw_health_bar(self, screen, font):
        pass


class WitheredSpirit(Enemy):
    def __init__(self, x, y, path, wave_num=1):
        super().__init__(x, y, path, wave_num)
        self.max_hp = 90 + wave_num * 13
        self.hp = self.max_hp
        self.speed = 1.8
        self.base_speed = 1.8
        self.reward = 30
        self.type = "withered_spirit"

    def draw(self, screen, font):
        super().draw(screen, font)
        x, y = int(self.x), int(self.y)
        float_bob = int(4 * math.sin(self.anim_timer * 2.5))
        pygame.draw.circle(screen, (120, 100, 120), (x, y + float_bob), 11)
        pygame.draw.circle(screen, (200, 80, 120), (x-4, y-3 + float_bob), 4)
        pygame.draw.circle(screen, (200, 80, 120), (x+4, y-3 + float_bob), 4)
        for i in range(6):
            angle = math.radians(i * 60)
            px = x + int(15 * math.cos(angle))
            py = y + float_bob + int(15 * math.sin(angle))
            pygame.draw.line(screen, (100, 80, 100), (x, y + float_bob), (px, py), 1)
        self.draw_health_bar(screen, font)

    def draw_health_bar(self, screen, font):
        pass


class PoisonMushroom(Enemy):
    def __init__(self, x, y, path, wave_num=1):
        super().__init__(x, y, path, wave_num)
        self.max_hp = 150 + wave_num * 20
        self.hp = self.max_hp
        self.speed = 0.3
        self.base_speed = 0.3
        self.reward = 25
        self.type = "poison_mushroom"

    def draw(self, screen, font):
        super().draw(screen, font)
        x, y = int(self.x), int(self.y)
        pygame.draw.rect(screen, (100, 80, 60), (x-6, y-5, 12, 15))
        pygame.draw.polygon(screen, (140, 80, 100), [(x, y-20), (x-15, y-5), (x+15, y-5)])
        pygame.draw.circle(screen, (80, 200, 80), (x-5, y-12), 4)
        pygame.draw.circle(screen, (80, 200, 80), (x+5, y-12), 4)
        pygame.draw.circle(screen, (80, 200, 80), (x, y-7), 3)
        self.draw_health_bar(screen, font)

    def draw_health_bar(self, screen, font):
        pass


class CorruptBeetle(Enemy):
    def __init__(self, x, y, path, wave_num=1):
        super().__init__(x, y, path, wave_num)
        self.max_hp = 60 + wave_num * 9
        self.hp = self.max_hp
        self.speed = 3.2
        self.base_speed = 3.2
        self.reward = 35
        self.type = "corrupt_beetle"

    def draw(self, screen, font):
        super().draw(screen, font)
        x, y = int(self.x), int(self.y)
        leg_move = int(3 * math.sin(self.anim_timer * 8))
        pygame.draw.ellipse(screen, (80, 70, 90), (x-10, y-6, 20, 12))
        pygame.draw.circle(screen, (80, 70, 90), (x+8, y), 6)
        pygame.draw.circle(screen, (200, 200, 80), (x+10, y-1), 3)
        pygame.draw.line(screen, (60, 50, 70), (x-8, y+3), (x-12, y+8 + leg_move), 2)
        pygame.draw.line(screen, (60, 50, 70), (x+5, y+3), (x+8, y+8 - leg_move), 2)
        self.draw_health_bar(screen, font)

    def draw_health_bar(self, screen, font):
        pass


class CorruptLord(Enemy):
    def __init__(self, x, y, path, wave_num=1):
        super().__init__(x, y, path, wave_num)
        self.max_hp = 1500 + wave_num * 150
        self.hp = self.max_hp
        self.speed = 0.5
        self.base_speed = 0.5
        self.reward = 400
        self.type = "corrupt_lord"

    def draw(self, screen, font):
        super().draw(screen, font)
        x, y = int(self.x), int(self.y)
        bob = int(3 * math.sin(self.anim_timer * 2))
        pygame.draw.rect(screen, (80, 60, 80), (x-20, y-18, 40, 36))
        pygame.draw.circle(screen, (80, 60, 80), (x, y-20 + bob), 18)
        pygame.draw.circle(screen, (150, 255, 100), (x-6, y-22 + bob), 6)
        pygame.draw.circle(screen, (150, 255, 100), (x+6, y-22 + bob), 6)
        pygame.draw.polygon(screen, (100, 80, 100), [(x-18, y-10 + bob), (x-25, y+5 + bob), (x-12, y-5 + bob)])
        pygame.draw.polygon(screen, (100, 80, 100), [(x+18, y-10 + bob), (x+25, y+5 + bob), (x+12, y-5 + bob)])
        self.draw_health_bar(screen, font)

    def draw_health_bar(self, screen, font):
        pass


class AshWalker(Enemy):
    def __init__(self, x, y, path, wave_num=1):
        super().__init__(x, y, path, wave_num)
        self.max_hp = 120 + wave_num * 18
        self.hp = self.max_hp
        self.speed = 1.5
        self.base_speed = 1.5
        self.reward = 35
        self.type = "ash_walker"

    def draw(self, screen, font):
        super().draw(screen, font)
        x, y = int(self.x), int(self.y)
        pygame.draw.rect(screen, (90, 85, 80), (x-10, y-5, 20, 25))
        pygame.draw.circle(screen, (90, 85, 80), (x, y-8), 10)
        pygame.draw.circle(screen, (255, 100, 80), (x-3, y-10), 3)
        pygame.draw.circle(screen, (255, 100, 80), (x+3, y-10), 3)
        self.draw_health_bar(screen, font)

    def draw_health_bar(self, screen, font):
        pass


class FusionPlains(Enemy):
    def __init__(self, x, y, path, wave_num=1):
        super().__init__(x, y, path, wave_num)
        self.max_hp = 200 + wave_num * 30
        self.hp = self.max_hp
        self.speed = 1.2
        self.base_speed = 1.2
        self.reward = 50
        self.type = "fusion_plains"

    def draw(self, screen, font):
        super().draw(screen, font)
        x, y = int(self.x), int(self.y)
        pygame.draw.rect(screen, (80, 150, 60), (x-14, y-12, 28, 24))
        pygame.draw.circle(screen, (80, 150, 60), (x, y-10), 12)
        pygame.draw.circle(screen, (100, 200, 100), (x-4, y-12), 4)
        pygame.draw.circle(screen, (100, 200, 100), (x+4, y-12), 4)
        pygame.draw.polygon(screen, (60, 120, 50), [(x-8, y-5), (x-4, y), (x-8, y+5)])
        self.draw_health_bar(screen, font)

    def draw_health_bar(self, screen, font):
        pass


class FusionSwamp(Enemy):
    def __init__(self, x, y, path, wave_num=1):
        super().__init__(x, y, path, wave_num)
        self.max_hp = 250 + wave_num * 35
        self.hp = self.max_hp
        self.speed = 0.8
        self.base_speed = 0.8
        self.reward = 60
        self.type = "fusion_swamp"

    def draw(self, screen, font):
        super().draw(screen, font)
        x, y = int(self.x), int(self.y)
        wobble = int(4 * math.sin(self.anim_timer * 4))
        pygame.draw.circle(screen, (40, 100, 80), (x, y + wobble), 18)
        pygame.draw.circle(screen, (150, 200, 100), (x-6, y-5 + wobble), 5)
        pygame.draw.circle(screen, (150, 200, 100), (x+6, y-5 + wobble), 5)
        self.draw_health_bar(screen, font)

    def draw_health_bar(self, screen, font):
        pass


class FusionSky(Enemy):
    def __init__(self, x, y, path, wave_num=1):
        super().__init__(x, y, path, wave_num)
        self.max_hp = 180 + wave_num * 25
        self.hp = self.max_hp
        self.speed = 2.0
        self.base_speed = 2.0
        self.reward = 55
        self.type = "fusion_sky"

    def draw(self, screen, font):
        super().draw(screen, font)
        x, y = int(self.x), int(self.y)
        float_bob = int(4 * math.sin(self.anim_timer * 3))
        pygame.draw.circle(screen, (180, 160, 200), (x, y + float_bob), 11)
        pygame.draw.circle(screen, (255, 200, 220), (x-3, y-2 + float_bob), 4)
        pygame.draw.circle(screen, (255, 200, 220), (x+3, y-2 + float_bob), 4)
        for i in range(4):
            wing_angle = math.radians(i * 90 + 45)
            wx = x + int(15 * math.cos(wing_angle))
            wy = y + float_bob + int(15 * math.sin(wing_angle))
            pygame.draw.circle(screen, (160, 140, 180), (wx, wy), 5)
        self.draw_health_bar(screen, font)

    def draw_health_bar(self, screen, font):
        pass


class FusionCorrupt(Enemy):
    def __init__(self, x, y, path, wave_num=1):
        super().__init__(x, y, path, wave_num)
        self.max_hp = 300 + wave_num * 40
        self.hp = self.max_hp
        self.speed = 0.6
        self.base_speed = 0.6
        self.reward = 70
        self.type = "fusion_corrupt"

    def draw(self, screen, font):
        super().draw(screen, font)
        x, y = int(self.x), int(self.y)
        pygame.draw.rect(screen, (100, 60, 100), (x-16, y-14, 32, 28))
        pygame.draw.circle(screen, (100, 60, 100), (x, y-12), 14)
        pygame.draw.circle(screen, (200, 100, 150), (x-5, y-14), 5)
        pygame.draw.circle(screen, (200, 100, 150), (x+5, y-14), 5)
        self.draw_health_bar(screen, font)

    def draw_health_bar(self, screen, font):
        pass


class ApocalypseLord(Enemy):
    def __init__(self, x, y, path, wave_num=1):
        super().__init__(x, y, path, wave_num)
        self.max_hp = 3000 + wave_num * 300
        self.hp = self.max_hp
        self.speed = 0.3
        self.base_speed = 0.3
        self.reward = 1000
        self.type = "apocalypse_lord"

    def draw(self, screen, font):
        super().draw(screen, font)
        x, y = int(self.x), int(self.y)
        pulse = int(5 * math.sin(self.anim_timer * 2))
        pygame.draw.rect(screen, (140, 30, 50), (x-25, y-22, 50, 44))
        pygame.draw.circle(screen, (140, 30, 50), (x, y-22 + pulse), 22)
        pygame.draw.circle(screen, (255, 200, 50), (x-8, y-24 + pulse), 8)
        pygame.draw.circle(screen, (255, 200, 50), (x+8, y-24 + pulse), 8)
        pygame.draw.polygon(screen, (160, 40, 60), [(x-25, y-5), (x-32, y+15), (x-18, y)])
        pygame.draw.polygon(screen, (160, 40, 60), [(x+25, y-5), (x+32, y+15), (x+18, y)])
        pygame.draw.polygon(screen, (180, 50, 70), [(x-5, y+15), (x, y+28), (x+5, y+15)])
        self.draw_health_bar(screen, font)

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
        elif enemy_type == EnemyType.SLIME:
            return SwampSlime(x, y, path, wave_num)
        elif enemy_type == EnemyType.SWAMP_BAT:
            return SwampBat(x, y, path, wave_num)
        elif enemy_type == EnemyType.MUD_GIANT:
            return MudGiant(x, y, path, wave_num)
        elif enemy_type == EnemyType.SWAMP_LORD:
            return SwampLord(x, y, path, wave_num)
        elif enemy_type == EnemyType.CHERRY_SPIRIT:
            return CherrySpirit(x, y, path, wave_num)
        elif enemy_type == EnemyType.CLOUD_BIRD:
            return CloudBird(x, y, path, wave_num)
        elif enemy_type == EnemyType.CLOUD_DEMON:
            return CloudDemon(x, y, path, wave_num)
        elif enemy_type == EnemyType.SKY_LORD:
            return SkyLord(x, y, path, wave_num)
        elif enemy_type == EnemyType.WITHERED_SPIRIT:
            return WitheredSpirit(x, y, path, wave_num)
        elif enemy_type == EnemyType.POISON_MUSHROOM:
            return PoisonMushroom(x, y, path, wave_num)
        elif enemy_type == EnemyType.CORRUPT_BEETLE:
            return CorruptBeetle(x, y, path, wave_num)
        elif enemy_type == EnemyType.CORRUPT_LORD:
            return CorruptLord(x, y, path, wave_num)
        elif enemy_type == EnemyType.ASH_WALKER:
            return AshWalker(x, y, path, wave_num)
        elif enemy_type == EnemyType.FUSION_PLAINS:
            return FusionPlains(x, y, path, wave_num)
        elif enemy_type == EnemyType.FUSION_SWAMP:
            return FusionSwamp(x, y, path, wave_num)
        elif enemy_type == EnemyType.FUSION_SKY:
            return FusionSky(x, y, path, wave_num)
        elif enemy_type == EnemyType.FUSION_CORRUPT:
            return FusionCorrupt(x, y, path, wave_num)
        elif enemy_type == EnemyType.APOCALYPSE_LORD:
            return ApocalypseLord(x, y, path, wave_num)
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
        
        if not self.skill_ready:
            time_since_skill = current_time_ms - self.last_skill_time
            if time_since_skill >= self.skill_cooldown:
                self.skill_ready = True
        
        self.find_target(enemies)
        
        if time_since_last_attack >= attack_interval:
            if self.target and self.target.alive:
                self.attack(enemies, current_time_ms, projectiles)
    
    def try_use_skill(self, enemies, projectiles):
        if not self.skill_ready:
            return False
        
        if hasattr(self, 'use_skill') and callable(getattr(self, 'use_skill')):
            self.use_skill(enemies, projectiles)
            self.skill_ready = False
            self.last_skill_time = pygame.time.get_ticks()
            return True
        return False

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
        self.damage = 15
        self.range = 150
        self.attack_speed = 0.8
        self.cost = 100
        self.upgrade_cost = 50
        self.color = (100, 180, 255)
        self.shape = 'triangle'
        self.skill_cooldown = 30000
        self.skill_name = "锁定射击"
        self.skill_active = False
        self.skill_charge = 0

    def update(self, enemies, current_time_ms, projectiles):
        super().update(enemies, current_time_ms, projectiles)
        
        if self.skill_active:
            self.skill_charge -= 1
            if self.skill_charge <= 0:
                self.skill_active = False

    def attack(self, enemies, current_time_ms, projectiles):
        self.last_attack_time = current_time_ms
        if self.target and self.target.alive:
            dx = self.target.x - self.x
            dy = self.target.y - self.y
            dist = math.hypot(dx, dy)
            if dist > 0:
                angle = math.atan2(dy, dx)
                
                for i in range(5):
                    spread_angle = angle + math.radians((i - 2) * 6)
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
        
        if self.skill_active:
            rr = 20 + int(5 * math.sin(self.anim_timer * 10))
            pygame.draw.circle(screen, (150, 200, 255), (x, y), rr, 2)
            pygame.draw.circle(screen, (100, 180, 255), (x, y), rr-5, 1)
        
        self.draw_health_bar(screen, font)

    def draw_health_bar(self, screen, font):
        pass
    
    def use_skill(self, enemies, projectiles, current_time_ms):
        time_since_last_skill = current_time_ms - self.last_skill_time
        if time_since_last_skill < self.skill_cooldown:
            return
        
        self.last_skill_time = current_time_ms
        self.skill_active = True
        self.skill_charge = 60
        
        target_enemies = []
        for enemy in enemies:
            if enemy.alive:
                dist = math.hypot(enemy.x - self.x, enemy.y - self.y)
                if dist <= self.range:
                    target_enemies.append(enemy)
                    if len(target_enemies) >= 3:
                        break
        
        for target in target_enemies:
            for i in range(10):
                projectile = HomingProjectile(self.x, self.y, target, self.damage * 1.5, 'arrow')
                projectiles.append(projectile)
        
        for i in range(12):
            angle = i * 30
            px = self.x + 30 * math.cos(math.radians(angle))
            py = self.y + 30 * math.sin(math.radians(angle))
            vx = math.cos(math.radians(angle)) * 2.5
            vy = math.sin(math.radians(angle)) * 2.5
            self.particles.append(Particle(px, py, vx, vy, (150, 200, 255), 4, 1.5))


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

    def update(self, enemies, current_time_ms, projectiles):
        super().update(enemies, current_time_ms, projectiles)
        
        if self.skill_active:
            self.skill_charge -= 1
            if self.skill_charge <= 0:
                self.skill_active = False

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
    
    def use_skill(self, enemies, projectiles, current_time_ms):
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
        pygame.display.set_caption("王国保卫战 - Kingdom Rush")
        
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
        self.dev_selected_tower = 0
        self.dev_selected_enemy = 0
        self.achievement_manager = AchievementManager()
        self.towers = []
        self.enemies = []
        
        self.weather_system = WeatherSystem()
        self.ambient_effects = AmbientEffects()
        self.theme_particles = []
        self.dialog_system = DialogSystem()
        self.showing_story = False
    
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
        self.levels[0].unlocked = True
        
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
            LevelTheme.PLAIN: {
                'sky_top': (135, 206, 235), 'sky_bottom': (86, 176, 58),
                'ground': (68, 140, 46), 'ground_alt': (50, 120, 35),
                'path': (180, 140, 100), 'path_border': (140, 100, 70)
            },
            LevelTheme.SWAMP: {
                'sky_top': (50, 55, 60), 'sky_bottom': (40, 60, 45),
                'ground': (25, 40, 30), 'ground_alt': (35, 50, 35),
                'path': (80, 70, 60), 'path_border': (60, 50, 45)
            },
            LevelTheme.SKY: {
                'sky_top': (135, 206, 235), 'sky_bottom': (255, 160, 122),
                'ground': (144, 238, 144), 'ground_alt': (139, 90, 43),
                'path': (160, 140, 120), 'path_border': (120, 100, 80)
            },
            LevelTheme.CORRUPT: {
                'sky_top': (80, 90, 70), 'sky_bottom': (40, 35, 30),
                'ground': (60, 50, 40), 'ground_alt': (40, 35, 30),
                'path': (100, 90, 80), 'path_border': (70, 60, 50)
            },
            LevelTheme.APOCALYPSE: {
                'sky_top': (50, 45, 55), 'sky_bottom': (45, 40, 35),
                'ground': (55, 50, 45), 'ground_alt': (45, 40, 35),
                'path': (75, 70, 65), 'path_border': (55, 50, 45)
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

        ground_color = colors['ground']
        pygame.draw.rect(self.screen, ground_color, (0, 380, SCREEN_WIDTH, 120))

        if self.current_level:
            self.draw_path(colors)
            self.draw_tower_positions()

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
        
        pygame.draw.circle(self.screen, COLOR_GREEN, (start_x, start_y), 15)
        pygame.draw.circle(self.screen, COLOR_DARK_GREEN, (start_x, start_y), 15, 3)
        
        pygame.draw.circle(self.screen, COLOR_RED, (end_x, end_y), 15)
        pygame.draw.circle(self.screen, COLOR_DARK_RED, (end_x, end_y), 15, 3)

    def draw_tower_positions(self):
        for pos in self.current_level.tower_positions:
            occupied = False
            for tower in self.towers:
                if math.hypot(tower.x - pos[0], tower.y - pos[1]) < 30:
                    occupied = True
                    break
            
            if not occupied:
                pygame.draw.circle(self.screen, COLOR_GRAY, pos, 22)
                pygame.draw.circle(self.screen, COLOR_DARK_GRAY, pos, 22, 2)
                pygame.draw.circle(self.screen, COLOR_GREEN, pos, 5)

    def init_theme_particles(self, theme):
        self.theme_particles = []
        if theme == LevelTheme.SWAMP:
            for _ in range(30):
                self.theme_particles.append({
                    'x': random.randint(0, SCREEN_WIDTH),
                    'y': random.randint(0, SCREEN_HEIGHT),
                    'vy': random.uniform(0.5, 2.0),
                    'vx': random.uniform(-0.5, 0.5),
                    'size': random.uniform(1, 3),
                    'color': (100, 120, 110),
                    'lifetime': random.uniform(2.0, 4.0),
                    'max_life': random.uniform(2.0, 4.0)
                })
        elif theme == LevelTheme.SKY:
            for _ in range(40):
                self.theme_particles.append({
                    'x': random.randint(0, SCREEN_WIDTH),
                    'y': random.randint(0, SCREEN_HEIGHT),
                    'vy': random.uniform(0.3, 0.8),
                    'vx': random.uniform(-0.3, 0.3),
                    'size': random.uniform(3, 6),
                    'color': (255, 180, 180),
                    'lifetime': random.uniform(5.0, 10.0),
                    'max_life': random.uniform(5.0, 10.0)
                })
        elif theme == LevelTheme.CORRUPT:
            for _ in range(25):
                self.theme_particles.append({
                    'x': random.randint(0, SCREEN_WIDTH),
                    'y': random.randint(0, SCREEN_HEIGHT),
                    'vy': random.uniform(-0.5, 0.5),
                    'vx': random.uniform(-0.3, 0.3),
                    'size': random.uniform(4, 8),
                    'color': (80, 120, 60),
                    'lifetime': random.uniform(3.0, 6.0),
                    'max_life': random.uniform(3.0, 6.0)
                })
        elif theme == LevelTheme.APOCALYPSE:
            for _ in range(35):
                self.theme_particles.append({
                    'x': random.randint(0, SCREEN_WIDTH),
                    'y': random.randint(0, SCREEN_HEIGHT),
                    'vy': random.uniform(-1.0, 0.5),
                    'vx': random.uniform(-0.5, 0.5),
                    'size': random.uniform(1, 3),
                    'color': (60, 55, 55),
                    'lifetime': random.uniform(2.0, 5.0),
                    'max_life': random.uniform(2.0, 5.0)
                })

    def update_theme_particles(self, dt):
        for p in list(self.theme_particles):
            p['x'] += p['vx']
            p['y'] += p['vy']
            p['lifetime'] -= dt
            
            if p['lifetime'] <= 0 or p['y'] > SCREEN_HEIGHT or p['y'] < -10:
                self.theme_particles.remove(p)
                continue
            
            if self.current_level and self.current_level.theme == LevelTheme.SWAMP:
                p['vx'] += random.uniform(-0.1, 0.1)
                p['vx'] = max(-1.0, min(1.0, p['vx']))
            elif self.current_level and self.current_level.theme == LevelTheme.SKY:
                p['vy'] += random.uniform(-0.05, 0.1)
                p['vx'] += random.uniform(-0.1, 0.1)

    def draw_theme_particles(self):
        for p in self.theme_particles:
            alpha = int(255 * (p['lifetime'] / p['max_life']))
            color = (p['color'][0], p['color'][1], p['color'][2])
            pygame.draw.circle(self.screen, color, (int(p['x']), int(p['y'])), int(p['size']))

    def set_level_weather(self, theme):
        if theme == LevelTheme.SWAMP:
            self.weather_system.set_weather("rain", 0.7)
        elif theme == LevelTheme.ICE:
            self.weather_system.set_weather("snow", 0.5)
        elif theme == LevelTheme.CORRUPT:
            self.weather_system.set_weather("fog", 0.4)
        else:
            self.weather_system.set_weather("clear")

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
        
        title_text = self.font_title.render("王国保卫战", True, COLOR_GOLD)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 150 + self.title_bob_offset))
        
        title_glow = pygame.Surface((title_rect.width + 20, title_rect.height + 20), pygame.SRCALPHA)
        pygame.draw.rect(title_glow, (255, 215, 0, 50), (0, 0, title_rect.width + 20, title_rect.height + 20), border_radius=10)
        self.screen.blit(title_glow, (title_rect.x - 10, title_rect.y - 10))
        
        self.screen.blit(title_text, title_rect)
        
        subtitle_text = self.font_large.render("Kingdom Rush", True, (200, 200, 255))
        subtitle_rect = subtitle_text.get_rect(center=(SCREEN_WIDTH // 2, 220 + self.title_bob_offset * 0.5))
        self.screen.blit(subtitle_text, subtitle_rect)
        
        buttons = [
            {"text": "开始游戏", "action": "level_select", "y": 300},
            {"text": "塔图鉴", "action": "tower_encyclopedia", "y": 360},
            {"text": "敌人图鉴", "action": "enemy_encyclopedia", "y": 420},
            {"text": "成就系统", "action": "achievements", "y": 480},
            {"text": "开发者模式", "action": "developer_mode", "y": 540},
            {"text": "退出游戏", "action": "quit", "y": 600}
        ]

        for btn in buttons:
            button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 120, btn["y"], 240, 50)
            is_hovered = button_rect.collidepoint(mouse_pos)
            
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
            
            scaled_rect = pygame.Rect(
                button_rect.x + (button_rect.width * (1 - scale)) / 2,
                button_rect.y + offset_y + (button_rect.height * (1 - scale)) / 2,
                button_rect.width * scale,
                button_rect.height * scale
            )
            
            pygame.draw.rect(self.screen, color, scaled_rect, border_radius=8)
            pygame.draw.rect(self.screen, border_color, scaled_rect, 3, border_radius=8)
            
            if is_hovered:
                glow_surface = pygame.Surface((scaled_rect.width, scaled_rect.height), pygame.SRCALPHA)
                pygame.draw.rect(glow_surface, (255, 215, 0, 30), glow_surface.get_rect(), border_radius=8)
                self.screen.blit(glow_surface, scaled_rect.topleft)
            
            text = self.font.render(btn["text"], True, text_color)
            text_rect = text.get_rect(center=scaled_rect.center)
            self.screen.blit(text, text_rect)
            
            if self.developer_mode:
                dev_text = self.font.render("✅ 开发者模式已开启", True, COLOR_GREEN)
                dev_rect = dev_text.get_rect(bottomright=(SCREEN_WIDTH - 20, SCREEN_HEIGHT - 20))
                self.screen.blit(dev_text, dev_rect)

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
            x = 80 + (i % 4) * 220
            y = 120 + (i // 4) * 180
            
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
        
        elif theme == LevelTheme.PLAIN:
            pygame.draw.rect(self.screen, (86, 176, 58), (x, y, 200, 150))
            for i in range(6):
                flower_x = x + 20 + i * 35
                flower_y = y + 120 + (i % 2) * 15
                pygame.draw.circle(self.screen, (255, 200, 200), (flower_x, flower_y), 8)
                pygame.draw.circle(self.screen, (255, 150, 150), (flower_x, flower_y), 4)
            for i in range(3):
                tree_x = x + 60 + i * 50
                pygame.draw.polygon(self.screen, (34, 139, 34), [(tree_x - 10, y + 150), (tree_x, y + 100), (tree_x + 10, y + 150)])
                pygame.draw.rect(self.screen, (139, 90, 43), (tree_x - 3, y + 135, 6, 15))
            sun_glow = int((math.sin(self.animation_timer + index) + 1) * 10)
            pygame.draw.circle(self.screen, (255, 200 + sun_glow, 100), (x + 170, y + 30), 20)
        
        elif theme == LevelTheme.SWAMP:
            pygame.draw.rect(self.screen, (40, 60, 45), (x, y, 200, 150))
            for i in range(5):
                bubble_x = x + 25 + i * 35
                bubble_y = y + 100 + (i % 2) * 20 + math.sin(self.animation_timer * 1.5 + i) * 8
                pygame.draw.circle(self.screen, (80, 120, 80), (bubble_x, bubble_y), 6)
                pygame.draw.circle(self.screen, (100, 140, 100), (bubble_x - 2, bubble_y - 2), 2)
            for i in range(3):
                reed_x = x + 40 + i * 50
                pygame.draw.line(self.screen, (20, 50, 30), (reed_x, y + 150), (reed_x, y + 90))
                pygame.draw.polygon(self.screen, (30, 70, 40), [(reed_x - 8, y + 90), (reed_x, y + 75), (reed_x + 8, y + 90)])
            for i in range(8):
                rain_y = (y + 20 + i * 18 + self.animation_timer * 5) % 150
                pygame.draw.line(self.screen, (100, 120, 110), (x + 10 + (i % 4) * 50, rain_y), (x + 15 + (i % 4) * 50, rain_y + 10))
        
        elif theme == LevelTheme.SKY:
            pygame.draw.rect(self.screen, (135, 206, 235), (x, y, 200, 150))
            for i in range(4):
                cloud_x = x + 25 + i * 45
                cloud_y = y + 35 + (i % 2) * 15 + math.sin(self.animation_timer * 0.3 + i) * 5
                pygame.draw.ellipse(self.screen, (255, 255, 255), (cloud_x, cloud_y, 30, 15))
                pygame.draw.ellipse(self.screen, (255, 255, 255), (cloud_x + 10, cloud_y - 5, 20, 12))
            for i in range(10):
                petal_x = x + 20 + (i * 17) % 160
                petal_y = (y + 60 + i * 12 + self.animation_timer * 0.8) % 150
                pygame.draw.circle(self.screen, (255, 180, 180), (petal_x, petal_y), 3)
            pygame.draw.polygon(self.screen, (144, 238, 144), [(x + 100, y + 150), (x + 70, y + 120), (x + 130, y + 120)])
        
        elif theme == LevelTheme.CORRUPT:
            pygame.draw.rect(self.screen, (60, 50, 40), (x, y, 200, 150))
            for i in range(6):
                poison_x = x + 20 + i * 30
                poison_y = y + 110 + (i % 2) * 15 + math.sin(self.animation_timer * 2 + i) * 10
                pygame.draw.circle(self.screen, (80, 120, 60), (poison_x, poison_y), 10)
                pygame.draw.circle(self.screen, (100, 150, 80), (poison_x - 3, poison_y - 3), 4)
            for i in range(4):
                mushroom_x = x + 40 + i * 45
                pygame.draw.polygon(self.screen, (120, 80, 100), [(mushroom_x - 8, y + 150), (mushroom_x + 8, y + 150), (mushroom_x, y + 130)])
                pygame.draw.ellipse(self.screen, (150, 60, 100), (mushroom_x - 10, y + 115, 20, 20))
                pygame.draw.circle(self.screen, (80, 40, 60), (mushroom_x, y + 125), 5)
        
        elif theme == LevelTheme.APOCALYPSE:
            pygame.draw.rect(self.screen, (45, 40, 35), (x, y, 200, 150))
            for i in range(5):
                ruin_x = x + 30 + i * 35
                pygame.draw.rect(self.screen, (55, 50, 45), (ruin_x - 5, y + 120, 10, 30))
                if i % 2 == 0:
                    pygame.draw.polygon(self.screen, (60, 55, 50), [(ruin_x - 8, y + 120), (ruin_x + 8, y + 120), (ruin_x, y + 105)])
            for i in range(8):
                ash_x = x + 15 + i * 22
                ash_y = (y + 20 + i * 15 + self.animation_timer * 2) % 150
                pygame.draw.circle(self.screen, (60, 55, 55), (ash_x, ash_y), 2)
            smoke_y = y + 40 + math.sin(self.animation_timer * 0.5 + index) * 15
            pygame.draw.circle(self.screen, (50, 45, 45), (x + 160, smoke_y), 12)
            pygame.draw.circle(self.screen, (60, 55, 55), (x + 165, smoke_y + 8), 8)
    
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
        
        elif theme == LevelTheme.PLAIN:
            pygame.draw.rect(self.screen, (43, 88, 29), (x, y, 200, 150))
            for i in range(4):
                flower_x = x + 30 + i * 40
                pygame.draw.circle(self.screen, (128, 100, 100), (flower_x, y + 125), 6)
        
        elif theme == LevelTheme.SWAMP:
            pygame.draw.rect(self.screen, (20, 30, 25), (x, y, 200, 150))
            for i in range(4):
                bubble_x = x + 30 + i * 40
                pygame.draw.circle(self.screen, (40, 60, 40), (bubble_x, y + 110), 5)
        
        elif theme == LevelTheme.SKY:
            pygame.draw.rect(self.screen, (68, 103, 118), (x, y, 200, 150))
            for i in range(3):
                cloud_x = x + 30 + i * 50
                pygame.draw.ellipse(self.screen, (100, 120, 130), (cloud_x, y + 40, 25, 12))
        
        elif theme == LevelTheme.CORRUPT:
            pygame.draw.rect(self.screen, (30, 25, 20), (x, y, 200, 150))
            for i in range(4):
                poison_x = x + 30 + i * 40
                pygame.draw.circle(self.screen, (40, 60, 30), (poison_x, y + 115), 8)
        
        elif theme == LevelTheme.APOCALYPSE:
            pygame.draw.rect(self.screen, (25, 22, 20), (x, y, 200, 150))
            for i in range(4):
                ruin_x = x + 35 + i * 35
                pygame.draw.rect(self.screen, (30, 28, 25), (ruin_x - 4, y + 125, 8, 25))
    
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
        
        title_text = self.font.render("🛠️ 开发者面板", True, COLOR_GOLD)
        title_rect = title_text.get_rect(center=(panel_x + panel_width // 2, panel_y + 25))
        self.screen.blit(title_text, title_rect)
        
        close_button = pygame.Rect(panel_x + panel_width - 35, panel_y + 8, 27, 27)
        pygame.draw.rect(self.screen, COLOR_RED, close_button, border_radius=6)
        close_text = self.font_small.render("✕", True, COLOR_WHITE)
        close_rect = close_text.get_rect(center=close_button.center)
        self.screen.blit(close_text, close_rect)
        
        tabs = ["塔数据", "敌人数据", "游戏控制"]
        tab_width = 115
        tab_height = 32
        tab_y = panel_y + 50
        
        for i, tab in enumerate(tabs):
            tab_x = panel_x + 5 + i * tab_width
            tab_rect = pygame.Rect(tab_x, tab_y, tab_width - 3, tab_height)
            
            if self.dev_selected_tab == i:
                pygame.draw.rect(self.screen, COLOR_GOLD, tab_rect, border_radius=6)
                text_color = COLOR_BLACK
            else:
                pygame.draw.rect(self.screen, COLOR_DARK_GRAY, tab_rect, border_radius=6)
                text_color = COLOR_WHITE
            
            tab_text = self.font_small.render(tab, True, text_color)
            tab_text_rect = tab_text.get_rect(center=tab_rect.center)
            self.screen.blit(tab_text, tab_text_rect)
        
        content_y = panel_y + 95
        
        if self.dev_selected_tab == 0:
            self.draw_dev_tower_panel(panel_x, panel_width, content_y)
        elif self.dev_selected_tab == 1:
            self.draw_dev_enemy_panel(panel_x, panel_width, content_y)
        elif self.dev_selected_tab == 2:
            self.draw_dev_game_panel(panel_x, panel_width, content_y)
    
    def draw_dev_tower_panel(self, panel_x, panel_width, content_y):
        tower_types = ["箭塔", "炮塔", "魔法塔", "减速塔", "狙击塔", "奥术塔", "火焰塔", "冰霜塔"]
        tower_params = [
            {"damage": 15, "range": 150, "attack_speed": 1.5, "cost": 100},
            {"damage": 40, "range": 100, "attack_speed": 0.8, "cost": 150},
            {"damage": 25, "range": 120, "attack_speed": 1.2, "cost": 120},
            {"damage": 10, "range": 130, "attack_speed": 2.0, "cost": 80},
            {"damage": 60, "range": 200, "attack_speed": 0.5, "cost": 200},
            {"damage": 35, "range": 140, "attack_speed": 1.0, "cost": 180},
            {"damage": 30, "range": 120, "attack_speed": 1.3, "cost": 160},
            {"damage": 18, "range": 130, "attack_speed": 1.8, "cost": 140}
        ]
        
        item_width = panel_width - 20
        item_height = 65
        gap = 8
        y = content_y
        
        for i, (name, params) in enumerate(zip(tower_types, tower_params)):
            item_rect = pygame.Rect(panel_x + 10, y, item_width, item_height)
            
            if self.dev_selected_tower == i:
                pygame.draw.rect(self.screen, COLOR_GOLD, item_rect, border_radius=6)
                text_color = COLOR_BLACK
                bg_color = COLOR_GOLD
            else:
                pygame.draw.rect(self.screen, COLOR_DARK_GRAY, item_rect, border_radius=6)
                text_color = COLOR_WHITE
                bg_color = COLOR_DARK_GRAY
            
            name_text = self.font.render(name, True, text_color)
            self.screen.blit(name_text, (panel_x + 18, y + 10))
            
            params_text = self.font_small.render(
                f"伤害: {params['damage']} | 范围: {params['range']} | 攻速: {params['attack_speed']} | 成本: {params['cost']}",
                True, text_color
            )
            self.screen.blit(params_text, (panel_x + 18, y + 38))
            
            y += item_height + gap
            if y > SCREEN_HEIGHT - 30:
                break
    
    def draw_dev_enemy_panel(self, panel_x, panel_width, content_y):
        enemy_types = ["哥布林", "兽人", "骷髅", "暗影狼", "巨魔", "石像鬼", "死亡骑士", "恶魔"]
        enemy_params = [
            {"health": 80, "speed": 2, "reward": 10, "damage": 1},
            {"health": 150, "speed": 1.5, "reward": 20, "damage": 2},
            {"health": 60, "speed": 2.5, "reward": 8, "damage": 1},
            {"health": 100, "speed": 3, "reward": 15, "damage": 2},
            {"health": 300, "speed": 1, "reward": 40, "damage": 3},
            {"health": 200, "speed": 1.8, "reward": 30, "damage": 2},
            {"health": 400, "speed": 1.2, "reward": 60, "damage": 4},
            {"health": 500, "speed": 1.5, "reward": 80, "damage": 5}
        ]
        
        item_width = panel_width - 20
        item_height = 65
        gap = 8
        y = content_y
        
        for i, (name, params) in enumerate(zip(enemy_types, enemy_params)):
            item_rect = pygame.Rect(panel_x + 10, y, item_width, item_height)
            
            if self.dev_selected_enemy == i:
                pygame.draw.rect(self.screen, COLOR_GOLD, item_rect, border_radius=6)
                text_color = COLOR_BLACK
            else:
                pygame.draw.rect(self.screen, COLOR_DARK_GRAY, item_rect, border_radius=6)
                text_color = COLOR_WHITE
            
            name_text = self.font.render(name, True, text_color)
            self.screen.blit(name_text, (panel_x + 18, y + 10))
            
            params_text = self.font_small.render(
                f"生命: {params['health']} | 速度: {params['speed']} | 奖励: {params['reward']} | 伤害: {params['damage']}",
                True, text_color
            )
            self.screen.blit(params_text, (panel_x + 18, y + 38))
            
            y += item_height + gap
            if y > SCREEN_HEIGHT - 30:
                break
    
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
        
        tab_width = 115
        tab_height = 32
        tab_y = panel_y + 50
        
        for i in range(3):
            tab_x = panel_x + 5 + i * tab_width
            tab_rect = pygame.Rect(tab_x, tab_y, tab_width - 3, tab_height)
            if tab_rect.collidepoint(pos):
                self.dev_selected_tab = i
                return
        
        content_y = panel_y + 95
        
        if self.dev_selected_tab == 0:
            item_width = panel_width - 20
            item_height = 65
            gap = 8
            y = content_y
            
            for i in range(8):
                item_rect = pygame.Rect(panel_x + 10, y, item_width, item_height)
                if item_rect.collidepoint(pos):
                    self.dev_selected_tower = i
                    break
                y += item_height + gap
        
        elif self.dev_selected_tab == 1:
            item_width = panel_width - 20
            item_height = 65
            gap = 8
            y = content_y
            
            for i in range(8):
                item_rect = pygame.Rect(panel_x + 10, y, item_width, item_height)
                if item_rect.collidepoint(pos):
                    self.dev_selected_enemy = i
                    break
                y += item_height + gap
        
        elif self.dev_selected_tab == 2:
            button_width = panel_width - 20
            button_height = 48
            gap = 10
            y = content_y
            
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
        wave_bar_bg_x = SCREEN_WIDTH - 20 - wave_bar_bg_width
        wave_bar_bg_y = 42
        
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
            fill_surface.fill((255, 215, 0))
            fill_surface.set_alpha(255)
            self.screen.blit(fill_surface, (wave_bar_x, wave_bar_y))
            
            highlight_surface = pygame.Surface((fill_width, wave_bar_height // 2))
            highlight_surface.fill((255, 255, 220))
            highlight_surface.set_alpha(100)
            self.screen.blit(highlight_surface, (wave_bar_x, wave_bar_y))
        
        wave_text = self.font.render(f"波次 {self.wave_index + 1}/{total_waves}", True, (255, 215, 0))
        wave_text_rect = wave_text.get_rect(centerx=wave_bar_bg_x + wave_bar_bg_width // 2, top=wave_bar_bg_y + 3)
        self.screen.blit(wave_text, wave_text_rect)
        
        enemy_bg_y = wave_bar_bg_y + wave_bar_bg_height + 5
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
                    self.developer_mode = not self.developer_mode
                    if self.developer_mode:
                        for level in self.levels:
                            level.unlocked = True
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
            
            if pygame.Rect(x, y, 200, 150).collidepoint(pos) and level.unlocked:
                self.selected_level = i
                self.start_level(level)
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
                if btn["action"] == "next_level":
                    next_index = self.selected_level + 1
                    if next_index < len(self.levels):
                        self.levels[self.selected_level].completed = True
                        self.levels[self.selected_level].high_score = max(self.levels[self.selected_level].high_score, self.score)
                        self.levels[next_index].unlocked = True
                        self.selected_level = next_index
                        self.start_level(self.levels[next_index])
                    else:
                        self.game_state = GameState.MENU
                elif btn["action"] == "menu":
                    self.levels[self.selected_level].completed = True
                    self.levels[self.selected_level].high_score = max(self.levels[self.selected_level].high_score, self.score)
                    self.game_state = GameState.MENU
                return

    def start_level(self, level):
        self.current_level = level
        self.gold = 150
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
        
        self.current_wave_total_enemies = 0
        self.current_wave_killed_enemies = 0
        
        self.init_theme_particles(level.theme)
        self.set_level_weather(level.theme)
        
        self.showing_story = True
        story = StoryData.get_story(level.theme)
        self.dialog_system.load_story(story)

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
        
        if not self.spawn_queue and not self.wave_in_progress:
            if not self.enemies:
                self.wave_index += 1
                if self.wave_index >= len(self.current_level.waves):
                    self.game_state = GameState.VICTORY

        self.particles.update(dt)
        self.weather_system.update(dt)
        self.update_theme_particles(dt)
        
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
    
    def check_enemy_attack_tower(self, enemy):
        attack_range = getattr(enemy, 'attack_range', 100)
        for tower in self.towers:
            dist = math.hypot(enemy.x - tower.x, enemy.y - tower.y)
            if dist <= attack_range:
                tower.take_damage(5)
                break

    def draw_game(self):
        self.draw_background(self.current_level.theme)
        
        self.draw_theme_particles()
        self.weather_system.draw(self.screen)
        
        if not self.showing_story:
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
        else:
            dialog_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            dialog_surface.fill((0, 0, 0, 150))
            self.screen.blit(dialog_surface, (0, 0))
        
        if self.showing_story:
            self.dialog_system.draw(self.screen)

    def run(self):
        running = True
        while running:
            dt = self.clock.tick(60) / 1000
            
            self.animation_timer += dt
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_F1 and self.developer_mode:
                        self.dev_panel_active = not self.dev_panel_active
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
                        self.handle_menu_click(pos)
                    elif self.game_state == GameState.LEVEL_SELECT:
                        self.handle_level_select_click(pos)
                    elif self.game_state == GameState.GAME:
                        if self.showing_story:
                            if self.dialog_system.is_complete():
                                self.dialog_system.next()
                                if not self.dialog_system.has_more_dialogs():
                                    self.showing_story = False
                        else:
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
                if self.showing_story:
                    self.dialog_system.update(dt)
                else:
                    self.update_game(dt)
            
            self.screen.fill(COLOR_BLACK)
            
            if self.game_state == GameState.MENU:
                self.draw_menu()
            elif self.game_state == GameState.LEVEL_SELECT:
                self.draw_level_select()
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


class CharacterPortrait:
    @staticmethod
    def draw_portrait(screen, speaker, x, y, size=80):
        center_x, center_y = x + size // 2, y + size // 2
        
        if speaker == "神秘先知":
            pygame.draw.circle(screen, (180, 150, 120), (center_x, center_y), size // 2)
            pygame.draw.circle(screen, (100, 80, 60), (center_x, center_y), size // 3)
            pygame.draw.polygon(screen, (150, 120, 80), [
                (center_x, center_y - size // 2 - 10),
                (center_x - 8, center_y - size // 2 + 15),
                (center_x + 8, center_y - size // 2 + 15)
            ])
            pygame.draw.circle(screen, (30, 30, 30), (center_x - 12, center_y - 8), 5)
            pygame.draw.circle(screen, (30, 30, 30), (center_x + 12, center_y - 8), 5)
            pygame.draw.circle(screen, (255, 255, 255), (center_x - 10, center_y - 10), 2)
            pygame.draw.circle(screen, (255, 255, 255), (center_x + 10, center_y - 10), 2)
            pygame.draw.arc(screen, (30, 30, 30), (center_x - 10, center_y + 5, 20, 10), 0, math.pi, 2)
        
        elif speaker == "精灵守卫":
            pygame.draw.circle(screen, (140, 180, 140), (center_x, center_y), size // 2)
            pygame.draw.polygon(screen, (100, 160, 100), [
                (center_x - 30, center_y - 5),
                (center_x - 15, center_y - size // 2 - 10),
                (center_x - 5, center_y - 5)
            ])
            pygame.draw.polygon(screen, (100, 160, 100), [
                (center_x + 30, center_y - 5),
                (center_x + 15, center_y - size // 2 - 10),
                (center_x + 5, center_y - 5)
            ])
            pygame.draw.circle(screen, (30, 50, 30), (center_x - 12, center_y - 8), 5)
            pygame.draw.circle(screen, (30, 50, 30), (center_x + 12, center_y - 8), 5)
            pygame.draw.circle(screen, (255, 255, 255), (center_x - 10, center_y - 10), 2)
            pygame.draw.circle(screen, (255, 255, 255), (center_x + 10, center_y - 10), 2)
            pygame.draw.rect(screen, (100, 80, 60), (center_x - 20, center_y + 20, 40, 25))
        
        elif speaker == "指挥官":
            pygame.draw.circle(screen, (180, 160, 140), (center_x, center_y), size // 2)
            pygame.draw.rect(screen, (100, 100, 100), (center_x - 25, center_y - size // 2 + 5, 50, 20))
            pygame.draw.polygon(screen, (100, 100, 100), [
                (center_x - 25, center_y - size // 2 + 5),
                (center_x - 20, center_y - size // 2 - 15),
                (center_x + 20, center_y - size // 2 - 15),
                (center_x + 25, center_y - size // 2 + 5)
            ])
            pygame.draw.circle(screen, (30, 30, 30), (center_x - 12, center_y - 5), 5)
            pygame.draw.circle(screen, (30, 30, 30), (center_x + 12, center_y - 5), 5)
            pygame.draw.circle(screen, (255, 255, 255), (center_x - 10, center_y - 7), 2)
            pygame.draw.circle(screen, (255, 255, 255), (center_x + 10, center_y - 7), 2)
            pygame.draw.rect(screen, (120, 80, 40), (center_x - 22, center_y + 15, 44, 22))
        
        elif speaker == "北境守卫":
            pygame.draw.circle(screen, (150, 170, 190), (center_x, center_y), size // 2)
            pygame.draw.polygon(screen, (80, 120, 160), [
                (center_x - 25, center_y - size // 2 + 10),
                (center_x - 15, center_y - size // 2 - 20),
                (center_x - 5, center_y - size // 2 + 10)
            ])
            pygame.draw.polygon(screen, (80, 120, 160), [
                (center_x + 25, center_y - size // 2 + 10),
                (center_x + 15, center_y - size // 2 - 20),
                (center_x + 5, center_y - size // 2 + 10)
            ])
            pygame.draw.circle(screen, (30, 50, 70), (center_x - 12, center_y - 8), 5)
            pygame.draw.circle(screen, (30, 50, 70), (center_x + 12, center_y - 8), 5)
            pygame.draw.circle(screen, (255, 255, 255), (center_x - 10, center_y - 10), 2)
            pygame.draw.circle(screen, (255, 255, 255), (center_x + 10, center_y - 10), 2)
        
        elif speaker == "冰霜法师":
            pygame.draw.circle(screen, (180, 200, 255), (center_x, center_y), size // 2)
            pygame.draw.polygon(screen, (120, 160, 220), [
                (center_x, center_y - size // 2 - 15),
                (center_x - 5, center_y - size // 2 + 10),
                (center_x + 5, center_y - size // 2 + 10)
            ])
            pygame.draw.circle(screen, (30, 60, 100), (center_x - 12, center_y - 8), 5)
            pygame.draw.circle(screen, (30, 60, 100), (center_x + 12, center_y - 8), 5)
            pygame.draw.circle(screen, (100, 180, 255), (center_x - 10, center_y - 10), 2)
            pygame.draw.circle(screen, (100, 180, 255), (center_x + 10, center_y - 10), 2)
            pygame.draw.polygon(screen, (150, 180, 255), [(center_x - 20, center_y + 25), (center_x, center_y + 35), (center_x + 20, center_y + 25)])
        
        elif speaker == "老骑士":
            pygame.draw.circle(screen, (160, 140, 120), (center_x, center_y), size // 2)
            pygame.draw.rect(screen, (80, 80, 80), (center_x - 30, center_y - size // 2 + 5, 60, 25))
            pygame.draw.circle(screen, (80, 80, 80), (center_x, center_y - size // 2 - 5), 20)
            pygame.draw.circle(screen, (120, 120, 120), (center_x, center_y - size // 2 - 5), 15)
            pygame.draw.circle(screen, (30, 30, 30), (center_x - 12, center_y - 5), 5)
            pygame.draw.circle(screen, (30, 30, 30), (center_x + 12, center_y - 5), 5)
            pygame.draw.circle(screen, (255, 255, 255), (center_x - 10, center_y - 7), 2)
            pygame.draw.circle(screen, (255, 255, 255), (center_x + 10, center_y - 7), 2)
        
        elif speaker == "皇家史官":
            pygame.draw.circle(screen, (180, 170, 160), (center_x, center_y), size // 2)
            pygame.draw.rect(screen, (100, 80, 60), (center_x - 20, center_y - size // 2 - 5, 40, 8))
            pygame.draw.line(screen, (100, 80, 60), (center_x - 18, center_y - size // 2 + 8), (center_x + 18, center_y - size // 2 + 8))
            pygame.draw.line(screen, (100, 80, 60), (center_x - 18, center_y - size // 2 + 18), (center_x + 18, center_y - size // 2 + 18))
            pygame.draw.circle(screen, (30, 30, 30), (center_x - 12, center_y - 8), 5)
            pygame.draw.circle(screen, (30, 30, 30), (center_x + 12, center_y - 8), 5)
            pygame.draw.circle(screen, (255, 255, 255), (center_x - 10, center_y - 10), 2)
            pygame.draw.circle(screen, (255, 255, 255), (center_x + 10, center_y - 10), 2)
        
        elif speaker == "沙漠旅者":
            pygame.draw.circle(screen, (200, 170, 120), (center_x, center_y), size // 2)
            pygame.draw.polygon(screen, (150, 120, 80), [
                (center_x - 35, center_y - 10),
                (center_x, center_y - size // 2 - 20),
                (center_x + 35, center_y - 10)
            ])
            pygame.draw.circle(screen, (30, 20, 10), (center_x - 12, center_y - 8), 5)
            pygame.draw.circle(screen, (30, 20, 10), (center_x + 12, center_y - 8), 5)
            pygame.draw.circle(screen, (255, 255, 255), (center_x - 10, center_y - 10), 2)
            pygame.draw.circle(screen, (255, 255, 255), (center_x + 10, center_y - 10), 2)
            pygame.draw.line(screen, (100, 80, 60), (center_x - 20, center_y + 20), (center_x + 20, center_y + 20))
        
        elif speaker == "部落长老":
            pygame.draw.circle(screen, (160, 140, 100), (center_x, center_y), size // 2)
            pygame.draw.polygon(screen, (120, 100, 70), [
                (center_x - 8, center_y - size // 2 - 25),
                (center_x, center_y - size // 2 - 10),
                (center_x + 8, center_y - size // 2 - 25)
            ])
            for i in range(3):
                pygame.draw.polygon(screen, (120, 100, 70), [
                    (center_x - 25 + i * 20, center_y - size // 2 + 5),
                    (center_x - 20 + i * 20, center_y - size // 2 + 15),
                    (center_x - 30 + i * 20, center_y - size // 2 + 15)
                ])
            pygame.draw.circle(screen, (30, 25, 15), (center_x - 12, center_y - 8), 5)
            pygame.draw.circle(screen, (30, 25, 15), (center_x + 12, center_y - 8), 5)
            pygame.draw.circle(screen, (255, 255, 255), (center_x - 10, center_y - 10), 2)
            pygame.draw.circle(screen, (255, 255, 255), (center_x + 10, center_y - 10), 2)
        
        elif speaker == "火山守护者":
            pygame.draw.circle(screen, (200, 100, 80), (center_x, center_y), size // 2)
            pygame.draw.polygon(screen, (150, 60, 40), [
                (center_x - 20, center_y - size // 2 + 10),
                (center_x - 10, center_y - size // 2 - 20),
                (center_x, center_y - size // 2 - 25),
                (center_x + 10, center_y - size // 2 - 20),
                (center_x + 20, center_y - size // 2 + 10)
            ])
            pygame.draw.circle(screen, (30, 15, 10), (center_x - 12, center_y - 8), 5)
            pygame.draw.circle(screen, (30, 15, 10), (center_x + 12, center_y - 8), 5)
            pygame.draw.circle(screen, (255, 200, 100), (center_x - 10, center_y - 10), 2)
            pygame.draw.circle(screen, (255, 200, 100), (center_x + 10, center_y - 10), 2)
        
        elif speaker == "熔岩术士":
            pygame.draw.circle(screen, (220, 120, 80), (center_x, center_y), size // 2)
            pygame.draw.polygon(screen, (180, 80, 40), [
                (center_x, center_y - size // 2 - 15),
                (center_x - 5, center_y - size // 2 + 10),
                (center_x + 5, center_y - size // 2 + 10)
            ])
            pygame.draw.circle(screen, (30, 15, 10), (center_x - 12, center_y - 8), 5)
            pygame.draw.circle(screen, (30, 15, 10), (center_x + 12, center_y - 8), 5)
            pygame.draw.circle(screen, (255, 150, 50), (center_x - 10, center_y - 10), 3)
            pygame.draw.circle(screen, (255, 150, 50), (center_x + 10, center_y - 10), 3)
        
        elif speaker == "暗影猎手":
            pygame.draw.circle(screen, (80, 70, 90), (center_x, center_y), size // 2)
            pygame.draw.polygon(screen, (50, 45, 60), [
                (center_x - 25, center_y - 5),
                (center_x - 10, center_y - size // 2 - 15),
                (center_x, center_y - size // 2 + 5)
            ])
            pygame.draw.polygon(screen, (50, 45, 60), [
                (center_x + 25, center_y - 5),
                (center_x + 10, center_y - size // 2 - 15),
                (center_x, center_y - size // 2 + 5)
            ])
            pygame.draw.circle(screen, (100, 90, 120), (center_x - 12, center_y - 8), 5)
            pygame.draw.circle(screen, (100, 90, 120), (center_x + 12, center_y - 8), 5)
            pygame.draw.circle(screen, (200, 180, 220), (center_x - 10, center_y - 10), 2)
            pygame.draw.circle(screen, (200, 180, 220), (center_x + 10, center_y - 10), 2)
        
        elif speaker == "光明牧师":
            pygame.draw.circle(screen, (220, 200, 180), (center_x, center_y), size // 2)
            pygame.draw.polygon(screen, (255, 255, 255), [
                (center_x, center_y - size // 2 - 20),
                (center_x - 15, center_y - size // 2 + 5),
                (center_x + 15, center_y - size // 2 + 5)
            ])
            pygame.draw.circle(screen, (30, 30, 30), (center_x - 12, center_y - 8), 5)
            pygame.draw.circle(screen, (30, 30, 30), (center_x + 12, center_y - 8), 5)
            pygame.draw.circle(screen, (255, 255, 255), (center_x - 10, center_y - 10), 2)
            pygame.draw.circle(screen, (255, 255, 255), (center_x + 10, center_y - 10), 2)
            pygame.draw.polygon(screen, (200, 180, 160), [(center_x - 15, center_y + 20), (center_x, center_y + 35), (center_x + 15, center_y + 20)])
        
        elif speaker == "平原农夫":
            pygame.draw.circle(screen, (180, 140, 100), (center_x, center_y), size // 2)
            pygame.draw.rect(screen, (80, 60, 40), (center_x - 25, center_y - size // 2 - 5, 50, 10))
            pygame.draw.circle(screen, (30, 20, 10), (center_x - 12, center_y - 8), 5)
            pygame.draw.circle(screen, (30, 20, 10), (center_x + 12, center_y - 8), 5)
            pygame.draw.circle(screen, (255, 255, 255), (center_x - 10, center_y - 10), 2)
            pygame.draw.circle(screen, (255, 255, 255), (center_x + 10, center_y - 10), 2)
            pygame.draw.rect(screen, (100, 80, 60), (center_x - 22, center_y + 15, 44, 20))
        
        elif speaker == "大地守护者":
            pygame.draw.circle(screen, (160, 180, 140), (center_x, center_y), size // 2)
            pygame.draw.polygon(screen, (100, 140, 80), [
                (center_x - 20, center_y - size // 2 + 5),
                (center_x, center_y - size // 2 - 25),
                (center_x + 20, center_y - size // 2 + 5)
            ])
            pygame.draw.circle(screen, (40, 60, 30), (center_x - 12, center_y - 8), 5)
            pygame.draw.circle(screen, (40, 60, 30), (center_x + 12, center_y - 8), 5)
            pygame.draw.circle(screen, (200, 220, 180), (center_x - 10, center_y - 10), 2)
            pygame.draw.circle(screen, (200, 220, 180), (center_x + 10, center_y - 10), 2)
        
        elif speaker == "沼泽向导":
            pygame.draw.circle(screen, (100, 120, 100), (center_x, center_y), size // 2)
            pygame.draw.polygon(screen, (60, 80, 60), [
                (center_x - 25, center_y - 10),
                (center_x, center_y - size // 2 - 15),
                (center_x + 25, center_y - 10)
            ])
            pygame.draw.circle(screen, (30, 40, 30), (center_x - 12, center_y - 8), 5)
            pygame.draw.circle(screen, (30, 40, 30), (center_x + 12, center_y - 8), 5)
            pygame.draw.circle(screen, (150, 180, 150), (center_x - 10, center_y - 10), 2)
            pygame.draw.circle(screen, (150, 180, 150), (center_x + 10, center_y - 10), 2)
        
        elif speaker == "自然德鲁伊":
            pygame.draw.circle(screen, (120, 160, 100), (center_x, center_y), size // 2)
            pygame.draw.polygon(screen, (80, 120, 60), [
                (center_x - 30, center_y - 5),
                (center_x - 15, center_y - size // 2 - 20),
                (center_x - 5, center_y - 5)
            ])
            pygame.draw.polygon(screen, (80, 120, 60), [
                (center_x + 30, center_y - 5),
                (center_x + 15, center_y - size // 2 - 20),
                (center_x + 5, center_y - 5)
            ])
            pygame.draw.circle(screen, (40, 60, 30), (center_x - 12, center_y - 8), 5)
            pygame.draw.circle(screen, (40, 60, 30), (center_x + 12, center_y - 8), 5)
            pygame.draw.circle(screen, (180, 220, 160), (center_x - 10, center_y - 10), 2)
            pygame.draw.circle(screen, (180, 220, 160), (center_x + 10, center_y - 10), 2)
        
        elif speaker == "天空信使":
            pygame.draw.circle(screen, (180, 200, 255), (center_x, center_y), size // 2)
            pygame.draw.polygon(screen, (120, 160, 220), [
                (center_x - 30, center_y + 10),
                (center_x - 15, center_y - size // 2 - 20),
                (center_x - 5, center_y + 10)
            ])
            pygame.draw.polygon(screen, (120, 160, 220), [
                (center_x + 30, center_y + 10),
                (center_x + 15, center_y - size // 2 - 20),
                (center_x + 5, center_y + 10)
            ])
            pygame.draw.circle(screen, (60, 80, 120), (center_x - 12, center_y - 8), 5)
            pygame.draw.circle(screen, (60, 80, 120), (center_x + 12, center_y - 8), 5)
            pygame.draw.circle(screen, (200, 220, 255), (center_x - 10, center_y - 10), 2)
            pygame.draw.circle(screen, (200, 220, 255), (center_x + 10, center_y - 10), 2)
        
        elif speaker == "风之精灵":
            pygame.draw.circle(screen, (200, 220, 255), (center_x, center_y), size // 2)
            pygame.draw.polygon(screen, (150, 180, 240), [
                (center_x, center_y - size // 2 - 20),
                (center_x - 8, center_y - size // 2 + 5),
                (center_x + 8, center_y - size // 2 + 5)
            ])
            pygame.draw.circle(screen, (60, 80, 120), (center_x - 12, center_y - 8), 5)
            pygame.draw.circle(screen, (60, 80, 120), (center_x + 12, center_y - 8), 5)
            pygame.draw.circle(screen, (100, 180, 255), (center_x - 10, center_y - 10), 3)
            pygame.draw.circle(screen, (100, 180, 255), (center_x + 10, center_y - 10), 3)
        
        elif speaker == "花园园丁":
            pygame.draw.circle(screen, (160, 180, 140), (center_x, center_y), size // 2)
            pygame.draw.rect(screen, (100, 120, 80), (center_x - 25, center_y - size // 2 + 5, 50, 15))
            pygame.draw.circle(screen, (40, 60, 30), (center_x - 12, center_y - 8), 5)
            pygame.draw.circle(screen, (40, 60, 30), (center_x + 12, center_y - 8), 5)
            pygame.draw.circle(screen, (200, 220, 180), (center_x - 10, center_y - 10), 2)
            pygame.draw.circle(screen, (200, 220, 180), (center_x + 10, center_y - 10), 2)
        
        elif speaker == "炼金术士":
            pygame.draw.circle(screen, (180, 160, 140), (center_x, center_y), size // 2)
            pygame.draw.polygon(screen, (120, 100, 80), [
                (center_x - 25, center_y - size // 2 + 10),
                (center_x - 10, center_y - size // 2 - 20),
                (center_x + 10, center_y - size // 2 - 20),
                (center_x + 25, center_y - size // 2 + 10)
            ])
            pygame.draw.circle(screen, (30, 30, 30), (center_x - 12, center_y - 8), 5)
            pygame.draw.circle(screen, (30, 30, 30), (center_x + 12, center_y - 8), 5)
            pygame.draw.circle(screen, (100, 200, 150), (center_x - 10, center_y - 10), 2)
            pygame.draw.circle(screen, (100, 200, 150), (center_x + 10, center_y - 10), 2)
        
        elif speaker == "末日预言者":
            pygame.draw.circle(screen, (100, 80, 100), (center_x, center_y), size // 2)
            pygame.draw.polygon(screen, (70, 50, 70), [
                (center_x - 30, center_y - 10),
                (center_x, center_y - size // 2 - 25),
                (center_x + 30, center_y - 10)
            ])
            pygame.draw.circle(screen, (150, 100, 150), (center_x - 12, center_y - 8), 5)
            pygame.draw.circle(screen, (150, 100, 150), (center_x + 12, center_y - 8), 5)
            pygame.draw.circle(screen, (255, 200, 255), (center_x - 10, center_y - 10), 3)
            pygame.draw.circle(screen, (255, 200, 255), (center_x + 10, center_y - 10), 3)
        
        elif speaker == "时间守望者":
            pygame.draw.circle(screen, (140, 160, 200), (center_x, center_y), size // 2)
            pygame.draw.polygon(screen, (100, 120, 160), [
                (center_x, center_y - size // 2 - 20),
                (center_x - 6, center_y - size // 2 + 10),
                (center_x + 6, center_y - size // 2 + 10)
            ])
            pygame.draw.circle(screen, (50, 60, 80), (center_x - 12, center_y - 8), 5)
            pygame.draw.circle(screen, (50, 60, 80), (center_x + 12, center_y - 8), 5)
            pygame.draw.circle(screen, (150, 200, 255), (center_x - 10, center_y - 10), 3)
            pygame.draw.circle(screen, (150, 200, 255), (center_x + 10, center_y - 10), 3)
            pygame.draw.circle(screen, (80, 100, 140), (center_x, center_y + 10), 8)
            pygame.draw.line(screen, (120, 140, 180), (center_x, center_y + 10), (center_x, center_y + 2))
            pygame.draw.line(screen, (120, 140, 180), (center_x, center_y + 10), (center_x + 6, center_y + 10))
        else:
            pygame.draw.circle(screen, (150, 150, 150), (center_x, center_y), size // 2)
            pygame.draw.circle(screen, (80, 80, 80), (center_x - 12, center_y - 8), 5)
            pygame.draw.circle(screen, (80, 80, 80), (center_x + 12, center_y - 8), 5)


class StoryData:
    FOREST_STORY = [
        {"speaker": "神秘先知", "text": "王国的边界正在遭受黑暗势力的入侵。精灵森林是第一道防线，我们必须守住这里！"},
        {"speaker": "精灵守卫", "text": "森林中的古树已经发出了警告，黑暗力量正在蔓延。战士们，准备战斗！"},
        {"speaker": "指挥官", "text": "敌人会从森林深处出现，利用地形优势建造防御塔，保护我们的家园！"}
    ]
    
    ICE_STORY = [
        {"speaker": "北境守卫", "text": "冰封峡谷的永冻之墙正在融化，古老的封印正在失效..."},
        {"speaker": "冰霜法师", "text": "我感受到了来自地底深处的寒意，那不是自然的力量，是黑暗魔法！"},
        {"speaker": "指挥官", "text": "在冰层完全崩解前，阻止黑暗势力突破这道防线！"}
    ]
    
    CASTLE_STORY = [
        {"speaker": "老骑士", "text": "这座古老的城堡见证了无数战役，如今它的废墟将成为我们的战场。"},
        {"speaker": "皇家史官", "text": "传说城堡深处封印着远古的邪恶，如今封印正在动摇..."},
        {"speaker": "指挥官", "text": "利用城堡的防御工事，坚守每一寸土地！"}
    ]
    
    DESERT_STORY = [
        {"speaker": "沙漠旅者", "text": "这片绿洲是沙漠中唯一的希望，千万不能让它落入敌人手中！"},
        {"speaker": "部落长老", "text": "沙暴中传来了不祥的征兆，黑暗正在吞噬这片土地。"},
        {"speaker": "指挥官", "text": "酷热的沙漠既是挑战也是优势，善用环境击败敌人！"}
    ]
    
    VOLCANO_STORY = [
        {"speaker": "火山守护者", "text": "火山的怒火正在被黑暗力量操控，岩浆已经开始沸腾！"},
        {"speaker": "熔岩术士", "text": "火焰元素变得狂暴不安，它们正在被邪恶力量腐化！"},
        {"speaker": "指挥官", "text": "在火山喷发前，消灭黑暗的源头！"}
    ]
    
    SHADOW_STORY = [
        {"speaker": "暗影猎手", "text": "暗影要塞是黑暗势力的老巢，这里充满了邪恶的气息..."},
        {"speaker": "光明牧师", "text": "光明与黑暗的最终对决即将开始，愿圣光庇佑我们！"},
        {"speaker": "指挥官", "text": "突破暗影的防线，直面最终的邪恶！"}
    ]
    
    PLAIN_STORY = [
        {"speaker": "平原农夫", "text": "万象平原曾经是王国最富饶的土地，如今却被黑暗笼罩..."},
        {"speaker": "大地守护者", "text": "土地在哭泣，生灵在凋零，我们必须净化这片被污染的大地！"},
        {"speaker": "指挥官", "text": "利用平原开阔的视野，布下天罗地网！"}
    ]
    
    SWAMP_STORY = [
        {"speaker": "沼泽向导", "text": "恶地沼泽是一片被诅咒的土地，进去的人很少能活着出来..."},
        {"speaker": "自然德鲁伊", "text": "沼泽中的生物已经被腐化，它们将成为黑暗的爪牙！"},
        {"speaker": "指挥官", "text": "小心沼泽的陷阱，在迷雾中找到敌人的弱点！"}
    ]
    
    SKY_STORY = [
        {"speaker": "天空信使", "text": "天落殷园曾经是天界的乐园，如今却被黑暗侵蚀..."},
        {"speaker": "风之精灵", "text": "樱花的飘落不再是美景，而是黑暗降临的预兆..."},
        {"speaker": "指挥官", "text": "在云端之上展开战斗，守护这片神圣的土地！"}
    ]
    
    CORRUPT_STORY = [
        {"speaker": "花园园丁", "text": "曾经美丽的花园，如今变成了滋生邪恶的温床..."},
        {"speaker": "炼金术士", "text": "毒雾正在扩散，所有接触到的生物都会被腐化！"},
        {"speaker": "指挥官", "text": "在被完全污染前，净化这片花园！"}
    ]
    
    APOCALYPSE_STORY = [
        {"speaker": "末日预言者", "text": "终末之地，一切的终结与开端。这里是最后的战场..."},
        {"speaker": "时间守望者", "text": "时空的裂隙正在扩大，各个世界的怪物都将涌入..."},
        {"speaker": "指挥官", "text": "这是最终的决战！所有的力量都汇聚于此，胜利或毁灭！"}
    ]

    @staticmethod
    def get_story(theme):
        stories = {
            LevelTheme.FOREST: StoryData.FOREST_STORY,
            LevelTheme.ICE: StoryData.ICE_STORY,
            LevelTheme.CASTLE: StoryData.CASTLE_STORY,
            LevelTheme.DESERT: StoryData.DESERT_STORY,
            LevelTheme.VOLCANO: StoryData.VOLCANO_STORY,
            LevelTheme.SHADOW: StoryData.SHADOW_STORY,
            LevelTheme.PLAIN: StoryData.PLAIN_STORY,
            LevelTheme.SWAMP: StoryData.SWAMP_STORY,
            LevelTheme.SKY: StoryData.SKY_STORY,
            LevelTheme.CORRUPT: StoryData.CORRUPT_STORY,
            LevelTheme.APOCALYPSE: StoryData.APOCALYPSE_STORY
        }
        return stories.get(theme, StoryData.FOREST_STORY)


class DialogSystem:
    def __init__(self):
        self.dialogs = []
        self.current_dialog = None
        self.text_index = 0
        self.text_timer = 0
        self.speed = 0.05
        self.font = get_chinese_font(24)
        self.skipped = False

    def add_dialog(self, speaker, text, choices=None):
        dialog = {
            'speaker': speaker,
            'text': text,
            'choices': choices or [],
            'completed': False
        }
        self.dialogs.append(dialog)

    def load_story(self, story_data):
        self.dialogs = []
        for line in story_data:
            self.add_dialog(line['speaker'], line['text'])
        self.start_dialog()

    def start_dialog(self):
        if self.dialogs:
            self.current_dialog = self.dialogs[0]
            self.text_index = 0
            self.text_timer = 0
            self.skipped = False

    def update(self, dt):
        if not self.current_dialog or self.skipped:
            return
        
        self.text_timer += dt
        if self.text_timer >= self.speed:
            self.text_timer = 0
            if self.text_index < len(self.current_dialog['text']):
                self.text_index += 1

    def is_complete(self):
        if self.skipped:
            return True
        return self.text_index >= len(self.current_dialog['text']) if self.current_dialog else True

    def has_more_dialogs(self):
        return len(self.dialogs) > 0 or (self.current_dialog and not self.is_complete())

    def skip(self):
        self.skipped = True
        self.dialogs = []
        self.current_dialog = None

    def next(self):
        if self.is_complete():
            if self.current_dialog:
                self.current_dialog['completed'] = True
                self.dialogs.pop(0)
                self.current_dialog = None
                self.text_index = 0
            self.start_dialog()

    def draw(self, screen):
        if not self.current_dialog or self.skipped:
            return
        
        CharacterPortrait.draw_portrait(screen, self.current_dialog['speaker'], 80, SCREEN_HEIGHT - 140, 100)
        
        dialog_box = pygame.Rect(200, SCREEN_HEIGHT - 150, SCREEN_WIDTH - 300, 130)
        pygame.draw.rect(screen, (30, 30, 50), dialog_box)
        pygame.draw.rect(screen, COLOR_WHITE, dialog_box, 3)
        
        speaker_text = self.font.render(self.current_dialog['speaker'], True, COLOR_GOLD)
        screen.blit(speaker_text, (220, SCREEN_HEIGHT - 130))
        
        displayed_text = self.current_dialog['text'][:self.text_index]
        text_surface = self.font.render(displayed_text, True, COLOR_WHITE)
        screen.blit(text_surface, (220, SCREEN_HEIGHT - 90))
        
        if self.is_complete():
            continue_text = self.font.render("点击继续...", True, COLOR_GRAY)
            screen.blit(continue_text, (SCREEN_WIDTH - 180, SCREEN_HEIGHT - 50))


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
                "menu_title": "王国保卫战",
                "menu_subtitle": "Kingdom Rush",
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
                "menu_title": "Kingdom Rush",
                "menu_subtitle": "王国保卫战",
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
            {'text': '欢迎来到王国保卫战！点击地图上的绿色圆圈建造塔', 'position': (640, 400)},
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
                    self.game.selected_level = level
                    self.game.start_level()
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


if __name__ == "__main__":
    game = Game()
    game.run()

