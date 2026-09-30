from pico2d import *

open_canvas(800, 600)

sonic = load_image('sonic-sprite.png')

# 프레임 위치 (left, top, width, height)
# 그림판에서 보이는 것처럼 시트 왼쪽 위를 (0, 0)으로 잰 픽셀 좌표
idle_frames = [(86, 40, 30, 38), (118, 40, 30, 38), (150, 40, 30, 38), (182, 40, 29, 38)]


# 프레임 하나를 (x, y)에 그린다.
# clip_draw는 시트 왼쪽 아래 기준이므로 top을 bottom으로 바꿔 준다.
def draw_frame(frame, x, y):
    left, top, w, h = frame
    bottom = sonic.h - top - h
    sonic.clip_draw(left, bottom, w, h, x, y)


clear_canvas()
draw_frame(idle_frames[0], 400, 300)
update_canvas()
delay(3)

close_canvas()
