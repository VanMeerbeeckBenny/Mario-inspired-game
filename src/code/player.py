from tools.tools import import_cut_graphics
from tools.player_image_helper import set_images
import pygame
from settings import SCREEN_HIGHT,TILE_HEIGHT_BIG,TILE_HEIGHT_REGULAR,BULLET_REGEN_TICK,FPS,CAMERA_ACTIVATION_DISTANCE
from tools.enums import Movement_enum
from tools.path_helper import PLAYER_TILES_PATH
from entities import Bullet
from pygame import Vector2
from tools.calculations import calculate_distance_between_objects,calculate_endpoints_withLength
from tools.pymunk_fysics import create_swing_effect,create_space
from audio import jump_sound,death_sound,pick_up_coin_sound,shoot_sound,swing_sound,live_up_sound
class Player():
    
    def __init__(self,surface:pygame.surface,start_position:tuple) -> None:
        self.surface:pygame.Surface = surface
        self.IMAGES = import_cut_graphics(PLAYER_TILES_PATH,TILE_HEIGHT_REGULAR)
        self.BIG_IMAGES = import_cut_graphics(PLAYER_TILES_PATH,TILE_HEIGHT_BIG)
        self.is_jumping = False
        self.is_falling = False
        self.invincible = False  
        self.invincible_timer = 0      
        self.prevent_movement_right = False
        self.prevent_movement_left = False
        self.direction = 1
        self.swing_velocity = Vector2() #Ben dit ergens tegen gekomen in een filmpje toen ik zocht achter iets anders      
        self.is_dead = False
        self.is_dieing = False
        self.level = 0
        self.speed = 3
        self.gravity = 0
        self.lives = 3  
        self.coins = 0
        self.bullets = 5
        self.bullet_regen_timer = 0   
        self.max_stop_swing_height = -15
        self.swing_distance = 0
        self.is_swinging = False
        self.prevent_swinging = False
        self.stop_swing = False
        self.rope_is_thrown = False
        self.current_swing_point:pygame.Rect() = None
        self.length_rope = 0     
        self.frames = []
        self.frame_speed = 0.2
        self.current_frame_index = 0
        self.image = self.IMAGES[41]
        self.stop_animation_timer = 0
        self.space = create_space(surface)
        self.rect = self.image.get_rect(topleft =(start_position[0],start_position[1]))       

    def draw(self):      
        self.image.set_colorkey([0,0,0])
        self.surface.blit(self.image,self.rect)
        self.space.step(1/FPS)
        if self.invincible == True:  
            self.invincible_timer += 0.1
            if self.invincible_timer >= 5:
                self.invincible = False
                self.invincible_timer = 0
            
        self.regen_bullets()

    def move_left(self): 
        self.direction = -1
        if not self.prevent_movement_left:
            self.prevent_movement_right = False 
            if self.rect.x >= 0:       
                self.rect.x -= self.speed
        self.move_animation()   

    def move_right(self,allow_movement:bool): 
        self.direction = 1
        if not self.prevent_movement_right:
            self.prevent_movement_left = False
            if self.rect.x  <= CAMERA_ACTIVATION_DISTANCE or allow_movement:       
                self.rect.x += self.speed
        self.move_animation()  

    def move_animation(self):
        set_images(self,Movement_enum.RUN)
        if not self.is_jumping :            
            if self.current_frame_index >= len(self.frames) -1:
                self.current_frame_index = 0
            else : self.current_frame_index += self.frame_speed        
    
    def jump(self): 
        jump_sound()      
        set_images(self,Movement_enum.JUMP)
        self.is_jumping = True
        self.gravity = -11
        self.rect.y += self.gravity        

    def stand(self):        
        if not self.is_jumping:
            if self.stop_animation_timer > 0 :self.stop_animation()
            if self.stop_animation_timer <= 0:
                set_images(self,Movement_enum.STAND)                    
                    
    def level_down(self):
        if self.level >= 1:
            self.level -= 1
            if self.level == 0:
                set_images(self,Movement_enum.RUN)
                x = self.rect.x
                y = self.rect.y + 32
                self.rect = self.image.get_rect(topleft = (x,y))                
            self.invincible = True
        else:self.death_animation()  

    def stop_animation(self):
        set_images(self,Movement_enum.STOP)   
        self.stop_animation_timer +=  0.1  
        if self.stop_animation_timer > 1:self.stop_animation_timer = 0        

    def death_animation(self):
        self.lives-= 1
        self.image = self.IMAGES[42]           
        self.gravity = -8
        self.is_dieing = True
        self.is_jumping = False
        self.is_falling = False
        self.is_swinging = False
        self.space = create_space(self.space)
        death_sound()  

    def shoot(self):
        if(self.level == 2) and self.bullets > 0:
            shoot_sound()
            if self.direction > 0:
                bullet = Bullet(self.rect.right,self.rect.centery,3,self.direction)
            else :
                bullet = Bullet(self.rect.left,self.rect.centery,2.5,self.direction)
                bullet.speed = -abs(bullet.speed)
                bullet.image = pygame.transform.flip(bullet.image,True,False)                
            self.bullets -= 1
            return bullet 

    def regen_bullets(self):
        if self.level == 2:
            self.bullet_regen_timer += BULLET_REGEN_TICK
            if self.bullet_regen_timer >= 2:
                self.bullet_regen_timer = 0
                if self.bullets < 5:self.bullets += 1

            
    def reset(self,position):
        self.rect.x = position[0]
        self.rect.y = position[1]
        self.rect.height = 32    
        
        self.level = 0
        self.is_dead = False
        self.is_dieing = False
        self.prevent_swinging = False
        
        self.swing_velocity.x = self.swing_velocity.y = 0
        self.direction = 1
        self.gravity = 0
        set_images(self,Movement_enum.STAND)
        self.invincible = True

    def schoot_rope(self,swing_point:pygame.Rect):
        offset_x = 12 if self.direction > 0 else -12
        player_rope_start_cord = (self.rect.midtop[0] + offset_x,self.rect.midtop[1])
        distance,angle = calculate_distance_between_objects(player_rope_start_cord,swing_point.midbottom)        
        if self.length_rope < distance and self.length_rope < SCREEN_HIGHT and not self.rope_is_thrown:          
            self.length_rope += 25
            new_end_point = calculate_endpoints_withLength(angle,self.length_rope,player_rope_start_cord)

            pygame.draw.line(self.surface,
                            "black",
                            player_rope_start_cord,
                            new_end_point,
                            2) 
            
        elif distance < SCREEN_HIGHT and (self.is_jumping  or self.is_falling): 
            #this prevent drawing to next swing point when stil attatched to the original
            new_swing_point = self.current_swing_point if self.is_swinging else swing_point
            self.swing(new_swing_point)
        else:
            self.rope_is_thrown = True 
            pygame.draw.line(self.surface,
                            "black",
                            player_rope_start_cord,
                            swing_point.midbottom,
                            2)  

    def swing(self,swing_point:pygame.Rect):        
        offset_x = 12 if self.direction > 0 else -12
        player_rope_start_cord = (self.rect.midtop[0] + offset_x,self.rect.midtop[1])        

        if self.is_jumping or self.is_falling:
            swing_sound()
            if self.is_falling or self.is_swinging:
                set_images(self,Movement_enum.JUMP)
               
            self.is_swinging = True
            self.current_swing_point = swing_point
            if len(self.space.bodies) == 0 :
                create_swing_effect(swing_point,self.rect.midtop,self.space)
                player_rope_start_cord = self.space.bodies[0].position[0] + offset_x,self.space.bodies[0].position[1]
                
            else: 
                
                self.swing_velocity.x = self.space.bodies[0].velocity.x / FPS 
                self.swing_velocity.y = self.space.bodies[0].velocity.y / FPS
                
                self.rect.midtop = self.space.bodies[0].position[0] ,self.space.bodies[0].position[1]            
                player_rope_start_cord =  self.space.bodies[0].position[0] + offset_x,self.space.bodies[0].position[1] 
          
            pygame.draw.line(self.surface,
                        "black",
                        player_rope_start_cord ,
                        swing_point.midbottom,
                        2)      
            

    def stop_swinging(self):
        if self.rect.x > CAMERA_ACTIVATION_DISTANCE:
            self.swing_distance = abs(self.rect.x - CAMERA_ACTIVATION_DISTANCE)  
        self.rope_is_thrown = False
        self.length_rope = 0
        if self.prevent_swinging:               
            self.prevent_swinging = False
        if self.is_swinging:
            self.stop_swing = True
            self.is_swinging = False                      
            self.gravity = 0
        self.swing_velocity.x = 0
        self.swing_velocity.y = 0      
        self.space = create_space(self.surface)
        
    def pick_up_coin(self,amount = 1):    
        self.coins += amount
        if self.coins >= 100:
            live_up_sound()
            self.coins = self.coins - 100
            self.lives += 1  
        pick_up_coin_sound()

