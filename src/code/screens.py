import pygame
from settings import SCREEN_HIGHT,SCREEN_WIDTH
from audio import is_bussy_dead_sound,is_bussy_finisched_level_sound,play_end_game_song,stop_music
from tools.tools import draw_level_and_lives
from tools.tools import draw_text
from game_info import Info
from player import Player
class screen():
    def __init__(self,screen,live_image) -> None:
        self.surface:pygame.Surface = screen
        self.lives_image = live_image
        self.off_set = 0  

    def death_screen(self,lives:int,level:str):
        self.surface.fill('Black') 
        draw_level_and_lives(self.surface,level,lives,self.lives_image)
        if not is_bussy_dead_sound() and lives >= 1:
            draw_text(self.surface,"Press space to try again...",
                    (SCREEN_WIDTH/2-20,SCREEN_HIGHT/2 + 100),
                    location='center',
                    color= 'white')
       
    def game_over_screen(self): 
        self.surface.fill('Black')        
        text_cordinates = (SCREEN_WIDTH/2,SCREEN_HIGHT/2)        
        text_level = 'Game over!!'

        draw_text(self.surface,text_level,
                  text_cordinates,
                  location='center',
                  color= 'white')
        
    def finisched_game_screen(self,game_info:Info): 
        play_end_game_song()        
        self.surface.fill('Black')      
        text_cordinates = (SCREEN_WIDTH/2,SCREEN_HIGHT/2 + self.off_set)        
        text = 'Game complete!!'

        draw_text(self.surface,text,
                  text_cordinates,
                  location='center',
                  color= 'white')
        
        text_cordinates = (SCREEN_WIDTH/2,SCREEN_HIGHT/2 + 200 + self.off_set)        
        text = 'Game design:'

        draw_text(self.surface,text,
                  text_cordinates,
                  location='center',
                  color= 'white')
        
        text_cordinates = (SCREEN_WIDTH/2,SCREEN_HIGHT/2 + 240 + self.off_set)        
        text = 'Van Meerbeeck Benny'

        draw_text(self.surface,text,
                  text_cordinates,
                  location='center',
                  color= 'white')
        
        text_cordinates = (SCREEN_WIDTH/2,SCREEN_HIGHT/2 + 300 + self.off_set)        
        text = 'Audio:'

        draw_text(self.surface,text,
                  text_cordinates,
                  location='center',
                  color= 'white')
        
        text_cordinates = (SCREEN_WIDTH/2,SCREEN_HIGHT/2 + 340 + self.off_set)        
        text = 'Van Meerbeeck Benny'

        draw_text(self.surface,text,
                  text_cordinates,
                  location='center',
                  color= 'white')
        
        text_cordinates = (SCREEN_WIDTH/2,SCREEN_HIGHT/2 + 400 + self.off_set)        
        text = 'Shout out to:'

        draw_text(self.surface,text,
                  text_cordinates,
                  location='center',
                  color= 'white')
        
        text_cordinates = (SCREEN_WIDTH/2,SCREEN_HIGHT/2 + 440 + self.off_set)        
        text = 'Lectors team Howest'

        draw_text(self.surface,text,
                  text_cordinates,
                  location='center',
                  color= 'white')
        
        text_cordinates = (SCREEN_WIDTH/2,SCREEN_HIGHT/2 + 480 + self.off_set)        
        text = 'PyMunk Team'

        draw_text(self.surface,text,
                  text_cordinates,
                  location='center',
                  color= 'white')
        
        text_cordinates = (SCREEN_WIDTH/2,SCREEN_HIGHT/2 + 520 + self.off_set)        
        text = 'PyGame Team'

        draw_text(self.surface,text,
                  text_cordinates,
                  location='center',
                  color= 'white')

        self.off_set += - 0.29
        if self.off_set <= (- 560 - SCREEN_HIGHT/2):
            self.off_set = 0
            game_info.restart = True
            game_info.game_ending = False 
            stop_music()


    
    def loading_screen(self,player:Player,level:str,game_info:Info) -> bool:        
        draw_level_and_lives(self.surface,level,player.lives,self.lives_image)                    
        is_busy =  is_bussy_finisched_level_sound()
        if not is_busy: 
            game_info.loading_next_level = False
            player.direction = 1 