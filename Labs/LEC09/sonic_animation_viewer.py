# LEC09 소닉 애니메이션 뷰어 (개발 문서: PRD.md)
# sonic-sprite.png에 있는 동작 10종(76프레임)을 화면 가운데에서 2배로 순서대로 재생한다.
# 동작마다 5회 반복 -> 마지막 프레임에서 1초 정지 -> 다음 동작, 마지막 동작 뒤에는 처음부터 다시.
# ESC나 창 닫기 버튼으로 종료한다.
from pico2d import *
import pico2d
import os

CANVAS_W, CANVAS_H = 800, 600
SCALE = 2                       # 확대 배율
GROUND_X, GROUND_Y = 400, 200   # 몸 중심선 x, 발 기준선 y
FRAME_TIME = 0.1                # 프레임 간격(초)
REPEAT_COUNT = 5                # 동작별 반복 횟수
PAUSE_TIME = 1.0                # 동작 사이 정지 시간(초)

open_canvas(CANVAS_W, CANVAS_H)

# 어느 폴더에서 실행해도 이미지를 찾도록 이 파일이 있는 폴더를 기준으로 경로를 만든다
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sonic = load_image(os.path.join(BASE_DIR, 'sonic-sprite.png'))
# 상태 표시용 글꼴: pico2d에 들어 있는 한글 글꼴을 쓴다
font = load_font(os.path.join(os.path.dirname(pico2d.__file__), 'data', 'ConsolaMalgun.ttf'), 22)
TEXT_COLOR = (20, 20, 60)

# 동작 목록: (이름, bottom, h, [(left, w, dx), ...])
# 시트의 한 줄이 한 동작이다. 같은 줄은 bottom과 h가 같고, 프레임마다 (left, w, dx)만 다르다
# dx: 프레임 가운데와 몸(머리·몸통) 중심의 차이(원본 픽셀). 이만큼 옮겨 그려 몸이 좌우로 흔들리지 않게 한다
#     달리기 1·2번과 대시는 뻗은 장갑과 다리 잔상 때문에 계산값이 어긋나, 머리 위치를 보고 직접 맞춘 값이다
ANIMATIONS = [
    ('대기', 447, 39, [(1, 29, 2), (31, 26, 2), (58, 28, 2), (86, 30, 3), (118, 30, 4), (150, 30, 4),
                      (182, 29, 3), (211, 29, 2), (240, 29, 2), (270, 24, 0), (302, 29, -3)]),
    ('걷기', 407, 39, [(8, 26, 0), (37, 27, 0), (65, 31, 1), (97, 37, 1), (135, 32, 1), (170, 32, 3),
                      (206, 26, 0), (238, 24, -1), (263, 30, 0), (295, 36, -1), (334, 32, -2), (370, 29, -3)]),
    ('가속', 361, 43, [(1, 33, -4), (39, 35, -6), (89, 35, -5), (130, 34, -5), (181, 34, 0), (228, 33, 2)]),
    # 공처럼 도는 동작은 머리 위치로 중심을 잡을 수 없어, 프레임 가운데(공의 중심)에 맞춘다(dx=0)
    ('몸 말기', 325, 33, [(1, 29, 0), (35, 29, 0), (67, 30, 0), (98, 31, 0), (131, 29, 0), (162, 29, 0),
                         (193, 30, 0), (230, 31, 0), (268, 30, 0)]),
    ('구르기', 292, 27, [(1, 30, 0), (36, 29, 0), (70, 29, 0), (105, 29, 0), (139, 29, 0), (174, 29, 0)]),
    ('달리기', 251, 36, [(1, 29, -2), (36, 30, -4), (74, 31, -4), (111, 31, -4), (149, 30, -3), (186, 31, -4)]),
    ('대시', 207, 35, [(1, 29, -2), (36, 30, -4), (72, 39, -8), (123, 39, -8), (172, 39, -8), (218, 38, -8)]),
    ('뒤돌기·피격', 154, 45, [(1, 24, 0), (31, 29, 0), (65, 20, 1), (90, 25, 4), (119, 25, -3), (149, 20, 0),
                             (184, 40, 4), (232, 39, 3)]),
    ('정면 달리기', 108, 40, [(1, 27, 0), (31, 31, 4), (64, 31, 3), (99, 33, 0), (136, 32, 1), (176, 33, 0),
                             (217, 33, 1), (254, 33, 0)]),
    ('포즈', 56, 43, [(6, 34, 1), (49, 34, 1), (96, 23, 0), (125, 23, 0)]),
]

# 재생하면서 좌우로 움직이는 동작의 이동 속도(화면 픽셀/초). 여기 없는 동작은 제자리에서 재생한다
MOVE_SPEED = {'걷기': 100, '가속': 180, '구르기': 300, '달리기': 260, '대시': 400}
MOVE_MARGIN = 60    # 몸 중심이 화면 끝에서 이만큼 안쪽에 닿으면 방향을 바꾼다

running = True
anim_index = 0                  # 지금 재생 중인 동작 번호
frame_index = 0                 # 그 동작의 몇 번째 프레임인지
loop_count = 0                  # 지금까지 끝낸 반복 횟수
paused = False                  # 5회 반복 뒤 정지 중인지
pause_start = 0.0               # 정지를 시작한 시각
last_frame_time = get_time()    # 마지막으로 프레임을 넘긴 시각
pos_x = GROUND_X                # 캐릭터 몸 중심 x (제자리 동작은 화면 가운데)
facing = 1                      # 보는 방향: 1 오른쪽, -1 왼쪽 (시트 그림은 모두 오른쪽을 본다)
last_update_time = get_time()   # 마지막으로 update()를 부른 시각 (이동 거리 계산용)


# 프레임 하나를 SCALE배로 그린다.
# 몸 중심이 pos_x에 오도록 dx만큼 옮기고, 발이 GROUND_Y에 오도록 높이의 절반만큼 올린다
# 왼쪽을 볼 때는 그림을 좌우로 뒤집으므로 dx도 반대쪽으로 적용한다
def draw_frame(left, w, dx, bottom, h):
    x = pos_x + dx * SCALE * facing
    y = GROUND_Y + h * SCALE / 2
    if facing == 1:
        sonic.clip_draw(left, bottom, w, h, x, y, w * SCALE, h * SCALE)
    else:
        sonic.clip_composite_draw(left, bottom, w, h, 0, 'h', x, y, w * SCALE, h * SCALE)


def handle_events():
    global running
    for event in get_events():
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False


# delay()를 쌓아서 재지 않고 실제 경과 시간으로 프레임을 넘긴다
def update():
    global anim_index, frame_index, loop_count, paused, pause_start, last_frame_time, pos_x, facing, last_update_time
    now = get_time()
    dt = now - last_update_time
    last_update_time = now
    name, frames = ANIMATIONS[anim_index][0], ANIMATIONS[anim_index][3]

    # 정지 중에는 마지막 프레임을 그대로 두고, PAUSE_TIME이 지나면 다음 동작으로 넘어간다
    # 마지막 동작 다음에는 첫 동작으로 돌아간다
    if paused:
        if now - pause_start >= PAUSE_TIME:
            paused = False
            anim_index = (anim_index + 1) % len(ANIMATIONS)
            frame_index = 0
            loop_count = 0
            last_frame_time = now
            pos_x = GROUND_X        # 새 동작은 화면 가운데에서 오른쪽을 보고 시작한다
            facing = 1
        return

    # 이동 동작은 프레임이 바뀔 때만이 아니라 매 루프마다 경과 시간만큼 움직여야 끊기지 않는다
    if name in MOVE_SPEED:
        pos_x += MOVE_SPEED[name] * dt * facing
        # 화면 끝 여백에 닿으면 그 자리에서 몸을 돌려 반대쪽으로 간다
        if pos_x > CANVAS_W - MOVE_MARGIN:
            pos_x = CANVAS_W - MOVE_MARGIN
            facing = -1
        elif pos_x < MOVE_MARGIN:
            pos_x = MOVE_MARGIN
            facing = 1

    if now - last_frame_time >= FRAME_TIME:
        frame_index += 1
        last_frame_time += FRAME_TIME
        # 마지막 프레임을 지나면 반복 1회를 끝낸 것이다
        if frame_index >= len(frames):
            loop_count += 1
            if loop_count >= REPEAT_COUNT:
                # 5회를 채웠으면 마지막 프레임에 머문 채 정지한다
                frame_index = len(frames) - 1
                paused = True
                pause_start = now
                return
            frame_index = 0
        # 창을 끌어 옮기는 동안처럼 시간이 크게 튀었으면 밀린 시간은 버린다 (한 번에 1프레임만)
        if now - last_frame_time >= FRAME_TIME:
            last_frame_time = now


# 화면을 지우고 캐릭터와 상태 글자를 그린 뒤 화면에 보여 준다
def draw():
    clear_canvas()
    name, bottom, h, frames = ANIMATIONS[anim_index]
    left, w, dx = frames[frame_index]
    draw_frame(left, w, dx, bottom, h)
    # 1줄: 동작 번호와 이름, 지금 몇 번째 반복인지 (loop_count는 끝낸 횟수라 1을 더해 보여 준다)
    if paused:
        repeat_text = '반복 %d/%d (정지)' % (REPEAT_COUNT, REPEAT_COUNT)
    else:
        repeat_text = '반복 %d/%d' % (loop_count + 1, REPEAT_COUNT)
    font.draw(20, CANVAS_H - 25, '[%d/%d] %s   %s' % (anim_index + 1, len(ANIMATIONS), name, repeat_text),
              TEXT_COLOR)
    # 2줄: 지금 프레임 번호와 원본 크기
    font.draw(20, CANVAS_H - 55, '프레임 %d/%d   크기 %dx%d' % (frame_index + 1, len(frames), w, h), TEXT_COLOR)
    update_canvas()


while running:
    handle_events()
    update()
    draw()
    delay(0.01)     # CPU를 너무 쓰지 않도록 잠깐 쉰다 (재생 속도는 get_time()으로 잰다)

close_canvas()
