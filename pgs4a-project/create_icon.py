#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame
import sys

def create_icon():
    pygame.init()
    size = 512
    icon = pygame.Surface((size, size))
    icon.fill((30, 30, 50))
    
    # 绘制城堡图标
    center = size // 2
    
    # 城堡主体
    pygame.draw.rect(icon, (100, 100, 100), (center - 60, center + 20, 120, 80))
    
    # 城堡塔楼
    pygame.draw.rect(icon, (80, 80, 80), (center - 100, center - 40, 40, 140))
    pygame.draw.rect(icon, (80, 80, 80), (center + 60, center - 40, 40, 140))
    
    # 塔楼顶部
    pygame.draw.polygon(icon, (120, 120, 120), [
        (center - 100, center - 60),
        (center - 80, center - 100),
        (center - 60, center - 60)
    ])
    pygame.draw.polygon(icon, (120, 120, 120), [
        (center + 60, center - 60),
        (center + 80, center - 100),
        (center + 100, center - 60)
    ])
    
    # 中央塔楼
    pygame.draw.rect(icon, (90, 90, 90), (center - 30, center - 80, 60, 100))
    pygame.draw.polygon(icon, (110, 110, 110), [
        (center - 35, center - 100),
        (center, center - 140),
        (center + 35, center - 100)
    ])
    
    # 旗帜
    flag_y = center - 130
    pygame.draw.line(icon, (100, 80, 60), (center, center - 140), (center, flag_y - 30))
    pygame.draw.polygon(icon, (255, 0, 0), [
        (center, flag_y),
        (center + 30, flag_y - 20),
        (center, flag_y - 15)
    ])
    
    # 大门
    pygame.draw.rect(icon, (60, 60, 60), (center - 20, center + 60, 40, 40))
    pygame.draw.circle(icon, (80, 60, 40), (center + 12, center + 80), 5)
    
    # 塔楼窗户
    for i in range(3):
        pygame.draw.rect(icon, (50, 50, 80), (center - 88, center - 20 + i * 40, 16, 16))
        pygame.draw.rect(icon, (50, 50, 80), (center + 72, center - 20 + i * 40, 16, 16))
    
    pygame.image.save(icon, "res/drawable/icon.png")
    pygame.quit()
    print("图标已创建: res/drawable/icon.png")

if __name__ == "__main__":
    create_icon()