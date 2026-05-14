# ================================
# 塔防游戏 - 鸿蒙防线 (Harmony Defense)
# 作者：未知
# 版本：1.0
# 描述：一个基于Pygame的塔防游戏
# ================================

# 导入必要的模块
import pygame   # Pygame游戏库，用于图形渲染和事件处理
import math     # 数学库，用于计算距离、角度等
import random   # 随机数库，用于随机生成等

# 初始化Pygame库（必须在使用Pygame功能前调用）
pygame.init()

# ================================
# 游戏常量定义（所有大写表示常量，不应被修改）
# ================================
SCREEN_WIDTH = 1280    # 游戏窗口宽度（像素）
SCREEN_HEIGHT = 720   # 游戏窗口高度（像素）
GRID_SIZE = 40        # 网格大小，每个格子的像素数
FPS = 60              # 游戏帧率，每秒刷新60次

# ================================
# 颜色定义字典（RGB格式）- 草地平原主题优化
# ================================
COLORS = {
    'background': (20, 50, 20),       # 游戏背景色（深绿色）
    'grass_base': (25, 80, 30),      # 草地基础色
    'grass_light': (40, 100, 45),    # 草地浅色
    'grass_dark': (15, 60, 20),     # 草地深色
    'grass_accent': (50, 120, 55),   # 草地点缀色
    'grid': (60, 100, 70),          # 网格线颜色（绿色调）
    'path': (139, 119, 101),         # 敌人行进路径颜色（土棕色）
    'path_dark': (101, 85, 70),      # 路径深色边缘
    'tower': (60, 180, 100),         # 防御塔默认颜色（绿色）
    'enemy': (200, 80, 80),          # 敌人默认颜色（红色）
    'bullet': (255, 200, 100),       # 子弹默认颜色（橙色）
    'text': (255, 255, 255),         # 文字颜色（白色）
    'gold': (255, 215, 0),           # 金币颜色（金色）
    'health': (255, 100, 100),       # 生命值颜色（粉红色）
}

# ================================
# 草地纹理配置
# ================================
GRASS_TYPES = ['light', 'normal', 'dark', 'accent']
GRASS_COLORS = {
    'light': COLORS['grass_light'],
    'normal': COLORS['grass_base'],
    'dark': COLORS['grass_dark'],
    'accent': COLORS['grass_accent']
}

# 预生成草地分布模式（基于网格的规律分布）
GRASS_PATTERN = []
random.seed(42)  # 固定随机种子保证一致性
for i in range(int(SCREEN_WIDTH / GRID_SIZE) + 1):
    row = []
    for j in range(int(SCREEN_HEIGHT / GRID_SIZE) + 1):
        # 使用伪随机算法创建规律的草地纹理
        value = (i * 7 + j * 13 + i * j) % 10
        if value < 2:
            row.append('light')
        elif value < 5:
            row.append('normal')
        elif value < 8:
            row.append('dark')
        else:
            row.append('accent')
    GRASS_PATTERN.append(row)

# 草地点缀物（小草、石头等）的位置
GRASS_DECORATIONS = []
for i in range(int(SCREEN_WIDTH / GRID_SIZE)):
    for j in range(int(SCREEN_HEIGHT / GRID_SIZE)):
        # 每个格子随机生成1-3个点缀
        count = random.randint(1, 3)
        for _ in range(count):
            GRASS_DECORATIONS.append({
                'grid_x': i,
                'grid_y': j,
                'offset_x': random.randint(5, GRID_SIZE - 5),
                'offset_y': random.randint(5, GRID_SIZE - 5),
                'size': random.randint(2, 4),
                'type': random.choice(['grass', 'stone', 'flower'])
            })

# ================================
# 防御塔配置字典
# 说明：定义了5种不同类型的防御塔，每种塔有独特的属性和功能
# 属性说明：
#   - name: 显示名称（中文）
#   - cost: 建造成本（金币）
#   - damage: 单次攻击伤害值
#   - range: 攻击范围（像素）
#   - attack_speed: 攻击速度（每秒攻击次数）
#   - color: 显示颜色（RGB）
#   - shape: 显示形状（triangle/hexagon/diamond/star/octagon）
#   - splash_radius: 溅射范围（仅炮塔）
#   - slow_effect: 减速效果（仅冰塔）
#   - chain_count: 链式攻击目标数（仅电塔）
#   - chain_range: 链式攻击跳转范围（仅电塔）
#   - pierce_count: 穿透目标数（仅魔法塔）
# ================================
TOWER_CONFIG = {
    'arrow': {              # 箭塔 - 发射三只箭矢，长方形弹幕
        'name': '箭塔',     # 显示名称
        'cost': 100,        # 建造成本：100金币
        'damage': 15,       # 伤害值：15点/箭
        'range': 150,       # 攻击范围：150像素
        'attack_speed': 0.8, # 攻击速度：每秒0.8次
        'arrow_count': 3,    # 每次发射箭矢数量
        'bullet_color': (139, 90, 43), # 棕色弹幕
        'bullet_shape': 'rect',       # 长方形弹幕
        'color': (100, 180, 255),  # 显示颜色：蓝色
        'shape': 'triangle',        # 显示形状：三角形
    },
    'cannon': {             # 炮塔 - 瞄准位置攻击，范围伤害
        'name': '炮塔',
        'cost': 200,        # 建造成本：200金币
        'damage': 60,       # 伤害值：60点
        'range': 120,       # 攻击范围：120像素
        'attack_speed': 0.4, # 攻击速度：每秒0.4次
        'splash_radius': 60,        # 溅射范围：1.5个敌人体积
        'bullet_color': (255, 80, 80),   # 红色弹幕
        'color': (255, 150, 100),   # 显示颜色：橙色
        'shape': 'hexagon',         # 显示形状：六边形
    },
    'ice': {                # 冰塔 - 减速+叠加标记+冰爆
        'name': '冰塔',
        'cost': 150,        # 建造成本：150金币
        'damage': 10,       # 伤害值：10点
        'range': 130,       # 攻击范围：130像素
        'attack_speed': 1.0, # 攻击速度：每秒1次
        'slow_factor': 0.35,         # 减速效果：35%
        'max_stacks': 3,             # 最大叠加层数
        'ice_explosion_radius': 80,  # 冰爆范围
        'ice_explosion_damage_pct': 0.05,  # 冰爆伤害：总生命值的5%
        'color': (100, 200, 255),   # 显示颜色：青色
        'bullet_color': (100, 220, 255),  # 冰弹颜色
        'shape': 'diamond',         # 显示形状：菱形
    },
    'lightning': {          # 电塔 - 金色弹幕，链式攻击4个敌人
        'name': '电塔',
        'cost': 250,        # 建造成本：250金币
        'damage': 30,       # 伤害值：30点
        'range': 140,       # 攻击范围：140像素
        'attack_speed': 0.5, # 攻击速度：每秒0.5次
        'chain_count': 4,           # 链式攻击：最多击中4个目标（1主+3链）
        'chain_range': 70,          # 链式跳转范围：70像素内可跳转
        'bullet_color': (255, 215, 0),   # 金色弹幕
        'color': (255, 200, 100),   # 显示颜色：黄色
        'shape': 'star',            # 显示形状：五角星
    },
    'magic': {              # 魔法塔 - 不发射弹幕，在敌人位置产生魔法柱
        'name': '魔法塔',
        'cost': 300,        # 建造成本：300金币（最贵）
        'damage': 45,       # 伤害值：45点
        'range': 150,       # 攻击范围：150像素
        'attack_speed': 0.6, # 攻击速度：每秒0.6次
        'magic_radius': 50,         # 魔法柱范围
        'color': (180, 100, 255),   # 显示颜色：紫色
        'shape': 'octagon',         # 显示形状：八边形
    },
}

# ================================
# 敌人配置字典
# 说明：定义了4种不同类型的敌人
# 属性说明：
#   - name: 显示名称（中文）
#   - health: 生命值
#   - speed: 移动速度（像素/帧）
#   - reward: 击杀奖励（金币）
#   - color: 显示颜色（RGB）
# ================================
ENEMY_CONFIG = {
    'normal': {             # 普通敌人 - 标准属性，最常见
        'name': '普通敌人',
        'health': 100,      # 生命值：100点
        'speed': 1.5,       # 移动速度：中等
        'reward': 20,       # 击杀奖励：20金币
        'color': (200, 80, 80),     # 显示颜色：红色
    },
    'fast': {               # 快速敌人 - 高机动性，难以拦截
        'name': '快速敌人',
        'health': 50,       # 生命值较低：50点
        'speed': 3.0,       # 移动速度快：是普通敌人的2倍
        'reward': 30,       # 击杀奖励：30金币
        'color': (255, 200, 80),    # 显示颜色：黄色
    },
    'tank': {               # 坦克敌人 - 高防御，需要集火
        'name': '坦克敌人',
        'health': 300,      # 高生命值：300点（普通的3倍）
        'speed': 0.8,       # 速度慢：比普通敌人慢
        'reward': 50,       # 击杀奖励：50金币
        'color': (100, 150, 200),   # 显示颜色：蓝色
    },
    'boss': {               # Boss敌人 - 终极挑战，出现在关卡末尾
        'name': 'Boss',
        'health': 1000,     # 极高生命值：1000点
        'speed': 0.5,       # 最慢速度
        'reward': 200,      # 高额奖励：200金币
        'color': (150, 50, 150),    # 显示颜色：紫色
    },
}

# ================================
# 动态生成波次配置
# 说明：根据波次数量动态生成难度递增的波次配置
# 参数：
#   - total_waves: 总波次数
#   - base_count: 基础敌人数
#   - base_delay: 基础生成间隔（毫秒）
# 返回：波次列表
# ================================
def generate_waves(total_waves, base_count=5, base_delay=1500):
    waves = []

    for wave_num in range(1, total_waves + 1):
        # 根据波次决定敌人类型（难度递增）
        if wave_num <= total_waves * 0.4:
            # 前期：以普通敌人为主
            enemy_type = 'normal'
        elif wave_num <= total_waves * 0.7:
            # 中期：混合普通和快速敌人
            if wave_num % 3 == 0:
                enemy_type = 'fast'
            else:
                enemy_type = 'normal'
        elif wave_num <= total_waves * 0.9:
            # 后期：加入坦克敌人
            if wave_num % 4 == 0:
                enemy_type = 'tank'
            elif wave_num % 2 == 0:
                enemy_type = 'fast'
            else:
                enemy_type = 'normal'
        else:
            # 最后阶段：Boss战
            if wave_num == total_waves:
                enemy_type = 'boss'
            else:
                # 最终波前的铺垫
                if wave_num % 3 == 0:
                    enemy_type = 'tank'
                else:
                    enemy_type = 'fast'

        # 计算敌人数量（随波次增加）
        count = base_count + (wave_num - 1) * 2

        # 计算生成间隔（随波次减少，敌人出现更快）
        delay = max(600, base_delay - (wave_num - 1) * 50)

        waves.append({
            'type': enemy_type,
            'count': count,
            'delay': delay
        })

    return waves

# ================================
# 关卡配置字典
# 说明：定义了2个关卡，难度逐渐递增
# 属性说明：
#   - waves: 波次列表
#   - start_gold: 初始金币
#   - lives: 初始生命值
# ================================
LEVEL_CONFIG = {
    'level_1': {            # 第一关 - 入门难度（适合新手）
        'name': '草地平原',  # 关卡名称
        'waves': generate_waves(15),  # 15波
        'start_gold': 500,  # 初始金币：500
        'lives': 20,        # 初始生命值：20
    },
    'level_2': {            # 第二关 - 进阶难度
        'name': '沙漠风暴',  # 关卡名称
        'waves': generate_waves(20, base_count=6, base_delay=1400),  # 20波
        'start_gold': 600,  # 初始金币：600
        'lives': 25,        # 初始生命值：25
    },
}

# ================================
# 敌人行进路径定义（网格坐标）
# 说明：路径由一系列网格点组成，敌人会按顺序经过这些点到达终点
# 坐标格式：(网格X, 网格Y)，从左上角(0,0)开始
# 绿色圆圈 = 起点，红色圆圈 = 终点
# ================================
PATH_POINTS = [
    (0, 4), (3, 4), (3, 10), (9, 10), (9, 3), (15, 3),
    (15, 12), (7, 12), (7, 16), (20, 16), (20, 7), (26, 7),
    (26, 14), (18, 14), (18, 9), (30, 9), (30, 16), (31, 16)
]

# ================================
# 游戏窗口和资源初始化
# ================================
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # 创建游戏窗口
pygame.display.set_caption("鸿蒙防线 - 塔防游戏")  # 设置窗口标题

clock = pygame.time.Clock()  # 时钟对象，用于控制游戏帧率

# 字体对象定义
# 尝试使用系统中文字体，解决中文乱码问题
# 按优先级尝试：微软雅黑 > 黑体 > 宋体 > 默认字体
def get_chinese_font(size):
    import os
    # Windows系统字体目录
    font_dirs = [
        os.path.join(os.environ.get('WINDIR', 'C:\\Windows'), 'Fonts'),
        '.',  # 当前目录
    ]

    font_files = [
        "msyh.ttc",           # 微软雅黑
        "msyhbd.ttc",         # 微软雅黑粗体
        "simhei.ttf",         # 黑体
        "simsun.ttc",         # 宋体
        "simkai.ttf",         # 楷体
        "mingliu.ttc",        # 细明体
        None                  # 默认字体（可能不支持中文）
    ]

    for font_dir in font_dirs:
        for font_file in font_files[:-1]:  # 排除None
            font_path = os.path.join(font_dir, font_file)
            if os.path.exists(font_path):
                try:
                    return pygame.font.Font(font_path, size)
                except:
                    continue

    # 如果所有字体都失败，使用默认字体
    return pygame.font.Font(None, size)

font = get_chinese_font(36)       # 标准字体（用于按钮文字、UI信息）
small_font = get_chinese_font(20) # 小字体（用于塔名称、说明文字）
large_font = get_chinese_font(72) # 大字体（用于标题）

# ================================
# 形状绘制函数
# 说明：用于绘制不同形状的防御塔，每种塔有独特的形状以便区分
# 参数：
#   - surface: 绘制表面（通常是screen）
#   - color: 填充颜色（RGB）
#   - center: 中心点坐标（元组）
#   - size: 形状大小（半径）
# ================================

# 绘制三角形（箭塔形状）
def draw_triangle(surface, color, center, size):
    # 定义三角形三个顶点坐标
    points = [
        (center[0], center[1] - size),      # 顶点（朝上）
        (center[0] - size, center[1] + size), # 左下角
        (center[0] + size, center[1] + size)  # 右下角
    ]
    pygame.draw.polygon(surface, color, points)           # 填充形状颜色
    pygame.draw.polygon(surface, (255, 255, 255), points, 2)  # 绘制白色边框（宽度2像素）

# 绘制六边形（炮塔形状）
def draw_hexagon(surface, color, center, size):
    points = []
    # 六边形有6个顶点，每个间隔60度
    for i in range(6):
        angle = (i * 60 - 90) * math.pi / 180  # -90度使第一个顶点朝上
        x = center[0] + size * math.cos(angle)  # 计算X坐标
        y = center[1] + size * math.sin(angle)  # 计算Y坐标
        points.append((x, y))
    pygame.draw.polygon(surface, color, points)           # 填充颜色
    pygame.draw.polygon(surface, (255, 255, 255), points, 2)  # 白色边框

# 绘制菱形（冰塔形状）
def draw_diamond(surface, color, center, size):
    # 定义菱形四个顶点坐标
    points = [
        (center[0], center[1] - size),  # 上顶点
        (center[0] + size, center[1]),  # 右顶点
        (center[0], center[1] + size),  # 下顶点
        (center[0] - size, center[1])   # 左顶点
    ]
    pygame.draw.polygon(surface, color, points)           # 填充颜色
    pygame.draw.polygon(surface, (255, 255, 255), points, 2)  # 白色边框

# 绘制五角星（电塔形状）
def draw_star(surface, color, center, size):
    points = []
    # 五角星有5个顶点，每个间隔72度
    for i in range(5):
        angle = (i * 72 - 90) * math.pi / 180  # -90度使第一个顶点朝上
        x = center[0] + size * math.cos(angle)  # 计算X坐标
        y = center[1] + size * math.sin(angle)  # 计算Y坐标
        points.append((x, y))
    pygame.draw.polygon(surface, color, points)           # 填充颜色
    pygame.draw.polygon(surface, (255, 255, 255), points, 2)  # 白色边框

# 绘制八边形（魔法塔形状）
def draw_octagon(surface, color, center, size):
    points = []
    # 八边形有8个顶点，每个间隔45度
    for i in range(8):
        angle = (i * 45 - 22.5) * math.pi / 180  # -22.5度调整起始位置
        x = center[0] + size * math.cos(angle)  # 计算X坐标
        y = center[1] + size * math.sin(angle)  # 计算Y坐标
        points.append((x, y))
    pygame.draw.polygon(surface, color, points)           # 填充颜色
    pygame.draw.polygon(surface, (255, 255, 255), points, 2)  # 白色边框

# ================================
# 草地绘制函数
# ================================
def draw_grass_background():
    """绘制精美的草地背景"""
    # 先绘制基础深绿色背景
    screen.fill(COLORS['background'])

    # 绘制草地网格（基于预生成模式）
    for i in range(len(GRASS_PATTERN)):
        for j in range(len(GRASS_PATTERN[i])):
            grass_type = GRASS_PATTERN[i][j]
            color = GRASS_COLORS[grass_type]

            # 绘制草地格子
            x = i * GRID_SIZE
            y = j * GRID_SIZE
            rect = pygame.Rect(x, y, GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(screen, color, rect)

            # 添加草地纹理细节（格子边缘的深色线条）
            if j > 0 and GRASS_PATTERN[i][j-1] != grass_type:
                pygame.draw.line(screen, COLORS['grass_dark'], (x, y), (x + GRID_SIZE, y), 1)
            if i > 0 and GRASS_PATTERN[i-1][j] != grass_type:
                pygame.draw.line(screen, COLORS['grass_dark'], (x, y), (x, y + GRID_SIZE), 1)

    # 绘制草地点缀物
    for decoration in GRASS_DECORATIONS:
        grid_x = decoration['grid_x']
        grid_y = decoration['grid_y']
        x = grid_x * GRID_SIZE + decoration['offset_x']
        y = grid_y * GRID_SIZE + decoration['offset_y']

        if decoration['type'] == 'grass':
            # 绘制小草
            pygame.draw.line(screen, COLORS['grass_accent'], (x, y), (x, y - decoration['size']), 2)
        elif decoration['type'] == 'stone':
            # 绘制小石头
            pygame.draw.circle(screen, (80, 80, 70), (x, y), decoration['size'])
        elif decoration['type'] == 'flower':
            # 绘制小花
            pygame.draw.circle(screen, (255, 200, 100), (x, y), decoration['size'])
            pygame.draw.circle(screen, (255, 255, 200), (x, y), decoration['size'] - 1)

def is_path_grid(grid_x, grid_y):
    """检查指定网格是否在路径上"""
    for i in range(len(PATH_POINTS) - 1):
        x1, y1 = PATH_POINTS[i]
        x2, y2 = PATH_POINTS[i + 1]
        min_x, max_x = min(x1, x2), max(x1, x2)
        min_y, max_y = min(y1, y2), max(y1, y2)
        if min_x <= grid_x <= max_x and min_y <= grid_y <= max_y:
            return True
    return False

def draw_grass_details():
    """在路径周围绘制额外的草地细节"""
    # 在路径周围绘制一些深色的草地边缘效果
    for i in range(len(PATH_POINTS) - 1):
        x1, y1 = PATH_POINTS[i]
        x2, y2 = PATH_POINTS[i + 1]

        # 绘制路径边缘的深色草地
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                if dx == 0 and dy == 0:
                    continue

                # 检查当前格子是否接近路径但不在路径上
                if x1 + dx >= 0 and x1 + dx < int(SCREEN_WIDTH / GRID_SIZE):
                    if y1 + dy >= 0 and y1 + dy < int(SCREEN_HEIGHT / GRID_SIZE):
                        if not is_path_grid(x1 + dx, y1 + dy):
                            # 绘制深色草地边缘
                            edge_x = (x1 + dx) * GRID_SIZE
                            edge_y = (y1 + dy) * GRID_SIZE
                            # 只绘制部分区域作为边缘效果
                            if abs(dx) + abs(dy) == 1:  # 直接相邻
                                pygame.draw.rect(screen, COLORS['grass_dark'],
                                               (edge_x, edge_y, GRID_SIZE, GRID_SIZE), 1)

# 防御塔类
class Tower:
    def __init__(self, x, y, tower_type):
        # 将网格坐标转换为像素坐标
        self.x = x * GRID_SIZE + GRID_SIZE // 2
        self.y = y * GRID_SIZE + GRID_SIZE // 2
        self.type = tower_type              # 塔类型
        self.config = TOWER_CONFIG[tower_type]  # 塔配置
        self.last_attack_time = 0           # 上次攻击时间
        self.target = None                  # 当前攻击目标

    def draw(self):
        """绘制防御塔"""
        color = self.config['color']
        size = GRID_SIZE // 2 - 2

        # 根据塔类型绘制不同形状
        shape = self.config['shape']
        if shape == 'triangle':
            draw_triangle(screen, color, (self.x, self.y), size)
        elif shape == 'hexagon':
            draw_hexagon(screen, color, (self.x, self.y), size)
        elif shape == 'diamond':
            draw_diamond(screen, color, (self.x, self.y), size)
        elif shape == 'star':
            draw_star(screen, color, (self.x, self.y), size)
        elif shape == 'octagon':
            draw_octagon(screen, color, (self.x, self.y), size)

        # 绘制塔名称文字（添加背景让文字更清晰）
        name_text = small_font.render(self.config['name'], True, (255, 255, 255))
        text_rect = name_text.get_rect(center=(self.x, self.y + GRID_SIZE // 2 + 12))

        # 绘制文字背景（半透明黑色背景）
        background_rect = pygame.Rect(
            text_rect.left - 4,
            text_rect.top - 2,
            text_rect.width + 8,
            text_rect.height + 4
        )
        pygame.draw.rect(screen, (0, 0, 0, 180), background_rect)

        # 绘制文字
        screen.blit(name_text, text_rect)

        # 绘制攻击范围（选中时显示）
        if self == selected_tower:
            pygame.draw.circle(screen, (255, 255, 255, 50), (self.x, self.y), self.config['range'], 1)

    def update(self, enemies, current_time):
        """更新防御塔状态，寻找目标并攻击"""
        self.target = None
        min_dist = float('inf')

        # 在攻击范围内寻找最近的敌人
        for enemy in enemies:
            dist = math.hypot(self.x - enemy.x, self.y - enemy.y)
            if dist <= self.config['range'] and dist < min_dist:
                min_dist = dist
                self.target = enemy

        # 检查是否可以攻击（根据攻击速度）
        attack_interval = 1000 / self.config['attack_speed']
        if self.target and current_time - self.last_attack_time >= attack_interval:
            self.last_attack_time = current_time

            # 根据塔类型执行不同攻击
            if self.type == 'arrow':
                return self.shoot_arrows(enemies)
            elif self.type == 'ice':
                return self.shoot_ice(enemies)
            elif self.type == 'lightning':
                return self.shoot_lightning(enemies)
            elif self.type == 'cannon':
                return self.shoot_cannon()
            elif self.type == 'magic':
                return self.cast_magic()

        return None

    def shoot_arrows(self, enemies):
        """箭塔：发射三只箭矢，长方形弹幕"""
        bullets = []
        bullet_color = self.config.get('bullet_color', (139, 90, 43))
        arrow_count = self.config.get('arrow_count', 3)

        # 计算朝向目标的方向
        dx = self.target.x - self.x
        dy = self.target.y - self.y
        dist = math.hypot(dx, dy)
        angle = math.atan2(dy, dx)

        # 发射多支箭矢，有轻微角度偏移
        for i in range(arrow_count):
            offset_angle = (i - 1) * 0.1  # -0.1, 0, +0.1 弧度偏移
            bullet = ArrowBullet(self.x, self.y, self.target, self.config, angle + offset_angle)
            bullets.append(bullet)

        return bullets

    def shoot_ice(self, enemies):
        """冰塔：减速+叠加标记+冰爆"""
        return IceBullet(self.x, self.y, self.target, self.config, enemies)

    def shoot_lightning(self, enemies):
        """电塔：金色弹幕，链式攻击多个敌人"""
        bullet = LightningBullet(self.x, self.y, self.target, self.config, enemies)
        return bullet

    def shoot_cannon(self):
        """炮塔：瞄准敌人位置，落地后范围伤害"""
        # 创建一个瞄准目标当前位置的子弹
        target_x, target_y = self.target.x, self.target.y
        return CannonBullet(self.x, self.y, target_x, target_y, self.config)

    def cast_magic(self):
        """魔法塔：在敌人位置产生魔法柱"""
        magic_pillar = MagicPillar(self.target.x, self.target.y, self.config)
        return magic_pillar

# 基础子弹类
class Bullet:
    def __init__(self, x, y, target, config):
        self.x = x                      # 子弹当前X坐标
        self.y = y                      # 子弹当前Y坐标
        self.target = target            # 目标敌人
        self.config = config            # 发射该子弹的塔配置
        self.speed = 12                 # 子弹飞行速度
        self.active = True              # 子弹是否活跃
        self.color = config.get('bullet_color', config['color'])

    def update(self, enemies=None):
        """更新子弹位置，检测碰撞"""
        if not self.active or not self.target:
            self.active = False
            return None

        # 检查目标是否仍然活跃
        if hasattr(self.target, 'active') and not self.target.active:
            self.active = False
            return None

        # 计算朝向目标的方向
        dx = self.target.x - self.x
        dy = self.target.y - self.y
        dist = math.hypot(dx, dy)

        # 检测是否命中目标
        if dist < 10:
            try:
                self.target.take_damage(self.config['damage'])
            except Exception:
                pass
            self.active = False
            return self.target
        elif dist > 0:
            # 向目标移动
            self.x += (dx / dist) * self.speed
            self.y += (dy / dist) * self.speed

        return None

    def draw(self):
        """绘制子弹"""
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), 6)

# 箭塔子弹：长方形弹幕
class ArrowBullet(Bullet):
    def __init__(self, x, y, target, config, angle):
        super().__init__(x, y, target, config)
        self.angle = angle
        self.length = 8
        self.width = 3

    def update(self, enemies=None):
        """沿固定方向移动"""
        if not self.active:
            return None

        # 沿固定角度移动
        self.x += math.cos(self.angle) * self.speed
        self.y += math.sin(self.angle) * self.speed

        # 检查是否超出屏幕
        if self.x < 0 or self.x > SCREEN_WIDTH or self.y < 0 or self.y > SCREEN_HEIGHT:
            self.active = False
            return None

        # 检测与目标的碰撞
        if enemies is not None:
            for enemy in enemies:
                if not enemy.active:
                    continue
                dx = enemy.x - self.x
                dy = enemy.y - self.y
                dist = math.hypot(dx, dy)
                if dist < 20:
                    enemy.take_damage(self.config['damage'])
                    self.active = False
                    return enemy

        return None

    def draw(self):
        """绘制长方形子弹"""
        x, y = int(self.x), int(self.y)
        # 绘制旋转的长方形
        points = [
            (x + self.length * math.cos(self.angle), y + self.length * math.sin(self.angle)),
            (x + self.width * math.cos(self.angle + math.pi/2), y + self.width * math.sin(self.angle + math.pi/2)),
            (x - self.length * math.cos(self.angle), y - self.length * math.sin(self.angle)),
            (x - self.width * math.cos(self.angle + math.pi/2), y - self.width * math.sin(self.angle + math.pi/2))
        ]
        pygame.draw.polygon(screen, self.color, points)

# 冰塔子弹：减速+叠加标记+冰爆
class IceBullet(Bullet):
    def __init__(self, x, y, target, config, enemies):
        super().__init__(x, y, target, config)
        self.enemies_list = enemies if enemies else []
        self.slow_factor = config.get('slow_factor', 0.35)
        self.max_stacks = config.get('max_stacks', 3)
        self.explosion_radius = config.get('ice_explosion_radius', 80)
        self.explosion_damage_pct = config.get('ice_explosion_damage_pct', 0.05)
        self.hit_explosion = False
        self.explosion_x = 0
        self.explosion_y = 0

    def update(self, enemies=None):
        if not self.active or not self.target:
            self.active = False
            return None

        if enemies is not None:
            self.enemies_list = enemies

        # 检查目标是否仍然活跃
        if hasattr(self.target, 'active') and not self.target.active:
            self.active = False
            return None

        # 计算朝向目标的方向
        dx = self.target.x - self.x
        dy = self.target.y - self.y
        dist = math.hypot(dx, dy)

        # 检测是否命中目标
        if dist < 10:
            # 处理冰弹命中逻辑
            self.handle_ice_hit()
            self.active = False
            return self.target
        elif dist > 0:
            # 向目标移动
            self.x += (dx / dist) * self.speed
            self.y += (dy / dist) * self.speed

        return None

    def handle_ice_hit(self):
        """处理冰弹命中逻辑"""
        try:
            if not hasattr(self.target, 'ice_stacks'):
                self.target.ice_stacks = 0

            # 增加标记层数
            self.target.ice_stacks += 1

            # 应用减速效果（减速35%）
            slow_duration = 2000  # 减速持续2秒
            if hasattr(self.target, 'slow_timer'):
                current_time = pygame.time.get_ticks()
                if self.target.slow_timer < current_time:
                    # 如果没有减速效果，设置新的减速
                    self.target.base_speed = self.target.speed
                self.target.speed = self.target.base_speed * (1 - self.slow_factor)
                self.target.slow_timer = current_time + slow_duration

            # 检查是否达到最大层数，触发冰爆
            if self.target.ice_stacks >= self.max_stacks:
                self.target.ice_stacks = 0  # 重置层数
                self.trigger_ice_explosion()

            # 造成基础伤害
            self.target.take_damage(self.config['damage'])
        except Exception as e:
            print(f"Ice hit error: {e}")

    def trigger_ice_explosion(self):
        """触发冰爆效果"""
        self.explosion_x = self.target.x
        self.explosion_y = self.target.y
        self.hit_explosion = True

        # 对主目标造成冰爆伤害（总生命值的5%）
        try:
            explosion_damage = int(self.target.max_health * self.explosion_damage_pct)
            self.target.take_damage(explosion_damage)
        except Exception:
            pass

        # 对范围内其他敌人造成伤害并附加标记
        for enemy in self.enemies_list:
            if enemy == self.target or not enemy.active:
                continue

            dx = enemy.x - self.explosion_x
            dy = enemy.y - self.explosion_y
            dist = math.hypot(dx, dy)

            if dist <= self.explosion_radius:
                # 对溅射目标造成冰爆伤害
                try:
                    explosion_damage = int(enemy.max_health * self.explosion_damage_pct)
                    enemy.take_damage(explosion_damage)

                    # 给溅射目标附加一层标记
                    if not hasattr(enemy, 'ice_stacks'):
                        enemy.ice_stacks = 0
                    enemy.ice_stacks = min(enemy.ice_stacks + 1, self.max_stacks)

                    # 应用减速效果
                    slow_duration = 2000
                    current_time = pygame.time.get_ticks()
                    if hasattr(enemy, 'slow_timer'):
                        if enemy.slow_timer < current_time:
                            enemy.base_speed = enemy.speed
                        enemy.speed = enemy.base_speed * (1 - self.slow_factor)
                        enemy.slow_timer = current_time + slow_duration
                except Exception as e:
                    print(f"Ice explosion error: {e}")

    def draw(self):
        """绘制冰弹"""
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), 5)
        # 绘制冰弹光晕效果
        pygame.draw.circle(screen, (150, 230, 255, 100), (int(self.x), int(self.y)), 10)

# 电塔子弹：链式攻击
class LightningBullet(Bullet):
    def __init__(self, x, y, target, config, enemies):
        super().__init__(x, y, target, config)
        self.enemies_list = enemies if enemies else []
        self.chain_count = config.get('chain_count', 4)
        self.chain_range = config.get('chain_range', 70)
        self.current_target = target
        self.hit_count = 1
        self.chain_complete = False

    def update(self, enemies=None):
        if not self.active:
            return None

        if enemies is not None:
            self.enemies_list = enemies

        # 检查当前目标是否有效
        if not self.current_target or (hasattr(self.current_target, 'active') and not self.current_target.active):
            self.active = False
            return None

        if not self.chain_complete:
            # 移动到当前目标
            dx = self.current_target.x - self.x
            dy = self.current_target.y - self.y
            dist = math.hypot(dx, dy)

            if dist < 10:
                # 命中目标
                try:
                    if hasattr(self.current_target, 'active') and self.current_target.active:
                        self.current_target.take_damage(self.config['damage'])
                except Exception:
                    pass
                self.hit_count += 1

                # 寻找下一个链式目标
                if self.hit_count <= self.chain_count:
                    self.find_next_target()
                else:
                    self.chain_complete = True
            elif dist > 0:
                self.x += (dx / dist) * self.speed
                self.y += (dy / dist) * self.speed
            else:
                self.chain_complete = True
        else:
            self.active = False

        return None

    def find_next_target(self):
        """寻找链式攻击的下一个目标"""
        min_dist = float('inf')
        next_target = None

        if not self.enemies_list or not self.current_target:
            self.chain_complete = True
            return

        try:
            for enemy in self.enemies_list:
                if enemy != self.current_target and enemy.active:
                    dist = math.hypot(enemy.x - self.current_target.x, enemy.y - self.current_target.y)
                    if dist <= self.chain_range and dist < min_dist:
                        min_dist = dist
                        next_target = enemy
        except Exception:
            next_target = None

        if next_target:
            self.x, self.y = self.current_target.x, self.current_target.y
            self.current_target = next_target
        else:
            self.chain_complete = True

    def draw(self):
        """绘制金色闪电子弹"""
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), 8)
        # 绘制闪电特效
        for i in range(3):
            offset_x = random.randint(-3, 3)
            offset_y = random.randint(-3, 3)
            pygame.draw.circle(screen, (255, 255, 200), (int(self.x) + offset_x, int(self.y) + offset_y), 4)

# 炮塔子弹：瞄准位置，落地后范围伤害
class CannonBullet(Bullet):
    def __init__(self, x, y, target_x, target_y, config):
        super().__init__(x, y, None, config)
        self.target_x = target_x
        self.target_y = target_y
        self.exploded = False
        self.explosion_radius = config.get('splash_radius', 60)

    def update(self, enemies=None):
        if not self.active:
            return None

        if not self.exploded:
            dx = self.target_x - self.x
            dy = self.target_y - self.y
            dist = math.hypot(dx, dy)

            if dist < 15:
                # 到达目标位置，产生爆炸
                self.exploded = True
                # 对范围内所有敌人造成伤害
                if enemies is not None:
                    for enemy in enemies:
                        if not enemy.active:
                            continue
                        edx = enemy.x - self.x
                        edy = enemy.y - self.y
                        e_dist = math.hypot(edx, edy)
                        if e_dist <= self.explosion_radius:
                            enemy.take_damage(self.config['damage'])
            else:
                self.x += (dx / dist) * self.speed
                self.y += (dy / dist) * self.speed
        else:
            # 爆炸效果持续一段时间后消失
            self.active = False

        return None

    def draw(self):
        if not self.exploded:
            # 绘制炮弹
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), 10)
        else:
            # 绘制爆炸效果
            pygame.draw.circle(screen, (255, 100, 50), (int(self.x), int(self.y)), int(self.explosion_radius * 0.5))
            pygame.draw.circle(screen, (255, 200, 100), (int(self.x), int(self.y)), int(self.explosion_radius * 0.3))

# 魔法柱类
class MagicPillar:
    def __init__(self, x, y, config):
        self.x = x
        self.y = y
        self.config = config
        self.radius = config.get('magic_radius', 50)
        self.active = True
        self.duration = 500  # 持续时间（毫秒）
        self.start_time = pygame.time.get_ticks()

    def update(self, enemies=None):
        current_time = pygame.time.get_ticks()
        if current_time - self.start_time >= self.duration:
            self.active = False
            return None

        # 对范围内敌人造成伤害
        if enemies is not None:
            for enemy in enemies:
                if not enemy.active:
                    continue
                dx = enemy.x - self.x
                dy = enemy.y - self.y
                dist = math.hypot(dx, dy)
                if dist <= self.radius:
                    enemy.take_damage(self.config['damage'])

        return None

    def draw(self):
        # 绘制魔法柱效果
        current_time = pygame.time.get_ticks()
        progress = (current_time - self.start_time) / self.duration

        # 外圈
        pygame.draw.circle(screen, (180, 100, 255, int(200 * (1 - progress))),
                          (int(self.x), int(self.y)), int(self.radius * (0.8 + progress * 0.2)), 2)
        # 内圈
        pygame.draw.circle(screen, (150, 80, 220, int(150 * (1 - progress))),
                          (int(self.x), int(self.y)), int(self.radius * 0.5))
        # 中心
        pygame.draw.circle(screen, (200, 150, 255), (int(self.x), int(self.y)), 8)

# 敌人类
class Enemy:
    def __init__(self, enemy_type, path_index=0, wave_num=1):
        self.type = enemy_type          # 敌人类型
        self.config = ENEMY_CONFIG[enemy_type]  # 敌人配置

        # 根据波次增强敌人属性
        wave_multiplier = 1 + (wave_num - 1) * 0.1  # 每波增加10%属性

        self.max_health = int(self.config['health'] * wave_multiplier)  # 最大生命值（随波次增加）
        self.health = self.max_health   # 当前生命值
        self.speed = self.config['speed'] * min(wave_multiplier, 2)    # 当前移动速度（最高提升100%）
        self.base_speed = self.speed     # 基础移动速度
        self.reward = int(self.config['reward'] * wave_multiplier)     # 击杀奖励（随波次增加）
        self.path_index = path_index    # 当前所在路径点索引
        self.x, self.y = self.get_position()    # 当前位置
        self.slow_timer = 0             # 减速效果剩余时间
        self.freeze_timer = 0           # 冰冻效果剩余时间
        self.active = True              # 是否活跃

        # 根据波次改变外观
        self.wave_num = wave_num
        self.size = int(15 + (wave_num - 1) * 0.5)  # 敌人大小随波次增加（最大25）
        self.size = min(self.size, 25)

        # 根据波次改变颜色（颜色变深表示更强）
        base_color = self.config['color']
        darken_factor = min(wave_num * 0.05, 0.4)  # 最多变暗40%
        self.color = (
            max(0, int(base_color[0] * (1 - darken_factor))),
            max(0, int(base_color[1] * (1 - darken_factor))),
            max(0, int(base_color[2] * (1 - darken_factor)))
        )

        # 波次光环效果（高波次敌人有发光效果）
        self.has_aura = wave_num >= 5
        self.aura_color = (255, 200, 100) if wave_num >= 10 else (200, 150, 255)

    def get_position(self):
        """根据路径索引获取当前位置"""
        if self.path_index < len(PATH_POINTS):
            x, y = PATH_POINTS[self.path_index]
            return x * GRID_SIZE + GRID_SIZE // 2, y * GRID_SIZE + GRID_SIZE // 2
        return SCREEN_WIDTH, SCREEN_HEIGHT // 2  # 默认位置

    def update(self, current_time):
        """更新敌人位置，沿路径移动"""
        # 检查是否到达终点
        if self.path_index >= len(PATH_POINTS):
            self.active = False
            return True  # 到达终点

        # 检查是否被冰冻
        if self.freeze_timer > current_time:
            return False  # 被冰冻，不移动

        # 获取下一个路径点
        target_x, target_y = PATH_POINTS[self.path_index]
        target_x = target_x * GRID_SIZE + GRID_SIZE // 2
        target_y = target_y * GRID_SIZE + GRID_SIZE // 2

        # 计算朝向目标的方向
        dx = target_x - self.x
        dy = target_y - self.y
        dist = math.hypot(dx, dy)

        # 到达当前路径点，移动到下一个
        if dist < 5:
            self.path_index += 1
        else:
            # 计算实际速度（考虑减速效果）
            speed = self.speed
            if self.slow_timer > current_time:
                speed *= 0.5  # 减速50%
            # 向目标移动
            self.x += (dx / dist) * speed
            self.y += (dy / dist) * speed

        return False  # 未到达终点

    def take_damage(self, damage):
        """受到伤害"""
        self.health -= damage
        if self.health <= 0:
            self.active = False

    def slow(self, factor):
        """应用减速效果（持续2秒）"""
        self.slow_timer = pygame.time.get_ticks() + 2000

    def freeze(self, duration):
        """应用冰冻效果"""
        self.freeze_timer = pygame.time.get_ticks() + duration

    def draw(self):
        """绘制敌人（外观随波次变化）"""
        # 绘制光环效果（高波次敌人）
        if self.has_aura:
            # 外层光晕
            aura_size = self.size + 15
            pygame.draw.circle(screen, (self.aura_color[0], self.aura_color[1], self.aura_color[2], 50),
                              (int(self.x), int(self.y)), aura_size)
            # 内层光晕
            aura_size = self.size + 8
            pygame.draw.circle(screen, (self.aura_color[0], self.aura_color[1], self.aura_color[2], 80),
                              (int(self.x), int(self.y)), aura_size)

        # 绘制敌人主体（大小随波次变化）
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size)

        # 绘制敌人边框（高波次敌人有金色边框）
        if self.wave_num >= 5:
            pygame.draw.circle(screen, (255, 215, 0), (int(self.x), int(self.y)), self.size, 2)
        else:
            pygame.draw.circle(screen, (255, 255, 255), (int(self.x), int(self.y)), self.size, 1)

        # 绘制生命值条背景
        bar_width = 30
        bar_height = 5
        pygame.draw.rect(screen, (0, 0, 0), (self.x - bar_width // 2, self.y - 25, bar_width, bar_height))

        # 根据生命值比例决定颜色
        health_ratio = self.health / self.max_health
        bar_color = (0, 255, 0) if health_ratio > 0.5 else (255, 255, 0) if health_ratio > 0.25 else (255, 0, 0)
        pygame.draw.rect(screen, bar_color, (self.x - bar_width // 2, self.y - 25, bar_width * health_ratio, bar_height))

# 游戏主类
class Game:
    def __init__(self):
        self.level = 'level_1'           # 当前关卡
        self.gold = LEVEL_CONFIG[self.level]['start_gold']  # 当前金币
        self.lives = LEVEL_CONFIG[self.level]['lives']      # 当前生命值
        self.towers = []                 # 防御塔列表
        self.enemies = []                # 敌人列表
        self.bullets = []                # 子弹列表
        self.selected_tower_type = None  # 选中的塔类型（用于建造）
        self.selected_tower = None       # 选中的塔（用于查看信息）
        self.wave_index = 0              # 当前波次索引（已开始的波次）
        self.enemy_index = 0             # 当前波次内敌人索引
        self.last_spawn_time = 0         # 上次生成敌人时间
        self.game_state = 'menu'         # 游戏状态：menu, preparing, playing, paused, victory, defeat
        self.wave_in_progress = False    # 是否有波次正在进行
        self.score = 0                   # 当前分数
        self.victory_time = 0            # 胜利界面开始时间
        self.confirm_dialog = None       # 确认对话框状态：None, 'restart', 'main_menu'
        self.pre_dialog_state = None     # 弹出对话框前的游戏状态

    def draw_grid(self):
        """绘制网格线 - 针对草地主题优化"""
        # 绘制淡色的网格线，与草地融合
        for x in range(0, SCREEN_WIDTH, GRID_SIZE):
            pygame.draw.line(screen, COLORS['grid'], (x, 0), (x, SCREEN_HEIGHT), 1)
        for y in range(0, SCREEN_HEIGHT, GRID_SIZE):
            pygame.draw.line(screen, COLORS['grid'], (0, y), (SCREEN_WIDTH, y), 1)

    def draw_path(self):
        """绘制敌人行进路径和箭头指示 - 针对草地主题优化"""
        # 绘制路径线段
        for i in range(len(PATH_POINTS) - 1):
            x1, y1 = PATH_POINTS[i]
            x2, y2 = PATH_POINTS[i + 1]

            # 绘制路径主体
            pygame.draw.line(screen, COLORS['path'],
                            (x1 * GRID_SIZE + GRID_SIZE // 2, y1 * GRID_SIZE + GRID_SIZE // 2),
                            (x2 * GRID_SIZE + GRID_SIZE // 2, y2 * GRID_SIZE + GRID_SIZE // 2),
                            GRID_SIZE)

            # 绘制路径边缘的深色线条，增加立体感
            pygame.draw.line(screen, COLORS['path_dark'],
                           (x1 * GRID_SIZE + GRID_SIZE // 2, y1 * GRID_SIZE + GRID_SIZE // 2),
                           (x2 * GRID_SIZE + GRID_SIZE // 2, y2 * GRID_SIZE + GRID_SIZE // 2),
                           2)

            # 计算线段中点（用于放置箭头）
            mid_x = (x1 + x2) * GRID_SIZE // 2 + GRID_SIZE // 2
            mid_y = (y1 + y2) * GRID_SIZE // 2 + GRID_SIZE // 2

            # 计算路径方向角度
            angle = math.atan2(y2 - y1, x2 - x1)

            # 绘制方向箭头
            arrow_size = 10
            pygame.draw.polygon(screen, (200, 180, 150), [
                (mid_x + arrow_size * math.cos(angle), mid_y + arrow_size * math.sin(angle)),
                (mid_x + arrow_size * math.cos(angle + 2.0), mid_y + arrow_size * math.sin(angle + 2.0)),
                (mid_x + arrow_size * math.cos(angle - 2.0), mid_y + arrow_size * math.sin(angle - 2.0))
            ])

        # 绘制起点和终点标记
        start_x, start_y = PATH_POINTS[0]
        end_x, end_y = PATH_POINTS[-1]
        pygame.draw.circle(screen, (0, 255, 0), (start_x * GRID_SIZE + GRID_SIZE // 2, start_y * GRID_SIZE + GRID_SIZE // 2), 15)
        pygame.draw.circle(screen, (255, 0, 0), (end_x * GRID_SIZE + GRID_SIZE // 2, end_y * GRID_SIZE + GRID_SIZE // 2), 15)
        start_text = small_font.render("起点", True, (0, 255, 0))
        end_text = small_font.render("终点", True, (255, 0, 0))
        screen.blit(start_text, (start_x * GRID_SIZE + GRID_SIZE // 2 - 20, start_y * GRID_SIZE - 10))
        screen.blit(end_text, (end_x * GRID_SIZE + GRID_SIZE // 2 - 20, end_y * GRID_SIZE - 10))

    def can_place_tower(self, grid_x, grid_y):
        """检查指定位置是否可以放置防御塔"""
        # 检查是否在路径上
        for i in range(len(PATH_POINTS) - 1):
            x1, y1 = PATH_POINTS[i]
            x2, y2 = PATH_POINTS[i + 1]

            min_x, max_x = min(x1, x2), max(x1, x2)
            min_y, max_y = min(y1, y2), max(y1, y2)

            if min_x <= grid_x <= max_x and min_y <= grid_y <= max_y:
                return False  # 不能放在路径上

        # 检查是否与已有塔重叠
        for tower in self.towers:
            tower_grid_x = int((tower.x - GRID_SIZE // 2) // GRID_SIZE)
            tower_grid_y = int((tower.y - GRID_SIZE // 2) // GRID_SIZE)
            if tower_grid_x == grid_x and tower_grid_y == grid_y:
                return False  # 已有塔在此位置

        return True  # 可以放置

    def reset_to_prepare(self):
        """重置到关卡开始时的状态（清空塔、重置生命值和金币）"""
        self.towers = []                 # 清空所有塔
        self.enemies = []                # 清空所有敌人
        self.bullets = []                # 清空所有子弹
        self.wave_index = 0              # 重置波次索引
        self.enemy_index = 0             # 重置敌人索引
        self.last_spawn_time = 0         # 重置生成时间
        self.wave_in_progress = False    # 重置波次状态
        self.lives = LEVEL_CONFIG[self.level]['lives']      # 重置生命值
        self.gold = LEVEL_CONFIG[self.level]['start_gold']  # 重置金币到初始值
        self.game_state = 'preparing'    # 设置为准备状态

    def spawn_enemy(self, enemy_type='normal'):
        """生成一个敌人（带有波次增强）"""
        enemy = Enemy(enemy_type, wave_num=self.wave_index + 1)
        self.enemies.append(enemy)

    def update_wave(self, current_time):
        """更新波次状态，控制敌人生成"""
        if self.game_state != 'playing':
            return

        level = LEVEL_CONFIG[self.level]

        # 检查是否所有波次都已完成
        if self.wave_index >= len(level['waves']):
            if not self.enemies:
                self.wave_in_progress = False
                self.game_state = 'victory'
                self.victory_time = current_time
            return

        wave = level['waves'][self.wave_index]

        # 开始新波次（游戏开始后立即开始）
        if not self.wave_in_progress:
            self.wave_in_progress = True
            self.enemy_index = 0
            self.last_spawn_time = current_time

        # 按间隔生成敌人
        if self.enemy_index < wave['count']:
            if current_time - self.last_spawn_time >= wave['delay']:
                self.spawn_enemy(wave['type'])
                self.enemy_index += 1
                self.last_spawn_time = current_time
        else:
            # 当前波次敌人全部生成完毕，检查是否所有敌人已打完
            if not self.enemies:
                self.wave_index += 1
                self.wave_in_progress = False

    def update(self):
        """更新游戏状态"""
        current_time = pygame.time.get_ticks()

        # 如果显示确认对话框，暂停游戏更新
        if self.confirm_dialog:
            return

        if self.game_state != 'playing':
            return

        # 更新波次（无倒计时，直接开始）
        self.update_wave(current_time)

        # 更新敌人
        for enemy in self.enemies[:]:
            reached_end = enemy.update(current_time)
            if reached_end:
                # 敌人到达终点，减少生命值
                self.lives -= 1
                self.enemies.remove(enemy)
                if self.lives <= 0:
                    self.game_state = 'defeat'  # 失败
            elif not enemy.active:
                # 敌人被击杀，获得奖励
                self.gold += enemy.reward
                self.score += enemy.reward * 10  # 击杀敌人获得分数
                self.enemies.remove(enemy)

        # 更新防御塔
        for tower in self.towers:
            result = tower.update(self.enemies, current_time)
            if result:
                if isinstance(result, list):
                    # 箭塔返回多个子弹
                    self.bullets.extend(result)
                else:
                    # 其他塔返回单个子弹或魔法柱
                    self.bullets.append(result)

        # 更新子弹
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

        if self.game_state == 'tower_intro':
            self.draw_tower_intro()
            return

        if self.game_state == 'tower_detail':
            self.draw_tower_detail(self.selected_tower_type)
            return

        # 使用草地背景替代纯色背景
        draw_grass_background()
        draw_grass_details()
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
            pygame.draw.rect(screen, (0, 0, 0, 180), (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
            victory_text = font.render("🎉 胜利！", True, (255, 215, 0))
            victory_text_rect = victory_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100))
            screen.blit(victory_text, victory_text_rect)

            score_text = font.render(f"🏆 分数: {self.score}", True, (200, 200, 255))
            score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
            screen.blit(score_text, score_rect)

            restart_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 10, 140, 50)
            pygame.draw.rect(screen, (80, 180, 80), restart_button_rect)
            pygame.draw.rect(screen, (255, 255, 255), restart_button_rect, 3)
            restart_text = font.render("重新开始", True, COLORS['text'])
            restart_text_rect = restart_text.get_rect(center=restart_button_rect.center)
            screen.blit(restart_text, restart_text_rect)

            level_list = list(LEVEL_CONFIG.keys())
            current_level_idx = level_list.index(self.level) if self.level in level_list else 0
            has_next_level = current_level_idx < len(level_list) - 1

            next_button_rect = pygame.Rect(SCREEN_WIDTH // 2 + 10, SCREEN_HEIGHT // 2 + 10, 140, 50)
            if has_next_level:
                pygame.draw.rect(screen, (80, 100, 180), next_button_rect)
            else:
                pygame.draw.rect(screen, (80, 80, 80), next_button_rect)
            pygame.draw.rect(screen, (255, 255, 255), next_button_rect, 3)
            next_text = font.render("下一关" if has_next_level else "已是最后", True, COLORS['text'])
            next_text_rect = next_text.get_rect(center=next_button_rect.center)
            screen.blit(next_text, next_text_rect)

            main_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 75, 300, 50)
            pygame.draw.rect(screen, (180, 80, 80), main_button_rect)
            pygame.draw.rect(screen, (255, 255, 255), main_button_rect, 3)
            main_text = font.render("返回主界面", True, COLORS['text'])
            main_text_rect = main_text.get_rect(center=main_button_rect.center)
            screen.blit(main_text, main_text_rect)

        if self.game_state == 'preparing':
            # 半透明覆盖层
            transparent_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            transparent_surface.fill((0, 0, 0, 80))
            screen.blit(transparent_surface, (0, 0))

            prepare_text = large_font.render("准备就绪", True, (255, 215, 0))
            prepare_rect = prepare_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 60))
            screen.blit(prepare_text, prepare_rect)

            start_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2, 200, 50)
            pygame.draw.rect(screen, (80, 180, 80), start_button_rect)
            pygame.draw.rect(screen, (255, 255, 255), start_button_rect, 3)
            start_text = font.render("开始游戏", True, COLORS['text'])
            start_text_rect = start_text.get_rect(center=start_button_rect.center)
            screen.blit(start_text, start_text_rect)

        if self.game_state == 'paused':
            transparent_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            transparent_surface.fill((0, 0, 0, 40))
            screen.blit(transparent_surface, (0, 0))

            pause_text = large_font.render("游戏暂停", True, (255, 255, 255))
            pause_rect = pause_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 60))
            screen.blit(pause_text, pause_rect)

            resume_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2, 200, 50)
            button_surface = pygame.Surface((200, 50), pygame.SRCALPHA)
            button_surface.fill((80, 80, 180, 200))
            screen.blit(button_surface, resume_button_rect)
            pygame.draw.rect(screen, (255, 255, 255), resume_button_rect, 3)
            resume_text = font.render("继续游戏", True, COLORS['text'])
            resume_text_rect = resume_text.get_rect(center=resume_button_rect.center)
            screen.blit(resume_text, resume_text_rect)

            key_text = font.render("点击空白处继续", True, (200, 200, 200))
            key_rect = key_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 70))
            screen.blit(key_text, key_rect)

    def draw_menu(self):
        # 使用深绿色背景
        screen.fill((20, 50, 20))

        title_text = large_font.render("鸿蒙防线", True, (255, 215, 0))
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 80))
        screen.blit(title_text, title_rect)

        start_hint_text = font.render("按空白处进入游戏", True, (200, 200, 200))
        start_hint_rect = start_hint_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(start_hint_text, start_hint_rect)

        tower_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 60, 200, 50)
        pygame.draw.rect(screen, (80, 100, 180), tower_button_rect)
        pygame.draw.rect(screen, (255, 255, 255), tower_button_rect, 3)
        tower_button_text = font.render("查看防御塔", True, COLORS['text'])
        tower_button_text_rect = tower_button_text.get_rect(center=tower_button_rect.center)
        screen.blit(tower_button_text, tower_button_text_rect)

    def draw_level_select(self):
        """绘制关卡选择界面"""
        # 使用深绿色背景
        screen.fill((20, 50, 20))

        # 标题
        title_text = large_font.render("选择关卡", True, (255, 215, 0))
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 120))
        screen.blit(title_text, title_rect)

        # 返回主菜单按钮
        back_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 120, 200, 50)
        pygame.draw.rect(screen, (80, 100, 180), back_button_rect)
        pygame.draw.rect(screen, (255, 255, 255), back_button_rect, 3)
        back_text = font.render("返回主菜单", True, COLORS['text'])
        back_text_rect = back_text.get_rect(center=back_button_rect.center)
        screen.blit(back_text, back_text_rect)

        # 关卡按钮
        levels = list(LEVEL_CONFIG.items())
        level_button_y = SCREEN_HEIGHT // 2 - 40

        for i, (level_id, config) in enumerate(levels):
            level_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 150 + (i % 2) * 320, level_button_y, 280, 80)
            pygame.draw.rect(screen, (60, 80, 100), level_button_rect)
            pygame.draw.rect(screen, (255, 255, 255), level_button_rect, 3)

            # 关卡名称
            level_name = font.render(config['name'], True, (255, 215, 0))
            level_name_rect = level_name.get_rect(center=(level_button_rect.centerx, level_button_rect.top + 25))
            screen.blit(level_name, level_name_rect)

            # 关卡信息
            wave_count = len(config['waves'])
            info_text = small_font.render(f"波次: {wave_count} | 金币: {config['start_gold']} | 生命: {config['lives']}",
                                        True, (200, 200, 200))
            info_rect = info_text.get_rect(center=(level_button_rect.centerx, level_button_rect.top + 55))
            screen.blit(info_text, info_rect)

    def draw_tower_intro(self):
        """绘制防御塔介绍界面"""
        # 使用深绿色背景
        screen.fill((20, 50, 20))

        # 标题
        title_text = large_font.render("防御塔介绍", True, (255, 215, 0))
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 60))
        screen.blit(title_text, title_rect)

        # 返回按钮
        back_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - 80, 200, 50)
        pygame.draw.rect(screen, (180, 80, 80), back_button_rect)
        pygame.draw.rect(screen, (255, 255, 255), back_button_rect, 3)
        back_text = font.render("返回主菜单", True, COLORS['text'])
        back_text_rect = back_text.get_rect(center=back_button_rect.center)
        screen.blit(back_text, back_text_rect)

        # 五个塔的按钮
        tower_types = list(TOWER_CONFIG.items())
        start_x = SCREEN_WIDTH // 2 - 220

        for i, (tower_id, config) in enumerate(tower_types):
            tower_button_rect = pygame.Rect(start_x + i * 110, SCREEN_HEIGHT // 2 - 80, 90, 120)
            pygame.draw.rect(screen, config['color'], tower_button_rect)
            pygame.draw.rect(screen, (255, 255, 255), tower_button_rect, 3)

            # 塔名称
            name_text = small_font.render(config['name'], True, COLORS['text'])
            name_text_rect = name_text.get_rect(center=(tower_button_rect.centerx, tower_button_rect.top + 20))
            screen.blit(name_text, name_text_rect)

            # 价格
            price_text = small_font.render(f"{config['cost']}金", True, (255, 215, 0))
            price_text_rect = price_text.get_rect(center=(tower_button_rect.centerx, tower_button_rect.top + 95))
            screen.blit(price_text, price_text_rect)

            # 伤害
            damage_text = small_font.render(f"⚔️{config['damage']}", True, (255, 150, 150))
            damage_text_rect = damage_text.get_rect(center=(tower_button_rect.centerx, tower_button_rect.top + 50))
            screen.blit(damage_text, damage_text_rect)

            # 范围
            range_text = small_font.render(f"📡{config['range']}", True, (150, 200, 255))
            range_text_rect = range_text.get_rect(center=(tower_button_rect.centerx, tower_button_rect.top + 70))
            screen.blit(range_text, range_text_rect)

    def draw_tower_detail(self, tower_id):
        """绘制单个塔的详细介绍界面"""
        # 使用深绿色背景
        screen.fill((20, 50, 20))

        config = TOWER_CONFIG.get(tower_id)
        if not config:
            return

        # 标题
        title_text = large_font.render(config['name'], True, config['color'])
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 60))
        screen.blit(title_text, title_rect)

        # 返回按钮
        back_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - 80, 200, 50)
        pygame.draw.rect(screen, (180, 80, 80), back_button_rect)
        pygame.draw.rect(screen, (255, 255, 255), back_button_rect, 3)
        back_text = font.render("返回", True, COLORS['text'])
        back_text_rect = back_text.get_rect(center=back_button_rect.center)
        screen.blit(back_text, back_text_rect)

        # 塔的信息卡片
        info_box_rect = pygame.Rect(SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 - 150, 400, 260)
        pygame.draw.rect(screen, (60, 80, 100), info_box_rect)
        pygame.draw.rect(screen, (255, 255, 255), info_box_rect, 3)

        # 价格
        price_text = font.render(f"💰 价格: {config['cost']} 金币", True, (255, 215, 0))
        screen.blit(price_text, (SCREEN_WIDTH // 2 - 180, SCREEN_HEIGHT // 2 - 120))

        # 伤害
        damage_text = font.render(f"⚔️ 伤害: {config['damage']}", True, (255, 150, 150))
        screen.blit(damage_text, (SCREEN_WIDTH // 2 - 180, SCREEN_HEIGHT // 2 - 80))

        # 攻击范围
        range_text = font.render(f"📡 攻击范围: {config['range']}", True, (150, 200, 255))
        screen.blit(range_text, (SCREEN_WIDTH // 2 - 180, SCREEN_HEIGHT // 2 - 40))

        # 攻击速度
        speed_text = font.render(f"⚡ 攻击速度: {config['attack_speed']}/秒", True, (255, 255, 150))
        screen.blit(speed_text, (SCREEN_WIDTH // 2 - 180, SCREEN_HEIGHT // 2))

        # 特殊效果
        effect_text = font.render(f"✨ 特殊效果:", True, (200, 150, 255))
        screen.blit(effect_text, (SCREEN_WIDTH // 2 - 180, SCREEN_HEIGHT // 2 + 40))

        # 特殊效果描述
        descriptions = {
            'arrow': '发射三支箭矢，呈三角形散开，可同时攻击多个敌人',
            'ice': '减速敌人35%并叠加标记，三层后触发冰爆造成范围伤害',
            'lightning': '发射金色闪电，可链式攻击最多4个敌人',
            'cannon': '发射炮弹瞄准敌人位置，落地后产生范围爆炸伤害',
            'magic': '在敌人位置产生魔法柱，持续造成范围伤害'
        }
        desc = descriptions.get(tower_id, '无特殊效果')
        desc_lines = []
        words = desc.split('，')
        current_line = ''
        for word in words:
            if len(current_line + word) <= 20:
                current_line += word + '，'
            else:
                desc_lines.append(current_line[:-1])
                current_line = word + '，'
        if current_line:
            desc_lines.append(current_line[:-1])

        for i, line in enumerate(desc_lines[:3]):
            desc_text = small_font.render(line, True, (200, 200, 200))
            screen.blit(desc_text, (SCREEN_WIDTH // 2 - 175, SCREEN_HEIGHT // 2 + 75 + i * 25))

    def draw_ui(self):
        # 顶部状态栏背景 - 调整为深色以配合草地主题
        top_bar_rect = pygame.Rect(0, 0, SCREEN_WIDTH, 45)
        pygame.draw.rect(screen, (30, 60, 30), top_bar_rect)

        # 金币显示（左上角，带背景色块）
        gold_bg_rect = pygame.Rect(8, 5, 100, 35)
        pygame.draw.rect(screen, (40, 70, 45), gold_bg_rect)
        gold_text = font.render(f"💰 {self.gold}", True, COLORS['gold'])
        gold_text_rect = gold_text.get_rect(center=gold_bg_rect.center)
        screen.blit(gold_text, gold_text_rect)

        # 生命值显示（金币右侧，带背景色块）
        lives_bg_rect = pygame.Rect(116, 5, 100, 35)
        pygame.draw.rect(screen, (40, 70, 45), lives_bg_rect)
        lives_text = font.render(f"❤️ {self.lives}", True, COLORS['health'])
        lives_text_rect = lives_text.get_rect(center=lives_bg_rect.center)
        screen.blit(lives_text, lives_text_rect)

        # 波次信息（生命值右侧，带背景色块）
        level = LEVEL_CONFIG[self.level]
        wave_bg_rect = pygame.Rect(224, 5, 110, 35)
        pygame.draw.rect(screen, (40, 70, 45), wave_bg_rect)
        wave_text = font.render(f"🌊 {self.wave_index + 1}/{len(level['waves'])}", True, COLORS['text'])
        wave_text_rect = wave_text.get_rect(center=wave_bg_rect.center)
        screen.blit(wave_text, wave_text_rect)

        # 暂停按钮（波次信息右侧）- 图标形式
        pause_button_rect = pygame.Rect(342, 5, 60, 35)
        pygame.draw.rect(screen, (120, 80, 180), pause_button_rect)
        pygame.draw.rect(screen, (255, 255, 255), pause_button_rect, 2)
        # 绘制暂停图标（两个竖线）
        pygame.draw.rect(screen, (255, 255, 255), (pause_button_rect.centerx - 12, pause_button_rect.centery - 7, 6, 14))
        pygame.draw.rect(screen, (255, 255, 255), (pause_button_rect.centerx + 6, pause_button_rect.centery - 7, 6, 14))

        # 重新开始按钮（暂停按钮右侧）- 图标形式
        restart_button_rect = pygame.Rect(410, 5, 60, 35)
        pygame.draw.rect(screen, (180, 120, 80), restart_button_rect)
        pygame.draw.rect(screen, (255, 255, 255), restart_button_rect, 2)
        # 绘制重新开始图标（圆形箭头）
        pygame.draw.arc(screen, (255, 255, 255), (restart_button_rect.centerx - 10, restart_button_rect.centery - 10, 20, 20), 0.2, 6.1, 2)
        pygame.draw.polygon(screen, (255, 255, 255), [
            (restart_button_rect.centerx + 8, restart_button_rect.centery - 5),
            (restart_button_rect.centerx + 14, restart_button_rect.centery),
            (restart_button_rect.centerx + 8, restart_button_rect.centery + 3)
        ])

        # 返回主界面按钮（重新开始按钮右侧）- 图标形式
        main_menu_button_rect = pygame.Rect(478, 5, 60, 35)
        pygame.draw.rect(screen, (80, 100, 180), main_menu_button_rect)
        pygame.draw.rect(screen, (255, 255, 255), main_menu_button_rect, 2)
        # 绘制房子图标
        pygame.draw.polygon(screen, (255, 255, 255), [
            (main_menu_button_rect.centerx, main_menu_button_rect.centery - 10),
            (main_menu_button_rect.centerx - 12, main_menu_button_rect.centery + 2),
            (main_menu_button_rect.centerx - 12, main_menu_button_rect.centery + 8),
            (main_menu_button_rect.centerx + 12, main_menu_button_rect.centery + 8),
            (main_menu_button_rect.centerx + 12, main_menu_button_rect.centery + 2)
        ])
        pygame.draw.rect(screen, (255, 255, 255), (main_menu_button_rect.centerx - 5, main_menu_button_rect.centery + 2, 10, 6))

        # 绘制确认对话框
        if self.confirm_dialog:
            # 半透明背景
            dialog_bg = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            dialog_bg.fill((0, 0, 0, 150))
            screen.blit(dialog_bg, (0, 0))

            # 对话框面板
            dialog_rect = pygame.Rect(SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 - 80, 400, 160)
            pygame.draw.rect(screen, (60, 60, 80), dialog_rect)
            pygame.draw.rect(screen, (255, 255, 255), dialog_rect, 3)

            # 对话框标题
            if self.confirm_dialog == 'restart':
                dialog_title = font.render("确认重新开始？", True, (255, 255, 255))
            else:
                dialog_title = font.render("确认返回主菜单？", True, (255, 255, 255))
            title_rect = dialog_title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 40))
            screen.blit(dialog_title, title_rect)

            # 提示文字
            hint_text = small_font.render("当前进度将丢失", True, (200, 200, 200))
            hint_rect = hint_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(hint_text, hint_rect)

            # 确定按钮
            confirm_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT // 2 + 30, 100, 40)
            pygame.draw.rect(screen, (80, 180, 80), confirm_button_rect)
            pygame.draw.rect(screen, (255, 255, 255), confirm_button_rect, 2)
            confirm_text = font.render("确定", True, COLORS['text'])
            confirm_text_rect = confirm_text.get_rect(center=confirm_button_rect.center)
            screen.blit(confirm_text, confirm_text_rect)

            # 取消按钮
            cancel_button_rect = pygame.Rect(SCREEN_WIDTH // 2 + 20, SCREEN_HEIGHT // 2 + 30, 100, 40)
            pygame.draw.rect(screen, (180, 80, 80), cancel_button_rect)
            pygame.draw.rect(screen, (255, 255, 255), cancel_button_rect, 2)
            cancel_text = font.render("取消", True, COLORS['text'])
            cancel_text_rect = cancel_text.get_rect(center=cancel_button_rect.center)
            screen.blit(cancel_text, cancel_text_rect)

        # 右侧塔选择面板 - 调整为深色以配合草地主题
        panel_x = SCREEN_WIDTH - 180
        panel_y = 50
        panel_width = 170
        panel_height = 310

        pygame.draw.rect(screen, (30, 60, 35), (panel_x, panel_y, panel_width, panel_height))
        panel_title = small_font.render("防御塔", True, COLORS['text'])
        panel_title_rect = panel_title.get_rect(center=(panel_x + panel_width // 2, panel_y + 15))
        screen.blit(panel_title, panel_title_rect)

        y_offset = panel_y + 38
        item_height = 56

        for tower_type, config in TOWER_CONFIG.items():
            color = config['color'] if self.gold >= config['cost'] else (100, 100, 100)

            # 每个塔项的背景区域
            item_bg_rect = pygame.Rect(panel_x + 5, y_offset - 3, panel_width - 10, item_height - 6)
            if self.selected_tower_type == tower_type:
                pygame.draw.rect(screen, (50, 80, 60), item_bg_rect)
                pygame.draw.rect(screen, (255, 255, 255), item_bg_rect, 2)
            else:
                pygame.draw.rect(screen, (25, 50, 30), item_bg_rect)

            # 绘制不同形状的塔预览（居中）
            icon_center_x = panel_x + 28
            icon_center_y = y_offset + item_height // 2
            size = 16

            if config['shape'] == 'triangle':
                draw_triangle(screen, color, (icon_center_x, icon_center_y), size)
            elif config['shape'] == 'hexagon':
                draw_hexagon(screen, color, (icon_center_x, icon_center_y), size)
            elif config['shape'] == 'diamond':
                draw_diamond(screen, color, (icon_center_x, icon_center_y), size)
            elif config['shape'] == 'star':
                draw_star(screen, color, (icon_center_x, icon_center_y), size)
            elif config['shape'] == 'octagon':
                draw_octagon(screen, color, (icon_center_x, icon_center_y), size)

            # 塔名称（右侧区域居中）
            name_text = small_font.render(config['name'], True, COLORS['text'])
            name_rect = name_text.get_rect(left=panel_x + 62, centery=y_offset + 14)
            screen.blit(name_text, name_rect)

            # 塔价格（居中）
            cost_text = small_font.render(f"¥{config['cost']}", True, COLORS['gold'])
            cost_rect = cost_text.get_rect(left=panel_x + 62, centery=y_offset + 30)
            screen.blit(cost_text, cost_rect)

            # 塔属性简要信息（居中）
            attr_text = small_font.render(f"伤害:{config['damage']} 范围:{config['range']}", True, (150, 150, 150))
            attr_rect = attr_text.get_rect(left=panel_x + 62, centery=y_offset + 46)
            screen.blit(attr_text, attr_rect)

            y_offset += item_height

        # 选中塔的详细信息面板
        if self.selected_tower:
            info_x = SCREEN_WIDTH - 180
            info_y = 375
            info_width = 170
            info_height = 130

            pygame.draw.rect(screen, (30, 60, 40), (info_x, info_y, info_width, info_height))
            info_title = small_font.render("塔详情", True, COLORS['text'])
            info_title_rect = info_title.get_rect(center=(info_x + info_width // 2, info_y + 15))
            screen.blit(info_title, info_title_rect)

            config = self.selected_tower.config
            name_text = font.render(config['name'], True, COLORS['text'])
            damage_text = small_font.render(f"⚔️ 伤害: {config['damage']}", True, (255, 150, 150))
            range_text = small_font.render(f"📡 范围: {config['range']}", True, (150, 200, 255))
            speed_text = small_font.render(f"⚡ 攻速: {config['attack_speed']}/s", True, (255, 255, 150))

            # 文字居中显示
            name_text_rect = name_text.get_rect(center=(info_x + info_width // 2, info_y + 35))
            screen.blit(name_text, name_text_rect)

            damage_text_rect = damage_text.get_rect(center=(info_x + info_width // 2, info_y + 65))
            screen.blit(damage_text, damage_text_rect)

            range_text_rect = range_text.get_rect(center=(info_x + info_width // 2, info_y + 90))
            screen.blit(range_text, range_text_rect)

            speed_text_rect = speed_text.get_rect(center=(info_x + info_width // 2, info_y + 115))
            screen.blit(speed_text, speed_text_rect)

        if self.game_state == 'victory':
            pygame.draw.rect(screen, (0, 0, 0, 180), (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
            victory_text = font.render("🎉 胜利！", True, (255, 215, 0))
            victory_text_rect = victory_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100))
            screen.blit(victory_text, victory_text_rect)

            # 分数显示
            score_text = font.render(f"🏆 分数: {self.score}", True, (200, 200, 255))
            score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
            screen.blit(score_text, score_rect)

            # 重新开始按钮
            restart_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 10, 140, 50)
            pygame.draw.rect(screen, (80, 180, 80), restart_button_rect)
            pygame.draw.rect(screen, (255, 255, 255), restart_button_rect, 3)
            restart_text = font.render("重新开始", True, COLORS['text'])
            restart_text_rect = restart_text.get_rect(center=restart_button_rect.center)
            screen.blit(restart_text, restart_text_rect)

            # 下一关按钮
            level_list = list(LEVEL_CONFIG.keys())
            current_level_idx = level_list.index(self.level) if self.level in level_list else 0
            has_next_level = current_level_idx < len(level_list) - 1

            next_button_rect = pygame.Rect(SCREEN_WIDTH // 2 + 10, SCREEN_HEIGHT // 2 + 10, 140, 50)
            if has_next_level:
                pygame.draw.rect(screen, (80, 100, 180), next_button_rect)
            else:
                pygame.draw.rect(screen, (80, 80, 80), next_button_rect)
            pygame.draw.rect(screen, (255, 255, 255), next_button_rect, 3)
            next_text = font.render("下一关" if has_next_level else "已是最后", True, COLORS['text'])
            next_text_rect = next_text.get_rect(center=next_button_rect.center)
            screen.blit(next_text, next_text_rect)

            # 返回主界面按钮
            main_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 75, 300, 50)
            pygame.draw.rect(screen, (180, 80, 80), main_button_rect)
            pygame.draw.rect(screen, (255, 255, 255), main_button_rect, 3)
            main_text = font.render("返回主界面", True, COLORS['text'])
            main_text_rect = main_text.get_rect(center=main_button_rect.center)
            screen.blit(main_text, main_text_rect)

        elif self.game_state == 'defeat':
            pygame.draw.rect(screen, (0, 0, 0, 180), (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
            defeat_text = font.render("💀 失败！", True, (255, 100, 100))
            defeat_text_rect = defeat_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 30))
            screen.blit(defeat_text, defeat_text_rect)

            restart_text = small_font.render("点击鼠标重新开始", True, COLORS['text'])
            restart_text_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))
            screen.blit(restart_text, restart_text_rect)

selected_tower_type = None
selected_tower = None

def main():
    global selected_tower_type, selected_tower

    game = Game()
    running = True

    while running:
        current_time = pygame.time.get_ticks()

        try:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        if game.game_state == 'playing':
                            game.game_state = 'paused'
                    elif event.key == pygame.K_a:
                        if game.game_state == 'preparing':
                            game.game_state = 'playing'

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = event.pos

                    if game.game_state == 'menu':
                        # 查看防御塔按钮
                        tower_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 60, 200, 50)
                        if tower_button_rect.collidepoint(mouse_x, mouse_y):
                            game.game_state = 'tower_intro'
                            continue
                        # 点击空白处进入关卡选择
                        game.game_state = 'level_select'
                        continue

                    if game.game_state == 'tower_intro':
                        # 返回主菜单按钮
                        back_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - 80, 200, 50)
                        if back_button_rect.collidepoint(mouse_x, mouse_y):
                            game.game_state = 'menu'
                            continue

                        # 五个塔的按钮
                        tower_types = list(TOWER_CONFIG.items())
                        start_x = SCREEN_WIDTH // 2 - 220
                        for i, (tower_id, config) in enumerate(tower_types):
                            tower_button_rect = pygame.Rect(start_x + i * 110, SCREEN_HEIGHT // 2 - 80, 90, 120)
                            if tower_button_rect.collidepoint(mouse_x, mouse_y):
                                game.selected_tower_type = tower_id
                                game.game_state = 'tower_detail'
                                break
                        continue

                    if game.game_state == 'tower_detail':
                        # 返回按钮
                        back_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - 80, 200, 50)
                        if back_button_rect.collidepoint(mouse_x, mouse_y):
                            game.game_state = 'tower_intro'
                            continue

                    if game.game_state == 'level_select':
                        # 返回主菜单按钮
                        back_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 120, 200, 50)
                        if back_button_rect.collidepoint(mouse_x, mouse_y):
                            game.game_state = 'menu'
                            continue

                        # 关卡按钮
                        levels = list(LEVEL_CONFIG.items())
                        level_button_y = SCREEN_HEIGHT // 2 - 40
                        for i, (level_id, config) in enumerate(levels):
                            level_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 150 + (i % 2) * 320, level_button_y, 280, 80)
                            if level_button_rect.collidepoint(mouse_x, mouse_y):
                                game.level = level_id
                                game.__init__()
                                game.level = level_id
                                game.gold = LEVEL_CONFIG[level_id]['start_gold']
                                game.lives = LEVEL_CONFIG[level_id]['lives']
                                game.game_state = 'preparing'
                                break
                        continue

                    if game.game_state == 'preparing':
                        start_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2, 200, 50)
                        if start_button_rect.collidepoint(mouse_x, mouse_y):
                            game.game_state = 'playing'
                        continue

                    if game.game_state == 'paused':
                        resume_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2, 200, 50)
                        if resume_button_rect.collidepoint(mouse_x, mouse_y):
                            game.game_state = 'playing'
                            continue
                        else:
                            game.game_state = 'playing'
                        continue

                    if game.game_state == 'victory':
                        # 重新开始按钮
                        restart_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 10, 140, 50)
                        if restart_button_rect.collidepoint(mouse_x, mouse_y):
                            game.reset_to_prepare()
                            selected_tower_type = None
                            selected_tower = None
                            continue

                        # 下一关按钮
                        level_list = list(LEVEL_CONFIG.keys())
                        current_level_idx = level_list.index(game.level) if game.level in level_list else 0
                        has_next_level = current_level_idx < len(level_list) - 1

                        next_button_rect = pygame.Rect(SCREEN_WIDTH // 2 + 10, SCREEN_HEIGHT // 2 + 10, 140, 50)
                        if next_button_rect.collidepoint(mouse_x, mouse_y) and has_next_level:
                            next_level = level_list[current_level_idx + 1]
                            game.level = next_level
                            game.__init__()
                            game.level = next_level
                            game.gold = LEVEL_CONFIG[next_level]['start_gold']
                            game.lives = LEVEL_CONFIG[next_level]['lives']
                            game.game_state = 'preparing'
                            selected_tower_type = None
                            selected_tower = None
                            continue

                        # 返回主界面按钮
                        main_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 75, 300, 50)
                        if main_button_rect.collidepoint(mouse_x, mouse_y):
                            game.game_state = 'menu'
                            selected_tower_type = None
                            selected_tower = None
                            continue

                    if game.game_state == 'defeat':
                        game = Game()
                        selected_tower_type = None
                        selected_tower = None
                        continue

                    # 如果显示确认对话框，只处理对话框按钮
                    if game.confirm_dialog:
                        # 确定按钮
                        confirm_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT // 2 + 30, 100, 40)
                        if confirm_button_rect.collidepoint(mouse_x, mouse_y):
                            if game.confirm_dialog == 'restart':
                                game.reset_to_prepare()
                            elif game.confirm_dialog == 'main_menu':
                                game.game_state = 'menu'
                            game.confirm_dialog = None
                            selected_tower_type = None
                            selected_tower = None
                            continue

                        # 取消按钮
                        cancel_button_rect = pygame.Rect(SCREEN_WIDTH // 2 + 20, SCREEN_HEIGHT // 2 + 30, 100, 40)
                        if cancel_button_rect.collidepoint(mouse_x, mouse_y):
                            game.confirm_dialog = None
                            continue

                        # 点击其他地方也取消
                        game.confirm_dialog = None
                        continue

                    pause_button_rect = pygame.Rect(342, 5, 60, 35)
                    if pause_button_rect.collidepoint(mouse_x, mouse_y):
                        game.game_state = 'paused'
                        continue

                    restart_button_rect = pygame.Rect(410, 5, 60, 35)
                    if restart_button_rect.collidepoint(mouse_x, mouse_y):
                        # 弹出确认对话框
                        game.confirm_dialog = 'restart'
                        continue

                    main_menu_button_rect = pygame.Rect(478, 5, 60, 35)
                    if main_menu_button_rect.collidepoint(mouse_x, mouse_y):
                        # 弹出确认对话框
                        game.confirm_dialog = 'main_menu'
                        continue

                    panel_x = SCREEN_WIDTH - 180
                    panel_width = 170
                    panel_y = 50
                    item_height = 56

                    if panel_x <= mouse_x <= panel_x + panel_width:
                        y_offset = panel_y + 38
                        for tower_type, config in TOWER_CONFIG.items():
                            if y_offset - 3 <= mouse_y <= y_offset + item_height - 9:
                                if game.gold >= config['cost']:
                                    selected_tower_type = tower_type
                                    selected_tower = None
                                break
                            y_offset += item_height
                        continue

                    info_x = SCREEN_WIDTH - 180
                    info_y = 375
                    info_width = 170
                    info_height = 130
                    if info_x <= mouse_x <= info_x + info_width and info_y <= mouse_y <= info_y + info_height:
                        selected_tower = None
                        continue

                    grid_x = mouse_x // GRID_SIZE
                    grid_y = mouse_y // GRID_SIZE

                    clicked_tower = None
                    for tower in game.towers:
                        tower_grid_x = int((tower.x - GRID_SIZE // 2) // GRID_SIZE)
                        tower_grid_y = int((tower.y - GRID_SIZE // 2) // GRID_SIZE)
                        if tower_grid_x == grid_x and tower_grid_y == grid_y:
                            clicked_tower = tower
                            break

                    if clicked_tower:
                        selected_tower = clicked_tower
                        selected_tower_type = None
                    elif selected_tower_type and game.can_place_tower(grid_x, grid_y):
                        config = TOWER_CONFIG.get(selected_tower_type)
                        if config and game.gold >= config['cost']:
                            game.gold -= config['cost']
                            game.towers.append(Tower(grid_x, grid_y, selected_tower_type))
                            selected_tower_type = None

            game.update()
            game.draw()

        except Exception as e:
            print(f"游戏异常: {e}")
            # 尝试恢复游戏状态
            if not hasattr(game, 'towers'):
                game = Game()
                selected_tower_type = None
                selected_tower = None

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
