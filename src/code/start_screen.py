import pygame
from tools.tmx_map_util import Map_builder
from tools.tools import import_cut_graphics,draw_text
from settings import TILE_HEIGHT_REGULAR,SCREEN_WIDTH,SCREEN_HIGHT
from tools.path_helper import LOGO_PATH,PLAYER_TILES_PATH,GAME_TILES_PATH
from entities import Brick,Cloud,StaticTile
from player import Player

class Start_screen():

    def __init__(self,screen:pygame.Surface) -> None:  
        self.screen = screen      

        self.map_builder:Map_builder = Map_builder('start_screen')
        self.player_and_mobs_sprite = import_cut_graphics(PLAYER_TILES_PATH,TILE_HEIGHT_REGULAR)
        self.spritesheet = import_cut_graphics(GAME_TILES_PATH,TILE_HEIGHT_REGULAR)  
        self.bricks:pygame.sprite.Group = self.map_builder.create_tiles(Brick,"collision_bloks")
        self.clouds:pygame.sprite.Group = self.map_builder.create_tiles(Cloud,"clouds") 
        self.grass:pygame.sprite.Group = self.map_builder.create_tiles(StaticTile,"grass")  
        self.mountens:pygame.sprite.Group = self.map_builder.create_tiles(StaticTile,"mountens")
        self.player_start_position = self.map_builder.get_player_startposition() 
        self.mario:Player = Player(self.screen,self.player_start_position)
        self.logo = pygame.image.load(LOGO_PATH).convert_alpha()
        self.logo_rect = self.logo.get_rect(center = (SCREEN_WIDTH/2,SCREEN_HIGHT/3))
        
    def run(self,game_info):
        self.bricks.draw(self.screen)
        self.clouds.draw(self.screen)
        self.grass.draw(self.screen)
        self.mountens.draw(self.screen)
        self.__start_game__(game_info)
        self.mario.draw()
        self.screen.blit(self.logo,(self.logo_rect.x,self.logo_rect.y))
        self.__create_press_space_text__()

    def __create_press_space_text__(self):
        text = 'Press space to start game !!'
        location = 'center'
        color = 'white'
        cordinates = (SCREEN_WIDTH/2,SCREEN_HIGHT/2 + 100)
        draw_text(self.screen,text,cordinates,location,color)

    def __start_game__(self,game_info):        
        if game_info.game_init:            
            self.mario.move_right(True)         
        if self.mario.rect.left > SCREEN_WIDTH:
            game_info.game_start = True
            self.mario:Player = Player(self.screen,self.player_start_position)

    
