from pico2d import *
import math

open_canvas(800, 600)
grass = load_image('grass.png')
character = load_image('character.png')

running = True


# 창 닫기와 ESC 처리
def handle_events():
    global running
    for event in get_events():
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False


# 한 장면 그리기
def draw_frame(x, y):
    clear_canvas()
    grass.draw(400, 30)
    character.draw(x, y)
    update_canvas()
    handle_events()
    delay(0.01)


# 원운동 한 바퀴
def move_circle():
    cx, cy, r = 400, 320, 230
    for deg in range(-90, 270, 2):
        if not running:
            return
        rad = math.radians(deg)
        draw_frame(cx + r * math.cos(rad), cy + r * math.sin(rad))


# 두 점 사이 직선 이동
def move_line(x1, y1, x2, y2):
    steps = int(max(abs(x2 - x1), abs(y2 - y1)) / 5)
    for i in range(steps):
        if not running:
            return
        t = i / steps
        draw_frame(x1 + (x2 - x1) * t, y1 + (y2 - y1) * t)


# 점 목록을 따라 이동
def move_path(points):
    for i in range(len(points) - 1):
        x1, y1 = points[i]
        x2, y2 = points[i + 1]
        move_line(x1, y1, x2, y2)


# 사각운동 한 바퀴
def move_rectangle():
    move_path([(400, 90), (770, 90), (770, 550), (30, 550), (30, 90), (400, 90)])


# 삼각운동 한 바퀴
def move_triangle():
    move_path([(400, 90), (740, 90), (400, 550), (60, 90), (400, 90)])


while running:
    move_circle()
    move_rectangle()
    move_triangle()

close_canvas()
