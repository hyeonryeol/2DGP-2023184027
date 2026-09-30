from pico2d import *

SCALE = 10      # 캐릭터 확대 배율 (키 38픽셀 -> 380픽셀, 화면 높이 600의 절반 이상)

open_canvas(800, 600)

sonic = load_image('sonic-sprite.png')

# 애니메이션 목록: (이름, 프레임 목록)
# 프레임 위치는 (left, top, width, height)
# 그림판에서 보이는 것처럼 시트 왼쪽 위를 (0, 0)으로 잰 픽셀 좌표
animations = [
    ('Idle', [(86, 40, 30, 38), (118, 40, 30, 38), (150, 40, 30, 38), (182, 40, 29, 38)]),
    ('Walk', [(8, 80, 26, 37), (37, 80, 27, 37), (65, 80, 31, 38),
              (97, 80, 37, 37), (135, 80, 32, 35), (170, 79, 32, 38)]),
    ('Run', [(72, 286, 39, 31), (123, 285, 39, 32), (172, 286, 39, 31), (218, 285, 38, 32)]),
    ('Spin', [(1, 169, 29, 30), (35, 167, 29, 31), (67, 169, 30, 29), (98, 169, 31, 29),
              (131, 168, 29, 30), (162, 168, 29, 31), (193, 170, 30, 29), (230, 170, 31, 29)]),
    ('Twirl', [(1, 326, 24, 45), (31, 327, 29, 44), (65, 327, 20, 44),
               (90, 327, 25, 43), (119, 327, 25, 43), (149, 327, 20, 44)]),
]


GROUND_X, GROUND_Y = 400, 100    # 캐릭터 발밑(땅) 위치


# 프레임 하나를 SCALE배 확대해서 그린다.
# 프레임마다 크기가 달라서 중심에 맞춰 그리면 캐릭터가 위아래로 흔들리므로,
# 프레임의 아래쪽 가운데(발밑)를 땅 위치 (GROUND_X, GROUND_Y)에 맞춘다.
# clip_draw는 시트 왼쪽 아래 기준이므로 top을 bottom으로 바꿔 준다.
def draw_frame(frame):
    left, top, w, h = frame
    bottom = sonic.h - top - h
    x = GROUND_X
    y = GROUND_Y + h * SCALE / 2
    sonic.clip_draw(left, bottom, w, h, x, y, w * SCALE, h * SCALE)


anim = 1
frame = 0
while True:
    name, frames = animations[anim]
    clear_canvas()
    draw_frame(frames[frame])
    update_canvas()
    frame = (frame + 1) % len(frames)
    delay(0.15)

close_canvas()
