from pico2d import *
open_canvas(800, 600)

character = load_image('character.png')

def draw_character():
    character.draw(400, 300)

def move_circle():
    print("Circle")
    clear_canvas()
    character.draw(400, 300)
    update_canvas()
    pass

def move_rectangle():
    print("Rectangle")
    pass

def move_triangle():
    print("Triangle")
    pass


while True:
    move_circle()
    move_rectangle()
    move_triangle()
    pass

close_canvas()