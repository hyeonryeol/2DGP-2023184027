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

# 1번 동작(대기): 시트에서 같은 줄이므로 bottom과 h는 같고, 프레임마다 (left, w, dx)만 다르다
# dx: 프레임 가운데와 몸(머리·몸통) 중심의 차이(원본 픽셀). 이만큼 옮겨 그려 몸이 좌우로 흔들리지 않게 한다
IDLE_BOTTOM, IDLE_H = 447, 39
IDLE_FRAMES = [(1, 29, 2), (31, 26, 2), (58, 28, 2), (86, 30, 3), (118, 30, 4), (150, 30, 4),
               (182, 29, 3), (211, 29, 2), (240, 29, 2), (270, 24, 0), (302, 29, -3)]

running = True
frame_index = 0
last_frame_time = get_time()    # 마지막으로 프레임을 넘긴 시각


# 프레임 하나를 4배로 그린다.
# 몸 중심이 GROUND_X에 오도록 dx만큼 옮기고, 발이 GROUND_Y에 오도록 높이의 절반만큼 올린다
def draw_frame(left, w, dx, bottom, h):
    x = GROUND_X + dx * SCALE
    y = GROUND_Y + h * SCALE / 2
    sonic.clip_draw(left, bottom, w, h, x, y, w * SCALE, h * SCALE)


def handle_events():
    global running
    for event in get_events():
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False


# delay()를 쌓아서 재지 않고 실제 경과 시간으로 프레임을 넘긴다
def update():
    global frame_index, last_frame_time
    now = get_time()
    if now - last_frame_time >= FRAME_TIME:
        frame_index = (frame_index + 1) % len(IDLE_FRAMES)
        last_frame_time += FRAME_TIME
        # 창을 끄는 동안처럼 시간이 크게 튀었으면 밀린 시간은 버린다 (한 번에 1프레임만)
        if now - last_frame_time >= FRAME_TIME:
            last_frame_time = now


while running:
    handle_events()
    update()
    clear_canvas()
    left, w, dx = IDLE_FRAMES[frame_index]
    draw_frame(left, w, dx, IDLE_BOTTOM, IDLE_H)
    update_canvas()
    delay(0.01)

close_canvas()
