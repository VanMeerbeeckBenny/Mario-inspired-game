from tools.enums import Movement_enum
import pygame


def set_images(player,movement_type:Movement_enum): 
    if player.level == 0:
        IMAGES = player.IMAGES
        STAND_IMAGE_LEVEL0 = IMAGES[41]
        STOP_IMAGE_LEVEL0 = IMAGES[44]
        JUMP_IMAGE_LEVEL0 = IMAGES[43]
        RUN_IMAGE_LEVEL0 = IMAGES[slice(51,56,1)]
        __set_player_images__(player,movement_type,JUMP_IMAGE_LEVEL0,STOP_IMAGE_LEVEL0,RUN_IMAGE_LEVEL0,STAND_IMAGE_LEVEL0)
    elif player.level == 1:
        BIG_IMAGES = player.BIG_IMAGES
        STAND_IMAGE_LEVEL1 = BIG_IMAGES[2]
        STOP_IMAGE_LEVEL1 = BIG_IMAGES[15] 
        JUMP_IMAGE_LEVEL1 = BIG_IMAGES[4]
        RUN_IMAGE_LEVEL1 = BIG_IMAGES[slice(11,16,1)]
        __set_player_images__(player,movement_type,JUMP_IMAGE_LEVEL1,STOP_IMAGE_LEVEL1,RUN_IMAGE_LEVEL1,STAND_IMAGE_LEVEL1)
    elif player.level == 2:
        BIG_IMAGES = player.BIG_IMAGES
        STAND_IMAGE_LEVEL2 = BIG_IMAGES[61] 
        STOP_IMAGE_LEVEL2 = BIG_IMAGES[64]
        JUMP_IMAGE_LEVEL2 = BIG_IMAGES[63]  
        RUN_IMAGE_LEVEL2 = BIG_IMAGES[slice(71,76,1)]
        __set_player_images__(player,movement_type,JUMP_IMAGE_LEVEL2,STOP_IMAGE_LEVEL2,RUN_IMAGE_LEVEL2,STAND_IMAGE_LEVEL2)

def __set_player_images__(player,movement_type:Movement_enum,jump_image,stop_image,run_images,stand_image): 
    if Movement_enum.STAND == movement_type:
        __set_stand_image__(player,stand_image)
    elif Movement_enum.JUMP == movement_type:        
        __set_jump_image__(player,jump_image)
    elif Movement_enum.RUN == movement_type:
        if not player.is_jumping :            
            __set_run_image__(player,run_images)
        else:__set_jump_image__(player,jump_image)
    elif Movement_enum.STOP == movement_type:
        __set_stop_image__(player,stop_image)
    


def __set_image_on_direction__(direction:int,image):    
    if direction < 0 :
        return pygame.transform.flip(image,True,False)
    elif direction > 0 : return image 

def __set_jump_image__(player,image):      
    player.image = __set_image_on_direction__(player.direction,image)

def __set_run_image__(player,frames):
    player.frames = frames
    image = player.frames[int(player.current_frame_index)]
    player.image = __set_image_on_direction__(player.direction,image)

def __set_stand_image__(player,image):
    if not player.is_jumping:
        player.image = __set_image_on_direction__(player.direction,image)

def __set_stop_image__(player,image):
    player.image = __set_image_on_direction__(player.direction,image)   
