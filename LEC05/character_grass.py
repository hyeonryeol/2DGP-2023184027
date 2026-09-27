from pico2d import *

open_canvas(1000,800)
grass = load_image('grass.png')
character = load_image('character.png')

x = 10
y = 90
direction = 1
while(1):
    clear_canvas()  
    character.draw(x, y)
    update_canvas()
    if direction == 1:
        x += 2
    if x >= 800 and direction == 1:
      y += 2
      x = 800
      if y == 600:
        direction = -1
    if y >= 600 and direction == -1:
        y = 600
        x -= 2
        
    if x <= 10 and direction == -1:
        y -= 2
        x = 10
        if y == 90:
            direction = 1
   

    delay(0.01)

