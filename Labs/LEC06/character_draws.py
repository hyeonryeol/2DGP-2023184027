from pico2d import *
import math
open_canvas(800, 600)

character = load_image('character.png')

cx, cy = 400, 300   
r = 200
def draw_character():
    character.draw(cx, cy)

   

def draw_character(x, y):
    clear_canvas()
    character.draw(x, y)
    update_canvas()
    delay(0.05)

def move_top():
    print("Top")
    for x in range(50, 750, 5):
        draw_character(x, 550)

def move_right():
    print("Right")
    for y in range(550, 50, -5):
        draw_character(750, y)

def move_bottom():
    print("Bottom")
    for x in range(750, 50, -5):
        draw_character(x, 50)
    pass
def move_left():
    print("Left")
    for y in range(50, 550, 5):
        draw_character(50, y)
    pass
def move_triangle_top():
    print("Triangle Top")
    pass
def move_triangle_right():
    print("Triangle Right")
    pass
def move_triangle_left():
    print("Triangle Left")
    pass

def move_circle():
    print("Circle")
    for deg in range(0, 360, 5):
        angle = math.radians(deg)
        x = cx + r * math.cos(angle)
        y = cy + r * math.sin(angle)
        draw_character(x, y)
      

def move_rectangle():
    print("Rectangle")
    move_top()
    move_right()
    move_bottom()
    move_left()
    pass

def move_triangle():
    print("Triangle")
    move_triangle_top()
    move_triangle_right()
    move_triangle_left()
    pass


while True:
    #move_circle()
    #move_rectangle()
    move_triangle()
    pass

close_canvas()