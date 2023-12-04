import pygame
from level import Level
from player import Player
from entities import Turtle,Question_box,Collision_block
from settings import SCREEN_HIGHT, TILE_SIZE,SCREEN_WIDTH
from tools.enums import Movement_enum
from game_info import Info
from tools.player_image_helper import set_images
from tools.calculations import calculate_distance_between_objects
from audio import pick_up_bonus_sound,hit_block_sound,success_sound,stop_music
from tools.collision_tools import check_bottomside,check_leftside,check_rightside,check_topside,check_mob_kill
from tools.collision_tools import create_basic_future_position,create_future_position



def get_lasso_point_in_range(level,player):
    level:Level = level
    player:Player = player
    swing_point:dict = {
        'swing_point':None,
        'distance':0
    }

    for lasso_point in level.swing_points:
        distance,angel = calculate_distance_between_objects(player.rect.center,lasso_point.rect.center)
        if distance < swing_point['distance'] or swing_point['distance'] == 0:
            swing_point['distance'] = distance
            swing_point['swing_point'] = lasso_point
    if swing_point['distance'] < 500: return swing_point['swing_point']
    else : return None

class Engine():    
    def __init__(self) -> None:                  
        self.previus_x = 0        

    def run(self,player:Player,level:Level,game_info:Info):
        self.__turtle_shell_controller__(level)  
        if not player.is_dieing:            
            self.__bonus_collision__(player,level)
            self.__ennemie_collision_controller__(player,level)
            self.__player_collision_controler__(player,level)  
        self.__set_direction_on_swinging__(player)         
        self.__ennemie_platform_controller__(level)         
        self.__bullet_collision__(level)
        self.__remove_out_of_frame_items__(level)
        self.__save_collision_controller__(player,level)
        self.__gravity__(player)        
        self.__coin_collision__(player,level)
        self.__turtle_projectile_collision_controller__(level)
        self.__load_next_level__(player,level,game_info)
        self.__bonus_movement_controller__(level)  
        
            

    def __turtle_shell_controller__(self,level:Level):
        for ennemie in level.ennemies:
            if ennemie.is_jumped_on and type(ennemie) == Turtle:
                self.__gravity__(ennemie)
                self.__base_collider_controler__(ennemie,level)

    def __bonus_movement_controller__(self,level:Level):
        for bonus in level.bonusses:
            if bonus.fully_spawned:
                self.__gravity__(bonus)
                self.__base_collider_controler__(bonus,level) 

    def __set_direction_on_swinging__(self,player:Player):
        if player.is_swinging:
            if self.previus_x == 0 or self.previus_x == player.rect.x:
                pass
            elif self.previus_x < player.rect.x:
                player.direction = 1
            else: 
                player.direction = -1
            self.previus_x = player.rect.x
        else: self.previus_x = 0
    
    def __ennemie_platform_controller__(self,level:Level):
        for ennemie in level.ennemies:
            for limiter in level.limiter_block:
                if ennemie.rect.colliderect(limiter.rect) and not  ennemie.is_jumped_on:                                          
                    ennemie.change_direction()
                    
    def __ennemie_collision_controller__(self,player:Player,level:Level):
        future_surf = pygame.Surface((32,player.rect.height))
        future_player_pos = future_surf.get_rect(topleft = (player.rect.x,player.rect.y + player.gravity))
        
        for ennemie in level.ennemies:                     
            if ennemie.rect.inflate(-5,0).colliderect(future_player_pos) and not ennemie.is_dead:
                if check_mob_kill(player,ennemie):                           
                    if player.rect.bottom != ennemie.rect.bottom:
                        player.gravity = -4 
                    ennemie.jumped_on(player.direction)  
                elif not player.invincible: 
                    player.level_down()

    def __load_next_level__(self,player:Player,level:Level,game_info:Info):
        for end_block in level.end_level:
            if player.rect.colliderect(end_block.rect) and not game_info.game_ending:                       
                succes = level.load_next_level()
                if not succes:                  
                    game_info.game_init = False
                    game_info.game_start = False                     
                    game_info.game_ending = True 
                    stop_music()                                  
                    break
                else:
                    success_sound()
                    player.rect.x = level.player_start_position[0]
                    player.rect.y = level.player_start_position[1] 
                    if player.level >= 1:player.rect.y -= 32
                    game_info.loading_next_level = True
                break                            

    def __turtle_projectile_collision_controller__(self,level:Level):
        for turtle in level.ennemies:
            if type(turtle) == Turtle:
                turtle:Turtle
                if turtle.is_projectil:
                    for ennemie in level.ennemies:
                        if turtle.rect.colliderect(ennemie) and ennemie != turtle and not ennemie.is_dead:
                            ennemie.death_by_bullet_annimation()

    def __bonus_collision__(self,player:Player,level:Level):
        for bonus in level.bonusses:
            if bonus.rect.colliderect(player.rect):
                if player.level <= 1:pick_up_bonus_sound()
                if bonus.level >= 1: 
                    player.bullets = 5   
                    if player.level < 1:                
                        player.rect.y -= TILE_SIZE
                        player.rect.height += TILE_SIZE
                if player.level == 2:
                    player.bullets = 5
                    player.pick_up_coin(5)
                player.level = bonus.level 
                                    
                if player.is_jumping: set_images(player,Movement_enum.JUMP)           
                level.bonusses.remove(bonus)

    def __coin_collision__(self,player:Player,level:Level):
        for coin in level.coins:
            inflated_rect = coin.rect.inflate(-30,0)
            if player.rect.colliderect(inflated_rect):
                player.pick_up_coin()
                level.coins.remove(coin)

    def __bullet_collision__(self,level:Level):
        for bullet in level.bullets:
            for ennemy in level.ennemies:
                if ennemy.rect.colliderect(bullet.rect) and bullet.destroyed == False:                    
                    if ennemy.is_dead == False:
                        level.bullets.remove(bullet)
                    ennemy.death_by_bullet_annimation()
            for block in level.collision_blocks:
                if block.rect.colliderect(bullet.rect):
                    bullet.impact_wall = True

    def __save_collision_controller__(self,player:Player,level:Level):
        for save in level.save:
            if save.rect.colliderect(player.rect.inflate(-10,0)):
                level.activate_save(save)

    def __remove_out_of_frame_items__(self,level:Level):
        for bullet in level.bullets:
            if bullet.rect.y >= SCREEN_HIGHT + 20: 
                level.bullets.remove(bullet)
            if bullet.rect.x <= -bullet.rect.width or bullet.rect.x >= (SCREEN_WIDTH + bullet.rect.width):
                level.bullets.remove(bullet)

        for ennemie in level.ennemies:
            if ennemie.rect.y >= SCREEN_HIGHT + 20:
                level.ennemies.remove(ennemie)    
    
    def __player_collision_controler__(self,player:Player,level:Level):
        if player.swing_distance >= 0:  
            # This prevent player to fall off the end off map =>
            # without it, check ending map in camera gets countered                          
            if player.rect.right <= SCREEN_WIDTH:                    
                    player.prevent_movement_right = False 
            player.prevent_movement_left = False 

        future_position = create_future_position(player,level.off_set)
        for block in level.collision_blocks:                      
            if future_position.colliderect(block.rect): 
                             
                if check_bottomside(player,block.rect):
                    player.is_jumping = False  
                    player.rect.bottom = block.rect.top
                    player.gravity = 0 
                    self.__abort_swing__(player)               
                    continue

                if check_topside(player,block.rect):
                    #if is bumped then the block is 5 pixels up
                    is_bumped_correction = block.bump_hight if block.is_bumped else 0 
                    player.rect.top = block.rect.bottom + is_bumped_correction                 
                    player.gravity = 0
                    self.__abort_swing__(player)                                                            
                    hit_block_sound()  
                    if isinstance(block,Collision_block):
                        block.bump_annimation()                     
                    if type(block) == Question_box:                                             
                        level.create_bonus_animation(block,player) 
                        for ennemie in level.ennemies:
                            if ennemie.rect.colliderect(block):
                                ennemie.death_by_bullet_annimation()                                                                         
                    break
                    
                elif check_rightside(player,block.rect):                                                                     
                        player.rect.right = block.rect.left  
                        player.prevent_movement_right = True
                        self.__abort_swing__(player) 
                         
                elif check_leftside(player,block.rect):                                
                    player.rect.left = block.rect.right    
                    player.prevent_movement_left = True
                    self.__abort_swing__(player)           

    def __abort_swing__(self,player:Player):
        player.stop_swing = False  
        if player.is_swinging: 
            player.gravity = 0  
            player.is_swinging = False
            player.stop_swinging()      
            player.prevent_swinging = True             
    
    def __base_collider_controler__(self,moving_object,level:Level):                                                                     
        future_position = create_basic_future_position(moving_object,level.off_set)
    
        for block in level.collision_blocks:                      
            if future_position.colliderect(block.rect):  
        
                if check_bottomside(moving_object,block.rect):                        
                        moving_object.rect.bottom = block.rect.top
                        moving_object.gravity = 0  
                        continue
                if check_topside(moving_object,block.rect):                               
                        moving_object.gravity = 0                  
                        continue   
                    
                if check_rightside(moving_object,block.rect):                                                                     
                    moving_object.change_direction() 
                    moving_object.gravity = 0 
                      
                elif check_leftside(moving_object,block.rect):   
                    moving_object.change_direction()   
                    moving_object.gravity = 0             
            

    
    def __gravity__(self,entitie):
         
        if type(entitie) == Player: 
            entitie: Player
            if entitie.stop_swing and not entitie.prevent_swinging:  
                entitie.gravity += -1.5 
                entitie.rect.x += 4 if entitie.direction > 0 else -4 
                entitie.rect.y -= 1.5
                if entitie.gravity <= entitie.max_stop_swing_height:
                    entitie.stop_swing = False                       
                    entitie.gravity = -1  
            elif not entitie.is_swinging and entitie.stop_swing == False:                       
                entitie.rect.y += entitie.gravity
                entitie.gravity += 0.5  
            if entitie.rect.top > (SCREEN_HIGHT + entitie.rect.height) and entitie.is_dieing:
                entitie.is_dead = True
            if entitie.rect.top > SCREEN_HIGHT and not entitie.is_dieing:
                entitie.death_animation()  
            if entitie.gravity > (4*0.3) : entitie.is_falling = True
            else: entitie.is_falling = False               
        else:                   
            entitie.rect.y += entitie.gravity
            entitie.gravity += 0.3      