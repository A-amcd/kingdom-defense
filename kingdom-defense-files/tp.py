#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Kingdom Defense - Tower Defense Game"""

import pygame
import sys
import math
import random

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Kingdom Defense")
        
    def run(self):
        running = True
        clock = pygame.time.Clock()
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
            
            self.screen.fill((30, 30, 50))
            
            font = pygame.font.Font(None, 74)
            text = font.render("Kingdom Defense", True, (255, 200, 100))
            text_rect = text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 50))
            self.screen.blit(text, text_rect)
            
            font_small = pygame.font.Font(None, 36)
            start_text = font_small.render("Press ENTER to Start", True, (200, 200, 200))
            start_rect = start_text.get_rect(center=(SCREEN_WIDTH