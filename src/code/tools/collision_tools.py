import pygame
from settings import SCREEN_HIGHT,TILE_SIZE
from entities import Killeble,Turtle
from player import Player
from math import ceil,floor

def check_rightside(moving_object:pygame.sprite,rect:pygame.Rect):
    is_hit = False
    if moving_object.rect.bottom != rect.top:              
        if moving_object.direction > 0 and moving_object.rect.right >= rect.left:
            if (moving_object.rect.right - rect.left)  < TILE_SIZE:#solves swing issue
                is_hit = True
    return is_hit

def check_leftside(moving_object:pygame.sprite,rect:pygame.Rect):
    is_hit = False
    if moving_object.rect.bottom != rect.top:              
        if moving_object.direction < 0 and moving_object.rect.left <= rect.right:
            if (rect.right - moving_object.rect.left)  < TILE_SIZE:#solves swing issue
                is_hit = True
    return is_hit

def check_topside(moving_object:pygame.sprite,rect:pygame.Rect):
    is_hit = False
    if not (moving_object.rect.right == rect.left) and not (moving_object.rect.left == rect.right):  
        if moving_object.rect.top >= rect.bottom and rect.bottom != SCREEN_HIGHT:
            is_hit = True
        if moving_object.rect.top - moving_object.gravity ==  rect.bottom:
            is_hit = True
    return is_hit

def check_bottomside(moving_object:pygame.sprite,rect:pygame.Rect):
    is_hit = False
    if not (moving_object.rect.right == rect.left) and not (moving_object.rect.left == rect.right):               
        if moving_object.rect.bottom <= rect.top:
            is_hit = True          
    return is_hit

def check_mob_kill(player:Player,ennemie:Killeble):
    mob_is_killed = False   
    if (player.rect.bottom <= ennemie.rect.top) or (ennemie.is_jumped_on and ennemie.speed == 0):
        mob_is_killed = True
    if isinstance(ennemie,Turtle):
        if player.rect.bottom <= ennemie.rect.top + 11 and ennemie.direction == player.direction:
            mob_is_killed = True
    return mob_is_killed

def create_future_position(player:Player,off_set) -> pygame.Rect:                
    future_position = create_basic_future_position(player,off_set)        
    if player.is_swinging: 
        speed_distance = player.speed if player.direction > 0 else -player.speed            
        future_position.x -= speed_distance
        future_position.x += ceil(player.swing_velocity.x)
        future_position.y -= floor(player.gravity)
        future_position.y += ceil(player.swing_velocity.y)
    return future_position
    
def create_basic_future_position(moving_object,off_set)-> pygame.Rect:
    future_surf = pygame.Surface((32,moving_object.rect.height))   
    speed_distance = moving_object.speed if moving_object.direction > 0 else -moving_object.speed                                                                
    future_position = future_surf.get_rect(topleft = (moving_object.rect.x + speed_distance + off_set ,moving_object.rect.y + moving_object.gravity))
    return future_position
       
    

                