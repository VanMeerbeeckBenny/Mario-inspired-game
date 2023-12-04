import pygame
import sys
from engine import get_lasso_point_in_range

from level import Level
from player import Player
from settings import MOVEMENT_KEYS,MOVEMENT_LEFT,MOVEMENT_RIGHT,CAMERA_ACTIVATION_DISTANCE
from game_info import Info
from audio import is_bussy_dead_sound
class Handler():         

    def check_input(self,game_info:Info,player:Player,level:Level):       
        level.movement_offset = 0
        if not player.is_dieing and game_info.game_start and not game_info.loading_next_level:
            key_pressed = pygame.key.get_pressed()                
            right_key_pressed = any([key_pressed[key] for key in MOVEMENT_RIGHT])
            left_key_pressed = any([key_pressed[key] for key in MOVEMENT_LEFT])

            if key_pressed[pygame.K_LSHIFT] and not player.prevent_swinging:
                swing_point = get_lasso_point_in_range(level,player)                   
                if swing_point != None:                        
                    player.schoot_rope(swing_point.rect)                    
            if right_key_pressed and not player.is_swinging:
                if player.rect.x  >= CAMERA_ACTIVATION_DISTANCE  and not level.end_map:
                    level.movement_offset = -player.speed                
                player.move_right(level.end_map)
            elif left_key_pressed and not player.is_swinging:                
                player.move_left()
            elif not player.is_swinging:
                player.stand()       
        
        
              
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if not player.is_dieing and game_info.game_start:                   
                if event.type == pygame.KEYDOWN and not player.is_swinging:
                    if event.key == pygame.K_SPACE and not player.is_jumping and not player.is_falling and not game_info.loading_next_level:
                        player.jump()
                if event.type == pygame.KEYUP: 
                    if event.key == pygame.K_LSHIFT:                                                                            
                        player.stop_swinging()                    
                    if event.key in MOVEMENT_KEYS and not player.is_swinging:
                        player.stop_animation_timer += 0.01
                    if event.key == pygame.K_RCTRL or event.key == pygame.K_a:                        
                        bullet = player.shoot()
                        if bullet is not None:level.bullets.add(bullet)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not is_bussy_dead_sound():
                    if player.is_dead and player.lives >= 1:
                        level.restart(player)
                    if not game_info.game_start:
                        game_info.game_init = True

        
        
        
                

