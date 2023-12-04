from pathlib import Path

SOURCEFILEDIR = Path(__file__).resolve().parents[2]

FONT_PATH = SOURCEFILEDIR.joinpath('font/Pixeltype.ttf')
PLAYER_TILES_PATH = SOURCEFILEDIR.joinpath('data/graphics/PlumberFellasSpritesheet.png').resolve()
GAME_TILES_PATH = SOURCEFILEDIR.joinpath('data/graphics/PlumberFellasTilesheet.png').resolve()
SAVE_TILES_PATH = SOURCEFILEDIR.joinpath('data/graphics/save.png')
LOGO_PATH = SOURCEFILEDIR.joinpath('data/graphics/super_mario_bros.png')
BULLET_IMAGE_PATH = SOURCEFILEDIR.joinpath('data/graphics/bullet.png')
BONUS_MUSHROOM_PATH = SOURCEFILEDIR.joinpath('data/graphics/mushroom.png')
BONUS_FLOWER0_PATH = SOURCEFILEDIR.joinpath('data/graphics/flower0.png')
BONUS_FLOWER1_PATH = SOURCEFILEDIR.joinpath('data/graphics/flower1.png')
BONUS_FLOWER2_PATH = SOURCEFILEDIR.joinpath('data/graphics/flower2.png')
BONUS_FLOWER3_PATH = SOURCEFILEDIR.joinpath('data/graphics/flower3.png')
FLOWER_PATHS = [BONUS_FLOWER0_PATH,BONUS_FLOWER1_PATH,BONUS_FLOWER2_PATH,BONUS_FLOWER3_PATH]
FULL_TURTLE_PATH_SPRITES = SOURCEFILEDIR.joinpath('data/graphics/full_turtle.png')
SHELL_TURTLE_PATH_SPRITES = SOURCEFILEDIR.joinpath('data/graphics/shell_turtle.png')

LEVEL_DICT:dict ={
    "level0_1" : SOURCEFILEDIR.joinpath("data/map/level0_1.tmx").resolve(),
    "level0_2" : SOURCEFILEDIR.joinpath("data/map/level0_2.tmx").resolve(),
    'start_screen':SOURCEFILEDIR.joinpath("data/map/start_screen.tmx").resolve(),    
}
