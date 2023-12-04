import pytmx
import pygame
from pytmx import TiledMap
from settings import TILE_SIZE,FULL_TURTLE_HEIGHT,ANIMATION_DICT
from tools.path_helper import LEVEL_DICT
from pytmx import TiledMap,TiledTileLayer,TiledTileLayer
from entities import AnimatedTile,Turtle
from tools.tools import import_cut_graphics

class Map_builder():
     
    def __init__(self,level):
        self.tmx_map:TiledMap = pytmx.load_pygame(LEVEL_DICT[level])
     
    def set_map(self,level):
        self.tmx_map:TiledMap = pytmx.load_pygame(LEVEL_DICT[level])


    def create_tiles(self,classType:object,layer_name:str,allow_image = True,group:pygame.sprite.Group = None) -> pygame.sprite.Group():
            
            layer:TiledTileLayer
            items = pygame.sprite.Group()
            for layer in self.tmx_map:
                if layer.name == layer_name:
                    for x,y,image in layer.tiles():                
                        x_pixel = x*32
                        y_pixel = y *32  
                        if allow_image:
                            item = classType(TILE_SIZE,x_pixel,y_pixel,image)
                            items.add(item)
                        else:
                            item = classType(TILE_SIZE,x_pixel,y_pixel)
                            items.add(item)
            if group == None:return items
            else: group.add(items)
   
    def create_animated_tiles(self,
                                animation_step:float,
                                classType:AnimatedTile,
                                layer_name:str,
                                movement:int = None,
                                group:pygame.sprite.Group = None):
            
            layer:TiledTileLayer
            items = pygame.sprite.Group()
            for layer in self.tmx_map:
                if layer.name == layer_name: 
                    for x,y,image in layer.tiles():                                        
                        x_pixel = x*32
                        y_pixel = y *32  
                        item:AnimatedTile = classType(TILE_SIZE,x_pixel,y_pixel,image)                        
                        for key,value in ANIMATION_DICT.items():                            
                            if layer_name in key:
                                for gid, props in self.tmx_map.tile_properties.items():
                                    if props["id"] == int(value):
                                        item.animation_step  = animation_step
                                        for i in range(0,len(props["frames"])):
                                            item.frames.append(self.tmx_map.get_tile_image_by_gid( props["frames"][i].gid))  
                                            item.image = item.frames[0] 
                                            item.max_animation_index = len(item.frames)-1    
                                            if movement != None: item.speed  = movement                   
                                            items.add(item)
                                        break        
            if group is not None:group.add(items)
            else: return items

    def create_animated_tile_with_onw_spritesheet(self,
                                                    animation_step,
                                                    height:int,
                                                    sprite_path:str,
                                                    layer_name:str,
                                                    movement:int):
            layer:TiledTileLayer
            items = pygame.sprite.Group()
            IMAGES = import_cut_graphics(sprite_path,height)
            for layer in self.tmx_map:
                if layer.name == layer_name: 
                    for x,y,image in layer.tiles():                                        
                        x_pixel = x*32
                        y_pixel = (y * 32) - (height - TILE_SIZE)                 
                        item:Turtle = Turtle(TILE_SIZE,x_pixel,y_pixel,IMAGES[0])
                        item.rect.height = FULL_TURTLE_HEIGHT
                        for image in IMAGES:                        
                            item.frames.append(image)
                        item.max_animation_index = len(IMAGES) - 1
                        item.animation_step = animation_step
                        item.speed = movement
                        items.add(item)
            return items

    def get_player_startposition(self,layer_name = 'player'):
            player_position:tuple
            for layer in self.tmx_map:
                if layer.name == layer_name:
                    for x,y,image in layer.tiles():                
                        x_pixel = x*32
                        y_pixel = y *32
                        player_position = (x_pixel,y_pixel)        
            return player_position 

    def get_map_dimensions(self)-> dict:    
        return {
            'width':self.tmx_map.width * TILE_SIZE,
            'height':self.tmx_map.height * TILE_SIZE
        }