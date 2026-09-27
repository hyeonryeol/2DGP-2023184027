from pico2d import *
import math
open_canvas(800, 600)

character = load_image('character.png')

cx, cy = 400, 300   
r = 200             
angle = 0

def draw_character():
    character.draw(cx, cy)

def move_circle():
    global angle
    print("Circle")
    clear_canvas()

    x = cx + r * math.cos(angle)
    y = cy + r * math.sin(angle)
    character.draw(x, y)

    update_canvas()
    
    angle += 0.05
    
    delay(0.01)

    pass

def move_rectangle():
    print("Rectangle")
    pass

def move_triangle():
    print("Triangle")
    pass


while True:
    while(2 * math.pi >= angle):
        move_circle()
    angle = 0
    move_rectangle()
    move_triangle()
    pass

close_canvas()