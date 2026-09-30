from pico2d import *

SCALE = 10      # 캐릭터 확대 배율 (키 38픽셀 -> 380픽셀, 화면 높이 600의 절반 이상)

open_canvas(800, 600)

sonic = load_image('sonic-sprite.png')

# 애니메이션 목록: (이름, 한 프레임 보여 주는 시간(초), 프레임 목록)
# 프레임 위치는 (left, top, width, height)
# 그림판에서 보이는 것처럼 시트 왼쪽 위를 (0, 0)으로 잰 픽셀 좌표
# 5번째 값이 있으면 그 프레임을 좌우로 옮길 픽셀 수(dx) - 몸통 위치를 맞추는 보정값
animations = [
    ('Idle', 0.15, [(86, 40, 30, 38), (118, 40, 30, 38), (150, 40, 30, 38), (182, 40, 29, 38)]),
    ('Walk', 0.1, [(8, 80, 26, 37, -1), (37, 80, 27, 37, -1), (65, 80, 31, 38),
                    (97, 80, 37, 37), (135, 80, 32, 35), (170, 79, 32, 38, 2)]),
    ('Run', 0.06, [(72, 286, 39, 31), (123, 285, 39, 32), (172, 286, 39, 31), (218, 285, 38, 32)]),
    ('Spin', 0.05, [(1, 169, 29, 30), (35, 167, 29, 31), (67, 169, 30, 29), (98, 169, 31, 29),
                    (131, 168, 29, 30), (162, 168, 29, 31), (193, 170, 30, 29), (230, 170, 31, 29)]),
    ('Twirl', 0.1, [(1, 326, 24, 45), (31, 327, 29, 44), (65, 327, 20, 44),
                    (90, 327, 25, 43), (119, 327, 25, 43), (149, 327, 20, 44)]),
]


GROUND_X, GROUND_Y = 400, 100    # 캐릭터 발밑(땅) 위치


# 프레임 하나를 SCALE배 확대해서 그린다.
# 프레임마다 크기가 달라서 중심에 맞춰 그리면 캐릭터가 위아래로 흔들리므로,
# 프레임의 아래쪽 가운데(발밑)를 땅 위치 (GROUND_X, GROUND_Y)에 맞춘다.
# 걷기처럼 다리를 뻗으면 프레임 폭이 넓어져 몸통이 옆으로 밀리므로 dx로 보정한다.
# clip_draw는 시트 왼쪽 아래 기준이므로 top을 bottom으로 바꿔 준다.
def draw_frame(frame):
    left, top, w, h = frame[:4]
    dx = frame[4] if len(frame) > 4 else 0
    bottom = sonic.h - top - h
    x = GROUND_X + dx * SCALE
    y = GROUND_Y + h * SCALE / 2
    sonic.clip_draw(left, bottom, w, h, x, y, w * SCALE, h * SCALE)


REPEAT_COUNT = 5    # 애니메이션 하나를 반복하는 횟수
PAUSE_TIME = 1.0    # 반복이 끝난 뒤 멈춰 있는 시간(초)

anim_index = 0      # 지금 재생 중인 애니메이션 번호
frame_index = 0     # 그 애니메이션의 몇 번째 프레임인지
repeat = 0          # 지금까지 반복한 횟수
paused = False      # 5회 반복 뒤 1초 정지 중인지
pause_start = 0.0
last_frame_time = get_time()


# 다음 애니메이션으로 넘어간다. 마지막 다음은 다시 처음 (무한 반복)
def start_next_animation():
    global anim_index, frame_index, repeat, paused, last_frame_time
    anim_index = (anim_index + 1) % len(animations)
    frame_index = 0
    repeat = 0
    paused = False
    last_frame_time = get_time()
    print(animations[anim_index][0])


# 시간을 재서 프레임을 넘긴다.
# 프레임 수가 애니메이션마다 다르므로 항상 지금 애니메이션의 len(frames)로 한 바퀴를 판단한다.
def update():
    global frame_index, repeat, paused, pause_start, last_frame_time
    if paused:
        if get_time() - pause_start >= PAUSE_TIME:
            start_next_animation()
        return

    name, frame_time, frames = animations[anim_index]
    if get_time() - last_frame_time < frame_time:
        return
    last_frame_time += frame_time

    frame_index += 1
    if frame_index == len(frames):      # 한 바퀴 끝
        repeat += 1
        if repeat == REPEAT_COUNT:
            frame_index -= 1            # 정지하는 동안 마지막 프레임을 보여 준다
            paused = True
            pause_start = get_time()
        else:
            frame_index = 0


# 창 닫기 버튼이나 ESC 키를 누르면 종료
def handle_events():
    global running
    for event in get_events():
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False


def draw():
    clear_canvas()
    name, frame_time, frames = animations[anim_index]
    draw_frame(frames[frame_index])
    update_canvas()


running = True
print(animations[anim_index][0])
while running:
    handle_events()
    update()
    draw()
    delay(0.01)

close_canvas()
