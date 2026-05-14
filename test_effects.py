"""
特效系统测试脚本
用于单独测试各个特效系统的视觉效果
"""

import pygame
import sys
from tp_integrated import (
    CherryPetalSystem,
    WaterSurface,
    ToxicBubbleSystem,
    RainSystem,
    BackgroundRenderer,
    LevelTheme
)

pygame.init()

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("特效系统测试")
clock = pygame.time.Clock()

# 创建所有特效系统
cherry_system = CherryPetalSystem(80)
water_system = WaterSurface()
toxic_bubble_system = ToxicBubbleSystem(50)
rain_system = RainSystem(300)

# 测试场景配置
test_scenes = [
    ("1 - 万象平原", LevelTheme.PLAIN),
    ("2 - 恶地沼泽", LevelTheme.SWAMP),
    ("3 - 天落殷园", LevelTheme.SKY),
    ("4 - 污染花园", LevelTheme.CORRUPT),
]

current_scene = 0
font = pygame.font.Font(None, 36)

print("=" * 60)
print("特效系统测试程序")
print("=" * 60)
print("按键说明:")
print("  1-4: 切换场景")
print("  ESC: 退出")
print("=" * 60)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_1:
                current_scene = 0
            elif event.key == pygame.K_2:
                current_scene = 1
            elif event.key == pygame.K_3:
                current_scene = 2
            elif event.key == pygame.K_4:
                current_scene = 3
    
    # 更新所有特效
    cherry_system.update()
    water_system.update()
    toxic_bubble_system.update()
    rain_system.update()
    
    # 绘制当前场景
    scene_name, theme = test_scenes[current_scene]
    
    # 绘制背景
    BackgroundRenderer.draw_generic_background(screen, theme)
    
    # 绘制特效
    if theme == LevelTheme.SKY:
        cherry_system.draw(screen)
    elif theme == LevelTheme.SWAMP:
        water_system.draw(screen)
        rain_system.draw(screen)
    elif theme == LevelTheme.CORRUPT:
        toxic_bubble_system.draw(screen)
    
    # 绘制场景名称
    text = font.render(f"场景: {scene_name}", True, (255, 255, 255))
    screen.blit(text, (20, 20))
    
    # 绘制提示
    hint = font.render("按 1-4 切换场景，ESC 退出", True, (200, 200, 200))
    screen.blit(hint, (20, 60))
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
