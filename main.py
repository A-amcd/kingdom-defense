#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import tp

if __name__ == '__main__':
    game = tp.Game()
    game.run()