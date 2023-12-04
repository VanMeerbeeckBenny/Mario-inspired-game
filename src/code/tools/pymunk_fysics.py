import pymunk
import pymunk.pygame_util
from pygame import Rect

def create_space(drawing_screen):
    space = pymunk.Space()
    space.gravity = (0, 981)    
    pymunk.pygame_util.DrawOptions(drawing_screen)
    return space

def create_swing_effect(swing_point:Rect,player_pos:Rect,space):
    rotation_center_body = pymunk.Body(body_type=pymunk.Body.STATIC)
    rotation_center_body.position = (swing_point.midbottom)

    body = pymunk.Body()
    body.position = (player_pos)

    rope  = pymunk.Segment(body, swing_point.midbottom, (player_pos), 1)
    rope.mass = 8      
    rope.friction = 1        
    
    rect = pymunk.Poly.create_box(body,(2, 2))     
    rect.friction = 1

    rect.mass = 30
    rect.elasticity = 0.95
    rotation_center_joint = pymunk.PinJoint(body, rotation_center_body, (0, 0), (0, 0))

    space.add(rect,body, rotation_center_joint)
