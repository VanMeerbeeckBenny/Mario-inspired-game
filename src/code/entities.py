import pygame
from tools.path_helper import BULLET_IMAGE_PATH
from audio import ennemie_hit_sound,kill_mob_sound

class BaseTile(pygame.sprite.Sprite):
    def __init__(self,size,x,y) -> None:
        super().__init__()
        self.image = pygame.Surface((size,size))
        self.rect= self.image.get_rect(topleft = (x,y))

    def update(self,off_set):
        self.rect.x += off_set

class StaticTile(BaseTile):
    def __init__(self,size,x,y,image):
        super().__init__(size,x,y)
        self.image = image  

class AnimatedTile(StaticTile):
    def __init__(self, size, x, y,image):
        super().__init__(size, x, y,image)
        self.frames= []
        self.max_animation_index = 0  
        self.current_animation_index = 0   
        self.image = image
        self.animation_step = 0             

    def update(self,off_set):
        self.rect.x += off_set        
        
        if len(self.frames) > 1:
            self.image = self.frames[int(self.current_animation_index)]
            if self.current_animation_index >= self.max_animation_index:
                self.current_animation_index = 0
            else: 
                self.current_animation_index += self.animation_step 

class Bullet (pygame.sprite.Sprite):
    def __init__(self,x,y,speed,direction) -> None:
        super().__init__()
        self.image = pygame.image.load(BULLET_IMAGE_PATH).convert_alpha()
        self.rect = self.image.get_rect(center = (x,y))
        self.speed = speed
        self.gravity = 0
        self.direction = direction
        self.destroyed = False
        self.impact_wall = False
    
    def update(self,off_set):        
        if self.impact_wall and self.destroyed == False:
            self.rect.width -= 5
            self.image = pygame.transform.scale(self.image,(self.rect.width,self.rect.height))
            # when width gets smaller a correction is needet to keep te bullet agains the wall
            correction =  4.5 if self.direction > 0 else 0.5
            total_off_set = correction + off_set
            self.rect.x += total_off_set
            self.speed = 0
            if self.rect.width <= 5: self.destroyed = True
        elif self.destroyed:
            self.gravity += 0.3
            self.rect.y += self.gravity
            self.rect.x += off_set
        else:self.rect.x += off_set + self.speed

    
class Save(StaticTile):
    def __init__(self, size, x, y, image):
        self.is_pressed = False
        super().__init__(size, x, y, image)

class Limiter(BaseTile):
    def __init__(self, size, x, y):
        super().__init__(size, x, y)
        self.image.set_colorkey([0,0,0])

class Collision_block(StaticTile):
    def __init__(self, size, x, y, image,bump_hight = 5):
        super().__init__(size, x, y, image) 
        self.is_bumped = False
        self.bump_timer = 0
        self.bump_max_time = 1
        self.bump_steps = 0.3
        self.bump_hight = bump_hight

    def update(self, off_set):        
        if self.is_bumped:
            if self.bump_timer <= self.bump_max_time:
                self.bump_timer += self.bump_steps
            else:
                self.rect.y += self.bump_hight
                self.bump_timer = 0
                self.is_bumped = False
        super().update(off_set)


    def bump_annimation(self):
        if not self.is_bumped:
            self.rect.y -= self.bump_hight
            self.is_bumped = True
        

        
class Brick(Collision_block):
    def __init__(self, size, x, y, image):
        super().__init__(size, x, y, image)

class Cloud(StaticTile):
    def __init__(self, size, x, y, image):
        super().__init__(size, x, y, image)

class Static_bonus(StaticTile):
    def __init__(self, size, x, y,speed, image,level):
        self.level = level
        self.speed = speed        
        self.start_position = y
        self.size = size
        self.direction = 1
        self.gravity = 0
        self.fully_spawned = False
        super().__init__(size, x, y, image)

    def update(self,off_set):
        super().update(off_set)
        end_position = self.start_position - self.size
        if self.rect.top > end_position and not self.fully_spawned:
            self.rect.y -=  1


class Mushroom_bonus(Static_bonus):
    def __init__(self, size, x, y,speed, image,level):
        super().__init__(size, x, y,speed, image,level)

    def update(self,off_set):
        super().update(off_set)
        end_position = self.start_position - self.size
        if self.rect.top < self.start_position and self.fully_spawned:
            self.rect.x += self.speed if self.direction > 0 else -abs(self.direction)-0.5
        elif self.rect.top == end_position:            
            self.fully_spawned = True  
        elif self.rect.top > end_position and self.fully_spawned:
            self.rect.x +=  self.speed if self.direction > 0 else -abs(self.direction)-0.5
    
    def change_direction(self):
        if self.direction > 0:
            self.speed = -abs(self.speed) 
            self.direction = -1 
        else:
            self.speed = abs(self.speed)
            self.direction = 1
        
class Flower_bonus(Static_bonus,AnimatedTile):
    def __init__(self, size, x, y, speed, image,level):
        super().__init__(size, x, y, speed, image,level)
class Coin(AnimatedTile):
    def __init__(self, size, x, y,image):
        super().__init__(size, x, y,image) 

class Question_box(AnimatedTile,Collision_block):
    def __init__(self, size, x, y,image):
        super().__init__(size, x, y,image) 

class Killeble(AnimatedTile):
    def __init__(self, size, x, y, image):
        self.death_gravity = -3        
        self.is_dead = False   
        self.speed = 0 
        self.is_jumped_on = False
        self.gravity = 0  
        self.direction = 1     
        super().__init__(size, x, y, image)   
    

    def death_by_bullet_annimation(self):
        if self.is_dead == False:
            ennemie_hit_sound()
            self.max_animation_index = 1            
            self.image = pygame.transform.flip(self.frames[0],False,True)
            self.frames.clear()            
            self.rect.y += self.death_gravity
            self.is_dead = True
        

    def update(self,off_set):           
        if self.is_dead :            
            self.death_gravity += 0.3
            self.rect.y += self.death_gravity
            self.speed = 0
            self.is_jumped_on = True 

        if not self.is_jumped_on:
            self.speed = 1 if self.direction > 0 else -1

        off_set = off_set + self.speed
        super().update(off_set)

    def change_direction(self):
        speed = 5 if self.is_jumped_on else 1
        if self.direction < 1:
            self.direction = 1
            self.speed = speed            
        else:
            self.direction = -1
            self.speed = -speed         
        flipped_images:list = []
        for image in self.frames:
            flipped_image = pygame.transform.flip(image,True,False)
            flipped_images.append(flipped_image)        
        self.frames = flipped_images
        self.rect.x += self.speed

class Mushroom(Killeble):
    def __init__(self, size, x, y,image):
        self.death_image = pygame.Surface((size,size))
        super().__init__(size, x, y,image)  

    def jumped_on(self,direction):
        self.frames.clear()
        self.image= self.death_image        
        self.speed = 0
        self.death_gravity = - 0.1
        self.rect.y += self.death_gravity
        self.is_dead = True
        kill_mob_sound()
    

class Turtle(Killeble):
    def __init__(self, size, x, y, image):
        super().__init__(size, x, y, image)   
        self.is_projectil = False     
        self.shell_time = 5
        self.shell_step = 0.03
        self.shell_wake_up_time = 2
        self.shell_wake_up_step = 0.03
        self.shell_frames:list[pygame.Surface] = []  
        self.moving_frames:list[pygame.Surface] = []  

    def jumped_on(self,direction):
        kill_mob_sound()
        if not self.is_jumped_on:
            self.speed = 0
            self.frames.clear()  
            self.frames.append(self.shell_frames[0])     
            self.image = self.shell_frames[0]            
            self.rect = self.image.get_rect(bottomright = self.rect.bottomright)
            self.is_jumped_on = True
        elif abs(self.speed) <= 1: 
            self.speed = 5 if direction > 0 else - 5
            self.rect.x += self.speed
            self.direction = direction
            self.is_projectil = True
        elif abs(self.speed) == 5:
            self.speed = 0
            self.is_projectil = False   

    def death_by_bullet_annimation(self):
        if self.is_dead == False:
            self.is_projectil = False 
        super().death_by_bullet_annimation()
                 
        