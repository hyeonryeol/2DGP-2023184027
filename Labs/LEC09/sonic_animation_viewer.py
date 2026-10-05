from pico2d import *

CANVAS_W, CANVAS_H = 800, 600
SCALE = 4                       # 확대 배율
GROUND_X, GROUND_Y = 400, 200   # 몸 중심선 x, 발 기준선 y
FRAME_TIME = 0.1                # 프레임 간격(초)
REPEAT_COUNT = 5                # 동작별 반복 횟수
PAUSE_TIME = 1.0                # 동작 사이 정지 시간(초)

open_canvas(CANVAS_W, CANVAS_H)

running = True


def handle_events():
    global running
    for event in get_events():
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False


while running:
    handle_events()
    clear_canvas()
    update_canvas()
    delay(0.01)

close_canvas()
