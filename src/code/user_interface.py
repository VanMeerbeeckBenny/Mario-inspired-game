import pygame
from settings import SCREEN_WIDTH,TILE_SIZE,TILE_HEIGHT_REGULAR,SCREEN_HIGHT
from tools.tools import import_cut_graphics,draw_text,draw_text_with_image,draw_lives_left
from tools.path_helper import GAME_TILES_PATH,FONT_PATH
from player import Player
from entities import Bullet



class Gui():
    def __init__(self,screen:pygame.display,lives_image:pygame.Surface) -> None:      
        self.surface = screen
        self.lives_image = lives_image
        plumberTileSheet = import_cut_graphics(GAME_TILES_PATH,TILE_HEIGHT_REGULAR)
        self.coins_image = plumberTileSheet[99]
         

        
            

    def create_interface(self,player:Player,level:str): 
        text_cordinates =(SCREEN_WIDTH - 10,10)
        image_coordinates= (SCREEN_WIDTH - 60,5)
        draw_lives_left(self.surface,player.lives,text_cordinates,image_coordinates,self.lives_image) 
        
        #display total coins
        text = f'x {player.coins}'
        text_cordinates = (SCREEN_WIDTH - 150,10)
        image_coordinates = (SCREEN_WIDTH - 200,5)
        draw_text_with_image(self.surface,text,text_cordinates,image_coordinates,self.coins_image)    

        #show level
        level = level.replace("level","").replace("_","-")
        draw_text(self.surface,f'level: {level}',(150,10))

        self.draw_bullet(player)


    def draw_bullet(self,player:Player):
        offset =  10
        if player.level == 2:
            for i in range(player.bullets):                              
                x = SCREEN_WIDTH - offset
                y = SCREEN_HIGHT - 20
                bullet = Bullet(x,y,0,1)     
                bullet.image = pygame.transform.rotate(bullet.image,90)   
                self.surface.blit(bullet.image,bullet.rect) 
                offset += 10 + TILE_SIZE/4
    
    
    
    