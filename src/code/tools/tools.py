import pygame
from settings import TILE_SIZE,SCREEN_WIDTH,SCREEN_HIGHT
from tools.path_helper import FONT_PATH

pygame.font.init()
font = pygame.font.Font(FONT_PATH,50)  

def import_cut_graphics(path:str, tile_height) -> list[pygame.Surface]:
    surface = pygame.image.load(path).convert_alpha()
    tile_num_x = int(surface.get_width() / TILE_SIZE)
    tile_num_y = int(surface.get_height() / tile_height)
    cut_tiles:list[pygame.Surface] = []
    for row in range(tile_num_y):
        for col in range(tile_num_x):
            x = col * TILE_SIZE
            y = row * tile_height
            new_surf = pygame.Surface((TILE_SIZE,tile_height))
            
            new_surf.blit(surface,(0,0),pygame.Rect(x,y,TILE_SIZE,tile_height)) #top left width and height
            new_surf.set_colorkey([0,0,0])
            cut_tiles.append(new_surf)
    return cut_tiles

def draw_text(surface:pygame.Surface,text:str,text_cordinate:tuple[int],location = 'topright',color = 'black'):
        text_surface= font.render(text,False,color)
        if location == 'topright' :text_rect = text_surface.get_rect(topright = (text_cordinate)) 
        if location == 'center' :text_rect = text_surface.get_rect(center = (text_cordinate))       
        
        surface.blit(text_surface,text_rect)
        return text_rect

def draw_lives_left(surface:pygame.Surface,lives,text_cordinates:tuple,image_coordinates:tuple,lives_image:pygame.image,location = 'topright',color = 'black'):         
        lives_text = f'x {lives}'        
        draw_text_with_image(
                            surface,
                            lives_text,
                            text_cordinates,
                            image_coordinates,
                            lives_image,
                            text_location = location,
                            text_color = color) 
               

def draw_level_and_lives(surface:pygame.Surface,level,lives,lives_image):
    text_cordinates = (SCREEN_WIDTH/2,SCREEN_HIGHT/2)
    image_coordinates = (SCREEN_WIDTH/2,SCREEN_HIGHT/2 - 5)
    text_level = f'level: {level.replace("level","").replace("_","-")}'
    draw_text(surface,text_level,
                (SCREEN_WIDTH/2-20,SCREEN_HIGHT/2 - 50),
                location='center',
                color= 'white')
    draw_lives_left(surface,
                    lives,
                    text_cordinates,
                    image_coordinates,
                    lives_image,
                    location= 'center',
                    color='white')
    
def draw_text_with_image(surface:pygame.Surface,
                        text:str,
                        text_cordinate:tuple,
                        image_cordinate:tuple,
                        image:pygame.Surface,                             
                        text_location = 'topright',
                        text_color = 'black'):
        
        text_rect = draw_text(surface,text,text_cordinate,text_location,text_color)
        image.set_colorkey([0,0,0])
        image_cordinate = (text_rect.left -20,image_cordinate[1])
        if text_location == 'topright' :rect = image.get_rect(topright = image_cordinate) 
        elif text_location == 'center':rect = image.get_rect(center = image_cordinate) 
        surface.blit(image,rect)  