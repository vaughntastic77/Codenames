#----------------------------------------------------------------------------------------------------------------------
# Codenames board game written in python by Jacob Vaughn 12/30/2025
#----------------------------------------------------------------------------------------------------------------------
import pygame as pg
import random
import numpy as np

# Initialize Pygame
pg.init()

# Set the size of the window
winSize = 800
screen = pg.display.set_mode((winSize,winSize))
pg.display.set_caption("Aggravation")

# Create clock for timing
clock = pg.time.Clock()
FPS = 60

# Background Color
BLACK = (0,0,0)
WHITE = (255,255,255)
screen.fill(BLACK) 

# Initialize fonts
titleFont = pg.font.SysFont("Arial",48,bold=True)
menuFont = pg.font.SysFont("Arial",36)
gameFont = pg.font.SysFont("Arial",24)

# Load board image
