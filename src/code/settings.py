import pygame
from pygame.locals import *

TILE_SIZE = 32
TILE_HEIGHT_REGULAR = 32
TILE_HEIGHT_BIG = 64
TILE_COUNT_Y = 15
TILE_COUNT_X = 60
FULL_TURTLE_HEIGHT = 43
FPS = 60
MAX_SCREEN_WIDTH = TILE_SIZE * TILE_COUNT_X
CAMERA_ACTIVATION_DISTANCE = 300

SCREEN_WIDTH = 960
SCREEN_HIGHT = TILE_SIZE * TILE_COUNT_Y
BULLET_REGEN_TICK = 0.01

MOVEMENT_KEYS = (pygame.K_d,pygame.K_q,pygame.K_LEFT,pygame.K_RIGHT)
MOVEMENT_LEFT = (pygame.K_q,pygame.K_LEFT)
MOVEMENT_RIGHT = (pygame.K_d,pygame.K_RIGHT)
AIR_COLOR = (100, 149, 237)


ANIMATION_DICT = {
    "animated_coin_id":"162",
    "animated_questionmarks_id":"161",
    "animated_mushroom_id":"177"
    }



    

