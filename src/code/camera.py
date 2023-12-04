from level import Level
from player import Player
from settings import SCREEN_WIDTH

class Camera():
    
    def run(self,player:Player,level:Level):
        self.map_dimensions = level.map_builder.get_map_dimensions()
        self.check_ending_map(player,level)
        self.shift_camera(player,level)

    def shift_camera(self,player:Player,level:Level):
        if not level.end_map:
            if player.swing_distance > 0 and not player.is_swinging:
                if player.swing_distance - 15 > 0:
                    player.swing_distance -= 15            
                    level.swing_offset= -15
                    player.rect.x -= 15
                else:
                    left_over_distance = player.swing_distance
                    player.swing_distance = 0
                    level.swing_offset= -left_over_distance
                    player.rect.x -= left_over_distance

            else: 
                player.swing_distance = 0 
                level.swing_offset= 0
        self.set_offset(player,level)
                
            

    def check_ending_map(self,player:Player,level:Level):           
        level.total_distance_traveled+= abs(level.off_set)
        
        if level.total_distance_traveled >= self.map_dimensions["width"] - SCREEN_WIDTH:
            level.end_map = True               
            if player.rect.right >= SCREEN_WIDTH:
                    player.prevent_movement_right = True 
   
    def set_offset(self,player:Player,level:Level):
        if not level.end_map:
            #this is used so there's no gap at the end, make the map stop perfect on the pixel
            future_total_distance = level.total_distance_traveled + abs(level.movement_offset + level.swing_offset)                           
            if future_total_distance >=  (self.map_dimensions["width"] - SCREEN_WIDTH):
                off_set = (self.map_dimensions["width"] - SCREEN_WIDTH) - level.total_distance_traveled
                level.off_set = off_set
            else :
                    level.off_set = level.movement_offset + level.swing_offset
        else: 
                 level.off_set = 0
                 player.swing_distance = 0