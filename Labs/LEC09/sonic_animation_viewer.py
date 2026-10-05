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

# 1번 동작(대기): 시트에서 같은 줄이므로 bottom과 h는 같고, 프레임마다 (left, w)만 다르다
IDLE_BOTTOM, IDLE_H = 447, 39
IDLE_FRAMES = [(1, 29), (31, 26), (58, 28), (86, 30), (118, 30), (150, 30),
               (182, 29), (211, 29), (240, 29), (270, 24), (302, 29)]

running = True
frame_index = 0


# 프레임 하나를 4배로 그린다. 발이 GROUND_Y에 오도록 높이의 절반만큼 올린다
def draw_frame(left, w, bottom, h):
    sonic.clip_draw(left, bottom, w, h, GROUND_X, GROUND_Y + h * SCALE / 2, w * SCALE, h * SCALE)


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
    left, w = IDLE_FRAMES[frame_index]
    draw_frame(left, w, IDLE_BOTTOM, IDLE_H)
    update_canvas()
    delay(0.01)

close_canvas()
