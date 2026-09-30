from pico2d import *

SCALE = 10      # 캐릭터 확대 배율 (키 38픽셀 -> 380픽셀, 화면 높이 600의 절반 이상)

open_canvas(800, 600)

sonic = load_image('sonic-sprite.png')

# 프레임 위치 (left, top, width, height)
# 그림판에서 보이는 것처럼 시트 왼쪽 위를 (0, 0)으로 잰 픽셀 좌표
idle_frames = [(86, 40, 30, 38), (118, 40, 30, 38), (150, 40, 30, 38), (182, 40, 29, 38)]


# 프레임 하나를 SCALE배 확대해서 (x, y)에 그린다.
# clip_draw는 시트 왼쪽 아래 기준이므로 top을 bottom으로 바꿔 준다.
def draw_frame(frame, x, y):
    left, top, w, h = frame
    bottom = sonic.h - top - h
    sonic.clip_draw(left, bottom, w, h, x, y, w * SCALE, h * SCALE)


frame = 0
while True:
    clear_canvas()
    draw_frame(idle_frames[frame], 400, 300)
    update_canvas()
    frame = (frame + 1) % len(idle_frames)
    delay(0.15)

close_canvas()
