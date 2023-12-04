
from entities import StaticTile,Brick,Limiter,Coin,Question_box,Mushroom,Cloud,Mushroom_bonus,Flower_bonus,Save,Turtle
import pygame
from settings import TILE_SIZE,FULL_TURTLE_HEIGHT,TILE_HEIGHT_REGULAR
from tools.path_helper import BONUS_MUSHROOM_PATH,FLOWER_PATHS,SHELL_TURTLE_PATH_SPRITES,FULL_TURTLE_PATH_SPRITES,PLAYER_TILES_PATH,GAME_TILES_PATH,SAVE_TILES_PATH
from tools.tools import import_cut_graphics
from audio import bonus_grow_sound
from tools.tmx_map_util import Map_builder

class Level:

    def __init__(self,level:str,surface:pygame.Surface):
        self.current_level = level
        self.map_builder:Map_builder = Map_builder(level)
        self.spritesheet = import_cut_graphics(GAME_TILES_PATH,TILE_HEIGHT_REGULAR)        
        self.save_spritesheet = import_cut_graphics(SAVE_TILES_PATH,TILE_HEIGHT_REGULAR)
        self.full_turtle_sprites = import_cut_graphics(FULL_TURTLE_PATH_SPRITES,FULL_TURTLE_HEIGHT)
        self.player_and_mobs_sprite = import_cut_graphics(PLAYER_TILES_PATH,TILE_HEIGHT_REGULAR) 
        self.bullets = pygame.sprite.Group()
        self.ennemies = pygame.sprite.Group()
        self.collision_blocks = pygame.sprite.Group()        
        self.bonusses:pygame.sprite.Group = pygame.sprite.Group()  

        self.map_builder.create_animated_tiles(0.05,Question_box,"questionmark",group = self.collision_blocks)
        self.map_builder.create_tiles(Brick,"collision_bloks",group= self.collision_blocks) 
        
        self.swing_points:pygame.sprite.Group = self.map_builder.create_tiles(Brick,"swing_points")              
        self.limiter_block:pygame.sprite.Group = self.map_builder.create_tiles(Limiter,"limiter_blok",allow_image= False)
        self.clouds:pygame.sprite.Group = self.map_builder.create_tiles(Cloud,"clouds") 
        self.save:pygame.sprite.Group = self.map_builder.create_tiles(Save,"save")
        self.coins:pygame.sprite.Group = self.map_builder.create_animated_tiles(0.15,Coin,"coin")        
        self.castle:pygame.sprite.Group = self.map_builder.create_tiles(StaticTile,"castle")
        self.end_level:pygame.sprite.Group = self.map_builder.create_tiles(StaticTile,"end_level")
        self.grass:pygame.sprite.Group = self.map_builder.create_tiles(StaticTile,"grass")  
        self.mountens:pygame.sprite.Group = self.map_builder.create_tiles(StaticTile,"mountens")  
        self.__create_mushroom__(self.ennemies)
        self.__create_turtle__(0.15,FULL_TURTLE_HEIGHT,FULL_TURTLE_PATH_SPRITES,"turtle",1)
             
               
        self.display = surface
        self.movement_offset = 0
        self.swing_offset = 0
        self.off_set = 0
        self.end_map = False          
        self.player_start_position = self.map_builder.get_player_startposition()
        self.save_button_x_location = -abs(self.save.sprites()[0].rect.x - 32)
        self.is_saved = False 
        self.is_restarted = False
        self.total_distance_traveled = 0 #first offset start when player is on 300px

    
    def __create_turtle__(self,
                      animation_step,
                      height:int,
                      sprite_path:str,
                      layer_name:str,
                      movement:int):
        shell_images = import_cut_graphics(SHELL_TURTLE_PATH_SPRITES,TILE_SIZE)
        items = self.map_builder.create_animated_tile_with_onw_spritesheet(animation_step,height,sprite_path,layer_name,movement)
        for item in items:
            item:Turtle
            item.shell_frames = shell_images
            item.moving_frames = item.frames
            self.ennemies.add(item)   
    
    def __create_mushroom__(self,group:pygame.sprite.Group):
        mushroom_group = self.map_builder.create_animated_tiles(0.15,Mushroom,"mushroom",1)
        for mushroom in mushroom_group:            
            mushroom:Mushroom
            mushroom.death_image = self.player_and_mobs_sprite[170]
        group.add(mushroom_group)     
     
    def __create_static_bonus__(self,size,x,y,speed,type,path,level):        
        image = pygame.image.load(str(path)).convert_alpha()         
        image = image
        bonus = type(size,x,y,speed,image,level)            
        return bonus
    
    def __create_animated_bonus__(self,size,x,y,speed,type,path,level,steps):
        bonus = self.__create_static_bonus__(size,x,y,speed,type,path,level)
        bonus.animation_step = steps         
        return bonus
    
    def create_bonus_animation(self,block,player):         
        bonus_grow_sound()
        if player.level  == 0:
            sprite = self.__create_static_bonus__(TILE_SIZE,block.rect.x,block.rect.top,2,Mushroom_bonus,BONUS_MUSHROOM_PATH,1)
        if player.level >= 1:
            sprite = self.__create_animated_bonus__(TILE_SIZE,block.rect.x,block.rect.top + block.bump_hight,2,Flower_bonus,FLOWER_PATHS[0],2,0.15)
            paths = FLOWER_PATHS
            for path in paths:
                image =  pygame.image.load(path).convert_alpha()
                sprite.frames.append(image)                
            sprite.max_animation_index = len(sprite.frames)- 1
            
        self.bonusses.add(sprite)                            
        self.collision_blocks.remove(block)        
                             
        new_brick = Brick(TILE_SIZE,block.rect.x,block.rect.y,self.spritesheet[113])  
        new_brick.bump_timer = block.bump_timer
        new_brick.is_bumped = block.is_bumped
        self.__order_collision_block_group__(new_brick)

    def __order_collision_block_group__(self,new_brick):
        #This is done so the player wil be collision checked on the importend blocks first
        #Question block, then empty question and then bricks. Giving a smoother game play
        group_question =  [sprite for sprite in self.collision_blocks if type(sprite) == Question_box]
        brick_group =  [sprite for sprite in self.collision_blocks if type(sprite) != Question_box]
        self.collision_blocks.empty() 
        self.collision_blocks.add(group_question,new_brick,brick_group) 

    def activate_save(self,save:Save):
        if save.is_pressed == False:            
            save.image = self.save_spritesheet[1]
            save.image.set_colorkey([0,0,0])            
            self.is_saved = True
            save.is_pressed = True
            self.player_start_position = (86,save.rect.y)
 
    def restart(self,player):             
        saved = self.is_saved            
        player.reset(self.player_start_position)        
        self.__init__(self.current_level,self.display)            
        self.is_restarted = True        
        if saved: self.activate_save(self.save.sprites()[0])       

    def __initialize_after_restart__(self):
        if self.is_restarted:
            if self.is_saved:
                self.off_set = self.save_button_x_location
            self.is_restarted = False

    def load_next_level(self):
        level:list[int]=  [int(x) for x in self.current_level.replace('level','').split('_')]
        if level[1] < 9:
            level[1] += 1
        else: 
            level[0] += 1
            level[1] = 1
        new_level = f'level{level[0]}_{level[1]}'        
        try:
            self.__init__(new_level,self.display)
            return True
        except Exception:
            return False

    def run(self):   
        self.__initialize_after_restart__()           
        self.limiter_block.update(self.off_set)
        self.limiter_block.draw(self.display)      

        self.clouds.update(self.off_set)
        self.clouds.draw(self.display)        

        self.grass.update(self.off_set)
        self.grass.draw(self.display)  

        self.mountens.update(self.off_set)
        self.mountens.draw(self.display)  

        self.castle.update(self.off_set)
        self.castle.draw(self.display)

        self.end_level.update(self.off_set)
        self.end_level.draw(self.display)

        self.coins.update(self.off_set)
        self.coins.draw(self.display)    

        self.bonusses.update(self.off_set)
        self.bonusses.draw(self.display)

        self.collision_blocks.update(self.off_set)
        self.collision_blocks.draw(self.display)
        
        self.save.update(self.off_set)
        self.save.draw(self.display)

        self.ennemies.update(self.off_set)
        self.ennemies.draw(self.display)  

        self.bullets.update(self.off_set)
        self.bullets.draw(self.display) 

        self.swing_points.update(self.off_set)
        self.swing_points.draw(self.display)        

        