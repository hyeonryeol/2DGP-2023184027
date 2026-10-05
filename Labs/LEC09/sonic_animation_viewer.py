from pico2d import *
import os

CANVAS_W, CANVAS_H = 800, 600
SCALE = 4                       # 확대 배율
GROUND_X, GROUND_Y = 400, 200   # 몸 중심선 x, 발 기준선 y
FRAME_TIME = 0.1                # 프레임 간격(초)
REPEAT_COUNT = 5                # 동작별 반복 횟수
PAUSE_TIME = 1.0                # 동작 사이 정지 시간(초)

open_canvas(CANVAS_W, CANVAS_H)

# 어느 폴더에서 실행해도 이미지를 찾도록 이 파일이 있는 폴더를 기준으로 경로를 만든다
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sonic = load_image(os.path.join(BASE_DIR, 'sonic-sprite.png'))

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
    # 1번 동작(대기)의 첫 프레임: left=1, bottom=447, 크기 29x39
    sonic.clip_draw(1, 447, 29, 39, GROUND_X, GROUND_Y)
    update_canvas()
    delay(0.01)

close_canvas()
