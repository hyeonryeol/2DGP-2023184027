from pico2d import *
import math

open_canvas(1000, 800)
grass = load_image('grass.png')
character = load_image('character.png')

cx, cy = 500, 400   
r = 200             
angle = 0          

while(1):
    clear_canvas()
    
    x = cx + r * math.cos(angle)
    y = cy + r * math.sin(angle)
    character.draw(x, y)

    update_canvas()

    angle += 0.05   
    delay(0.01)
