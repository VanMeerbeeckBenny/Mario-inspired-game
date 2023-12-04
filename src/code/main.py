import pygame
from settings import *

from level import Level
from engine import Engine
from player import Player
from handle_player_input import Handler
from user_interface import Gui
from audio import play_music,is_bussy_dead_sound,game_over_sound,is_bussy_game_over_sound
from camera import Camera
from start_screen import Start_screen
from game_info import Info
from screens import screen

resizeble_screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HIGHT),HWSURFACE|DOUBLEBUF|RESIZABLE)
drawing_screen = resizeble_screen.copy()
level:Level = Level("level0_1",drawing_screen)
clock = pygame.time.Clock()

player_position = level.player_start_position
player = Player(drawing_screen,player_position)
engine = Engine()
screens = screen(drawing_screen,player.IMAGES[41])
input_handler:Handler = Handler()
camera = Camera()
user_interface = Gui(drawing_screen,player.IMAGES[41])
start_screen = Start_screen(drawing_screen)
game_info = Info()

while True:      
    drawing_screen.fill(AIR_COLOR)
    camera.run(player,level)    
    engine.run(player,level,game_info)    
    input_handler.check_input(game_info,player,level)
    
    if not player.is_dead and game_info.game_start and not game_info.loading_next_level:               
        if not player.is_dieing:play_music()                             
        level.run()            
        player.draw()      
        user_interface.create_interface(player,level.current_level) 
    elif game_info.game_ending:        
        screens.finisched_game_screen(game_info)                
    elif not game_info.game_start and not game_info.restart:  
        start_screen.run(game_info) 
    elif game_info.loading_next_level:
        screens.loading_screen(player,level.current_level,game_info)      
    else :               
        if player.lives < 1 and not game_info.restart:                 
            if not is_bussy_dead_sound():                
                game_over_sound()           
                game_info.restart = True
        if is_bussy_game_over_sound(): screens.game_over_screen()
        else:screens.death_screen(player.lives,level= level.current_level)
        

    #restart game when out of lives
    if game_info.restart and not is_bussy_game_over_sound():      
        level = Level("level0_1",drawing_screen)
        player = Player(drawing_screen,level.player_start_position)
        game_info.game_start = False
        game_info.game_init = False   
        game_info.restart = False         
    

    resizeble_screen.blit(pygame.transform.scale(drawing_screen,resizeble_screen.get_rect().size),(0,0))
    
    pygame.display.update()    
    clock.tick(FPS)
 
 