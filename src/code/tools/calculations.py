from math import pow,sqrt,floor,atan2,cos,sin

def calculate_distance_between_objects(object1:tuple,object2:tuple):
    b = object2[0] - object1[0]
    c =  abs(object1[1] - object2[1])
    # a² = b² + c²
    a = sqrt(pow(b,2) + pow(c,2))
    angle = atan2(c, b) #angle berekenen komt van chatGTP maar 
                        #wel wat moete spelen om juist te weten of het c 
                        #en b is en in die volgorde
    return (floor(a),angle)

def calculate_endpoints_withLength(angle,length,start_pos):#Letterlijk copie paste van chatGTP
    new_dx = length * cos(angle)
    new_dy = length * sin(angle)
    new_end_point = (start_pos[0] + new_dx, start_pos[1] - new_dy)
    return new_end_point